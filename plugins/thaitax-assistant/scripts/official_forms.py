#!/usr/bin/env python3
"""Fill the official Thai Revenue Department / SSO PDF forms, so the user gets the real form
(same layout, boxes and line numbers) to send to the accountant, plus a short explanation sheet.

    python3 -I official_forms.py list                                  # forms bundled with the plugin
    python3 -I official_forms.py fields PND90 [--page 1] [--named]     # every box: name, page, label next to it
    python3 -I official_forms.py fill PND90 values.json out.pdf [--final]
    python3 -I official_forms.py preview out.pdf outdir [--dpi 110]    # PNG of each page, to check the result
    python3 -I official_forms.py debug PND90 names.pdf                  # every box labelled with its name (for mapping)
    python3 -I official_forms.py explain values.json out.pdf [--title ...]

values.json:
  {"form": "PND90",
   "values": {"tin": "1234567890123", "Text80": "Amir", "total_income": {"value": "1,250,000.00", "note": "Salary from GmbH"}, "chk_single": true}}
Keys may be raw field names (from `fields`) or semantic names from forms/<FORM>.map.json.
A value may be a string, a number, true/false (checkbox), or {"value": ..., "note": "..."}; notes go to the
explanation sheet only, never onto the form.

The form is never altered except for the values drawn into its boxes; widgets are flattened so the
values print everywhere. Unless --final, a small grey "Draft for review" line is printed in the bottom margin.
Requires pypdf, reportlab, pdfplumber (and pypdfium2 for preview).
"""
from __future__ import annotations

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FORMS = os.path.join(HERE, "..", "assets", "forms")
FONT = os.path.join(HERE, "..", "assets", "fonts", "Sarabun-Regular.ttf")


def _catalog():
    with open(os.path.join(FORMS, "catalog.json"), encoding="utf-8") as f:
        return json.load(f)


def form_path(form):
    if os.path.exists(form):
        return form
    cat = _catalog()
    if form not in cat:
        raise SystemExit(f"unknown form {form}; known: {', '.join(cat)}")
    return os.path.join(FORMS, cat[form]["file"])


def _full_name(annot):
    parts = []
    a = annot
    while a is not None:
        t = a.get("/T")
        if t is not None:
            parts.append(str(t))
        a = a.get("/Parent")
        a = a.get_object() if a is not None else None
    return ".".join(reversed(parts))


def _inherit(annot, key):
    a = annot
    while a is not None:
        if key in a:
            return a[key]
        a = a.get("/Parent")
        a = a.get_object() if a is not None else None
    return None


def widgets(pdf_path):
    from pypdf import PdfReader
    r = PdfReader(pdf_path)
    out = []
    for pi, page in enumerate(r.pages):
        for ref in page.get("/Annots") or []:
            a = ref.get_object()
            if a.get("/Subtype") != "/Widget":
                continue
            name = _full_name(a)
            if not name:
                continue
            ft = _inherit(a, "/FT")
            ff = int(_inherit(a, "/Ff") or 0)
            rect = [float(x) for x in a["/Rect"]]
            x0, y0, x1, y1 = min(rect[0], rect[2]), min(rect[1], rect[3]), max(rect[0], rect[2]), max(rect[1], rect[3])
            on = None
            if ft == "/Btn":
                ap = a.get("/AP", {}).get("/N", {})
                states = [k for k in ap.keys() if k != "/Off"] if hasattr(ap, "keys") else []
                on = states[0] if states else "/Yes"
            out.append({
                "name": name, "page": pi + 1, "rect": [round(x0, 1), round(y0, 1), round(x1, 1), round(y1, 1)],
                "type": "checkbox" if ft == "/Btn" else "text",
                "maxlen": int(_inherit(a, "/MaxLen") or 0), "comb": bool(ff & (1 << 24)),
                "align": int(_inherit(a, "/Q") or 0), "on": on,
                "page_h": float(page.mediabox.height),
            })
    # several boxes with one name (radio buttons, repeated fields): number them name#1, name#2 ...
    count = {}
    for w in out:
        count[w["name"]] = count.get(w["name"], 0) + 1
    seen = {}
    for w in out:
        if count[w["name"]] > 1:
            seen[w["name"]] = seen.get(w["name"], 0) + 1
            w["name"] = f'{w["name"]}#{seen[w["name"]]}'
    return out


