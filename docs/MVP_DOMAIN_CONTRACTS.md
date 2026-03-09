# MVP Domain Contracts

## Purpose

These contracts freeze the MVP data model for a built-in paper trading account while preserving a clean upgrade path to Phase 2 Fidelity market-account integration.

## Design rules

- The same operator workflow must work for both MVP paper trading and future Fidelity-backed execution.
- Contract names and IDs should remain stable across phases.
- Broker-specific fields belong in adapter metadata, not in core contracts.
- Every execution-relevant object must be journaled.
- AI recommendation objects must stay separate from hard risk and approval objects.

## Core identifiers

- `account_id`: stable account identifier. MVP format: `paper:<workspace_or_user>:<name>`.
- `recommendation_id`: unique recommendation identifier.
- `approval_id`: unique approval decision identifier.
- `order_id`: platform order identifier.
- `broker_order_id`: adapter-specific order identifier. Optional in MVP.
- `fill_id`: unique fill identifier.
- `position_id`: stable position identifier by account and symbol.
- `journal_event_id`: unique journal event identifier.
- `correlation_id`: shared workflow trace identifier across recommendation, approval, order, fill, and journal events.

## Canonical contracts

### 1. Paper account

Represents the built-in paper trading account.

```json
{
  "account_id": "paper:local:primary",
  "account_type": "paper",
  "base_currency": "USD",
  "status": "active",
  "owner_ref": "local-operator",
  "created_at": "2026-03-08T00:00:00Z",
  "buying_power": 100000.0,
  "cash_available": 100000.0,
  "cash_reserved": 0.0,
  "equity": 100000.0,
  "market_value": 0.0,
  "realized_pnl": 0.0,
  "unrealized_pnl": 0.0,
  "metadata": {
    "simulation_mode": "end_of_bar_or_quote_snapshot"
  }
}
```

### 2. Cash ledger entry

Tracks paper cash movements.

```json
{
  "ledger_entry_id": "ledg_001",
  "account_id": "paper:local:primary",
  "entry_type": "reserve|release|fill_debit|fill_credit|fee|adjustment",
  "amount": 1250.25,
  "currency": "USD",
  "related_order_id": "ord_001",
  "timestamp": "2026-03-08T00:00:00Z",
  "notes": "paper buy reserve"
}
```

### 3. Position summary

Represents current holdings.

```json
{
  "position_id": "paper:local:primary:AAPL",
  "account_id": "paper:local:primary",
  "symbol": "AAPL",
  "quantity": 10,
  "average_cost": 180.25,
  "market_price": 182.1,
  "market_value": 1821.0,
  "unrealized_pnl": 18.5,
  "realized_pnl": 0.0,
  "opened_at": "2026-03-08T00:00:00Z",
  "updated_at": "2026-03-08T00:05:00Z"
}
```

### 4. Portfolio summary

Aggregated account snapshot for the GUI.

```json
{
  "account_id": "paper:local:primary",
  "timestamp": "2026-03-08T00:05:00Z",
  "equity": 100018.5,
  "cash_available": 98197.5,
  "cash_reserved": 0.0,
  "market_value": 1821.0,
  "day_pnl": 18.5,
  "total_realized_pnl": 0.0,
  "total_unrealized_pnl": 18.5,
  "open_positions": 1,
  "open_orders": 0,
  "pending_approvals": 0
}
```

### 5. Watchlist item

```json
{
  "watchlist_id": "wl_primary",
  "symbol": "AAPL",
  "thesis": "Large-cap momentum with earnings support",
  "priority": "high",
  "added_at": "2026-03-08T00:00:00Z",
  "tags": ["momentum", "earnings"]
}
```

### 6. Recommendation

AI or rules-generated trade idea, separate from approval and execution.

```json
{
  "recommendation_id": "rec_001",
  "account_id": "paper:local:primary",
  "symbol": "AAPL",
  "action": "buy",
  "thesis": "Breakout above resistance with positive breadth",
  "strategy_id": "momentum_v1",
  "confidence": 0.74,
  "expected_holding_period": "swing",
  "entry_zone": {
    "low": 181.5,
    "high": 182.5
  },
  "targets": [186.0],
  "stop_loss": 178.4,
  "expected_return_pct": 0.021,
  "risk_reward_ratio": 2.1,
  "max_position_size_pct": 0.05,
  "created_at": "2026-03-08T00:00:00Z",
  "expires_at": "2026-03-08T01:00:00Z",
  "correlation_id": "corr_001",
  "explanation": {
    "signals": ["price_breakout", "volume_confirmation"],
    "risks": ["gap_down", "macro_event_today"]
  }
}
```

