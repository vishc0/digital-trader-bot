"""API Gateway Flask service"""

import os
import logging
import json
import uuid
import base64
from email.mime.text import MIMEText
from flask import Flask, jsonify, request
from api_gateway import APIGateway
from auth import get_user_from_request, authenticate_user, issue_jwt

# Optional deps for Workspace integrations
try:
    import requests as _requests
except Exception:
    _requests = None
try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from googleapiclient.http import MediaIoBaseUpload
    import io
except Exception:
    service_account = None
    build = None
    HttpError = Exception
    MediaIoBaseUpload = None
    io = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PORT = int(os.environ.get('PORT', 8000))
MOCK_MODE = str(os.environ.get('MOCK_MODE', '')).lower() in {'1', 'true', 'yes'}
WORKSPACE_ENABLED = str(os.environ.get('WORKSPACE_ENABLED', '')).lower() in {'1', 'true', 'yes'}
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
    if MOCK_MODE:
        reason = (request.get_json() or {}).get('reason', '')
        requester_id = 'dev-user'
        result = gateway.request_live_trading(requester_id, reason)
        return jsonify(result['data']), result['status']

    user = get_user_from_request(request)
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
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
    if MOCK_MODE:
        approver_id = 'dev-approver'
        result = gateway.approve_live_trading(request_id, approver_id)
        return jsonify(result['data']), result['status']

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
    if MOCK_MODE:
        result = gateway.disable_live_trading()
        return jsonify(result['data']), result['status']

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
    if MOCK_MODE:
        data = request.get_json() or {}
        idempotency_key = request.headers.get('Idempotency-Key')
        trace_id = request.trace_id
        result = gateway.place_order(data, idempotency_key=idempotency_key, trace_id=trace_id)
        return jsonify(result.get('data')), result.get('status', 200)

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


# --- Workspace Integrations ---

def _get_workspace_credentials(scopes, subject=None):
    """Load service account credentials for Workspace APIs.

    Reads from env `WORKSPACE_SA_JSON` (inline JSON) or `WORKSPACE_SA_FILE` (path).
    Supports domain-wide delegation via `subject`.
    """
    if service_account is None:
        return None, 'google auth libraries not available'
    sa_json = os.environ.get('WORKSPACE_SA_JSON')
    sa_file = os.environ.get('WORKSPACE_SA_FILE')
    try:
        if sa_json:
            info = json.loads(sa_json)
            creds = service_account.Credentials.from_service_account_info(info, scopes=scopes, subject=subject)
        elif sa_file and os.path.exists(sa_file):
            creds = service_account.Credentials.from_service_account_file(sa_file, scopes=scopes, subject=subject)
        else:
            return None, 'service account credentials not configured'
        return creds, None
    except Exception as e:
        return None, str(e)


@app.route('/workspace/chat/ping', methods=['POST'])
def workspace_chat_ping():
    """Post a message to a Google Chat webhook for approvals/alerts.

    Env: `CHAT_WEBHOOK_URL`
    Body (optional): { "text": "..." }
    """
    if not WORKSPACE_ENABLED:
        return jsonify({'error': 'workspace integration disabled'}), 400
    if _requests is None:
        return jsonify({'error': 'requests library not available'}), 501
    webhook = os.environ.get('CHAT_WEBHOOK_URL')
    if not webhook:
        return jsonify({'error': 'CHAT_WEBHOOK_URL not set'}), 400
    payload = request.get_json() or {"text": "Workspace ping from API Gateway"}
    try:
        resp = _requests.post(webhook, json=payload, timeout=10)
        return jsonify({'status': 'delivered', 'code': resp.status_code}), 200 if resp.ok else 502
    except Exception as e:
        logger.error(f"Chat webhook error: {e}")
        return jsonify({'error': 'chat delivery failed', 'details': str(e)}), 500