def labels(pdf_path, ws):
    """Attach the printed text nearest to each box (same line to the left, else the line above)."""
    import pdfplumber
    by_page = {}
    with pdfplumber.open(pdf_path) as pdf:
        for i, p in enumerate(pdf.pages):
            by_page[i + 1] = p.extract_words(keep_blank_chars=False, use_text_flow=True, extra_attrs=[])
    for w in ws:
        H = w["page_h"]
        x0, y0, x1, y1 = w["rect"]
        top, bottom = H - y1, H - y0  # pdfplumber coordinates
        words = by_page.get(w["page"], [])
        if w["type"] == "checkbox":  # a tick box is described by the words to its right
            right = [t for t in words if t["x0"] >= x1 - 2 and t["x0"] - x1 < 200 and abs((t["top"] + t["bottom"]) / 2 - (top + bottom) / 2) < 6]
            right.sort(key=lambda t: t["x0"])
            if right:
                w["label"] = " ".join(t["text"] for t in right[:7]).strip()
                continue
        same = [t for t in words if t["x1"] <= x0 + 2 and abs((t["top"] + t["bottom"]) / 2 - (top + bottom) / 2) < 7 and x0 - t["x1"] < 260]
        same.sort(key=lambda t: t["x0"])
        label = " ".join(t["text"] for t in same[-8:])
        if not label:
            above = [t for t in words if bottom - 2 > t["bottom"] > top - 22 and t["x0"] < x1 and t["x1"] > x0 - 40]
            above.sort(key=lambda t: (t["top"], t["x0"]))
            label = " ".join(t["text"] for t in above[:8])
        w["label"] = label.strip()
    return ws


def _dividers(pdf_path):
    """Vertical rule segments per page (PDF coordinates), to find the baht | satang split inside amount boxes."""
    import pdfplumber
    out = {}
    with pdfplumber.open(pdf_path) as pdf:
        for i, p in enumerate(pdf.pages):
            H = float(p.height)
            segs = []
            for ln in p.lines:
                if abs(ln["x0"] - ln["x1"]) < 0.8:
                    segs.append((ln["x0"], H - ln["bottom"], H - ln["top"]))
            for r in p.rects:
                for x in (r["x0"], r["x1"]):
                    segs.append((x, H - r["bottom"], H - r["top"]))
            out[i + 1] = segs
    return out


def _satang_split(w, divs):
    x0, y0, x1, y1 = w["rect"]
    wd = x1 - x0
    best = None
    for x, b, t in divs.get(w["page"], []):
        if x0 + wd * 0.6 < x < x1 - 4 and b < y0 + (y1 - y0) * 0.6 and t > y0 + (y1 - y0) * 0.4:
            best = x if best is None else max(best, x)
    return best


def load_map(form):
    p = os.path.join(FORMS, f"{form}.map.json")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f).get("fields", {})
    return {}


def _fmt(v):
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return f"{v:,.2f}"
    return str(v)


