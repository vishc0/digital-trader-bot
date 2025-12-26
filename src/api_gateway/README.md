API Gateway - Dev Login
======================

This API Gateway includes a simple username/password login for local development only.

Location:

- `src/api_gateway/users.json` — simple dev users (plaintext passwords).
- `src/api_gateway/auth.py` — authentication helpers (`authenticate_user`, `issue_jwt`, `get_user_from_request`).

Usage (PowerShell examples):

Login and get a token:

```powershell
curl -X POST http://localhost:8000/auth/login -H "Content-Type: application/json" -d '{"username":"operator1","password":"operatorpass"}'
```

The response contains `access_token`. Use it in subsequent requests:

```powershell
$token = "<access_token>"
curl http://localhost:8000/trading/approval-status -H "Authorization: Bearer $token"
```

Security note:

This mechanism is intentionally minimal for developer convenience. For any staging or production deployment, replace this with a proper identity provider, hashed password store, and TLS-protected endpoints. Consider using OAuth/OIDC and a secret manager.
