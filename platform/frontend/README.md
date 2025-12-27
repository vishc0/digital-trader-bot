# Web UI - Digital Trader (Operator Console)

This is a minimal React (Vite) application that consumes the `api-gateway` endpoints.

Quick start (development):

1. Install dependencies

```bash
cd src/web_ui
npm install
```

2. Run dev server

```bash
npm run dev
```

3. Build for production

```bash
npm run build
```

Notes:
- The app expects an API proxy so client calls to `/api/...` are forwarded to the `api-gateway` service. When running with `docker-compose`, the `api-gateway` helper is configured to serve at `/api`.
- This scaffold provides Dashboard, Approvals, Strategies, and Order placement views. It's intentionally minimal and should be extended for production use.
