#!/usr/bin/env python3
"""Render a family budget dashboard (one self-contained HTML page) from budget.py's summary.

    python3 -I budget_dashboard.py summary.json out.html [--lang en|he|th] [--title "Family budget"]

No external libraries or network: charts are inline SVG. Light and dark themes.
"""
from __future__ import annotations

import html
import json
import sys

T = {
    "en": dict(title="Family budget", income="Money in", spending="Money out", net="Left over", avg="Average spending / month",
               fixed="Fixed payments / month", months="Month by month", where="Where the money goes", recurring="Fixed payments and subscriptions",
               per_year="per year", flags="Worth a look", overlap="You pay for {n} {fam} services", overlap2="together {amt} a month",
               changed="Price changed", uncat="{n} payments still need a category", period="Period", fx="Exchange rate used",
               src="From your bank statements. Transfers between your own accounts are left out.", merchant="Payment", typical="Usually", last="Last",
               cat="Category", share="Share", none="Nothing unusual this period."),
    "he": dict(title="התקציב המשפחתי", income="נכנס", spending="יצא", net="נשאר", avg="הוצאה ממוצעת לחודש",
               fixed="תשלומים קבועים לחודש", months="חודש אחרי חודש", where="לאן הולך הכסף", recurring="תשלומים קבועים ומנויים",
               per_year="לשנה", flags="שווה הצצה", overlap="אתם משלמים על {n} שירותי {fam}", overlap2="ביחד {amt} לחודש",
               changed="המחיר השתנה", uncat="ל-{n} תשלומים עדיין אין קטגוריה", period="תקופה", fx="שער המרה",
               src="מתוך דפי הבנק שלכם. העברות בין החשבונות שלכם לא נספרות.", merchant="תשלום", typical="בדרך כלל", last="אחרון",
               cat="קטגוריה", share="חלק", none="אין משהו חריג בתקופה הזו."),
    "th": dict(title="งบประมาณครอบครัว", income="เงินเข้า", spending="เงินออก", net="คงเหลือ", avg="ค่าใช้จ่ายเฉลี่ยต่อเดือน",
               fixed="รายจ่ายประจำต่อเดือน", months="รายเดือน", where="เงินไปที่ไหน", recurring="รายจ่ายประจำและค่าสมาชิก",
               per_year="ต่อปี", flags="ควรดู", overlap="คุณจ่ายบริการ{fam} {n} รายการ", overlap2="รวม {amt} ต่อเดือน",
               changed="ราคาเปลี่ยน", uncat="ยังมี {n} รายการที่ไม่มีหมวด", period="ช่วงเวลา", fx="อัตราแลกเปลี่ยน",
               src="จากสเตทเมนต์ธนาคารของคุณ ไม่นับการโอนระหว่างบัญชีของตัวเอง", merchant="รายการ", typical="ปกติ", last="ล่าสุด",
               cat="หมวด", share="สัดส่วน", none="ไม่มีรายการผิดปกติในช่วงนี้"),
}
FAM = {"he": {"cloud storage": "אחסון ענן", "video streaming": "סטרימינג", "music": "מוזיקה", "AI assistants": "בינה מלאכותית"},
       "th": {"cloud storage": "พื้นที่เก็บข้อมูล", "video streaming": "สตรีมมิง", "music": "เพลง", "AI assistants": "AI"}}
PALETTE = ["#2c7a68", "#e2962b", "#3d6fb6", "#b5544a", "#7a5aa6", "#4f9e9a", "#c4a23a", "#8a8f99"]


def fmt(x):
    return f"฿{x:,.0f}"


