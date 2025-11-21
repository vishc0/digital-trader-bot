"""
State Manager Flask API Service - The Central Brain

Provides REST endpoints for other microservices to interact with the central brain.
All critical operations use Redis + MsgPack for efficiency.
"""

import os
import logging
from datetime import datetime
from flask import Flask, jsonify, request
from state_manager import StateManager, CircuitBreakerOpen

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
PORT = int(os.environ.get("PORT", 8080))

# Initialize Flask app
app = Flask(__name__)
state_manager = None


def init_app():
    """Initialize State Manager on first request."""
    global state_manager
    try:
        state_manager = StateManager()
        logger.info("State Manager initialized")
    except Exception as e:
        logger.error(f"Failed to initialize State Manager: {e}")
        raise


@app.before_request
def before_request():
    """Ensure state manager is initialized."""
    if state_manager is None:
        init_app()


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    status = state_manager.get_health_status()
    status_code = 200 if status['status'] == 'healthy' else 503
    return jsonify(status), status_code


@app.route('/circuit-breaker', methods=['GET'])
def get_circuit_breaker():
    """Check circuit breaker status."""
    try:
        state_manager.check_circuit_breaker()
        return jsonify({'status': 'NORMAL', 'trading_allowed': True}), 200
    except CircuitBreakerOpen as e:
        return jsonify({'status': 'TRIPPED', 'trading_allowed': False, 'message': str(e)}), 200


@app.route('/circuit-breaker/trigger', methods=['POST'])
def trigger_circuit_breaker():
    """Trigger circuit breaker."""
    data = request.get_json() or {}
    reason = data.get('reason', 'Manual stop')
    state_manager.trigger_circuit_breaker(reason)
    return jsonify({'status': 'TRIGGERED', 'reason': reason}), 200


@app.route('/circuit-breaker/reset', methods=['POST'])
def reset_circuit_breaker():
    """Reset circuit breaker."""
    state_manager.reset_circuit_breaker()
    return jsonify({'status': 'RESET'}), 200


@app.route('/market-state', methods=['GET'])
def get_market_state():
    """Get market state."""
    market_state = state_manager.get_market_state()
    if market_state is None:
        return jsonify({'error': 'Not available'}), 404
    return jsonify(market_state), 200


@app.route('/market-state', methods=['PUT'])
def update_market_state():
    """Update market state."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400
    try:
        state_manager.update_market_state(data)
        return jsonify({'status': 'updated'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/strategy-vector/<strategy_id>', methods=['GET'])
def get_strategy_vector(strategy_id):
    """Get strategy vector."""
    vector = state_manager.get_strategy_vector(strategy_id)
    return jsonify({'strategy_id': strategy_id, 'vector': vector}), 200


@app.route('/strategy-vector/<strategy_id>', methods=['PUT'])
def update_strategy_vector(strategy_id):
    """Update strategy vector."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400
    try:
        state_manager.update_strategy_vector(strategy_id, data if isinstance(data, list) else data.values())
        return jsonify({'status': 'updated'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/daily-pnl', methods=['GET'])
def get_daily_pnl():
    """Get daily PnL."""
    pnl = state_manager.get_daily_pnl()
    return jsonify({'daily_pnl': pnl}), 200


@app.route('/daily-pnl', methods=['POST'])
def update_daily_pnl():
    """Update daily PnL."""
    data = request.get_json() or {}
    pnl_delta = data.get('pnl_delta', 0.0)
    try:
        state_manager.update_daily_pnl(pnl_delta)
        return jsonify({'status': 'updated', 'new_pnl': state_manager.get_daily_pnl()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/daily-pnl/reset', methods=['POST'])
def reset_daily_pnl():
    """Reset daily PnL."""
    state_manager.reset_daily_pnl()
    return jsonify({'status': 'reset'}), 200


@app.errorhandler(Exception)
def handle_error(error):
    """Global error handler."""
    logger.error(f"Error: {error}")
    return jsonify({'error': str(error)}), 500


if __name__ == '__main__':
    logger.info(f"Starting State Manager on port {PORT}")
    init_app()
    app.run(host='0.0.0.0', port=PORT, debug=False, threaded=True)
