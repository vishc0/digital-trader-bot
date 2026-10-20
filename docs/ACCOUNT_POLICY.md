# Account-aware portfolio policy and restrictions (2026-10-20)

## Safety-first scope
Platform is research, portfolio monitoring and proposal generation only. Broker execution is DISABLED until audited adapter, explicit human approval, and production controls are validated. Deny-by-default when permission, cash settlement, legal ownership, account status or data freshness are unknown. Do not infer a capability from account type or holdings alone.

## Account registry
Keys are internal opaque IDs; display masked account identifiers only. Exact provider account IDs must remain in secrets/config, never committed. Linked read-only financial observations (2026-10-20) show:
- Fidelity ••6005 — Shivam Roth IRA, IRA subtype. Custodial Roth relationship is prior user-provided context; verify the legal registration at broker.
- Fidelity ••3868 — Shourya Roth IRA, IRA subtype. Custodial Roth relationship is prior user-provided context; verify the legal registration at broker.
- Charles Schwab ••4792 — Contributory IRA, IRA subtype; retirement type specifics need verification.
- E*TRADE ••9845 — Individual brokerage account, subtype brokerage; cash/margin and options privileges unknown.

Balances from account aggregators are snapshots, NOT evidence of settled funds, buying power, account trading permissions, or up-to-date fills. Linked-account refresh time != source balance timestamp. Do not persist actual balances in this static policy.

## Schema
For each account store:
- account_key, broker, masked_number, legal_registration, tax_wrapper, custodian_owner_roles, beneficiary, residency_jurisdiction, base_currency
- access_mode (read_only|paper|order_preview|manual_execution_only), permissions_verified_at, broker_permissions_source, approval_ledger
- asset_allowlist / denylist, option_level, margin_type (none|limited_ira|full|unknown), shorting_enabled, day_trade_restrictions, trading_violations
- cash_settled, cash_unsettled, available_to_trade, available_to_withdraw, pending_orders_commitment, holds, balances_as_of, buying_power_as_of
- contribution_tax_year, earned_income_verified, permitted_annual_ira_contribution, contributions_ytd, rollovers, distribution_tracking
- concentration_limits, risk_budget, strategy_allowlist, time_horizon, suitability_guard, order_precision, market_hours, settlement_calendar
- ownership_transition_date or age-jurisdiction event with verification status; review_on_change and manual_override with audit trail.

Each permission is ALLOWED / DENIED / UNKNOWN plus evidence timestamp and source. UNKNOWN is always DENIED for order eligibility. Account-level policy overrides global strategy and model suggestions.

## Initial default policy
| Scope | Default |
|---|---|
| Fidelity child Roth x2 | Stocks/eligible funds for research; prohibit shorting and borrowed margin; no options, leverage or automated orders; verify eligibility and broker approval for each specific security |
| Schwab contributory IRA | No shorting, borrowed margin or automated orders; options disabled until explicit verified broker permissions AND user policy approval |
| E*TRADE taxable brokerage | Conservative cash-account assumptions until margin/options status confirmed; automated execution disabled |
| All | Never cross-use buying power, proceeds or tax lots between accounts; no invented source timestamps, zero holdings or approved positions |

Fidelity official references: https://www.fidelity.com/retirement/roth-ira-kids and https://www.fidelity.com/learning-center/trading-investing/trading/limited-margin-trading-ira . Broker-specific restrictions and latest authoritative agreements must be checked before policy changes.

## Mandatory proposal evaluation
1. Validate account status, role authorization, latest broker permissions and source freshness.
2. Match security identity and asset eligibility (including fractional-share/order-type support).
3. Check hard blocks: short, leverage, unauthorized options, age/custodial controls, transfer restrictions, open-order conflicts, sanctions and restricted securities.
4. Verify independently authoritative broker settled cash, current open orders, settlement dates, executable quantity, trading session and minimum notional. If missing: research only.
5. Evaluate portfolio cash reserve, exposure to correlated companies/themes, price volatility, liquidity, earnings and corporate-action windows.
6. Produce explainable proposal with account, ticker, side, quantity, limit/notional, max spend, expected resulting weights, data timestamp, expiry, thesis, counterargument and named policy checks. Do not route order from prose.
7. Require explicit account-specific human approval to create order preview; then revalidate the entire gate at placement. Approval != submission != fill.
8. Reconcile partial fills, commissions, corporate actions and provider transaction identifiers; manual confirmation when broker feed is incomplete.
9. Audit immutable events and an emergency disable switch. Violation or stale data causes hard-stop, not model-based exception.

## Regulatory/tax guardrails
- Roth IRA for Kids contributions require qualifying earned income; enforce applicable year's lesser-of-earned-income-or-limit only after broker/tax-source validation. 2026 Fidelity published nominal maximum $7,500. Flag, do not infer, earned income.
- Retirement assets must be kept distinct from taxable brokerage for wash-sale exposure analysis, tax reporting and portfolio-level analytics. A wash sale involving purchases in an IRA can have distinct tax consequences; consult current tax guidance before tax suggestions.
- Child account control belongs to custodian until actual transfer under applicable registration and jurisdiction; age thresholds are not a universal constant.
- Cash accounts: T+1 settlement for applicable US securities; watch good-faith, freeriding and cash liquidation violations. Brokerage trading restrictions are not derivable from account subtype alone.
- Do not conflate Fidelity Youth Accounts, UGMA/UTMA accounts, and a Roth IRA for Kids.

## Required tests
- Unknown settled cash -> no order proposal ready.
- IRA short sale, borrowed margin, option approval unknown -> block.
- Wrong account and shared portfolio cash leakage -> block.
- Duplicate order, stale quote, unrecognized symbol, corporate action, restricted security -> block.
- Partial fill or cancel state never recognized as a confirmed full fill.
- Earned income unknown or contributions close to annual limit -> stop contribution recommendation pending verification.
- Custodian-role unverified or ownership transfer event -> lock order privileges.
- System/model failure -> fail closed with readable explanation.