def bars_month(months, t):
    if not months:
        return ""
    W, H, pad, gap = 640, 220, 34, 10
    mx = max(max(m["income"], m["spending"]) for m in months) or 1
    n = len(months)
    gw = (W - pad * 2) / n
    bw = min(34, (gw - gap * 3) / 2)
    out = [f'<svg viewBox="0 0 {W} {H + 40}" role="img" aria-label="{html.escape(t["months"])}" class="chart">']
    for k in range(5):
        y = pad + (H - pad) * k / 4
        out.append(f'<line x1="{pad}" x2="{W - 8}" y1="{y:.1f}" y2="{y:.1f}" class="grid"/>')
        out.append(f'<text x="{pad - 6}" y="{y + 4:.1f}" class="axis" text-anchor="end">{fmt(mx * (4 - k) / 4 / 1000)}k</text>' if k < 4 else "")
    for i, m in enumerate(months):
        x0 = pad + gw * i + (gw - bw * 2 - gap) / 2
        for j, (key, cls) in enumerate((("income", "in"), ("spending", "out"))):
            h = (H - pad) * m[key] / mx
            x = x0 + j * (bw + gap)
            out.append(f'<rect x="{x:.1f}" y="{H - h:.1f}" width="{bw:.1f}" height="{h:.1f}" rx="4" class="{cls}"><title>{html.escape(t[key])} {m["month"]}: {fmt(m[key])}</title></rect>')
        out.append(f'<text x="{pad + gw * i + gw / 2:.1f}" y="{H + 20}" class="axis" text-anchor="middle">{m["month"]}</text>')
    out.append("</svg>")
    return "".join(out)


def bars_cat(cats):
    top = cats[:8]
    if not top:
        return ""
    mx = top[0]["thb"] or 1
    rows = []
    for i, c in enumerate(top):
        w = 100 * c["thb"] / mx
        rows.append(f'<div class="crow"><span class="cname">{html.escape(c["category"])}</span>'
                    f'<span class="cbar"><i style="width:{w:.1f}%;background:{PALETTE[i % len(PALETTE)]}"></i></span>'
                    f'<span class="cval">{fmt(c["thb"])} <small>{c["share"] * 100:.0f}%</small></span></div>')
    rest = sum(c["thb"] for c in cats[8:])
    if rest:
        rows.append(f'<div class="crow muted"><span class="cname">+{len(cats) - 8}</span><span class="cbar"></span><span class="cval">{fmt(rest)}</span></div>')
    return "".join(rows)