@app.route('/workspace/gmail/send', methods=['POST'])
def workspace_gmail_send():
    """Send an email via Gmail API using service account with DWD.

    Env: `GMAIL_IMPERSONATE_USER` (user email to send as)
    Body: { "to": "user@example.com", "subject": "...", "body": "..." }
    """
    if not WORKSPACE_ENABLED:
        return jsonify({'error': 'workspace integration disabled'}), 400
    if build is None:
        return jsonify({'error': 'google api client not available'}), 501
    data = request.get_json() or {}
    to = data.get('to')
    subject = data.get('subject', 'Gateway Test')
    body = data.get('body', 'This is a test message from API Gateway.')
    if not to:
        return jsonify({'error': 'missing "to"'}), 400
    sender = os.environ.get('GMAIL_IMPERSONATE_USER')
    if not sender:
        return jsonify({'error': 'GMAIL_IMPERSONATE_USER not set'}), 400
    scopes = ['https://www.googleapis.com/auth/gmail.send']
    creds, err = _get_workspace_credentials(scopes, subject=sender)
    if err:
        return jsonify({'error': err}), 500
    try:
        service = build('gmail', 'v1', credentials=creds)
        msg = MIMEText(body)
        msg['to'] = to
        msg['from'] = sender
        msg['subject'] = subject
        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        sent = service.users().messages().send(userId='me', body={'raw': raw}).execute()
        return jsonify({'status': 'sent', 'id': sent.get('id')}), 200
    except HttpError as he:
        logger.error(f"Gmail API error: {he}")
        return jsonify({'error': 'gmail api error', 'details': str(he)}), 502
    except Exception as e:
        logger.error(f"Gmail send failed: {e}")
        return jsonify({'error': 'gmail send failed', 'details': str(e)}), 500


@app.route('/workspace/sheets/read', methods=['GET'])
def workspace_sheets_read():
    """Read a range from Google Sheets.

    Env: `SHEETS_SPREADSHEET_ID`, optional `SHEETS_RANGE_DEFAULT`
    Query: `range=A1:B10`
    """
    if not WORKSPACE_ENABLED:
        return jsonify({'error': 'workspace integration disabled'}), 400
    if build is None:
        return jsonify({'error': 'google api client not available'}), 501
    spreadsheet_id = os.environ.get('SHEETS_SPREADSHEET_ID')
    if not spreadsheet_id:
        return jsonify({'error': 'SHEETS_SPREADSHEET_ID not set'}), 400
    rng = request.args.get('range') or os.environ.get('SHEETS_RANGE_DEFAULT', 'A1:C10')
    scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    creds, err = _get_workspace_credentials(scopes)
    if err:
        return jsonify({'error': err}), 500
    try:
        service = build('sheets', 'v4', credentials=creds)
        resp = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=rng).execute()
        return jsonify({'range': resp.get('range'), 'values': resp.get('values', [])}), 200
    except HttpError as he:
        logger.error(f"Sheets API error: {he}")
        return jsonify({'error': 'sheets api error', 'details': str(he)}), 502
    except Exception as e:
        logger.error(f"Sheets read failed: {e}")
        return jsonify({'error': 'sheets read failed', 'details': str(e)}), 500


@app.route('/workspace/drive/write', methods=['POST'])
def workspace_drive_write():
    """Create a text file in Drive using app file scope.

    Body: { "name": "test.txt", "content": "hello" }
    """
    if not WORKSPACE_ENABLED:
        return jsonify({'error': 'workspace integration disabled'}), 400
    if build is None or MediaIoBaseUpload is None or io is None:
        return jsonify({'error': 'google drive client not available'}), 501
    data = request.get_json() or {}
    name = data.get('name', 'gateway-test.txt')
    content = data.get('content', 'Gateway test file')
    scopes = ['https://www.googleapis.com/auth/drive.file']
    creds, err = _get_workspace_credentials(scopes)
    if err:
        return jsonify({'error': err}), 500
    try:
        service = build('drive', 'v3', credentials=creds)
        media = MediaIoBaseUpload(io.BytesIO(content.encode()), mimetype='text/plain', resumable=False)
        file_meta = {'name': name}
        created = service.files().create(body=file_meta, media_body=media, fields='id,name').execute()
        return jsonify({'status': 'created', 'id': created.get('id'), 'name': created.get('name')}), 200
    except HttpError as he:
        logger.error(f"Drive API error: {he}")
        return jsonify({'error': 'drive api error', 'details': str(he)}), 502
    except Exception as e:
        logger.error(f"Drive write failed: {e}")
        return jsonify({'error': 'drive write failed', 'details': str(e)}), 500


@app.route('/journal/summary', methods=['GET'])
def journal_summary():
    """Get journal summary statistics."""
    result = gateway.get_journal_summary()
    return jsonify(result['data']), result['status']


if __name__ == '__main__':
    logger.info(f"Starting API Gateway on port {PORT}")
    init_gateway()
    app.run(host='0.0.0.0', port=PORT, debug=False, threaded=True)