def fill(form, values_path, out_path, final=False, label_checkboxes=False, raw=False):
    from io import BytesIO
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import ArrayObject, NameObject
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen import canvas

    src = form_path(form)
    with open(values_path, encoding="utf-8") as f:
        data = json.load(f)
    vals = data.get("values", data)
    fmap = load_map(form if not os.path.exists(form) else data.get("form", ""))
    ws = {w["name"]: w for w in widgets(src)}
    resolved, unknown = {}, []
    for k, v in vals.items():
        if isinstance(v, dict):
            v = v.get("value")
        name = fmap.get(k, {}).get("field", k) if isinstance(fmap.get(k), dict) else fmap.get(k, k)
        if name in ws:
            resolved[name] = _fmt(v)
        else:
            unknown.append(k)
    if unknown:
        raise SystemExit(f"no such box on {form}: {', '.join(unknown)} (run `fields {form}` to see names)")

    pdfmetrics.registerFont(TTFont("Sarabun", FONT))
    divs = _dividers(src)
    reader = PdfReader(src)
    writer = PdfWriter()
    for pi, page in enumerate(reader.pages):
        W, H = float(page.mediabox.width), float(page.mediabox.height)
        buf = BytesIO()
        c = canvas.Canvas(buf, pagesize=(W, H))
        for name, v in resolved.items():
            w = ws[name]
            if w["page"] != pi + 1:
                continue
            x0, y0, x1, y1 = w["rect"]
            h, wd = y1 - y0, x1 - x0
            if w["type"] == "checkbox":
                if v is True or str(v).lower() in ("1", "true", "yes", "x", "✓"):
                    c.setLineWidth(1.1)
                    c.line(x0 + wd * .2, y0 + h * .5, x0 + wd * .42, y0 + h * .22)
                    c.line(x0 + wd * .42, y0 + h * .22, x0 + wd * .82, y0 + h * .82)
                if label_checkboxes:
                    c.setFont("Sarabun", 5.5); c.setFillColorRGB(.8, 0, 0)
                    c.drawString(x1 + 1, y0 + 1, name.replace("Radio Button", "R").replace("Check Box", "C"))
                    c.setFillColorRGB(0, 0, 0)
                continue
            text = str(v)
            if raw:
                c.setFont("Sarabun", 5.5); c.setFillColorRGB(0, 0, .8)
                c.drawString(x0 + 1, y0 + 1, text); c.setFillColorRGB(0, 0, 0)
                continue
            size = max(6.5, min(11.0, h * 0.72))
            c.setFont("Sarabun", size)
            base = y0 + (h - size * 0.72) / 2
            if w["comb"] and w["maxlen"]:
                n = w["maxlen"]
                digits = re.sub(r"\D", "", text)
                if n == 17 and len(digits) == 13:  # 13-digit ID: boxes 1-2345-67890-12-3, dashes are printed
                    text = f"{digits[0]} {digits[1:5]} {digits[5:10]} {digits[10:12]} {digits[12]}"
                elif re.fullmatch(r"-?[\d,]+(\.\d{1,2})?", text) and n >= 4:
                    # amount boxes: baht digits, a printed "-", then 2 satang boxes
                    baht, _, sat = text.replace(",", "").partition(".")
                    text = baht.rjust(n - 3) + " " + (sat or "00").ljust(2, "0")
                cell = wd / n
                for i, ch in enumerate(text[:n]):
                    if ch != " ":
                        c.drawCentredString(x0 + cell * (i + .5), base, ch)
                continue
            while c.stringWidth(text, "Sarabun", size) > wd - 3 and size > 5.5:
                size -= 0.5
                c.setFont("Sarabun", size)
            numeric = bool(re.fullmatch(r"[-\d,.\s()]+", text))
            amount = re.fullmatch(r"-?[\d,]+(\.\d{1,2})?", text)
            split = _satang_split(w, divs) if (amount and w["align"] == 2) else None
            if split:
                baht, _, sat = text.partition(".")
                if "," not in baht and len(baht.lstrip("-")) > 3:
                    baht = f"{int(baht):,}"
                c.drawRightString(split - 2, base, baht)
                c.drawCentredString((split + x1) / 2, base, (sat or "00").ljust(2, "0"))
                continue
            if w["align"] == 2 or (numeric and w["align"] != 1 and not w["maxlen"]):
                c.drawRightString(x1 - 2, base, text)
            elif w["align"] == 1:
                c.drawCentredString((x0 + x1) / 2, base, text)
            else:
                c.drawString(x0 + 2, base, text)
        if not final:
            c.setFont("Sarabun", 6.5)
            c.setFillGray(0.45)
            c.drawString(18, 8, "Draft for review – prepared with ThaiTax Assistant. Check every figure before filing. ร่างเพื่อตรวจสอบ")
        c.showPage()
        c.save()
        buf.seek(0)
        overlay = PdfReader(buf).pages[0]
        if "/Annots" in page:
            keep = [a for a in page["/Annots"] if a.get_object().get("/Subtype") != "/Widget"]
            page[NameObject("/Annots")] = ArrayObject(keep)
        page.merge_page(overlay)
        writer.add_page(page)
    with open(out_path, "wb") as f:
        writer.write(f)
    return {"written": out_path, "form": form, "filled": len(resolved), "draft": not final}


