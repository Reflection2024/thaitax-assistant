#!/usr/bin/env python3
"""Suppliers & contracts register: match every payment to a contract and an invoice, and check withholding.

    python3 -I contracts.py check contracts.csv payments.csv [--as-of 2026-11-30] [--e-wht]

contracts.csv (one row per contract):
    contract_id, supplier, tax_id, legal_form (individual|company|foreign), service_type
    (a key of rates.json wht_resident: services, professional_fees, contractor, commission, rent,
    advertising, transport, insurance_premium, royalties, prizes; or "none" e.g. goods, utilities),
    amount_before_vat (per payment or per month), vat (yes|no), start (YYYY-MM-DD), end (YYYY-MM-DD or empty), file (link or path)
payments.csv (one row per payment, from the bank statement or the books):
    date, supplier, amount_paid (what left the bank), invoice_no, invoice_before_vat, invoice_vat,
    wht_withheld, cert_no (50 ทวิ number), contract_id (optional; matched by supplier if empty)

Prints JSON: each payment with its contract, the expected withholding (rate, form, amount), the
expected net transfer, and flags. Standard library only. Amounts in THB.
"""
from __future__ import annotations

import csv
import json
import os
import sys
from datetime import date, timedelta
from decimal import ROUND_HALF_UP, Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "rates.json"), encoding="utf-8") as _f:
    RATES = json.load(_f)
WHT = RATES["wht_resident"]
MIN_PAYMENT = Decimal("1000")  # withholding applies to payments of 1,000 baht or more (or instalments of a contract worth that)
FORM = {"individual": "PND.3", "company": "PND.53", "foreign": "PND.54"}


def D(x):
    try:
        return Decimal(str(x).replace(",", "").strip() or "0")
    except Exception:
        return Decimal("0")


def money(x):
    return x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def read(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return [{k.strip(): (v or "").strip() for k, v in r.items()} for r in csv.DictReader(f)]


def rate_for(contract, e_wht=False):
    st = (contract.get("service_type") or "").strip()
    if contract.get("legal_form") == "foreign":
        return None, "PND.54", "non-resident: rate depends on income type and tax treaty, check before paying"
    if st in ("", "none"):
        return Decimal("0"), None, None
    if st not in WHT or st.startswith("e_wht"):
        return None, None, f"unknown service_type '{st}'"
    r = Decimal(str(WHT[st]))
    if e_wht and float(r) in WHT["e_wht_applies_to"]:
        r = Decimal(str(WHT["e_wht_reduced_rate"]))
    return r, FORM.get(contract.get("legal_form"), "PND.3/53"), None


def check(contracts, payments, as_of, e_wht=False):
    by_id = {c["contract_id"]: c for c in contracts if c.get("contract_id")}
    by_supplier = {}
    for c in contracts:
        by_supplier.setdefault(c.get("supplier", "").lower(), []).append(c)
    out, totals = [], {"payments": 0, "flagged": 0, "wht_missing_thb": Decimal(0)}
    for p in payments:
        flags = []
        c = by_id.get(p.get("contract_id")) if p.get("contract_id") else None
        if c is None:
            cands = by_supplier.get(p.get("supplier", "").lower(), [])
            pdate = p.get("date", "")
            cands = [x for x in cands if (not x.get("start") or x["start"] <= pdate) and (not x.get("end") or pdate <= x["end"])] or cands
            c = cands[0] if len(cands) == 1 else None
            if len(cands) > 1:
                flags.append("several contracts with this supplier: say which one")
        if c is None:
            flags.append("no contract on file for this payment")
        if not p.get("invoice_no"):
            flags.append("no invoice / tax invoice on file")
        base = D(p.get("invoice_before_vat")) or None
        exp = {}
        if c:
            if c.get("end") and p.get("date", "") > c["end"]:
                flags.append(f"paid after the contract ended ({c['end']})")
            agreed = D(c.get("amount_before_vat"))
            if base is not None and agreed and base != agreed:
                flags.append(f"invoice {base:,.2f} differs from contract {agreed:,.2f}")
            if c.get("vat") == "yes" and base is not None and D(p.get("invoice_vat")) == 0:
                flags.append("supplier is VAT-registered but no VAT on the invoice: ask for a full tax invoice")
            rate, form, note = rate_for(c, e_wht)
            if note:
                flags.append(note)
            if rate is not None and base is not None:
                due = money(base * rate) if base >= MIN_PAYMENT else Decimal("0")
                withheld = D(p.get("wht_withheld"))
                exp = {"wht_rate": str(rate), "wht_form": form, "wht_due": str(due),
                       "net_to_pay": str(money(base + D(p.get("invoice_vat")) - due))}
                if due > 0 and withheld == 0:
                    flags.append(f"withholding not taken: {due:,.2f} ({rate * 100:.0f}%, {form})")
                    totals["wht_missing_thb"] += due
                elif due > 0 and abs(withheld - due) > Decimal("0.05"):
                    flags.append(f"withheld {withheld:,.2f}, expected {due:,.2f}")
                if due > 0 and not p.get("cert_no"):
                    flags.append("no 50 ทวิ certificate number: issue it and give it to the supplier")
        out.append({"date": p.get("date"), "supplier": p.get("supplier"), "amount_paid": p.get("amount_paid"),
                    "invoice_no": p.get("invoice_no"), "contract_id": c.get("contract_id") if c else None, **exp, "flags": flags})
        totals["payments"] += 1
        totals["flagged"] += 1 if flags else 0
    soon = as_of + timedelta(days=30)
    expiring = [{"contract_id": c["contract_id"], "supplier": c["supplier"], "end": c["end"]} for c in contracts
                if c.get("end") and as_of.isoformat() <= c["end"] <= soon.isoformat()]
    totals["wht_missing_thb"] = str(totals["wht_missing_thb"])
    return {"as_of": as_of.isoformat(), "totals": totals, "payments": out, "contracts_ending_within_30_days": expiring}


def main(argv):
    if len(argv) < 4 or argv[1] != "check":
        print(__doc__)
        return 2
    as_of = date.fromisoformat(argv[argv.index("--as-of") + 1]) if "--as-of" in argv else date.today()
    print(json.dumps(check(read(argv[2]), read(argv[3]), as_of, "--e-wht" in argv), ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
