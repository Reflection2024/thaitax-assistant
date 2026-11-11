#!/usr/bin/env python3
"""ThaiTax Assistant: family budget engine.

Turns bank and card transactions (already read from statements) into a
categorised household picture: income vs. spending per month, where the
money goes, and recurring payments / subscriptions (with price changes and
possible duplicates).

    python3 -I budget.py summarize transactions.csv [--rules rules.json] [--fx fx.json] [--out summary.json]
    python3 -I budget.py actual-export transactions.csv --out actual_import.csv   # for Actual Budget

transactions.csv columns (UTF-8, header row):
    date (YYYY-MM-DD), description, amount (signed: + in, - out), currency (THB, EUR, ...),
    account (label, never a full account number), category (optional, overrides rules)

fx.json: {"EUR": 37.8, "USD": 35.1}  THB per unit, from the statement or Bank of Thailand
         reference rate for the period. Amounts in a currency with no rate are reported
         separately and never converted silently.
rules.json: {"keyword or merchant": "Category"}  the family's own corrections; checked
            before the built-in rules.

Standard library only.
"""
from __future__ import annotations

import csv
import json
import re
import statistics
import sys
from collections import defaultdict
from datetime import date

# Built-in rules: lower-case keyword -> category. Thai and international merchants
# common in Thailand. The family's rules.json is applied first.
RULES = [
    # transfers between own accounts are excluded from income/spending
    (r"transfer (to|from) (my )?own|own (account )?transfer|between (my )?own accounts|to self|from self|โอนเงินระหว่างบัญชีตนเอง|โอนเข้าบัญชีตนเอง", "Transfer (own accounts)"),
    (r"salary|payroll|เงินเดือน|wage", "Income: salary"),
    (r"dividend|interest|ดอกเบี้ย|เงินปันผล", "Income: interest & dividends"),
    (r"rent received|ค่าเช่ารับ|airbnb payout|booking\.com payout", "Income: rent"),
    (r"refund|คืนเงิน", "Refunds"),
    (r"7-eleven|7 eleven|seven eleven|makro|big ?c|lotus|tops|foodland|villa market|gourmet market|family ?mart|cj express|แม็คโคร|โลตัส|บิ๊กซี", "Groceries"),
    (r"grab ?food|foodpanda|line ?man|robinhood|restaurant|cafe|coffee|starbucks|kfc|mcdonald|ร้านอาหาร|กาแฟ", "Eating out"),
    (r"\bgrab\b|bolt|taxi|bts|mrt|airport rail|ptt|shell|bangchak|caltex|esso|น้ำมัน|ปตท|บางจาก|ทางด่วน|easy pass|m-?flow", "Transport & fuel"),
    (r"pea|mea|การไฟฟ้า|electric", "Utilities: electricity"),
    (r"pwa|mwa|การประปา|water supply", "Utilities: water"),
    (r"\bais\b|true ?move|truemove|dtac|3bb|true online|nt broadband|internet|fibre", "Phone & internet"),
    (r"netflix|spotify|youtube|disney|apple\.com|icloud|google storage|google one|chatgpt|openai|anthropic|claude|amazon prime|hbo|viu|wetv|canva|microsoft 365|adobe|dropbox|notion", "Subscriptions"),
    (r"school|international school|tuition|kindergarten|โรงเรียน|ค่าเทอม|university", "Education & kids"),
    (r"hospital|clinic|pharmacy|bangkok hospital|bumrungrad|samitivej|dental|boots|watsons|โรงพยาบาล|คลินิก|ร้านยา", "Health"),
    (r"insurance|allianz|aia|axa|muang thai|ประกัน", "Insurance"),
    (r"rent|landlord|condo fee|common fee|ค่าเช่า|ค่าส่วนกลาง|juristic", "Housing"),
    (r"lazada|shopee|amazon|central|robinson|ikea|homepro|power ?buy|uniqlo|h&m|zara", "Shopping"),
    (r"agoda|booking\.com|airasia|thai airways|bangkok airways|nok ?air|hotel|airbnb|trip\.com|lompraya|seatran|raja ferry", "Travel"),
    (r"visa|immigration|90 ?day|work permit|ตม|ใบอนุญาตทำงาน", "Visa & admin"),
    (r"revenue department|กรมสรรพากร|sso|ประกันสังคม|land tax|ภาษี", "Taxes & social security"),
    (r"gym|fitness|yoga|muay thai|golf|dive|diving", "Sport & leisure"),
    (r"atm|cash withdrawal|ถอนเงินสด", "Cash withdrawals"),
    (r"bank fee|ค่าธรรมเนียม|annual fee|fx fee|conversion fee", "Bank fees"),
    (r"donation|บริจาค|temple|วัด", "Donations"),
]


