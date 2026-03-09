# 🔐 Security Assessment & Secret Inventory

**Classification**: CONFIDENTIAL
**Last Drafted**: 2025-12-27

## 1. Security Posture Overview

The system currently relies on **Perimeter Security** (Tailscale) and **Host Security** (SSH Keys). Service-to-service communication is currently trusted and unencrypted inside the mesh.

### Critical Vulnerabilities

1. **Open Data Layer**: Redis is unauthenticated. Anyone on the Tailscale network can read/write state.
2. **Secret sprawl**: API keys are currently passed as plaintext Environment Variables or potentially hardcoded.

## 2. Secret Inventory (The "Keys to the Kingdom")

| Component | Secret Type | Location | Usage | Rotation Strategy |
|-----------|-------------|----------|-------|-------------------|
| **Node Access** | SSH Private Key | `~/.ssh/id_ed25519` (Local PC) | Accessing Node 1 & 2 | Manual `ssh-keygen` |
| **Tailscale** | Auth Key | Node System Config | Joining Mesh Network | Expire in Admin Console |
| **Google AI** | API Key | `.env` (Node 2) | `External Intelligence` -> Gemini | GCP Console Revoke |
| **Broker (IBKR)** | TWS Port/Account | `paper_account_config` | Execution Manager | Change Password |
| **Redis** | **Default User** | *None (Currently Empty)* | **Database Access** | **URGENT: Set Password** |

## 3. Component Authentication Map

* **User -> Frontend**: (Planned) JWT Auth via API Gateway.
* **Gateway -> Services**: Internal HTTP (Trusted).
* **Services -> Redis**: TCP (Currently Open). planned: `redis://:password@host:6379`.

## 4. Remediation Plan

1. **Immediate**: Generate a strong random string for Redis Password.
2. **Short Term**: Store this password in a `.env` file on Node 1 (backed up securely).
3. **Long Term**: Use Docker Secrets or a Vault service.
