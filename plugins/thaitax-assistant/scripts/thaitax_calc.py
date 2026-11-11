#!/usr/bin/env python3
"""ThaiTax Assistant: deterministic calculations.

Every skill calls this module for arithmetic instead of computing in prose:
VAT, Buddhist-Era dates, social security, withholding, overtime, personal
income tax (PND.90/91 incl. minimum tax and foreign tax credit), filing
deadlines, and Thai baht amounts in words.

Usage:  python3 -I thaitax_calc.py <command> '<json args>'
        python3 -I thaitax_calc.py help
Output: JSON on stdout. Money is returned as strings with 2 decimals.

Rates live in rates.json next to this file (updated yearly). Standard
library only.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys
from decimal import ROUND_HALF_UP, Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "rates.json"), encoding="utf-8") as fh:
    RATES = json.load(fh)

D = Decimal
CENT = D("0.01")
BAHT = D("1")


def money(x) -> Decimal:
    return D(str(x)).quantize(CENT, rounding=ROUND_HALF_UP)


def s(x) -> str:
    return str(money(x))


# ---------------------------------------------------------------- VAT
def vat(amount, inclusive=False, rate=None):
    """VAT on a pre-VAT amount, or split a VAT-inclusive amount."""
    r = D(str(rate if rate is not None else RATES["vat"]["rate"]))
    a = D(str(amount))
    if inclusive:
        net = money(a / (1 + r))
        v = money(a - net)
        gross = money(a)
    else:
        net = money(a)
        v = money(net * r)
        gross = net + v
    return {"net": s(net), "vat": s(v), "gross": s(gross), "rate": str(r),
            "rate_valid_until": RATES["vat"]["valid_until"]}


def vat_check(net, vat_amount, tolerance="0.02", rate=None):
    """Check a document's VAT line against rate x net."""
    r = D(str(rate if rate is not None else RATES["vat"]["rate"]))
    expected = money(D(str(net)) * r)
    diff = money(D(str(vat_amount)) - expected)
    return {"expected_vat": s(expected), "stated_vat": s(vat_amount),
            "difference": s(diff), "ok": abs(diff) <= D(tolerance)}


# ---------------------------------------------------------------- dates
def be(value):
    """Convert BE<->CE. Accepts a year (int/str) or a date 'DD/MM/YYYY' or 'YYYY-MM-DD'."""
    v = str(value).strip()
    if v.isdigit():
        y = int(v)
        return {"input": y, "era": "BE" if y > 2400 else "CE",
                "ce": y - 543 if y > 2400 else y, "be": y if y > 2400 else y + 543}
    if "/" in v:
        d_, m_, y_ = [int(p) for p in v.split("/")]
    else:
        y_, m_, d_ = [int(p) for p in v.split("-")]
    ce_y = y_ - 543 if y_ > 2400 else y_
    date = dt.date(ce_y, m_, d_)
    return {"input": v, "converted": y_ > 2400, "iso_ce": date.isoformat(),
            "be_display": f"{date.day}/{date.month}/{ce_y + 543}"}


def _shift(date, holidays):
    hs = {dt.date.fromisoformat(h) for h in holidays}
    while date.weekday() >= 5 or date in hs:
        date += dt.timedelta(days=1)
    return date


def deadlines(period, holidays=None):
    """Deadlines for a monthly period 'YYYY-MM'. Holidays: list of ISO dates (verify yearly)."""
    holidays = holidays or []
    y, m = [int(p) for p in period.split("-")]
    ny, nm = (y + 1, 1) if m == 12 else (y, m + 1)
    dl = RATES["deadlines"]

    def at(day):
        raw = dt.date(ny, nm, day)
        moved = _shift(raw, holidays)
        return {"date": moved.isoformat(), "moved_from": raw.isoformat() if moved != raw else None}

    return {
        "period": period,
        "PND.1/3/53/54 (withholding)": {"paper": at(dl["pnd_wht"]["paper_day"]), "online": at(dl["pnd_wht"]["online_day"])},
        "PP.30 (VAT)": {"paper": at(dl["pp30"]["paper_day"]), "online": at(dl["pp30"]["online_day"])},
        "PP.36 (reverse charge)": {"paper": at(dl["pp36"]["paper_day"]), "online": at(dl["pp36"]["online_day"])},
        "SSO (SPS 1-10)": at(dl["sso"]["day"]),
        "holidays_supplied": len(holidays),
        "note": "Online extensions are renewed by Ministry of Finance notice; confirm. Supply the year's public holidays.",
    }


