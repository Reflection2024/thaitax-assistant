#!/usr/bin/env python3
"""Tests for contracts.py. Run: python3 -I test_contracts.py"""
import os
import sys
import unittest
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import contracts as ct  # noqa: E402

SAMPLE = os.path.join(HERE, "..", "..", "..", "pilot", "sample-data")


class Contracts(unittest.TestCase):
    def setUp(self):
        self.r = ct.check(ct.read(os.path.join(SAMPLE, "supplier-contracts.csv")),
                          ct.read(os.path.join(SAMPLE, "supplier-payments-2569-10.csv")), date(2026, 11, 30))
        self.p = {x["supplier"]: x for x in self.r["payments"]}

    def test_correct_payment_has_no_flags(self):
        self.assertEqual(self.p["Clean Service Co."]["flags"], [])
        self.assertEqual(self.p["Clean Service Co."]["net_to_pay"], "26000.00")

    def test_rent_to_individual_5pct_pnd3(self):
        x = self.p["Somchai Jaidee"]
        self.assertEqual((x["wht_rate"], x["wht_form"], x["wht_due"]), ("0.05", "PND.3", "2000.00"))
        self.assertTrue(any("withholding not taken" in f for f in x["flags"]))

    def test_amount_differs_and_advertising_2pct(self):
        x = self.p["Samui Ads Co."]
        self.assertEqual(x["wht_due"], "240.00")
        self.assertTrue(any("differs from contract" in f for f in x["flags"]))

    def test_no_contract_no_invoice(self):
        f = self.p["Island Plumbing"]["flags"]
        self.assertIn("no contract on file for this payment", f)
        self.assertIn("no invoice / tax invoice on file", f)

    def test_totals_and_expiring(self):
        self.assertEqual(self.r["totals"]["wht_missing_thb"], "2240.00")
        self.assertEqual([c["contract_id"] for c in self.r["contracts_ending_within_30_days"]], ["C1"])

    def test_small_payment_no_withholding(self):
        c = [{"contract_id": "X", "supplier": "A", "legal_form": "company", "service_type": "services", "amount_before_vat": "900"}]
        p = [{"date": "2026-10-01", "supplier": "A", "invoice_no": "1", "invoice_before_vat": "900", "invoice_vat": "63", "wht_withheld": "0"}]
        self.assertEqual(ct.check(c, p, date(2026, 10, 31))["payments"][0]["wht_due"], "0")


if __name__ == "__main__":
    unittest.main(verbosity=1)
