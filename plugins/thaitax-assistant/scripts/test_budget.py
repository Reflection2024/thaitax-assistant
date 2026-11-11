#!/usr/bin/env python3
"""Tests for budget.py and budget_dashboard.py. Run: python3 -I test_budget.py"""
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import budget  # noqa: E402
import budget_dashboard  # noqa: E402


def t(d, desc, amt, cur="THB", acc="KBank 1234", cat=""):
    return {"date": d, "description": desc, "amount": amt, "currency": cur, "account": acc, "category": cat}


def load_rows(rows):
    fd, path = tempfile.mkstemp(suffix=".csv")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write("date,description,amount,currency,account,category\n")
        for r in rows:
            f.write(f'{r["date"]},{r["description"]},{r["amount"]},{r["currency"]},{r["account"]},{r["category"]}\n')
    txns = budget.load(path)
    os.unlink(path)
    return txns


class Budget(unittest.TestCase):
    def test_categorize_builtin_and_user_rule(self):
        self.assertEqual(budget.categorize("NETFLIX.COM", -419, {}), "Subscriptions")
        self.assertEqual(budget.categorize("Villa Mimosa", -45000, {"villa mimosa": "Housing"}), "Housing")

    def test_own_transfers_excluded(self):
        txns = load_rows([t("2026-08-01", "Salary", 100000), t("2026-08-02", "Transfer from own Wise account", 50000),
                          t("2026-08-03", "7-Eleven", -500)])
        s = budget.summarize(txns, {}, {})
        self.assertEqual(s["totals"]["income"], 100000)
        self.assertEqual(s["totals"]["spending"], 500)

    def test_fx_and_unconverted(self):
        txns = load_rows([t("2026-08-01", "Salary GmbH", 1000, "EUR"), t("2026-08-05", "Shop", -10, "GBP")])
        s = budget.summarize(txns, {}, {"EUR": 37.6})
        self.assertEqual(s["totals"]["income"], 37600)
        self.assertIn("GBP", s["unconverted_by_currency"])

    def test_recurring_and_duplicates(self):
        rows = []
        for m in ("08", "09", "10"):
            rows += [t(f"2026-{m}-03", "NETFLIX.COM", -419), t(f"2026-{m}-04", "DISNEY PLUS", -289),
                     t(f"2026-{m}-05", "GOOGLE ONE", -350), t(f"2026-{m}-06", "APPLE ICLOUD", -349),
                     t(f"2026-{m}-10", "ATM withdrawal", -5000)]
        s = budget.summarize(load_rows(rows), {}, {})
        merchants = {r["merchant"] for r in s["recurring"]}
        self.assertEqual(len(s["recurring"]), 4)
        self.assertFalse(any("atm" in m.lower() for m in merchants))
        self.assertIn("video streaming", s["possible_duplicate_subscriptions"])
        self.assertIn("cloud storage", s["possible_duplicate_subscriptions"])

    def test_sample_data(self):
        sample = os.path.join(HERE, "..", "..", "..", "pilot", "sample-data")
        csv_path = os.path.join(sample, "family-transactions-2026Q3.csv")
        if not os.path.exists(csv_path):
            self.skipTest("sample data not present")
        s = budget.summarize(budget.load(csv_path), {}, {"EUR": 37.6})
        self.assertAlmostEqual(s["totals"]["income"], 473760, delta=1)
        self.assertAlmostEqual(s["totals"]["spending"], 306907, delta=1)
        self.assertEqual(len(s["recurring"]), 12)

    def test_dashboard_renders_rtl(self):
        txns = load_rows([t("2026-08-01", "Salary", 100000), t("2026-08-03", "Makro", -3000)])
        s = budget.summarize(txns, {}, {})
        page = budget_dashboard.render(s, "he")
        self.assertIn('dir="rtl"', page)
        self.assertIn("฿100,000", page)
        self.assertNotIn("http", page.split("<body>")[1])  # no external resources

    def test_actual_export(self):
        txns = load_rows([t("2026-08-03", "Makro", -3000)])
        fd, out = tempfile.mkstemp(suffix=".csv")
        os.close(fd)
        budget.actual_export(txns, out, {})
        with open(out, encoding="utf-8") as f:
            head = f.readline()
        os.unlink(out)
        self.assertTrue(head.startswith("Date,Payee"))


if __name__ == "__main__":
    unittest.main(verbosity=1)