# ---------------------------------------------------------------- payroll
def sso(wage, ceiling=None, floor=None, rate=None):
    """Social security per person: 5% each side on wage within floor/ceiling."""
    c = D(str(ceiling or RATES["sso"]["wage_ceiling_thb"]))
    f = D(str(floor or RATES["sso"]["wage_floor_thb"]))
    r = D(str(rate or RATES["sso"]["rate"]))
    w = D(str(wage))
    base = min(max(w, f), c)
    each = (base * r).quantize(BAHT, rounding=ROUND_HALF_UP)
    return {"wage": s(w), "contribution_base": s(base), "employee": s(each), "employer": s(each),
            "total": s(each * 2), "capped": w > c, "floor_applied": w < f,
            "rounding": RATES["sso"]["rounding"], "verified": RATES["sso"]["verified"]}


def overtime(monthly_salary, hours_per_day=8, ot_hours=0, holiday_hours=0,
             holiday_ot_hours=0, holiday_pay_entitled=True):
    """Overtime and holiday pay under the Labour Protection Act."""
    m = D(str(monthly_salary))
    hourly = m / (D(30) * D(str(hours_per_day)))
    ot = hourly * D("1.5") * D(str(ot_hours))
    hol = hourly * (D(1) if holiday_pay_entitled else D(2)) * D(str(holiday_hours))
    hot = hourly * D(3) * D(str(holiday_ot_hours))
    return {"hourly_rate": s(hourly), "overtime_1_5x": s(ot), "holiday_work": s(hol),
            "holiday_overtime_3x": s(hot), "total_extra": s(ot + hol + hot),
            "formula": "hourly = monthly / (30 x normal daily hours)"}


# ---------------------------------------------------------------- withholding
def wht(amount_before_vat, kind, e_wht=False):
    """Withholding tax on a payment to a Thai resident (amount before VAT)."""
    t = RATES["wht_resident"]
    if kind not in t or kind.startswith("e_wht") or kind in ("verified", "source"):
        raise ValueError(f"unknown kind '{kind}'. Known: " + ", ".join(
            k for k in t if not k.startswith("e_wht") and k not in ("verified", "source")))
    rate = D(str(t[kind]))
    if e_wht and float(rate) in t["e_wht_applies_to"]:
        rate = D(str(t["e_wht_reduced_rate"]))
    a = money(amount_before_vat)
    tax = money(a * rate)
    return {"base_before_vat": s(a), "kind": kind, "rate": str(rate), "tax_withheld": s(tax),
            "e_wht": e_wht, "note": "Payee legal form decides the form: PND.3 individual, PND.53 company, PND.54 non-resident."}


# ---------------------------------------------------------------- personal income tax
def _progressive(net):
    tax, lower, steps = D(0), D(0), []
    for upper, rate in RATES["pit"]["bands"]:
        up = D(str(upper)) if upper is not None else None
        if net <= lower:
            break
        top = min(net, up) if up is not None else net
        part = (top - lower) * D(str(rate))
        steps.append({"from": s(lower), "to": s(top), "rate": rate, "tax": s(part)})
        tax += part
        if up is None or net <= up:
            break
        lower = up
    return money(tax), steps


