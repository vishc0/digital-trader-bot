"""
Execution Manager core logic

Provides an abstraction for order placement. Supports `paper` (simulation) and `live` (broker adapters) modes.
This skeleton implements a safe paper mode and basic checks against State Manager (circuit breaker) and Journaling Service.
"""
import os
import time
import uuid
import logging
import json
import requests
import redis

from .broker_adapters.base import BrokerAdapter
from .broker_adapters.fidelity_mock import FidelityMockAdapter
from .broker_adapters.alpaca_mock import AlpacaMockAdapter

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ExecutionManager:
    def __init__(self, state_manager_host='state-manager', journaling_host='journaling-service', mode=None, broker_provider=None):
        self.state_manager_base = f'http://{state_manager_host}:8080'
        self.journaling_base = f'http://{journaling_host}:8084'
        self.mode = (mode or os.environ.get('EXECUTION_MODE', 'paper')).lower()
        self.broker_provider = (broker_provider or os.environ.get('BROKER_PROVIDER', 'fidelity_mock')).lower()
        self.broker_adapter = None
        # Redis idempotency store
        self.redis_host = os.environ.get('REDIS_HOST', 'redis')
        self.redis_port = int(os.environ.get('REDIS_PORT', 6379))
        self.idempotency_ttl = int(os.environ.get('IDEMPOTENCY_TTL', 604800))  # 7 days default
        try:
            self.redis = redis.Redis(host=self.redis_host, port=self.redis_port, decode_responses=True)
            # quick ping to test connection
            self.redis.ping()
        except Exception as e:
            logger.warning(f'Could not connect to Redis ({self.redis_host}:{self.redis_port}): {e}')
            self.redis = None

        # Initialize broker adapter if running in live/shadow mode
        if self.mode in ('live', 'shadow'):
            self.broker_adapter = self._load_adapter(self.broker_provider)

    def _load_adapter(self, provider):
        # Factory selection for adapters
        if provider == 'fidelity_mock':
            return FidelityMockAdapter()
        if provider == 'alpaca_mock':
            return AlpacaMockAdapter()
        raise RuntimeError(f'Unknown broker provider: {provider}')

    def is_trading_allowed(self):
        try:
            r = requests.get(f'{self.state_manager_base}/circuit-breaker', timeout=3)
            if r.status_code == 200:
                payload = r.json()
                return payload.get('trading_allowed', False)
        except Exception as e:
            logger.warning(f'Could not reach state manager for circuit breaker: {e}')
            # Conservatively disallow trading if state manager unavailable
            return False
        return False

    def place_order(self, order, idempotency_key=None):
        """Place an order according to current mode.

        order: dict containing {ticker, side, qty, price, order_type}
        idempotency_key: optional unique key for dedup
        """
        if not self.is_trading_allowed():
            raise RuntimeError('Trading disallowed by circuit breaker or state manager')

        if idempotency_key is None:
            idempotency_key = str(uuid.uuid4())

        # Check idempotency store first
        idemp_key = f'idemp:{idempotency_key}'
        if self.redis:
            try:
                existing = self.redis.get(idemp_key)
                if existing:
                    logger.info(f'Idempotency hit for {idempotency_key}')
                    return json.loads(existing)
            except Exception as e:
                logger.warning(f'Failed to read idempotency key {idemp_key}: {e}')

        if self.mode == 'paper':
            result = self._simulate_fill(order, idempotency_key)
            # store result in idempotency store
            if self.redis:
                try:
                    stored = json.dumps(result)
                    # attempt to set only if not exists
                    ok = self.redis.set(idemp_key, stored, nx=True, ex=self.idempotency_ttl)
                    if not ok:
                        # another process set it first, return authoritative value
                        existing = self.redis.get(idemp_key)
                        if existing:
                            return json.loads(existing)
                except Exception as e:
                    logger.warning(f'Failed to write idempotency key {idemp_key}: {e}')
            return result
        elif self.mode == 'shadow':
            # Shadow: attempt live placement but do not affect real accounts (adapter should support dry-run)
            if self.broker_adapter:
                fill = self.broker_adapter.place_order(order, idempotency_key=idempotency_key)
                # journal the shadow fill
                fill['mode'] = 'shadow'
                self._journal_fill(fill)
                # store idempotency
                if self.redis:
                    try:
                        stored = json.dumps(fill)
                        ok = self.redis.set(idemp_key, stored, nx=True, ex=self.idempotency_ttl)
                        if not ok:
                            existing = self.redis.get(idemp_key)
                            if existing:
                                return json.loads(existing)
                    except Exception as e:
                        logger.warning(f'Failed to write idempotency key {idemp_key}: {e}')
                return fill
            else:
                return self._simulate_fill(order, idempotency_key)
        else:
            # live
            fill = self._place_live_order(order, idempotency_key)
            if self.redis:
                try:
                    stored = json.dumps(fill)
                    ok = self.redis.set(idemp_key, stored, nx=True, ex=self.idempotency_ttl)
                    if not ok:
                        existing = self.redis.get(idemp_key)
                        if existing:
                            return json.loads(existing)
                except Exception as e:
                    logger.warning(f'Failed to write idempotency key {idemp_key}: {e}')
            return fill

    def _simulate_fill(self, order, idempotency_key):
        """Simple simulation: immediate fill at requested price with tiny slippage."""
        # simulate network / execution delay
        time.sleep(0.1)
        fill_price = order.get('price') or order.get('expected_price') or 0
        # apply minimal slippage
        slippage = 0.0005 * (1 if order.get('side', 'buy') == 'buy' else -1)
        fill_price = round(fill_price * (1 + slippage), 6)

        fill = {
            'trade_id': idempotency_key,
            'ticker': order.get('ticker'),
            'side': order.get('side'),
            'qty': order.get('qty'),
            'fill_price': fill_price,
            'status': 'filled',
            'mode': 'paper',
            'timestamp': int(time.time() * 1000)
        }

        # Log to journaling service (best-effort)
        try:
            payload = {
                'trade_id': fill['trade_id'],
                'event_type': 'FILL',
                'data': fill,
                'market_regime': 'UNKNOWN'
            }
            requests.post(f'{self.journaling_base}/trade-event', json=payload, timeout=3)
        except Exception as e:
            logger.warning(f'Failed to log fill to journaling service: {e}')

        return fill

    def _place_live_order(self, order, idempotency_key):
        """Place live order using configured broker adapter."""
        if not self.broker_adapter:
            # Lazy load if not initialized
            self.broker_adapter = self._load_adapter(self.broker_provider)

        # Delegate to adapter
        fill = self.broker_adapter.place_order(order, idempotency_key=idempotency_key)
        # Journal the fill
        try:
            self._journal_fill(fill)
        except Exception as e:
            logger.warning(f'Failed to journal live fill: {e}')

        return fill

    def _journal_fill(self, fill):
        payload = {
            'trade_id': fill.get('trade_id'),
            'event_type': 'FILL',
            'data': fill,
            'market_regime': fill.get('market_regime', 'UNKNOWN')
        }
        requests.post(f'{self.journaling_base}/trade-event', json=payload, timeout=3)

