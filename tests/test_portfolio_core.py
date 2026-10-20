"""Stdlib unit tests: python -m unittest discover -s tests -p 'test_portfolio_core.py'."""
import sys
from pathlib import Path
import unittest
from decimal import Decimal as D

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "platform" / "backend"))
from portfolio_core.policy import Account, Holding, Proposal, evaluate, summarize, reconcile

class PortfolioPolicyTests(unittest.TestCase):
    def setUp(self):
        self.ira = Account("fidelity_child_1", "Fidelity", "roth_ira", "6005", custodial=True)
        self.buy = Proposal("fidelity_child_1", "MSFT", "BUY", D("1"), D("400"))

    def test_unknown_permissions_and_cash_fail_closed(self):
        result = evaluate(self.ira, self.buy)
        self.assertFalse(result["eligible_for_manual_review"])
        self.assertFalse(result["execution_enabled"])
        self.assertIn("permissions_unverified", result["reasons"])
        self.assertIn("settled_cash_unverified", result["reasons"])

    def test_wrong_account_blocked(self):
        permitted = Account("other", "Fidelity", "ira", "3868", permissions={"trade_stock": True},
                            permissions_verified=True, settled_cash=D("1000"), settled_cash_verified=True)
        self.assertIn("wrong_account", evaluate(permitted, self.buy)["reasons"])

    def test_overspending_blocked(self):
        acc = Account("fidelity_child_1", "Fidelity", "roth_ira", "6005", True,
                      {"trade_stock": True}, D("100"), True, True)
        self.assertIn("insufficient_settled_cash", evaluate(acc, self.buy)["reasons"])

    def test_short_sell_blocked(self):
        acc = Account("fidelity_child_1", "Fidelity", "roth_ira", "6005", True,
                      {"trade_stock": True}, D("1000"), True, True)
        sell = Proposal(acc.key, "MSFT", "SELL", D("2"), D("400"))
        self.assertIn("short_or_missing_position", evaluate(acc, sell,
                      [Holding("MSFT", D("1"), D("400"), "2026-10-19")])["reasons"])

    def test_eligible_only_for_manual_review(self):
        acc = Account("fidelity_child_1", "Fidelity", "roth_ira", "6005", True,
                      {"trade_stock": True}, D("1000"), True, True)
        result = evaluate(acc, self.buy)
        self.assertTrue(result["eligible_for_manual_review"])
        self.assertFalse(result["execution_enabled"])

    def test_dated_portfolio_summary(self):
        data = summarize([Holding("MSFT", D("2"), D("400"), "2026-10-19")])
        self.assertEqual(data["security_value"], "800")
        self.assertFalse(data["mixed_price_dates"])

    def test_reconciliation_preserves_missing_status(self):
        result = reconcile({"MSFT": D("2")}, {})
        self.assertEqual(result["missing_from_broker"], ["MSFT"])

if __name__ == "__main__":
    unittest.main()