def _expense(item, emp_total):
    sec = item["section"]
    a = D(str(item["amount"]))
    e = RATES["pit"]["expense"]
    if isinstance(item.get("expense"), dict) and "actual" in item["expense"]:
        return D(str(item["expense"]["actual"])), "actual (documents required)"
    if sec in ("40(1)", "40(2)"):
        return None, "combined 40(1)+40(2)"
    if sec == "40(3)":
        return min(a * D(str(e["40(3)"]["rate"])), D(str(e["40(3)"]["cap"]))), "50% capped 100,000"
    if sec == "40(4)":
        return D(0), "no expense deduction"
    if sec == "40(5)":
        k = item.get("kind", "building")
        return a * D(str(e["40(5)"][k])), f"{int(e['40(5)'][k]*100)}% ({k})"
    if sec == "40(6)":
        k = item.get("kind", "other")
        return a * D(str(e["40(6)"][k])), f"{int(e['40(6)'][k]*100)}% ({k})"
    if sec == "40(7)":
        return a * D(str(e["40(7)"]["rate"])), "60%"
    if sec == "40(8)":
        if item.get("kind") == "performer":
            p = e["40(8)"]["performer"]
            first = min(a, D(str(p["first"])))
            ex = first * D(str(p["rate_first"])) + max(a - first, D(0)) * D(str(p["rate_rest"]))
            return min(ex, D(str(p["cap"]))), "performer 60%/40%, cap 600,000"
        if item.get("kind") == "actual_only":
            return D(0), "activity not listed: actual expenses only (none supplied)"
        return a * D(str(e["40(8)"]["rate"])), "60%"
    raise ValueError(f"unknown section {sec}")


def pit(income, allowances=0, donations_double=0, donations_general=0,
        withholding_credit=0, pnd94_paid=0, pnd93_paid=0, dividend_credit=0,
        foreign=None):
    """Estimate PND.90/91 tax, mirroring the No. 11 computation.

    income: list of {section:'40(1)'..'40(8)', amount, kind?, expense?:'standard'|{'actual':x}, source?}
    foreign: list of {country, remitted_thb, foreign_tax_paid_thb, treaty: bool}
    """
    foreign = foreign or []
    lines, total_exp = [], D(0)
    emp = sum(D(str(i["amount"])) for i in income
              if i["section"] in ("40(1)", "40(2)") and not isinstance(i.get("expense"), dict))
    emp_rule = RATES["pit"]["expense"]["40(1)+40(2)"]
    emp_exp = min(emp * D(str(emp_rule["rate"])), D(str(emp_rule["cap"])))
    total_exp += emp_exp
    for it in income:
        ex, rule = _expense(it, emp)
        if ex is not None:
            total_exp += ex
        lines.append({"section": it["section"], "amount": s(it["amount"]), "source": it.get("source", "TH"),
                      "expense": s(ex) if ex is not None else "(in combined 40(1)+40(2))", "rule": rule})
    assessable = sum(D(str(i["amount"])) for i in income)
    after_exp = assessable - total_exp
    bal = after_exp - D(str(allowances))
    bal = max(bal, D(0))
    cap = D(str(RATES["pit"]["donation_cap_ratio"]))
    dd = min(D(str(donations_double)) * 2, bal * cap)
    bal2 = bal - dd
    dg = min(D(str(donations_general)), bal2 * cap)
    net = max(bal2 - dg, D(0))
    prog, steps = _progressive(net)
    mt = RATES["pit"]["minimum_tax"]
    non_emp = sum(D(str(i["amount"])) for i in income if i["section"] != "40(1)")
    min_tax = D(0)
    if non_emp >= D(str(mt["income_threshold"])):
        cand = money(non_emp * D(str(mt["rate"])))
        if cand >= D(str(mt["tax_threshold"])):
            min_tax = cand
    tax = max(prog, min_tax)
    ftc_lines, ftc_total = [], D(0)
    for f in foreign:
        paid = D(str(f.get("foreign_tax_paid_thb", 0)))
        rem = D(str(f.get("remitted_thb", 0)))
        if not f.get("treaty", True):
            ftc_lines.append({"country": f.get("country"), "credit": "0.00", "reason": "no double-tax treaty"})
            continue
        limit = money(rem / assessable * tax) if assessable else D(0)
        credit = min(paid, limit)
        ftc_total += credit
        ftc_lines.append({"country": f.get("country"), "remitted": s(rem), "foreign_tax_paid": s(paid),
                          "limit": s(limit), "credit": s(credit)})
    credits = (D(str(withholding_credit)) + D(str(pnd94_paid)) + D(str(pnd93_paid))
               + D(str(dividend_credit)) + ftc_total)
    result = money(tax - credits)
    return {
        "income_lines": lines,
        "assessable_income": s(assessable),
        "expenses": s(total_exp),
        "employment_expense_40_1_2": s(emp_exp),
        "income_after_expenses": s(after_exp),
        "allowances": s(allowances),
        "donations_double_deducted": s(dd),
        "donations_general_deducted": s(dg),
        "net_income": s(net),
        "progressive_tax": s(prog),
        "progressive_steps": steps,
        "minimum_tax_0_5pct": s(min_tax),
        "tax_payable": s(tax),
        "method": "minimum tax (0.5%)" if min_tax > prog else "progressive",
        "credits": {"withholding": s(withholding_credit), "pnd94": s(pnd94_paid), "pnd93": s(pnd93_paid),
                    "dividend": s(dividend_credit), "foreign_tax_credit": s(ftc_total)},
        "foreign_tax_credit_lines": ftc_lines,
        "result": s(result),
        "result_meaning": "payable" if result > 0 else ("refund" if result < 0 else "nil"),
        "instalments_allowed": result >= 3000,
        "estimate_only": True,
        "rates_verified": RATES["pit"]["verified"],
    }


