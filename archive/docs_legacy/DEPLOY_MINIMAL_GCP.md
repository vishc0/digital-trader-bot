# Minimal GCP Deploy (Near-Zero Cost Testing)

This guide deploys only the **API Gateway** (in MOCK_MODE) and the **Web UI** to Cloud Run. No other services are required. The UI proxies `/api` calls to the Gateway, which returns synthetic data so you can test end-to-end.

## Prerequisites

- `gcloud` CLI authenticated and default project set
- Artifact Registry enabled (automatically used by Cloud Build)

## 1) Build & Deploy API Gateway (MOCK_MODE)

```bash
# Build
gcloud builds submit \
  --tag gcr.io/$(gcloud config get-value project)/api-gateway:latest \
  src/api_gateway

# Deploy (unauthenticated for quick testing)
gcloud run deploy api-gateway \
  --image gcr.io/$(gcloud config get-value project)/api-gateway:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars=PORT=8000,MOCK_MODE=true

# Get URL
APIGW_URL=$(gcloud run services describe api-gateway --region us-central1 --platform managed --format='value(status.url)')
echo $APIGW_URL
```

## 2) Build & Deploy Web UI (proxy to Gateway)

```bash
# Build
gcloud builds submit \
  --tag gcr.io/$(gcloud config get-value project)/web-ui:latest \
  src/web_ui

# Deploy
gcloud run deploy web-ui \
  --image gcr.io/$(gcloud config get-value project)/web-ui:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars=API_GATEWAY_URL=$APIGW_URL,PORT=8080

# Get UI URL
WEBUI_URL=$(gcloud run services describe web-ui --region us-central1 --platform managed --format='value(status.url)')
echo $WEBUI_URL
```

## 3) Smoke Tests

```bash
# UI reachable
curl -I "$WEBUI_URL"

# UI proxy reaches Gateway health
curl -I "$WEBUI_URL/api/health"

# Gateway health
curl -I "$APIGW_URL/health"

# Dashboard snapshot (synthetic data)
curl "$WEBUI_URL/api/dashboard/snapshot"

# Strategies (synthetic data)
curl "$WEBUI_URL/api/strategies"
```

## Notes

- **Cost control:** Cloud Run min instances are 0 by default; you pay only per request. This setup is typically <$5/month at light usage and near $0 when idle.
- **Auth:** In MOCK_MODE, API Gateway bypasses JWT checks for selected endpoints to let the UI function out of the box.
- **Next:** Deploy real services and set API Gateway env vars (`STATE_MANAGER_URL`, `STRATEGY_ENGINE_URL`, etc.) when ready.
