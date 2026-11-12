#!/usr/bin/env python3
"""Render any ThaiTax Assistant dashboard (one self-contained HTML page) from a JSON spec.

    python3 -I dashboard.py spec.json out.html

The spec holds only numbers and words that were already computed from the user's own files
(by thaitax_calc.py, budget.py, contracts.py or the skill's own working). This script draws;
it never calculates tax. No external libraries, no network: charts are inline SVG.

Spec:
{
  "lang": "he",                      # any BCP-47 tag; he/ar/fa/ur render right to left
  "title": "...", "subtitle": "...",
  "kpis": [{"label": "...", "value": "฿10,605", "note": "...", "tone": "good|warn|bad|neutral"}],
  "sections": [
    {"type": "bars",  "title": "...", "labels": ["Jan", ...], "series": [{"name": "...", "values": [..]}], "unit": "฿"},
    {"type": "hbars", "title": "...", "items": [{"label": "...", "value": 48500, "display": "฿48,500", "tone": "good"}]},
    {"type": "line",  "title": "...", "labels": [...], "values": [...], "unit": "฿"},
    {"type": "ring",  "title": "...", "value": 214, "max": 365, "target": 180, "label": "days", "note": "..."},
    {"type": "table", "title": "...", "columns": ["...", ...], "rows": [["...", ...]], "tones": ["good", ...]},
    {"type": "list",  "title": "...", "items": [{"text": "...", "tone": "warn"}]}
  ],
  "footer": "Sample numbers / source line"
}
"""
from __future__ import annotations

import html
import json
import sys

RTL = {"he", "iw", "ar", "fa", "ur", "yi"}
TONE = {"good": "#127a52", "warn": "#c77a12", "bad": "#b4402a", "neutral": "#6b5646"}
PALETTE = ["#127a52", "#e2962b", "#3d6fb6", "#b5544a", "#7a5aa6", "#4f9e9a"]


def e(s) -> str:
    return html.escape(str(s if s is not None else ""))


def iso(s) -> str:
    """Numbers, amounts, codes: keep them in their own left-to-right run."""
    return f"<bdi>{e(s)}</bdi>"


def num(v, unit=""):
    if isinstance(v, (int, float)):
        return f"{unit}{v:,.0f}"
    return str(v)


def bars(sec):
    labels = sec.get("labels", [])
    series = sec.get("series", [])
    vmax = max([v for s in series for v in s.get("values", []) if isinstance(v, (int, float))] or [1]) or 1
    n, k = max(len(labels), 1), max(len(series), 1)
    W, H, pad = 640, 200, 24
    gw = (W - pad * 2) / n
    bw = max(4, gw * 0.7 / k)
    out = [f'<svg viewBox="0 0 {W} {H + 26}" class="chart" role="img">']
    for i, lab in enumerate(labels):
        for j, s in enumerate(series):
            vals = s.get("values", [])
            v = vals[i] if i < len(vals) and isinstance(vals[i], (int, float)) else 0
            h = (v / vmax) * (H - 10)
            x = pad + i * gw + (gw - bw * k) / 2 + j * bw
            out.append(f'<rect x="{x:.1f}" y="{H - h:.1f}" width="{bw - 2:.1f}" height="{h:.1f}" rx="3" fill="{PALETTE[j % 6]}">'
                       f'<title>{e(s.get("name", ""))} {e(lab)}: {e(num(v, sec.get("unit", "")))}</title></rect>')
        out.append(f'<text x="{pad + i * gw + gw / 2:.1f}" y="{H + 18}" text-anchor="middle">{e(lab)}</text>')
    out.append(f'<line x1="{pad}" y1="{H}" x2="{W - pad}" y2="{H}" class="axis"/></svg>')
    if len(series) > 1:
        out.append('<p class="legend">' + "".join(
            f'<span><i style="background:{PALETTE[j % 6]}"></i>{e(s.get("name", ""))}</span>' for j, s in enumerate(series)) + "</p>")
    return "".join(out)


