#!/usr/bin/env python3
"""Tests for official_forms.py. Run: python3 -I test_official_forms.py"""
import json
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import official_forms as of  # noqa: E402


class OfficialForms(unittest.TestCase):
    def test_catalog_files_exist(self):
        for fid, meta in of._catalog().items():
            self.assertTrue(os.path.exists(os.path.join(of.FORMS, meta["file"])), fid)

    def test_every_map_entry_is_a_real_box(self):
        for fid, meta in of._catalog().items():
            if not meta.get("map"):
                continue
            names = {w["name"] for w in of.widgets(of.form_path(fid))}
            for key, field in of.load_map(fid).items():
                self.assertIn(field, names, f"{fid}: {key} -> {field}")

    def _fill(self, form, values):
        d = tempfile.mkdtemp()
        vp, out = os.path.join(d, "v.json"), os.path.join(d, "out.pdf")
        with open(vp, "w", encoding="utf-8") as f:
            json.dump({"form": form, "values": values}, f, ensure_ascii=False)
        res = of.fill(form, vp, out)
        from pypdf import PdfReader
        r = PdfReader(out)
        self.assertEqual(len(r.pages), len(PdfReader(of.form_path(form)).pages))
        for p in r.pages:  # flattened: no form widgets left
            self.assertFalse(any(a.get_object().get("/Subtype") == "/Widget" for a in (p.get("/Annots") or [])))
        return res, r

    def test_fill_pp30_and_values_printed(self):
        res, r = self._fill("PP30", {"tin": "0845566001234", "chk_month_10": True, "line5_output_vat": "33775.00",
                                      "operator_name": "บริษัท ตัวอย่าง จำกัด"})
        self.assertEqual(res["filled"], 4)
        text = r.pages[0].extract_text()
        self.assertIn("บริษัทตัวอย่างจำกัด", text.replace(" ", ""))
        self.assertIn("3\n3\n7\n7\n5", text)  # amount digits, one per box
        self.assertIn("Draft for review", text)

    def test_unknown_box_is_refused(self):
        with self.assertRaises(SystemExit):
            self._fill("PND53", {"no_such_box": "1"})

    def test_all_mapped_forms_fill(self):
        for fid, meta in of._catalog().items():
            if meta.get("map"):
                key = next(iter(of.load_map(fid)))
                self._fill(fid, {key: "1"})


if __name__ == "__main__":
    unittest.main(verbosity=1)