def debug(form, out_path):
    """Write each box's name into it (checkboxes get their name beside them), to map boxes to lines."""
    ws = widgets(form_path(form))
    vals = {}
    for w in ws:
        vals[w["name"]] = True if w["type"] == "checkbox" else w["name"]
    tmp = out_path + ".json"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump({"form": form, "values": vals}, f, ensure_ascii=False)
    res = fill(form, tmp, out_path, final=True, label_checkboxes=True, raw=True)
    os.remove(tmp)
    return res


def preview(pdf_path, outdir, dpi=110):
    import pypdfium2 as pdfium
    os.makedirs(outdir, exist_ok=True)
    doc = pdfium.PdfDocument(pdf_path)
    files = []
    for i in range(len(doc)):
        img = doc[i].render(scale=dpi / 72).to_pil()
        p = os.path.join(outdir, f"page-{i + 1}.png")
        img.save(p)
        files.append(p)
    return {"pages": files}


def explain(values_path, out_path, title=None):
    """One-page explanation: each filled line, its amount and the note (Thai/English)."""
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen import canvas
    with open(values_path, encoding="utf-8") as f:
        data = json.load(f)
    vals = data.get("values", data)
    pdfmetrics.registerFont(TTFont("Sarabun", FONT))
    c = canvas.Canvas(out_path, pagesize=A4)
    W, H = A4
    y = H - 50
    c.setFont("Sarabun", 15)
    c.drawString(40, y, title or f"{data.get('form', 'Form')}: what is in each line")
    y -= 26
    c.setFont("Sarabun", 9.5)
    for k, v in vals.items():
        if not isinstance(v, dict) or not v.get("note"):
            continue
        val = _fmt(v.get("value"))
        if isinstance(val, str) and re.fullmatch(r"-?\d+(\.\d+)?", val):
            val = f"{float(val):,.2f}"
        line = f"{v.get('line', k)}"
        c.drawString(40, y, line[:40])
        c.drawRightString(300, y, "✓" if val is True else str(val))
        c.drawString(315, y, str(v["note"])[:70])
        y -= 15
        if y < 60:
            c.showPage(); c.setFont("Sarabun", 9.5); y = H - 50
    c.setFillGray(0.45); c.setFont("Sarabun", 7.5)
    c.drawString(40, 30, "Explanation for you. Send the official form to your accountant; keep this sheet for your records.")
    c.save()
    return {"written": out_path}


def main(argv):
    if len(argv) < 2:
        print(__doc__); return 2
    cmd = argv[1]
    if cmd == "list":
        print(json.dumps(_catalog(), ensure_ascii=False, indent=1)); return 0
    if cmd == "fields":
        form = argv[2]
        ws = labels(form_path(form), widgets(form_path(form)))
        if "--page" in argv:
            pg = int(argv[argv.index("--page") + 1]); ws = [w for w in ws if w["page"] == pg]
        fmap = load_map(form)
        rev = {(v["field"] if isinstance(v, dict) else v): k for k, v in fmap.items()}
        for w in ws:
            w.pop("page_h", None)
            if w["name"] in rev:
                w["semantic"] = rev[w["name"]]
        if "--named" in argv:
            ws = [w for w in ws if "semantic" in w]
        print(json.dumps(ws, ensure_ascii=False, indent=0)); return 0
    if cmd == "fill":
        print(json.dumps(fill(argv[2], argv[3], argv[4], final="--final" in argv), ensure_ascii=False)); return 0
    if cmd == "debug":
        print(json.dumps(debug(argv[2], argv[3]))); return 0
    if cmd == "preview":
        dpi = int(argv[argv.index("--dpi") + 1]) if "--dpi" in argv else 110
        print(json.dumps(preview(argv[2], argv[3], dpi))); return 0
    if cmd == "explain":
        t = argv[argv.index("--title") + 1] if "--title" in argv else None
        print(json.dumps(explain(argv[2], argv[3], t), ensure_ascii=False)); return 0
    print(__doc__); return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
