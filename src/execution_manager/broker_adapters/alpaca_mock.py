"""Mock Alpaca broker adapter

Simulates Alpaca-like fills for testing.
"""
import time
import uuid
import random

from .base import BrokerAdapter


class AlpacaMockAdapter(BrokerAdapter):
    def __init__(self, latency_ms=50):
        self.latency_ms = latency_ms

    def place_order(self, order, idempotency_key=None):
        time.sleep(self.latency_ms / 1000.0)
        if idempotency_key is None:
            idempotency_key = str(uuid.uuid4())

        base_price = order.get('price') or order.get('expected_price') or 0
        # Alpaca mock: generally tighter fills
        if order.get('order_type', 'limit') == 'market':
            slippage_pct = random.uniform(0.0003, 0.001)
        else:
            slippage_pct = random.uniform(0.00005, 0.0004)

        slippage = base_price * slippage_pct * (1 if order.get('side', 'buy') == 'buy' else -1)
        fill_price = round(base_price + slippage, 6)

        fill = {
            'trade_id': idempotency_key,
            'provider': 'alpaca_mock',
            'broker_order_id': str(uuid.uuid4()),
            'ticker': order.get('ticker'),
            'side': order.get('side'),
            'qty': order.get('qty'),
            'fill_price': fill_price,
            'status': 'filled',
            'timestamp': int(time.time() * 1000)
        }
        return fill

    def cancel_order(self, broker_order_id):
        return {'broker_order_id': broker_order_id, 'status': 'cancelled'}