def render(s, lang="en", title=None):
    t = T.get(lang, T["en"])
    rtl = lang == "he"
    tot = s["totals"]
    flags = []
    for fam, d in s.get("possible_duplicate_subscriptions", {}).items():
        famname = FAM.get(lang, {}).get(fam, fam)
        flags.append(f'<li><b>{html.escape(t["overlap"].format(n=len(d["services"]), fam=famname))}</b>: '
                     f'{html.escape(", ".join(d["services"]))}, {t["overlap2"].format(amt=fmt(d["monthly_thb"]))}</li>')
    for r in s.get("recurring", []):
        if r.get("price_changed"):
            flags.append(f'<li><b>{t["changed"]}</b>: {html.escape(r["merchant"])}, {fmt(r["typical_thb"])} → {fmt(r["last_thb"])}</li>')
    if s.get("uncategorised_count"):
        flags.append(f'<li>{t["uncat"].format(n=s["uncategorised_count"])}</li>')
    rec_rows = "".join(
        f'<tr><td>{html.escape(r["merchant"])}</td><td>{html.escape(r["category"])}</td><td class="num">{fmt(r["typical_thb"])}</td>'
        f'<td class="num muted">{fmt(r["per_year_thb"])}</td></tr>' for r in s.get("recurring", []))
    fx = ", ".join(f"1 {k} = ฿{v:g}" for k, v in s.get("fx_used", {}).items() if k != "THB") or "—"
    period = f'{s["period"]["from"]} – {s["period"]["to"]}'
    net_cls = "good" if tot["net"] >= 0 else "bad"
    return f'''<!DOCTYPE html>
<html lang="{lang}" dir="{'rtl' if rtl else 'ltr'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title or t["title"])}</title>
<style>
:root{{--bg:#f6f4ee;--card:#fff;--ink:#16243a;--muted:#5b6574;--line:#e2ddd0;--in:#2c7a68;--out:#e2962b;--bad:#b5544a;color-scheme:light;
font-family:"IBM Plex Sans Thai","IBM Plex Sans Hebrew",system-ui,-apple-system,"Segoe UI",Tahoma,Arial,sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#111a28;--card:#18243a;--ink:#eef0f3;--muted:#a3adbb;--line:#2b3a52;--in:#5cc0a6;--out:#f0aa45;--bad:#e07a6f;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#111a28;--card:#18243a;--ink:#eef0f3;--muted:#a3adbb;--line:#2b3a52;--in:#5cc0a6;--out:#f0aa45;--bad:#e07a6f;color-scheme:dark}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink)}}
.wrap{{max-width:1040px;margin:0 auto;padding:24px 18px 48px;display:grid;gap:18px}}
h1{{font-size:26px;margin:0}}.sub{{color:var(--muted);font-size:14px;margin-top:4px}}
.tiles{{display:grid;grid-template-columns:repeat(5,1fr);gap:12px}}
.tile{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px}}
.tile span{{display:block;font-size:12.5px;color:var(--muted)}}.tile b{{font-size:22px;font-variant-numeric:tabular-nums}}
.good{{color:var(--in)}}.bad{{color:var(--bad)}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px;min-width:0}}
.card h2{{font-size:16px;margin:0 0 12px}}.two{{display:grid;grid-template-columns:1.2fr 1fr;gap:18px}}
.chart{{width:100%;height:auto}}.grid{{stroke:var(--line)}}.axis{{fill:var(--muted);font-size:11px}}
rect.in{{fill:var(--in)}}rect.out{{fill:var(--out)}}
.legend{{display:flex;gap:16px;font-size:13px;color:var(--muted)}}.legend i{{display:inline-block;width:10px;height:10px;border-radius:3px;margin-inline-end:6px}}
.crow{{display:grid;grid-template-columns:minmax(0,9em) 1fr auto;gap:10px;align-items:center;margin:8px 0;font-size:13.5px}}
.cname{{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}.cbar{{background:var(--line);height:10px;border-radius:6px;overflow:hidden}}
.cbar i{{display:block;height:100%;border-radius:6px}}.cval{{font-variant-numeric:tabular-nums;white-space:nowrap}}.cval small,.muted{{color:var(--muted)}}
table{{width:100%;border-collapse:collapse;font-size:13.5px}}th{{text-align:start;color:var(--muted);font-weight:500;font-size:12px;border-bottom:1px solid var(--line);padding:6px 4px}}
td{{padding:8px 4px;border-bottom:1px solid var(--line)}}td.num{{text-align:end;font-variant-numeric:tabular-nums;white-space:nowrap}}
.flags li{{margin:6px 0}}.foot{{color:var(--muted);font-size:12.5px}}
.scroll{{overflow-x:auto}}
@media (max-width:820px){{.tiles{{grid-template-columns:repeat(2,1fr)}}.two{{grid-template-columns:1fr}}}}
</style></head><body><div class="wrap">
<header><h1>{html.escape(title or t["title"])}</h1><div class="sub">{t["period"]}: {period}</div></header>
<section class="tiles">
<div class="tile"><span>{t["income"]}</span><b>{fmt(tot["income"])}</b></div>
<div class="tile"><span>{t["spending"]}</span><b>{fmt(tot["spending"])}</b></div>
<div class="tile"><span>{t["net"]}</span><b class="{net_cls}">{fmt(tot["net"])}</b></div>
<div class="tile"><span>{t["avg"]}</span><b>{fmt(tot["avg_monthly_spending"])}</b></div>
<div class="tile"><span>{t["fixed"]}</span><b>{fmt(s.get("recurring_total_monthly", 0))}</b></div>
</section>
<section class="two">
<div class="card"><h2>{t["months"]}</h2><div class="legend"><span><i style="background:var(--in)"></i>{t["income"]}</span><span><i style="background:var(--out)"></i>{t["spending"]}</span></div>{bars_month(s["months"], t)}</div>
<div class="card"><h2>{t["where"]}</h2>{bars_cat(s["categories"])}</div>
</section>
<section class="card"><h2>{t["flags"]}</h2><ul class="flags">{"".join(flags) or "<li>" + t["none"] + "</li>"}</ul></section>
<section class="card"><h2>{t["recurring"]}</h2><div class="scroll"><table><thead><tr><th>{t["merchant"]}</th><th>{t["cat"]}</th><th style="text-align:end">{t["typical"]}</th><th style="text-align:end">{t["per_year"]}</th></tr></thead><tbody>{rec_rows}</tbody></table></div></section>
<p class="foot">{t["src"]} {t["fx"]}: {html.escape(fx)}. ThaiTax Assistant.</p>
</div></body></html>'''


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    opts = {"lang": "en", "title": None}
    i = 3
    while i < len(argv):
        opts[argv[i].lstrip("-")] = argv[i + 1]
        i += 2
    s = json.load(open(argv[1], encoding="utf-8"))
    open(argv[2], "w", encoding="utf-8").write(render(s, opts["lang"], opts["title"]))
    print(json.dumps({"written": argv[2], "lang": opts["lang"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
