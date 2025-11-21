"""
Journaling Service - Immutable Audit Trail

Responsibilities:
- Logs all trade events (SIGNAL, FILL, EXIT)
- Tracks execution metrics (slippage, latency)
- Stores wisdom adjustments
- Maintains pattern repository
"""

import logging
import uuid
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class JournalingService:
    """
    Persistent logging of all trading events and system decisions.
    In production, backed by Firestore/DynamoDB.
    """

    def __init__(self):
        """Initialize journaling service."""
        self.in_memory_journal = {
            'trade_events': [],
            'execution_metrics': [],
            'wisdom_adjustments': [],
            'system_health': []
        }
        logger.info("Journaling Service initialized (in-memory)")

    def log_trade_event(self, trade_id, event_type, data, market_regime='UNKNOWN'):
        """
        Log a trade event.
        event_type: SIGNAL, ORDER_SENT, FILL, CANCEL, EXIT
        """
        entry = {
            'id': str(uuid.uuid4()),
            'trade_id': trade_id,
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'data': data,
            'market_regime': market_regime
        }
        self.in_memory_journal['trade_events'].append(entry)
        logger.info(f"Logged {event_type} for {trade_id}")
        return entry['id']

    def log_execution_metrics(self, trade_id, expected_price, fill_price, latency_ms):
        """Log execution quality metrics."""
        slippage = fill_price - expected_price
        slippage_pct = (slippage / expected_price * 100) if expected_price != 0 else 0
        
        metric = {
            'trade_id': trade_id,
            'timestamp': datetime.utcnow().isoformat(),
            'slippage_abs': slippage,
            'slippage_pct': slippage_pct,
            'latency_ms': latency_ms
        }
        self.in_memory_journal['execution_metrics'].append(metric)
        logger.info(f"Execution metric: {trade_id} slippage={slippage_pct:.4f}%")

    def log_wisdom_adjustment(self, strategy_id, adjustment_type, old_value, new_value, reason):
        """Log changes made by Wisdom Builder."""
        entry = {
            'strategy_id': strategy_id,
            'timestamp': datetime.utcnow().isoformat(),
            'adjustment_type': adjustment_type,  # E1_PARAM_TUNE, E2_REGIME_SWITCH
            'old_value': old_value,
            'new_value': new_value,
            'reason': reason
        }
        self.in_memory_journal['wisdom_adjustments'].append(entry)
        logger.info(f"Wisdom adjustment: {strategy_id} - {adjustment_type}")

    def log_system_health(self, health_status):
        """Log system health snapshot."""
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'status': health_status
        }
        self.in_memory_journal['system_health'].append(entry)

    def get_recent_trades(self, limit=50):
        """Retrieve recent trade events."""
        events = self.in_memory_journal['trade_events']
        return events[-limit:] if events else []

    def get_trade_by_id(self, trade_id):
        """Get all events for a specific trade."""
        return [e for e in self.in_memory_journal['trade_events'] if e['trade_id'] == trade_id]

    def get_journal_summary(self):
        """Get journal statistics."""
        return {
            'total_trades': len(self.in_memory_journal['trade_events']),
            'total_metrics': len(self.in_memory_journal['execution_metrics']),
            'total_adjustments': len(self.in_memory_journal['wisdom_adjustments']),
            'total_health_snapshots': len(self.in_memory_journal['system_health'])
        }
