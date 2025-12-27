"""
Strategy Engine Flask API
"""

import os
import logging
import json
from flask import Flask, jsonify, request
from strategy_engine import StrategyEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PORT = int(os.environ.get("PORT", 8081))
app = Flask(__name__)
engine = StrategyEngine()


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'strategy-engine'}), 200


@app.route('/signals', methods=['POST'])
def generate_signals():
    """Generate trade signals from market data."""
    data = request.get_json() or {}
    try:
        # Expected format: {'market_data': {...}}
        market_data = data.get('market_data', {})
        signals = engine.generate_signals(market_data)
        return jsonify({'signals': signals, 'count': len(signals)}), 200
    except Exception as e:
        logger.error(f"Error generating signals: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/expected-value/<strategy_id>', methods=['GET'])
def get_expected_value(strategy_id):
    """Get EV for a strategy."""
    ev = engine.calculate_expected_value(strategy_id)
    return jsonify({'strategy_id': strategy_id, 'expected_value': ev}), 200


if __name__ == '__main__':
    logger.info(f"Starting Strategy Engine on port {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=False)