### 7. Approval decision

Human or policy decision on a recommendation or order.

```json
{
  "approval_id": "apr_001",
  "recommendation_id": "rec_001",
  "account_id": "paper:local:primary",
  "decision": "approved|rejected|expired",
  "approved_action": "buy",
  "approved_quantity": 10,
  "approved_notional": 1820.0,
  "reviewer_id": "operator_1",
  "review_notes": "Position size acceptable",
  "expires_at": "2026-03-08T00:15:00Z",
  "created_at": "2026-03-08T00:05:00Z",
  "correlation_id": "corr_001"
}
```

### 8. Order record

Platform order object used by both paper execution and future broker adapters.

```json
{
  "order_id": "ord_001",
  "account_id": "paper:local:primary",
  "recommendation_id": "rec_001",
  "approval_id": "apr_001",
  "symbol": "AAPL",
  "side": "buy",
  "order_type": "market|limit|stop|stop_limit",
  "time_in_force": "day",
  "quantity": 10,
  "limit_price": null,
  "stop_price": null,
  "status": "pending|accepted|partially_filled|filled|cancelled|rejected|expired",
  "submitted_at": "2026-03-08T00:05:10Z",
  "broker_name": "paper_engine",
  "broker_order_id": null,
  "correlation_id": "corr_001",
  "metadata": {
    "source": "approved_recommendation"
  }
}
```

### 9. Fill record

```json
{
  "fill_id": "fill_001",
  "order_id": "ord_001",
  "account_id": "paper:local:primary",
  "symbol": "AAPL",
  "side": "buy",
  "quantity": 10,
  "price": 182.0,
  "fees": 0.0,
  "filled_at": "2026-03-08T00:05:12Z",
  "liquidity": "simulated",
  "correlation_id": "corr_001"
}
```

### 10. Expected vs actual outcome

Used for post-trade review.

```json
{
  "outcome_id": "out_001",
  "recommendation_id": "rec_001",
  "order_id": "ord_001",
  "account_id": "paper:local:primary",
  "symbol": "AAPL",
  "expected_entry": 182.0,
  "actual_entry": 182.0,
  "expected_return_pct": 0.021,
  "realized_return_pct": 0.013,
  "expected_max_drawdown_pct": 0.01,
  "actual_max_drawdown_pct": 0.008,
  "outcome_status": "open|closed|expired",
  "measured_at": "2026-03-08T04:00:00Z",
  "correlation_id": "corr_001"
}
```

### 11. Exit review

```json
{
  "exit_review_id": "exit_001",
  "position_id": "paper:local:primary:AAPL",
  "symbol": "AAPL",
  "recommended_action": "hold|trim|exit",
  "reason_codes": ["target_hit", "trend_weakened"],
  "created_at": "2026-03-08T04:00:00Z",
  "correlation_id": "corr_001"
}
```

### 12. Journal event

The minimum durable audit record.

```json
{
  "journal_event_id": "je_001",
  "event_type": "recommendation_created",
  "category": "ai_decision|approval|order|fill|position|risk|system_health",
  "account_id": "paper:local:primary",
  "entity_id": "rec_001",
  "correlation_id": "corr_001",
  "timestamp": "2026-03-08T00:00:00Z",
  "service": "strategy_engine",
  "severity": "info",
  "payload": {
    "symbol": "AAPL",
    "action": "buy"
  }
}
```

## Minimum status enums

- `account.status`: `active`, `paused`, `archived`
- `recommendation.action`: `buy`, `sell`, `trim`, `hold`, `exit`
- `approval.decision`: `approved`, `rejected`, `expired`
- `order.status`: `pending`, `accepted`, `partially_filled`, `filled`, `cancelled`, `rejected`, `expired`
- `journal.category`: `ai_decision`, `approval`, `order`, `fill`, `position`, `risk`, `system_health`

## MVP workflow map

1. Strategy engine creates `recommendation`.
2. Risk rules validate position size and action eligibility.
3. Human creates `approval decision`.
4. Execution manager creates `order record`.
5. Paper engine creates `fill record` and updates `cash ledger` plus `position summary`.
6. Journaling service persists `journal event` records for each state change.
7. Outcome service computes `expected vs actual outcome` and `exit review`.

## Phase 2 compatibility note

When Fidelity integration is added:

- `account_type` may become `broker_live` or `broker_paper`.
- `broker_name` becomes `fidelity`.
- `broker_order_id` is populated by the adapter.
- Broker-specific payloads stay under `metadata` or adapter event payloads.
- Core workflow objects and IDs stay unchanged.