def hbars(sec):
    items = sec.get("items", [])
    vmax = max([i.get("value", 0) for i in items if isinstance(i.get("value"), (int, float))] or [1]) or 1
    rows = []
    for it in items:
        v = it.get("value", 0) if isinstance(it.get("value"), (int, float)) else 0
        col = TONE.get(it.get("tone"), PALETTE[1])
        rows.append(f'<div class="hrow"><span>{e(it.get("label"))}</span><span class="hb"><i style="width:{100 * v / vmax:.1f}%;background:{col}"></i></span>'
                    f'<b>{iso(it.get("display", num(v, sec.get("unit", ""))))}</b></div>')
    return "".join(rows)


def line(sec):
    vals = [v for v in sec.get("values", []) if isinstance(v, (int, float))]
    labels = sec.get("labels", [])
    if not vals:
        return ""
    W, H, pad = 640, 180, 24
    lo, hi = min(vals), max(vals)
    if lo > 0:
        lo = lo * 0.85
    span = (hi - lo) or 1
    step = (W - pad * 2) / max(len(vals) - 1, 1)
    pts = " ".join(f"{pad + i * step:.1f},{H - (v - lo) / span * (H - 16):.1f}" for i, v in enumerate(vals))
    zero = H - (max(lo, 0) - lo) / span * (H - 16)
    lab = "".join(f'<text x="{pad + i * step:.1f}" y="{H + 18}" text-anchor="middle">{e(l)}</text>' for i, l in enumerate(labels[:len(vals)]))
    return (f'<svg viewBox="0 0 {W} {H + 26}" class="chart" role="img"><line x1="{pad}" y1="{zero:.1f}" x2="{W - pad}" y2="{zero:.1f}" class="axis"/>'
            f'<polyline points="{pts}" fill="none" stroke="{PALETTE[0]}" stroke-width="3"/>{lab}</svg>')


def ring(sec):
    v, mx = float(sec.get("value", 0)), float(sec.get("max", 100)) or 100
    c = 2 * 3.14159 * 42
    tgt = sec.get("target")
    tick = ""
    if isinstance(tgt, (int, float)):
        import math
        a = 2 * math.pi * tgt / mx - math.pi / 2
        x1, y1 = 50 + 34 * math.cos(a), 50 + 34 * math.sin(a)
        x2, y2 = 50 + 50 * math.cos(a), 50 + 50 * math.sin(a)
        tick = f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#1d140d" stroke-width="2"/>'
    return (f'<div class="ringrow"><svg viewBox="0 0 100 100" class="ring"><circle cx="50" cy="50" r="42" class="trk"/>'
            f'<circle cx="50" cy="50" r="42" class="val" stroke-dasharray="{c * min(v / mx, 1):.1f} {c:.1f}" transform="rotate(-90 50 50)"/>{tick}'
            f'<text x="50" y="54" text-anchor="middle">{e(num(sec.get("value")))}</text></svg>'
            f'<div><p class="big">{iso(num(sec.get("value")))} <span>{e(sec.get("label", ""))}</span></p><p>{e(sec.get("note", ""))}</p></div></div>')


def table(sec):
    cols = sec.get("columns", [])
    tones = sec.get("tones", [])
    head = "".join(f"<th>{e(c)}</th>" for c in cols)
    body = []
    for i, r in enumerate(sec.get("rows", [])):
        t = tones[i] if i < len(tones) else None
        dot = f'<i class="dot" style="background:{TONE[t]}"></i>' if t in TONE else ""
        body.append("<tr>" + "".join(f"<td>{dot if j == 0 else ''}{iso(c)}</td>" for j, c in enumerate(r)) + "</tr>")
    return f"<table><thead><tr>{head}</tr></thead><tbody>{''.join(body)}</tbody></table>"


def lst(sec):
    return "<ul class='items'>" + "".join(
        f'<li><i class="dot" style="background:{TONE.get(i.get("tone"), TONE["neutral"])}"></i>{e(i.get("text"))}</li>' for i in sec.get("items", [])) + "</ul>"


DRAW = {"bars": bars, "hbars": hbars, "line": line, "ring": ring, "table": table, "list": lst}

