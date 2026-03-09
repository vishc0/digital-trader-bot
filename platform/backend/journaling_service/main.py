"""
Journaling Service Flask API
"""

import os
import logging
import json
from flask import Flask, jsonify, request
from journaling_service import JournalingService
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PORT = int(os.environ.get("PORT", 8084))
app = Flask(__name__)
journal = JournalingService()


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'journaling-service',
        'backend': 'sqlite',
        'db_path': journal.db_path
    }), 200


@app.route('/trade-event', methods=['POST'])
def log_trade_event():
    """Log a trade event."""
    data = request.get_json() or {}
    try:
        trade_id = data.get('trade_id')
        event_type = data.get('event_type')
        trade_data = data.get('data', {})
        regime = data.get('market_regime', 'UNKNOWN')
        
        event_id = journal.log_trade_event(trade_id, event_type, trade_data, regime)
        
        return jsonify({
            'status': 'logged',
            'event_id': event_id,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Error logging trade event: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/execution-metrics', methods=['POST'])
def log_execution_metrics():
    """Log execution metrics."""
    data = request.get_json() or {}
    try:
        journal.log_execution_metrics(
            data.get('trade_id'),
            data.get('expected_price'),
            data.get('fill_price'),
            data.get('latency_ms')
        )
        return jsonify({'status': 'logged'}), 200
    except Exception as e:
        logger.error(f"Error logging metrics: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/wisdom-adjustment', methods=['POST'])
def log_wisdom_adjustment():
    """Log wisdom adjustment."""
    data = request.get_json() or {}
    try:
        journal.log_wisdom_adjustment(
            data.get('strategy_id'),
            data.get('adjustment_type'),
            data.get('old_value'),
            data.get('new_value'),
            data.get('reason')
        )
        return jsonify({'status': 'logged'}), 200
    except Exception as e:
        logger.error(f"Error logging adjustment: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/system-health', methods=['POST'])
def log_system_health():
    """Log a system health snapshot."""
    data = request.get_json() or {}
    try:
        health_id = journal.log_system_health(data.get('status', data))
        return jsonify({'status': 'logged', 'health_id': health_id}), 200
    except Exception as e:
        logger.error(f"Error logging system health: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/trades/recent', methods=['GET'])
def get_recent_trades():
    """Get recent trades."""
    limit = request.args.get('limit', default=50, type=int)
    trades = journal.get_recent_trades(limit)
    return jsonify({'trades': trades, 'count': len(trades)}), 200


@app.route('/trades/<trade_id>', methods=['GET'])
def get_trade_details(trade_id):
    """Get all events for a specific trade."""
    events = journal.get_trade_by_id(trade_id)
    return jsonify({'trade_id': trade_id, 'events': events}), 200


@app.route('/journal/summary', methods=['GET'])
def get_journal_summary():
    """Get journal statistics."""
    summary = journal.get_journal_summary()
    return jsonify(summary), 200


if __name__ == '__main__':
    logger.info(f"Starting Journaling Service on port {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=False)
