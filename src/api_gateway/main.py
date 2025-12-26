"""API Gateway Flask service"""

import os
import logging
import json
import uuid
from flask import Flask, jsonify, request
from api_gateway import APIGateway
from auth import get_user_from_request, authenticate_user, issue_jwt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PORT = int(os.environ.get('PORT', 8000))
app = Flask(__name__)
gateway = None


def init_gateway():
    global gateway
    try:
        gateway = APIGateway()
        logger.info("API Gateway initialized")
    except Exception as e:
        logger.error(f"Failed to initialize API Gateway: {e}")
        raise


@app.before_request
def before_request():
    if gateway is None:
        init_gateway()
    
    # Add trace ID to request context
    request.trace_id = request.headers.get('Trace-ID', str(uuid.uuid4()))


# --- System Health ---

@app.route('/health', methods=['GET'])
def health():
    """API Gateway health check."""
    return jsonify({'status': 'healthy', 'service': 'api-gateway'}), 200


@app.route('/system/health', methods=['GET'])
def system_health():
    """Aggregate health from all services."""
    health = gateway.get_system_health()
    return jsonify(health), 200



@app.route('/auth/login', methods=['POST'])
def login():
    """Simple username/password login for dev/testing.

    POST JSON: { "username": "...", "password": "..." }
    Returns: { access_token, token_type, expires_in }
    """
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'username and password are required'}), 400

    user = authenticate_user(username, password)
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401

    token = issue_jwt(user)
    return jsonify({'access_token': token, 'token_type': 'bearer', 'expires_in': int(os.environ.get('API_JWT_EXP_SECONDS', 3600))}), 200


# --- Dashboard ---

@app.route('/dashboard/snapshot', methods=['GET'])
def dashboard_snapshot():
    """Unified dashboard view."""
    snapshot = gateway.get_dashboard_snapshot()
    if 'error' in snapshot:
        return jsonify(snapshot), 500
    return jsonify(snapshot), 200


# --- Trading Control ---

@app.route('/trading/request-live', methods=['POST'])
def request_live():
    """Request to enable live trading.

    Requires authenticated operator JWT. The token's `sub` or `user_id` will be used as requester_id.
    """
    user = get_user_from_request(request)
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
    # minimal role check: operator role required
    roles = user.get('roles', []) or user.get('role', [])
    if isinstance(roles, str):
        roles = [roles]
    if 'operator' not in roles and 'admin' not in roles:
        return jsonify({'error': 'Forbidden'}), 403

    reason = (request.get_json() or {}).get('reason', '')
    requester_id = user.get('sub') or user.get('user_id')
    result = gateway.request_live_trading(requester_id, reason)
    return jsonify(result['data']), result['status']


@app.route('/trading/approve-live/<request_id>', methods=['POST'])
def approve_live(request_id):
    """Approve live trading request.

    Requires authenticated operator JWT. The token's `sub` or `user_id` will be used as approver_id.
    """
    user = get_user_from_request(request)
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
    roles = user.get('roles', []) or user.get('role', [])
    if isinstance(roles, str):
        roles = [roles]
    if 'operator' not in roles and 'admin' not in roles:
        return jsonify({'error': 'Forbidden'}), 403

    approver_id = user.get('sub') or user.get('user_id')
    result = gateway.approve_live_trading(request_id, approver_id)
    return jsonify(result['data']), result['status']


@app.route('/trading/approval-status', methods=['GET'])
def approval_status():
    """Get current approval status."""
    result = gateway.get_approval_status()
    return jsonify(result['data']), result['status']


@app.route('/trading/disable-live', methods=['POST'])
def disable_live():
    """Disable live trading (emergency).

    Requires admin role.
    """
    user = get_user_from_request(request)
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
    roles = user.get('roles', []) or user.get('role', [])
    if isinstance(roles, str):
        roles = [roles]
    if 'admin' not in roles:
        return jsonify({'error': 'Forbidden'}), 403

    result = gateway.disable_live_trading()
    return jsonify(result['data']), result['status']


@app.route('/trading/circuit-breaker', methods=['GET'])
def circuit_breaker_status():
    """Check circuit breaker status."""
    result = gateway.check_circuit_breaker()
    return jsonify(result['data']), result['status']


@app.route('/trading/circuit-breaker/trigger', methods=['POST'])
def trigger_circuit_breaker():
    """Trigger emergency stop."""
    data = request.get_json() or {}
    reason = data.get('reason', 'Manual stop')
    result = gateway.trigger_circuit_breaker(reason)
    return jsonify(result['data']), result['status']


# --- Strategies ---

@app.route('/strategies', methods=['GET'])
def strategies():
    """Get all strategies with vectors and EV."""
    result = gateway.get_strategies()
    if 'error' in result:
        return jsonify(result), 500
    return jsonify(result), 200


# --- Orders ---

@app.route('/orders/place', methods=['POST'])
def place_order():
    """Place an order.

    Requires authenticated operator token. The user's id is included in trace headers.
    """
    user = get_user_from_request(request)
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
    roles = user.get('roles', []) or user.get('role', [])
    if isinstance(roles, str):
        roles = [roles]
    if 'operator' not in roles and 'trader' not in roles and 'admin' not in roles:
        return jsonify({'error': 'Forbidden'}), 403

    data = request.get_json() or {}
    idempotency_key = request.headers.get('Idempotency-Key')
    trace_id = request.trace_id
    # attach user info to headers forwarded by gateway
    headers = {'Authorization': request.headers.get('Authorization'), 'Trace-ID': trace_id}
    result = gateway._call(gateway.execution, '/place-order', method='POST', data=data, headers=headers)
    return jsonify(result.get('data')), result.get('status', 500)


# --- Signals ---

@app.route('/signals/generate', methods=['POST'])
def generate_signals():
    """Generate trading signals."""
    data = request.get_json() or {}
    market_data = data.get('market_data')
    
    result = gateway.generate_signals(market_data)
    return jsonify(result['data']), result['status']


# --- Data ---

@app.route('/data/snapshot', methods=['GET'])
def data_snapshot():
    """Get market data snapshot."""
    lookback = request.args.get('lookback_days', default=20, type=int)
    result = gateway.get_market_data_snapshot(lookback)
    return jsonify(result['data']), result['status']


# --- Journal ---

@app.route('/journal/recent', methods=['GET'])
def recent_trades():
    """Get recent trades."""
    limit = request.args.get('limit', default=50, type=int)
    result = gateway.get_recent_trades(limit)
    return jsonify(result['data']), result['status']


@app.route('/journal/trade/<trade_id>', methods=['GET'])
def trade_details(trade_id):
    """Get trade details."""
    result = gateway.get_trade_details(trade_id)
    return jsonify(result['data']), result['status']


@app.route('/journal/summary', methods=['GET'])
def journal_summary():
    """Get journal summary statistics."""
    result = gateway.get_journal_summary()
    return jsonify(result['data']), result['status']


if __name__ == '__main__':
    logger.info(f"Starting API Gateway on port {PORT}")
    init_gateway()
    app.run(host='0.0.0.0', port=PORT, debug=False, threaded=True)