def categorize(desc: str, amount: float, user_rules: dict) -> str:
    d = desc.lower()
    for k, cat in user_rules.items():
        if k.lower() in d:
            return cat
    for pattern, cat in RULES:
        if re.search(pattern, d):
            if cat.startswith("Income") and amount < 0:
                continue
            return cat
    return "Income: other" if amount > 0 else "Other / uncategorised"


def _merchant_key(desc: str) -> str:
    d = desc.lower()
    d = re.sub(r"\d{2,}", " ", d)            # strip refs, dates, card digits
    d = re.sub(r"[^a-zก-๙ ]+", " ", d)
    words = [w for w in d.split() if len(w) > 1][:3]
    return " ".join(words) or desc.lower()[:20]


def load(path):
    with open(path, encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    out = []
    for i, r in enumerate(rows, 1):
        try:
            out.append({"date": date.fromisoformat(r["date"].strip()), "description": r["description"].strip(),
                        "amount": float(str(r["amount"]).replace(",", "")), "currency": (r.get("currency") or "THB").strip().upper(),
                        "account": (r.get("account") or "").strip(), "category": (r.get("category") or "").strip()})
        except Exception as e:  # report, never guess
            raise ValueError(f"row {i}: {e}")
    return out


def summarize(txns, user_rules=None, fx=None):
    user_rules, fx = user_rules or {}, {k.upper(): float(v) for k, v in (fx or {}).items()}
    fx["THB"] = 1.0
    unconverted = defaultdict(float)
    months = defaultdict(lambda: {"income": 0.0, "spending": 0.0})
    by_cat = defaultdict(float)
    by_cat_month = defaultdict(lambda: defaultdict(float))
    merchants = defaultdict(list)
    uncategorised = []
    for t in txns:
        cat = t["category"] or categorize(t["description"], t["amount"], user_rules)
        if t["currency"] not in fx:
            unconverted[t["currency"]] += t["amount"]
            continue
        thb = t["amount"] * fx[t["currency"]]
        m = t["date"].strftime("%Y-%m")
        if cat == "Transfer (own accounts)":
            continue
        if thb > 0:
            months[m]["income"] += thb
        else:
            months[m]["spending"] += -thb
            by_cat[cat] += -thb
            by_cat_month[cat][m] += -thb
            merchants[_merchant_key(t["description"])].append((t["date"], -thb, t["description"], cat))
        if cat == "Other / uncategorised":
            uncategorised.append({"date": t["date"].isoformat(), "description": t["description"], "thb": round(thb, 2)})

    # recurring payments: same merchant in >= 2 different months, amounts within 15% of median
    recurring = []
    for key, items in merchants.items():
        ms = sorted({d.strftime("%Y-%m") for d, *_ in items})
        if len(ms) < 2:
            continue
        amts = [a for _, a, *_ in items]
        med = statistics.median(amts)
        cat0 = items[-1][3]
        steady_cats = ("Subscriptions", "Phone & internet", "Utilities: electricity", "Utilities: water",
                       "Housing", "Insurance", "Education & kids")
        spread = (statistics.pstdev(amts) / med) if med > 0 else 1
        if cat0 in ("Cash withdrawals", "Transfer (own accounts)"):
            continue
        if cat0 not in steady_cats and spread > 0.05:
            continue                       # varying amounts at the same shop: a habit, not a fixed payment
        last = sorted(items)[-1]
        first = sorted(items)[0]
        changed = abs(last[1] - first[1]) / first[1] > 0.02 if first[1] else False
        per_month = len(items) / max(len(ms), 1)
        if per_month > 3:          # many purchases a month = shopping habit, not a subscription
            continue
        recurring.append({"merchant": last[2], "category": last[3], "months_seen": len(ms),
                          "typical_thb": round(med, 2), "last_thb": round(last[1], 2), "last_date": last[0].isoformat(),
                          "price_changed": changed, "per_year_thb": round(med * 12, 2)})
    recurring.sort(key=lambda r: -r["typical_thb"])
    # possible overlaps: more than one paid service doing the same job
    families = {
        "cloud storage": ("icloud", "google one", "google storage", "dropbox", "onedrive"),
        "video streaming": ("netflix", "disney", "hbo", "prime video", "amazon prime", "viu", "wetv", "iqiyi", "youtube premium"),
        "music": ("spotify", "apple music", "youtube music", "joox", "tidal"),
        "AI assistants": ("chatgpt", "openai", "claude", "anthropic", "gemini", "perplexity"),
    }
    dups = {}
    for fam, keys in families.items():
        hits = [r for r in recurring if any(k in r["merchant"].lower() for k in keys)]
        if len(hits) > 1:
            dups[fam] = {"services": [r["merchant"] for r in hits], "monthly_thb": round(sum(r["typical_thb"] for r in hits), 2)}

    mlist = sorted(months)
    total_in = sum(months[m]["income"] for m in mlist)
    total_out = sum(months[m]["spending"] for m in mlist)
    return {
        "period": {"from": mlist[0] if mlist else None, "to": mlist[-1] if mlist else None, "months": len(mlist)},
        "currency": "THB",
        "fx_used": fx,
        "unconverted_by_currency": dict(unconverted),
        "totals": {"income": round(total_in, 2), "spending": round(total_out, 2), "net": round(total_in - total_out, 2),
                   "avg_monthly_spending": round(total_out / len(mlist), 2) if mlist else 0},
        "months": [{"month": m, "income": round(months[m]["income"], 2), "spending": round(months[m]["spending"], 2),
                    "net": round(months[m]["income"] - months[m]["spending"], 2)} for m in mlist],
        "categories": [{"category": c, "thb": round(v, 2), "share": round(v / total_out, 4) if total_out else 0,
                        "by_month": {m: round(by_cat_month[c].get(m, 0), 2) for m in mlist}}
                       for c, v in sorted(by_cat.items(), key=lambda x: -x[1])],
        "recurring": recurring,
        "recurring_total_monthly": round(sum(r["typical_thb"] for r in recurring), 2),
        "possible_duplicate_subscriptions": dups,
        "uncategorised": uncategorised[:50],
        "uncategorised_count": len(uncategorised),
    }


def actual_export(txns, out_path, user_rules=None):
    """CSV in a layout Actual Budget's importer maps easily: Date, Payee, Notes, Category, Amount."""
    with open(out_path, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["Date", "Payee", "Notes", "Category", "Amount", "Currency", "Account"])
        for t in txns:
            cat = t["category"] or categorize(t["description"], t["amount"], user_rules or {})
            w.writerow([t["date"].isoformat(), t["description"][:60], "", cat, f"{t['amount']:.2f}", t["currency"], t["account"]])
    return {"written": out_path, "rows": len(txns)}


def main(argv):
    if len(argv) < 3 or argv[1] not in ("summarize", "actual-export"):
        print(__doc__)
        return 2
    args = {"rules": None, "fx": None, "out": None}
    i = 3
    while i < len(argv):
        args[argv[i].lstrip("-")] = argv[i + 1]
        i += 2
    txns = load(argv[2])
    rules = json.load(open(args["rules"], encoding="utf-8")) if args["rules"] else {}
    fx = json.load(open(args["fx"], encoding="utf-8")) if args["fx"] else {}
    if argv[1] == "summarize":
        s = summarize(txns, rules, fx)
        txt = json.dumps(s, ensure_ascii=False, indent=2)
        if args["out"]:
            open(args["out"], "w", encoding="utf-8").write(txt)
            print(json.dumps({"written": args["out"], "months": s["period"]["months"], "uncategorised": s["uncategorised_count"]}))
        else:
            print(txt)
    else:
        print(json.dumps(actual_export(txns, args["out"] or "actual_import.csv", rules)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
