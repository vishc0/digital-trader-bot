import os
import jwt
import json
from jwt import InvalidTokenError
from datetime import datetime, timedelta

JWT_SECRET = os.environ.get('API_JWT_SECRET', 'dev-secret')
JWT_ALGORITHM = os.environ.get('API_JWT_ALGO', 'HS256')
JWT_EXP_SECONDS = int(os.environ.get('API_JWT_EXP_SECONDS', 3600))

# Dev-only simple user store file (plaintext passwords for local/dev testing)
USERS_FILE = os.path.join(os.path.dirname(__file__), 'users.json')


def _load_users():
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            j = json.load(f)
            users = {u['username']: u for u in j.get('users', [])}
            return users
    except Exception:
        return {}


_USERS = _load_users()


def authenticate_user(username: str, password: str):
    """Simple plaintext username/password check against `users.json`.

    WARNING: This is intentionally minimal for local development only.
    Do NOT use plaintext user stores or this mechanism in production.
    """
    user = _USERS.get(username)
    if not user:
        return None
    if user.get('password') != password:
        return None
    return {'username': username, 'roles': user.get('roles', []), 'display_name': user.get('display_name', username)}


def issue_jwt(user: dict):
    now = datetime.utcnow()
    payload = {
        'sub': user.get('username'),
        'roles': user.get('roles', []),
        'name': user.get('display_name'),
        'iat': int(now.timestamp()),
        'exp': int((now + timedelta(seconds=JWT_EXP_SECONDS)).timestamp())
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    # PyJWT may return bytes on some versions; ensure str
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token



def decode_jwt(token: str):
    """Decode and verify a JWT token. Returns payload dict or raises InvalidTokenError."""
    if not token:
        raise InvalidTokenError('No token provided')
    # token may include 'Bearer '
    if token.lower().startswith('bearer '):
        token = token.split(' ', 1)[1]
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])


def get_user_from_request(req):
    """Extract JWT from Authorization header and return claims.
    Returns dict with `sub` or `user_id` and `roles`.
    """
    auth = req.headers.get('Authorization')
    if not auth:
        return None
    try:
        payload = decode_jwt(auth)
        return payload
    except InvalidTokenError:
        return None
*** End Patch