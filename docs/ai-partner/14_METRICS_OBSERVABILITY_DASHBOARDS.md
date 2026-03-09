# Metrics, Observability, and Dashboards

## Monitoring goals
- Detect broken trading workflows quickly.
- Understand system health and business health together.
- Measure AI value, latency, and token cost.
- Make paper-to-live progression auditable.

## Core metric groups
### Platform metrics
- Service uptime
- Request latency
- Error rate
- Queue depth
- Redis health
- Journal write success rate

### Trading metrics
- Suggested trades per day
- Approved vs rejected trades
- Fill rate
- Slippage
- Realized P&L
- Unrealized P&L
- Drawdown
- Expected vs actual outcome delta
- Exit quality score

### AI metrics
- Tokens in
- Tokens out
- Cost per workflow
- Latency per model call
- Cache hit rate
- Hallucination or invalid-output rate
- Recommendation acceptance rate

### Risk and compliance metrics
- Max position breaches prevented
- Circuit breaker activations
- Price sanity rejections
- Policy rejections
- Manual override count

## Dashboards
### 1. Operator dashboard
- Portfolio value
- Open positions
- Watchlist
- Suggested actions
- Approval queue
- P&L and exits

### 2. Platform health dashboard
- Service health by module
- Dependency health
- Error heatmap
- Trace latency waterfall

### 3. AI cost and quality dashboard
- Token usage by workflow
- Cost by day and by feature
- Model success rate
- Cache effectiveness

### 4. Risk dashboard
- Exposure by symbol and sector
- Daily drawdown
- Rejected orders
- Compliance warnings

## Minimum implementation stack
- OpenTelemetry for traces and metrics.
- Prometheus-compatible metrics endpoints.
- Grafana dashboards.
- Structured logs to a central sink.
- Journal-backed business analytics.