CSS = """
*{box-sizing:border-box}body{margin:0;background:#fffaf4;color:#1d140d;font:15px/1.5 Inter,"Noto Sans","Noto Sans Thai","Noto Sans Hebrew",Sarabun,Arial,sans-serif}
.wrap{max-width:1040px;margin:0 auto;padding:28px 20px 40px}h1{font-size:28px;margin:0}.sub{color:#6b5646;margin:4px 0 22px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px;margin-bottom:18px}
.kpi{background:#fff;border:1px solid #efe4d8;border-radius:14px;padding:14px 16px}.kpi .l{color:#6b5646;font-size:13px}.kpi .v{font-size:24px;font-weight:700}.kpi .n{font-size:13px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(420px,1fr));gap:16px}
.card{background:#fff;border:1px solid #efe4d8;border-radius:16px;padding:16px 18px}.card h2{font-size:16px;margin:0 0 10px}
.chart{width:100%;height:auto}.chart text{font-size:12px;fill:#6b5646}.axis{stroke:#efe4d8}
.legend span{display:inline-flex;align-items:center;gap:6px;margin-inline-end:14px;font-size:13px}.legend i,.dot{display:inline-block;width:10px;height:10px;border-radius:50%}
.dot{margin-inline-end:8px}.hrow{display:grid;grid-template-columns:1.1fr 1.4fr auto;gap:10px;align-items:center;margin:8px 0}
.hb{height:10px;background:#f3ebe1;border-radius:6px;overflow:hidden}.hb i{display:block;height:100%}
.ringrow{display:flex;gap:18px;align-items:center}.ring{width:130px;height:130px;flex:none}.ring circle{fill:none;stroke-width:10}.ring .trk{stroke:#f3ebe1}.ring .val{stroke:#127a52;stroke-linecap:round}.ring text{font-size:20px;font-weight:700;fill:#1d140d}
.big{font-size:22px;font-weight:700;margin:0}.big span{font-size:14px;color:#6b5646;font-weight:400}
table{width:100%;border-collapse:collapse}th,td{text-align:start;padding:7px 6px;border-bottom:1px solid #f3ebe1;font-size:14px}th{color:#6b5646;font-weight:500}
.items{list-style:none;margin:0;padding:0}.items li{padding:6px 0;border-bottom:1px dashed #efe4d8}
footer{color:#6b5646;font-size:12.5px;margin-top:18px}
@media print{body{background:#fff}.card,.kpi{break-inside:avoid}}
"""


def render(spec: dict) -> str:
    lang = (spec.get("lang") or "en").split("-")[0].lower()
    d = "rtl" if lang in RTL else "ltr"
    kp = "".join(
        f'<div class="kpi"><div class="l">{e(k.get("label"))}</div><div class="v" style="color:{TONE.get(k.get("tone"), "#1d140d")}">{iso(k.get("value"))}</div>'
        f'<div class="n">{e(k.get("note", ""))}</div></div>' for k in spec.get("kpis", []))
    cards = []
    for s in spec.get("sections", []):
        fn = DRAW.get(s.get("type"))
        if not fn:
            raise ValueError(f"unknown section type: {s.get('type')}")
        cards.append(f'<section class="card"><h2>{e(s.get("title", ""))}</h2>{fn(s)}</section>')
    return (f'<!DOCTYPE html><html lang="{e(spec.get("lang", "en"))}" dir="{d}"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(spec.get("title", "Dashboard"))}</title><style>{CSS}</style></head>'
            f'<body><div class="wrap"><h1>{e(spec.get("title", ""))}</h1><p class="sub">{e(spec.get("subtitle", ""))}</p>'
            f'<div class="kpis">{kp}</div><div class="grid">{"".join(cards)}</div><footer>{e(spec.get("footer", ""))}</footer></div></body></html>')


def main(argv):
    if len(argv) != 3:
        print(__doc__)
        return 2
    with open(argv[1], encoding="utf-8") as f:
        spec = json.load(f)
    with open(argv[2], "w", encoding="utf-8") as f:
        f.write(render(spec))
    print(json.dumps({"written": argv[2], "sections": len(spec.get("sections", []))}))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
