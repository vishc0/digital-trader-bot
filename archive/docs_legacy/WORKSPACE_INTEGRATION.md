# Google Workspace Integration Guide

This guide connects your Cloud Run deployment to Google Workspace (Chat, Gmail, Sheets, Drive) with secure, least-privilege access and simple smoke tests via the API Gateway.

## Prerequisites

- Google Workspace Admin access (or Cloud Identity)
- GCP project under the same organization (recommended)
- `gcloud` CLI authenticated and project set

## Enable APIs

```bash
gcloud services enable gmail.googleapis.com calendar-json.googleapis.com drive.googleapis.com sheets.googleapis.com chat.googleapis.com people.googleapis.com admin.googleapis.com
```

## OAuth Consent & Service Account (DWD)

- OAuth Consent Screen: Set to **Internal**, add test users.
- Create a **service account** (e.g., `workspace-bot`) and configure **Domain-Wide Delegation (DWD)** in Admin Console.
- Scopes to grant (least-privilege):
  - Gmail send: `https://www.googleapis.com/auth/gmail.send`
  - Sheets read-only: `https://www.googleapis.com/auth/spreadsheets.readonly`
  - Drive app files: `https://www.googleapis.com/auth/drive.file`
- Download the service account JSON key or use **Workload Identity**; store the JSON in **Secret Manager**.

## Configure Secrets & Env Vars

- Secrets:
  - `workspace-sa-json`: Service account JSON content.
  - `chat-webhook-url`: Incoming webhook URL for a Google Chat Space.
- Deploy API Gateway with envs:

```bash
gcloud run services update api-gateway \
  --region us-central1 \
  --set-env-vars=WORKSPACE_ENABLED=true,GMAIL_IMPERSONATE_USER=bot@yourdomain.com,SHEETS_SPREADSHEET_ID=YOUR_SHEET_ID,SHEETS_RANGE_DEFAULT=A1:C10 \
  --set-secrets=WORKSPACE_SA_JSON=workspace-sa-json:latest,CHAT_WEBHOOK_URL=chat-webhook-url:latest
```

Env var options:

- `WORKSPACE_ENABLED`: `true` to enable endpoints
- `WORKSPACE_SA_JSON`: Inline JSON from Secret Manager (or use `WORKSPACE_SA_FILE` for file path)
- `GMAIL_IMPERSONATE_USER`: Email address to send as (must be in your domain)
- `SHEETS_SPREADSHEET_ID`: Target Sheet ID
- `SHEETS_RANGE_DEFAULT`: Default read range (e.g., `A1:C10`)
- `CHAT_WEBHOOK_URL`: Chat incoming webhook URL

## Smoke Tests

Assuming `WEBUI_URL` and `APIGW_URL` are set.

```bash
# Chat webhook
curl -X POST "$APIGW_URL/workspace/chat/ping" \
  -H "Content-Type: application/json" \
  -d '{"text":"Approval ping from Gateway"}'

# Gmail send
curl -X POST "$APIGW_URL/workspace/gmail/send" \
  -H "Content-Type: application/json" \
  -d '{"to":"you@yourdomain.com","subject":"Gateway Test","body":"Hello from Gateway"}'

# Sheets read
curl "$APIGW_URL/workspace/sheets/read?range=A1:C5"

# Drive write
curl -X POST "$APIGW_URL/workspace/drive/write" \
  -H "Content-Type: application/json" \
  -d '{"name":"gateway-test.txt","content":"Hello from Gateway"}'
```

## Notes

- Keep OAuth consent **Internal** to minimize verification overhead.
- Prefer **Domain-Wide Delegation** for server-to-server actions; limit scopes strictly.
- Store secrets in **Secret Manager**; avoid embedding credentials in images.
- For Chat bots beyond webhooks, consider Chat API and app review steps; webhooks are simplest for approvals and alerts.
- Monitor Admin audit logs for delegated access; rotate service account keys; consider Workload Identity Federation to avoid static keys.