# ---------------------------------------------------------------- baht in words
_DIG = ["", "หนึ่ง", "สอง", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า"]
_POS = ["", "สิบ", "ร้อย", "พัน", "หมื่น", "แสน"]


def _words(n: int) -> str:
    if n == 0:
        return ""
    if n >= 1_000_000:
        return _words(n // 1_000_000) + "ล้าน" + _words(n % 1_000_000)
    txt, digits = "", str(n)
    L = len(digits)
    for i, ch in enumerate(digits):
        d, pos = int(ch), L - i - 1
        if d == 0:
            continue
        if pos == 1 and d == 1:
            txt += "สิบ"
        elif pos == 1 and d == 2:
            txt += "ยี่สิบ"
        elif pos == 0 and d == 1 and L > 1:
            txt += "เอ็ด"
        else:
            txt += _DIG[d] + _POS[pos]
    return txt


def bahttext(amount):
    """Thai words for a baht amount, as on invoices and receipts."""
    a = money(amount)
    baht = int(a)
    satang = int((a - baht) * 100)
    head = (_words(baht) or "ศูนย์") + "บาท"
    tail = "ถ้วน" if satang == 0 else _words(satang) + "สตางค์"
    if baht == 0 and satang:
        head = ""
    return {"amount": s(a), "text": head + tail}


# ---------------------------------------------------------------- CLI
COMMANDS = {"vat": vat, "vat_check": vat_check, "be": be, "deadlines": deadlines, "sso": sso,
            "overtime": overtime, "wht": wht, "pit": pit, "bahttext": bahttext}


def main(argv):
    if len(argv) < 2 or argv[1] in ("help", "-h", "--help"):
        print(json.dumps({"commands": {k: (v.__doc__ or "").strip().split("\n")[0] for k, v in COMMANDS.items()}},
                         ensure_ascii=False, indent=2))
        return 0
    cmd = argv[1]
    if cmd not in COMMANDS:
        print(json.dumps({"error": f"unknown command {cmd}"}))
        return 2
    args = json.loads(argv[2]) if len(argv) > 2 else {}
    try:
        out = COMMANDS[cmd](**args) if isinstance(args, dict) else COMMANDS[cmd](args)
    except Exception as e:  # report, never guess
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        return 1
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
