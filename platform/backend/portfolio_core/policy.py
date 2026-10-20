"""Fail-closed portfolio analysis and account restriction checks. No order submission."""
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional

D = Decimal

@dataclass(frozen=True)
class Account:
    key: str
    broker: str
    kind: str
    masked_number: str
    custodial: bool = False
    permissions: dict = field(default_factory=dict)
    settled_cash: Optional[Decimal] = None
    settled_cash_verified: bool = False
    permissions_verified: bool = False

@dataclass(frozen=True)
class Holding:
    ticker: str
    quantity: Decimal
    price: Decimal
    price_as_of: str
    currency: str = "USD"

@dataclass(frozen=True)
class Proposal:
    account_key: str
    ticker: str
    side: str
    quantity: Decimal
    limit_price: Decimal
    asset_type: str = "stock"

def evaluate(account: Account, proposal: Proposal, holdings=()):
    """Returns a non-executable assessment; unknown inputs block order-readiness."""
    reasons = []
    if proposal.account_key != account.key:
        reasons.append("wrong_account")
    if proposal.side not in ("BUY", "SELL") or proposal.quantity <= 0 or proposal.limit_price <= 0:
        reasons.append("invalid_order")
    if proposal.asset_type not in ("stock", "etf"):
        reasons.append("unsupported_asset")
    if not account.permissions_verified:
        reasons.append("permissions_unverified")
    if account.permissions.get("trade_" + proposal.asset_type) is not True:
        reasons.append("asset_permission_missing")
    if proposal.side == "SELL":
        position = sum((h.quantity for h in holdings if h.ticker == proposal.ticker), D("0"))
        if position < proposal.quantity:
            reasons.append("short_or_missing_position")
    if proposal.side == "BUY":
        if not account.settled_cash_verified or account.settled_cash is None:
            reasons.append("settled_cash_unverified")
        elif account.settled_cash < proposal.quantity * proposal.limit_price:
            reasons.append("insufficient_settled_cash")
    # This module intentionally never approves/places an order.
    return {"account": account.key, "eligible_for_manual_review": not reasons,
            "execution_enabled": False, "reasons": sorted(set(reasons))}

def summarize(holdings):
    """Totals only dated, valid observations; no inferred missing positions."""
    values = {}
    dates = set()
    for h in holdings:
        if h.quantity < 0 or h.price < 0 or not h.price_as_of:
            raise ValueError("invalid or undated holding")
        dates.add(h.price_as_of)
        values[h.ticker] = values.get(h.ticker, D("0")) + h.quantity * h.price
    total = sum(values.values(), D("0"))
    return {"security_value": str(total), "value_by_ticker": {k: str(v) for k,v in values.items()},
            "source_price_dates": sorted(dates), "mixed_price_dates": len(dates)>1}

def reconcile(expected, observed):
    """Distinguish missing observations from confirmed zero positions."""
    expected, observed = dict(expected), dict(observed)
    return {"missing_from_broker": sorted(set(expected)-set(observed)),
            "unmatched_at_broker": sorted(set(observed)-set(expected)),
            "quantity_mismatches": {
                ticker: {"expected": str(expected[ticker]), "observed": str(observed[ticker])}
                for ticker in sorted(set(expected)&set(observed))
                if expected[ticker] != observed[ticker]
            }}
