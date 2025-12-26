"""API Gateway - Service Orchestration Layer

Routes requests to appropriate microservices and aggregates responses for the UI.
Handles authentication, request logging, and error translation.
"""

import os
import logging
import requests
import json
from typing import Dict, Any

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class APIGateway:
    def __init__(self):
        # Service URLs
        self.state_manager = os.environ.get('STATE_MANAGER_URL', 'http://state-manager:8080')
        self.strategy_engine = os.environ.get('STRATEGY_ENGINE_URL', 'http://strategy-engine:8081')
        self.wisdom_builder = os.environ.get('WISDOM_BUILDER_URL', 'http://wisdom-builder:8082')
        self.external_intel = os.environ.get('EXTERNAL_INTEL_URL', 'http://external-intelligence:8083')
        self.journaling = os.environ.get('JOURNALING_URL', 'http://journaling-service:8084')
        self.execution = os.environ.get('EXECUTION_URL', 'http://execution-manager:8086')
        self.data_handler = os.environ.get('DATA_HANDLER_URL', 'http://data-handler:8085')
        
        self.timeout = 5

    def _call(self, base_url: str, endpoint: str, method: str = 'GET', data: Dict = None, headers: Dict = None) -> Dict[str, Any]:
        """Helper to call a microservice endpoint."""
        url = f"{base_url}{endpoint}"
        try:
            if method == 'GET':
                r = requests.get(url, timeout=self.timeout, headers=headers)
            elif method == 'POST':
                r = requests.post(url, json=data, timeout=self.timeout, headers=headers)
            elif method == 'PUT':
                r = requests.put(url, json=data, timeout=self.timeout, headers=headers)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            return {
                'status': r.status_code,
                'data': r.json() if r.text else {},
                'error': None
            }
        except Exception as e:
            logger.error(f"Error calling {url}: {e}")
            return {
                'status': 500,
                'data': {},
                'error': str(e)
            }

    # --- System Health & Status ---

    def get_system_health(self) -> Dict:
        """Aggregate health status from all services."""
        services = {
            'state_manager': self._call(self.state_manager, '/health'),
            'strategy_engine': self._call(self.strategy_engine, '/health'),
            'wisdom_builder': self._call(self.wisdom_builder, '/health'),
            'external_intelligence': self._call(self.external_intel, '/health'),
            'journaling_service': self._call(self.journaling, '/health'),
            'execution_manager': self._call(self.execution, '/health'),
            'data_handler': self._call(self.data_handler, '/health'),
        }
        
        all_healthy = all(s['status'] == 200 for s in services.values())
        
        return {
            'overall_status': 'healthy' if all_healthy else 'degraded',
            'services': services
        }

    # --- Trading Control ---

    def request_live_trading(self, requester_id: str, reason: str = "") -> Dict:
        """Request permission to enable live trading."""
        return self._call(
            self.state_manager,
            '/live-approval/request',
            method='POST',
            data={'requester_id': requester_id, 'reason': reason}
        )

    def approve_live_trading(self, request_id: str, approver_id: str) -> Dict:
        """Approve a live trading request."""
        return self._call(
            self.state_manager,
            f'/live-approval/approve/{request_id}',
            method='POST',
            data={'approver_id': approver_id}
        )

    def get_approval_status(self) -> Dict:
        """Get current live trading approval status."""
        return self._call(self.state_manager, '/live-approval/status')

    def disable_live_trading(self) -> Dict:
        """Immediately disable live trading."""
        return self._call(self.state_manager, '/live-approval/disable', method='POST')

    # --- Circuit Breaker ---

    def check_circuit_breaker(self) -> Dict:
        """Check if trading is allowed."""
        return self._call(self.state_manager, '/circuit-breaker')

    def trigger_circuit_breaker(self, reason: str) -> Dict:
        """Trigger emergency stop."""
        return self._call(
            self.state_manager,
            '/circuit-breaker/trigger',
            method='POST',
            data={'reason': reason}
        )

    # --- Dashboard Data ---

    def get_dashboard_snapshot(self) -> Dict:
        """Get unified dashboard view with market state, positions, PnL, etc."""
        try:
            market_state = self._call(self.state_manager, '/market-state')
            daily_pnl = self._call(self.state_manager, '/daily-pnl')
            approval_status = self._call(self.state_manager, '/live-approval/status')
            circuit_breaker = self._call(self.state_manager, '/circuit-breaker')
            data_snapshot = self._call(self.data_handler, '/snapshot')
            recent_trades = self._call(self.journaling, '/trades/recent?limit=10')
            
            return {
                'market_state': market_state.get('data'),
                'daily_pnl': daily_pnl.get('data'),
                'approval_status': approval_status.get('data'),
                'circuit_breaker': circuit_breaker.get('data'),
                'data_snapshot': data_snapshot.get('data'),
                'recent_trades': recent_trades.get('data'),
                'timestamp': None,
                'error': None
            }
        except Exception as e:
            logger.error(f"Error building dashboard snapshot: {e}")
            return {'error': str(e)}

    # --- Strategy Management ---

    def get_strategies(self) -> Dict:
        """Get all strategies with their vectors and performance."""
        try:
            strategies = {}
            for strategy_id in ['A1_MR', 'A2_TF', 'A3_SA']:
                vector_resp = self._call(self.state_manager, f'/strategy-vector/{strategy_id}')
                ev_resp = self._call(self.strategy_engine, f'/expected-value/{strategy_id}')
                strategies[strategy_id] = {
                    'vector': vector_resp.get('data', {}).get('vector'),
                    'expected_value': ev_resp.get('data', {}).get('expected_value'),
                }
            return {'strategies': strategies}
        except Exception as e:
            logger.error(f"Error fetching strategies: {e}")
            return {'error': str(e)}

    # --- Order Placement ---

    def place_order(self, order: Dict, idempotency_key: str = None, trace_id: str = None) -> Dict:
        """Place an order."""
        headers = {}
        if idempotency_key:
            headers['Idempotency-Key'] = idempotency_key
        if trace_id:
            headers['Trace-ID'] = trace_id
        
        return self._call(
            self.execution,
            '/place-order',
            method='POST',
            data=order,
            headers=headers
        )

    # --- Data & Signals ---

    def generate_signals(self, market_data: Dict = None) -> Dict:
        """Generate trading signals."""
        return self._call(
            self.strategy_engine,
            '/signals',
            method='POST',
            data={'market_data': market_data or {}}
        )

    def get_market_data_snapshot(self, lookback_days: int = 20) -> Dict:
        """Get full market data snapshot."""
        return self._call(self.data_handler, f'/snapshot?lookback_days={lookback_days}')

    # --- Journal & Analysis ---

    def get_recent_trades(self, limit: int = 50) -> Dict:
        """Get recent closed trades."""
        return self._call(self.journaling, f'/trades/recent?limit={limit}')

    def get_trade_details(self, trade_id: str) -> Dict:
        """Get all events for a specific trade."""
        return self._call(self.journaling, f'/trades/{trade_id}')

    def get_journal_summary(self) -> Dict:
        """Get journaling service statistics."""
        return self._call(self.journaling, '/journal/summary')
