"""Journaling Service - durable audit trail for MVP paper trading.

Responsibilities:
- Logs trade events (SIGNAL, ORDER_SENT, FILL, CANCEL, EXIT)
- Tracks execution metrics (slippage, latency)
- Stores wisdom adjustments
- Stores system-health snapshots
"""

import json
import logging
import os
import sqlite3
import threading
import uuid
from contextlib import contextmanager
from datetime import datetime

logger = logging.getLogger(__name__)


class JournalingService:
    """Persistent logging of trading events and system decisions using SQLite."""

    def __init__(self, db_path=None):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        default_db_path = os.path.join(base_dir, 'data', 'journal.db')
        self.db_path = os.path.abspath(db_path or os.environ.get('JOURNAL_DB_PATH', default_db_path))
        self._lock = threading.Lock()
        self._initialize_database()
        logger.info('Journaling Service initialized with SQLite backend at %s', self.db_path)

    def _initialize_database(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS trade_events (
                    id TEXT PRIMARY KEY,
                    trade_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    data TEXT NOT NULL,
                    market_regime TEXT NOT NULL
                );

                CREATE INDEX IF NOT EXISTS idx_trade_events_trade_id
                ON trade_events(trade_id);

                CREATE INDEX IF NOT EXISTS idx_trade_events_timestamp
                ON trade_events(timestamp DESC);

                CREATE TABLE IF NOT EXISTS execution_metrics (
                    id TEXT PRIMARY KEY,
                    trade_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    expected_price REAL,
                    fill_price REAL,
                    slippage_abs REAL,
                    slippage_pct REAL,
                    latency_ms REAL
                );

                CREATE INDEX IF NOT EXISTS idx_execution_metrics_trade_id
                ON execution_metrics(trade_id);

                CREATE TABLE IF NOT EXISTS wisdom_adjustments (
                    id TEXT PRIMARY KEY,
                    strategy_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    adjustment_type TEXT NOT NULL,
                    old_value TEXT,
                    new_value TEXT,
                    reason TEXT
                );

                CREATE TABLE IF NOT EXISTS system_health (
                    id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    status TEXT NOT NULL
                );
                """
            )
            conn.commit()

    @contextmanager
    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    @staticmethod
    def _now_iso():
        return datetime.utcnow().isoformat()

    @staticmethod
    def _to_json(value):
        return json.dumps(value)

    @staticmethod
    def _from_json(value):
        if value is None:
            return None
        try:
            return json.loads(value)
        except (TypeError, json.JSONDecodeError):
            return value

    def log_trade_event(self, trade_id, event_type, data, market_regime='UNKNOWN'):
        """Log a trade event and return the durable event ID."""
        event_id = str(uuid.uuid4())
        entry = {
            'id': event_id,
            'trade_id': trade_id,
            'timestamp': self._now_iso(),
            'event_type': event_type,
            'data': data or {},
            'market_regime': market_regime or 'UNKNOWN'
        }
        with self._lock:
            with self._connect() as conn:
                conn.execute(
                    """
                    INSERT INTO trade_events (id, trade_id, timestamp, event_type, data, market_regime)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        entry['id'],
                        entry['trade_id'],
                        entry['timestamp'],
                        entry['event_type'],
                        self._to_json(entry['data']),
                        entry['market_regime']
                    )
                )
                conn.commit()
        logger.info('Logged %s for %s', event_type, trade_id)
        return event_id

    def log_execution_metrics(self, trade_id, expected_price, fill_price, latency_ms):
        """Log execution quality metrics."""
        expected = float(expected_price or 0)
        actual = float(fill_price or 0)
        slippage = actual - expected
        slippage_pct = (slippage / expected * 100) if expected else 0
        metric_id = str(uuid.uuid4())
        timestamp = self._now_iso()

        with self._lock:
            with self._connect() as conn:
                conn.execute(
                    """
                    INSERT INTO execution_metrics (
                        id, trade_id, timestamp, expected_price, fill_price, slippage_abs, slippage_pct, latency_ms
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (metric_id, trade_id, timestamp, expected, actual, slippage, slippage_pct, latency_ms)
                )
                conn.commit()
        logger.info('Execution metric stored for %s slippage=%.4f%%', trade_id, slippage_pct)
        return metric_id

    def log_wisdom_adjustment(self, strategy_id, adjustment_type, old_value, new_value, reason):
        """Log changes made by Wisdom Builder."""
        adjustment_id = str(uuid.uuid4())
        timestamp = self._now_iso()
        with self._lock:
            with self._connect() as conn:
                conn.execute(
                    """
                    INSERT INTO wisdom_adjustments (
                        id, strategy_id, timestamp, adjustment_type, old_value, new_value, reason
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        adjustment_id,
                        strategy_id,
                        timestamp,
                        adjustment_type,
                        self._to_json(old_value),
                        self._to_json(new_value),
                        reason
                    )
                )
                conn.commit()
        logger.info('Wisdom adjustment stored for %s - %s', strategy_id, adjustment_type)
        return adjustment_id

    def log_system_health(self, health_status):
        """Log a system-health snapshot."""
        health_id = str(uuid.uuid4())
        timestamp = self._now_iso()
        with self._lock:
            with self._connect() as conn:
                conn.execute(
                    """
                    INSERT INTO system_health (id, timestamp, status)
                    VALUES (?, ?, ?)
                    """,
                    (health_id, timestamp, self._to_json(health_status))
                )
                conn.commit()
        return health_id

    def get_recent_trades(self, limit=50):
        """Retrieve recent trade events."""
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, trade_id, timestamp, event_type, data, market_regime
                FROM trade_events
                ORDER BY timestamp DESC
                LIMIT ?
                """,
                (limit,)
            ).fetchall()
        return [
            {
                'id': row['id'],
                'trade_id': row['trade_id'],
                'timestamp': row['timestamp'],
                'event_type': row['event_type'],
                'data': self._from_json(row['data']),
                'market_regime': row['market_regime']
            }
            for row in rows
        ]

    def get_trade_by_id(self, trade_id):
        """Get all events for a specific trade."""
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, trade_id, timestamp, event_type, data, market_regime
                FROM trade_events
                WHERE trade_id = ?
                ORDER BY timestamp ASC
                """,
                (trade_id,)
            ).fetchall()
        return [
            {
                'id': row['id'],
                'trade_id': row['trade_id'],
                'timestamp': row['timestamp'],
                'event_type': row['event_type'],
                'data': self._from_json(row['data']),
                'market_regime': row['market_regime']
            }
            for row in rows
        ]

    def get_journal_summary(self):
        """Get journal statistics."""
        with self._connect() as conn:
            total_trades = conn.execute('SELECT COUNT(*) FROM trade_events').fetchone()[0]
            total_metrics = conn.execute('SELECT COUNT(*) FROM execution_metrics').fetchone()[0]
            total_adjustments = conn.execute('SELECT COUNT(*) FROM wisdom_adjustments').fetchone()[0]
            total_health_snapshots = conn.execute('SELECT COUNT(*) FROM system_health').fetchone()[0]

        return {
            'backend': 'sqlite',
            'db_path': self.db_path,
            'total_trades': total_trades,
            'total_metrics': total_metrics,
            'total_adjustments': total_adjustments,
            'total_health_snapshots': total_health_snapshots
        }
