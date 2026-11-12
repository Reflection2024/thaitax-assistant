"""Tests for thaitax_calc.py. Run: python3 -I test_thaitax_calc.py."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import thaitax_calc as c  # noqa: E402


class T(unittest.TestCase):
    def test_vat(self):
        r = c.vat(85000)
        self.assertEqual((r["vat"], r["gross"]), ("5950.00", "90950.00"))
        r = c.vat(107, inclusive=True)
        self.assertEqual((r["net"], r["vat"]), ("100.00", "7.00"))
        self.assertTrue(c.vat_check(1000, "70.01")["ok"])
        self.assertFalse(c.vat_check(1000, "70.50")["ok"])

    def test_be(self):
        self.assertEqual(c.be("11/11/2569")["iso_ce"], "2026-11-11")
        self.assertEqual(c.be(2569)["ce"], 2026)
        self.assertEqual(c.be(2026)["be"], 2569)

    def test_sso(self):
        self.assertEqual(c.sso(30000)["employee"], "875.00")
        self.assertEqual(c.sso(10000)["employee"], "500.00")
        self.assertEqual(c.sso(1000)["employee"], "83.00")  # floor 1,650

    def test_wht(self):
        self.assertEqual(c.wht(85000, "services")["tax_withheld"], "2550.00")
        self.assertEqual(c.wht(85000, "services", e_wht=True)["tax_withheld"], "850.00")
        self.assertEqual(c.wht(20000, "rent")["tax_withheld"], "1000.00")
        with self.assertRaises(ValueError):
            c.wht(1, "nonsense")

    def test_overtime(self):
        r = c.overtime(30000, 8, ot_hours=10)
        self.assertEqual((r["hourly_rate"], r["overtime_1_5x"]), ("125.00", "1875.00"))

    def test_pit_foreign_salary_with_ftc(self):
        r = c.pit(income=[{"section": "40(1)", "amount": 1200000, "source": "DE"}], allowances=60000,
                  foreign=[{"country": "DE", "remitted_thb": 1200000, "foreign_tax_paid_thb": 200000, "treaty": True}])
        self.assertEqual(r["net_income"], "1040000.00")
        self.assertEqual(r["tax_payable"], "125000.00")
        self.assertEqual(r["credits"]["foreign_tax_credit"], "125000.00")
        self.assertEqual(r["result"], "0.00")

    def test_pit_rent_and_fees(self):
        r = c.pit(income=[{"section": "40(2)", "amount": 400000},
                          {"section": "40(5)", "amount": 240000, "kind": "building"}],
                  allowances=60000, withholding_credit=12000 + 12000)
        # 40(2): 50% capped 100k; rent 30% = 72,000
        self.assertEqual(r["expenses"], "172000.00")
        self.assertEqual(r["net_income"], "408000.00")
        self.assertEqual(r["progressive_tax"], "18300.00")  # 7,500 + 10,800
        self.assertEqual(r["method"], "progressive")

    def test_pit_minimum_tax(self):
        r = c.pit(income=[{"section": "40(8)", "amount": 2000000, "expense": {"actual": 1900000}}], allowances=60000)
        self.assertEqual(r["progressive_tax"], "0.00")
        self.assertEqual(r["minimum_tax_0_5pct"], "10000.00")
        self.assertEqual(r["tax_payable"], "10000.00")

    def test_bahttext(self):
        self.assertEqual(c.bahttext(90950)["text"], "เก้าหมื่นเก้าร้อยห้าสิบบาทถ้วน")
        self.assertEqual(c.bahttext("21.50")["text"], "ยี่สิบเอ็ดบาทห้าสิบสตางค์")
        self.assertEqual(c.bahttext(1000000)["text"], "หนึ่งล้านบาทถ้วน")
        self.assertEqual(c.bahttext(11)["text"], "สิบเอ็ดบาทถ้วน")

    def test_deadlines_shift(self):
        r = c.deadlines("2026-11", holidays=["2026-12-07"])
        self.assertEqual(r["PND.1/3/53/54 (withholding)"]["paper"]["date"], "2026-12-08")
        self.assertEqual(r["PP.30 (VAT)"]["online"]["date"], "2026-12-23")


    def test_land_building_tax(self):
        self.assertEqual(c.land_building_tax(20000000, "residential_other")["annual_tax"], "4000.00")
        self.assertEqual(c.land_building_tax(40000000, "main_home")["annual_tax"], "0.00")
        self.assertEqual(c.land_building_tax(5000000, "commercial")["annual_tax"], "15000.00")
        self.assertEqual(c.land_building_tax(100000000, "vacant", years_unused=3)["annual_tax"], "650000.00")

    def test_property_sale_company(self):
        r = c.property_sale(4000000, 5000000, seller="company", transfer_date="2026-11-11")
        self.assertEqual(r["transfer_fee"]["amount"], "80000.00")
        self.assertEqual(r["specific_business_tax"]["amount"], "165000.00")
        self.assertEqual(r["withholding_tax"]["amount"], "50000.00")

    def test_property_sale_individual_long_hold(self):
        r = c.property_sale(5000000, 5000000, seller="individual", years_held=8, transfer_date="2026-11-11")
        self.assertFalse(r["specific_business_tax"]["applies"])
        self.assertEqual(r["stamp_duty"]["amount"], "25000.00")
        # 50% expense -> 2.5m / 8 = 312,500/yr -> 15,000 + 1,250 = 16,250 x 8 = 130,000
        self.assertEqual(r["withholding_tax"]["amount"], "130000.00")

    def test_property_sale_cap_and_tambon(self):
        r = c.property_sale(10000000, 300000, seller="individual", years_held=1, transfer_date="2026-11-11")
        self.assertTrue(r["withholding_tax"]["capped"])
        self.assertEqual(r["withholding_tax"]["amount"], "60000.00")
        r2 = c.property_sale(1000000, 1000000, acquired_by="inheritance", years_held=5, in_tambon_area=True, transfer_date="2026-11-11")
        self.assertEqual(r2["withholding_tax"]["tambon_inheritance_exemption"], "200000.00")

    def test_deadline_extension_warning(self):
        self.assertIsNone(c.deadlines("2026-11")["online_extension_warning"])
        self.assertIsNotNone(c.deadlines("2027-01")["online_extension_warning"])

    def test_lease_registration(self):
        self.assertEqual(c.lease_registration(36000000)["total"], "396000.00")

if __name__ == "__main__":
    unittest.main()
