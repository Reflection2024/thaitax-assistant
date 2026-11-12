#!/usr/bin/env node
/*
 * ThaiTax Assistant: bilingual Thai business documents (.docx).
 *
 *   node make_document.js <input.json> <output.docx>
 *   node make_document.js --sample <type> > sample.json   (types: tax_invoice, receipt, quotation, billing_note, payslip)
 *
 * Thai first, then a second language ("en" or "he") under each label. Totals,
 * VAT and baht-in-words are computed here in satang (integers) so the numbers
 * always reconcile. The serial number stays blank unless "number" is given,
 * and a DRAFT line is printed unless "final": true. A legal tax invoice
 * is issued from the user's own accounting system.
 *
 * Requires the npm package "docx" (npm install docx).
 */
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType,
  AlignmentType, BorderStyle, ShadingType,
} = require("docx");

const FONT = "Tahoma"; // Thai-capable on Windows and macOS; Sarabun is a good alternative
const W = 9638; // A4 text width (DXA) with 2 cm margins

const L = {
  tax_invoice: { th: "ใบกำกับภาษี", en: "TAX INVOICE", he: "חשבונית מס" },
  receipt: { th: "ใบเสร็จรับเงิน", en: "RECEIPT", he: "קבלה" },
  quotation: { th: "ใบเสนอราคา", en: "QUOTATION", he: "הצעת מחיר" },
  billing_note: { th: "ใบวางบิล", en: "BILLING NOTE", he: "דרישת תשלום" },
  payslip: { th: "สลิปเงินเดือน", en: "PAYSLIP", he: "תלוש שכר" },
  seller: { th: "ผู้ขาย", en: "Seller", he: "מוכר" },
  buyer: { th: "ผู้ซื้อ", en: "Buyer", he: "קונה" },
  employer: { th: "นายจ้าง", en: "Employer", he: "מעסיק" },
  employee: { th: "ลูกจ้าง", en: "Employee", he: "עובד" },
  taxid: { th: "เลขประจำตัวผู้เสียภาษี", en: "Tax ID", he: "מספר נישום" },
  branch: { th: "สาขา", en: "Branch", he: "סניף" },
  hq: { th: "สำนักงานใหญ่", en: "Head office", he: "משרד ראשי" },
  no: { th: "เลขที่", en: "No.", he: "מס'" },
  date: { th: "วันที่", en: "Date", he: "תאריך" },
  item: { th: "ลำดับ", en: "#", he: "#" },
  desc: { th: "รายการ", en: "Description", he: "תיאור" },
  qty: { th: "จำนวน", en: "Qty", he: "כמות" },
  price: { th: "ราคาต่อหน่วย", en: "Unit price", he: "מחיר ליחידה" },
  amount: { th: "จำนวนเงิน", en: "Amount", he: "סכום" },
  subtotal: { th: "มูลค่าก่อนภาษี", en: "Amount before VAT", he: "סכום לפני מע\"מ" },
  vat: { th: "ภาษีมูลค่าเพิ่ม", en: "VAT", he: "מע\"מ" },
  total: { th: "จำนวนเงินรวมทั้งสิ้น", en: "Grand total", he: "סה\"כ לתשלום" },
  words: { th: "ตัวอักษร", en: "In words", he: "במילים" },
  wht: { th: "หักภาษี ณ ที่จ่าย (โดยผู้จ่ายเงิน)", en: "Withholding tax (by payer)", he: "ניכוי במקור (על ידי המשלם)" },
  net_pay: { th: "ยอดชำระสุทธิหลังหัก ณ ที่จ่าย", en: "Net after withholding", he: "נטו לאחר ניכוי" },
  valid: { th: "ยืนราคาถึง", en: "Valid until", he: "בתוקף עד" },
  terms: { th: "เงื่อนไขการชำระเงิน", en: "Payment terms", he: "תנאי תשלום" },
  due: { th: "กำหนดชำระ", en: "Due date", he: "מועד תשלום" },
  ref: { th: "อ้างอิงใบแจ้งหนี้", en: "Invoice reference", he: "אסמכתא לחשבונית" },
  method: { th: "ชำระโดย", en: "Paid by", he: "שולם באמצעות" },
  period: { th: "งวดเงินเดือน", en: "Pay period", he: "תקופת שכר" },
  earnings: { th: "รายได้", en: "Earnings", he: "הכנסות" },
  deductions: { th: "รายการหัก", en: "Deductions", he: "ניכויים" },
  gross: { th: "รวมรายได้", en: "Gross pay", he: "ברוטו" },
  total_ded: { th: "รวมรายการหัก", en: "Total deductions", he: "סך ניכויים" },
  net: { th: "เงินได้สุทธิ", en: "Net pay", he: "נטו לתשלום" },
  sign_issuer: { th: "ผู้มีอำนาจลงนาม", en: "Authorised signature", he: "חתימה מורשית" },
  sign_receiver: { th: "ผู้รับเอกสาร", en: "Received by", he: "התקבל על ידי" },
  draft: { th: "ร่างเอกสาร โปรดออกจากระบบบัญชีของท่าน", en: "DRAFT: issue from your accounting system", he: "טיוטה: יש להפיק ממערכת הנהלת החשבונות" },
};

const THMONTH = ["มกราคม","กุมภาพันธ์","มีนาคม","เมษายน","พฤษภาคม","มิถุนายน","กรกฎาคม","สิงหาคม","กันยายน","ตุลาคม","พฤศจิกายน","ธันวาคม"];
function thDate(iso) { const [y, m, d] = iso.split("-").map(Number); return `${d} ${THMONTH[m - 1]} ${y + 543} (${y})`; }

const DIG = ["", "หนึ่ง", "สอง", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า"], POS = ["", "สิบ", "ร้อย", "พัน", "หมื่น", "แสน"];
function words(n) {
  if (n === 0) return "";
  if (n >= 1e6) return words(Math.floor(n / 1e6)) + "ล้าน" + words(n % 1e6);
  const s = String(n); let t = "";
  for (let i = 0; i < s.length; i++) {
    const d = +s[i], p = s.length - i - 1; if (!d) continue;
    if (p === 1 && d === 1) t += "สิบ"; else if (p === 1 && d === 2) t += "ยี่สิบ";
    else if (p === 0 && d === 1 && s.length > 1) t += "เอ็ด"; else t += DIG[d] + POS[p];
  }
  return t;
}
function bahttext(satang) { const b = Math.floor(satang / 100), st = satang % 100; return (b ? words(b) + "บาท" : (st ? "" : "ศูนย์บาท")) + (st ? words(st) + "สตางค์" : "ถ้วน"); }
const toSat = (x) => Math.round(Number(x) * 100);
const fmt = (sat) => (sat / 100).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });

function run(text, o = {}) { return new TextRun({ text: String(text), font: FONT, size: o.size || 20, bold: !!o.bold, color: o.color, rightToLeft: !!o.rtl }); }
function para(children, o = {}) { return new Paragraph({ children: Array.isArray(children) ? children : [children], alignment: o.align, spacing: { before: o.before || 0, after: o.after ?? 60 }, bidirectional: !!o.rtl }); }
function label(key, lang, o = {}) { return para([run(L[key].th, { bold: true, size: o.size }), run("  " + (L[key][lang] || ""), { size: (o.size || 20) - 4, color: "555555", rtl: lang === "he" })], o); }
const thin = { style: BorderStyle.SINGLE, size: 4, color: "BBBBBB" };
const borders = { top: thin, bottom: thin, left: thin, right: thin };
function cell(children, w, o = {}) {
  return new TableCell({ width: { size: w, type: WidthType.DXA }, borders, margins: { top: 60, bottom: 60, left: 100, right: 100 },
    shading: o.fill ? { type: ShadingType.CLEAR, color: "auto", fill: o.fill } : undefined, children: Array.isArray(children) ? children : [children] });
}
function party(key, p, lang) {
  const br = p.branch && p.branch !== "00000" ? `${L.branch.th} ${p.branch}` : L.hq.th;
  return [label(key, lang), para(run(p.name || "[ ____ ]", { bold: true })), para(run(p.address || "[ ____ ]")),
    para(run(`${L.taxid.th} / ${L.taxid[lang]}: ${p.tax_id || "[ _____________ ]"}   ${br}`))];
}

function build(d) {
  const lang = d.second_language || "en";
  const type = d.type; const out = [];
  out.push(para([run(L[type].th, { size: 36, bold: true })], { align: AlignmentType.CENTER }));
  out.push(para([run(L[type][lang], { size: 24, color: "555555", rtl: lang === "he" })], { align: AlignmentType.CENTER, after: 120 }));
  if (!d.final) out.push(para([run(`${L.draft.th} | ${L.draft[lang]}`, { color: "B00020", bold: true, size: 18 })], { align: AlignmentType.CENTER, after: 160 }));

  const half = W / 2;
  if (type === "payslip") {
    out.push(new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: [half, half], rows: [new TableRow({ children: [
      cell(party("employer", d.employer, lang), half),
      cell([label("employee", lang), para(run(d.employee.name, { bold: true })), para(run(d.employee.position || "")),
        para(run(`${L.period.th} / ${L.period[lang]}: ${d.period}`))], half)] })] }));
    const e = d.earnings || [], x = d.deductions || [];
    const gs = e.reduce((a, r) => a + toSat(r.amount), 0), ds = x.reduce((a, r) => a + toSat(r.amount), 0);
    const rows = Math.max(e.length, x.length); const q = W / 4;
    const body = [];
    for (let i = 0; i < rows; i++) {
      const a = e[i], b = x[i];
      body.push(new TableRow({ children: [cell(para(run(a ? a.label : "")), q), cell(para(run(a ? fmt(toSat(a.amount)) : ""), { align: AlignmentType.RIGHT }), q),
        cell(para(run(b ? b.label : "")), q), cell(para(run(b ? fmt(toSat(b.amount)) : ""), { align: AlignmentType.RIGHT }), q)] }));
    }
    body.push(new TableRow({ children: [cell(label("gross", lang), q), cell(para(run(fmt(gs), { bold: true }), { align: AlignmentType.RIGHT }), q),
      cell(label("total_ded", lang), q), cell(para(run(fmt(ds), { bold: true }), { align: AlignmentType.RIGHT }), q)] }));
    out.push(para(run(""), { after: 120 }));
    out.push(new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: [q, q, q, q], rows: [
      new TableRow({ children: [cell(label("earnings", lang), q * 2, { fill: "EEF2F6" }), cell(label("deductions", lang), q * 2, { fill: "EEF2F6" })] }), ...body] }));
    out.push(para([run(`${L.net.th} / ${L.net[lang]}: `, { bold: true, size: 24 }), run(`THB ${fmt(gs - ds)}`, { bold: true, size: 24 })], { before: 200 }));
    out.push(para(run(`(${bahttext(gs - ds)})`)));
    return out;
  }

  // header parties + document info
  out.push(new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: [half, half], rows: [new TableRow({ children: [
    cell(party("seller", d.seller, lang), half),
    cell([...party("buyer", d.buyer, lang),
      para(run(`${L.no.th} / ${L.no[lang]}: ${d.number || "[ ออกจากระบบบัญชี ]"}`, { bold: true }), { before: 80 }),
      para(run(`${L.date.th} / ${L.date[lang]}: ${thDate(d.date)}`))], half)] })] }));
  const extra = [];
  if (type === "quotation") { if (d.valid_until) extra.push(`${L.valid.th} / ${L.valid[lang]}: ${thDate(d.valid_until)}`); if (d.terms) extra.push(`${L.terms.th} / ${L.terms[lang]}: ${d.terms}`); }
  if (type === "billing_note" && d.due_date) extra.push(`${L.due.th} / ${L.due[lang]}: ${thDate(d.due_date)}`);
  if (type === "receipt") { if (d.invoice_ref) extra.push(`${L.ref.th} / ${L.ref[lang]}: ${d.invoice_ref}`); if (d.payment_method) extra.push(`${L.method.th} / ${L.method[lang]}: ${d.payment_method}`); }
  extra.forEach((t) => out.push(para(run(t), { before: 60 })));
  out.push(para(run(""), { after: 120 }));

  // items
  const cw = [700, 4338, 1100, 1700, 1800];
  const head = ["item", "desc", "qty", "price", "amount"].map((k, i) => cell([para(run(L[k].th, { bold: true, size: 18 })), para(run(L[k][lang], { size: 16, color: "555555", rtl: lang === "he" }))], cw[i], { fill: "EEF2F6" }));
  let sub = 0;
  const rows = (d.items || []).map((it, i) => {
    const line = Math.round(Number(it.qty) * toSat(it.unit_price)); sub += line;
    return new TableRow({ children: [cell(para(run(i + 1)), cw[0]), cell(para(run(it.description)), cw[1]),
      cell(para(run(it.qty), { align: AlignmentType.RIGHT }), cw[2]), cell(para(run(fmt(toSat(it.unit_price))), { align: AlignmentType.RIGHT }), cw[3]),
      cell(para(run(fmt(line)), { align: AlignmentType.RIGHT }), cw[4])] });
  });
  out.push(new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: cw, rows: [new TableRow({ children: head, tableHeader: true }), ...rows] }));

  // totals
  const rate = d.vat_rate ?? 0.07, vatOn = d.vat !== false && type !== "billing_note" ? true : d.vat !== false;
  const vat = vatOn ? Math.round(sub * rate) : 0, total = sub + vat;
  const tw = [W - 2600, 2600];
  const trow = (k, sat, bold, suffix = "") => new TableRow({ children: [cell(para([run(L[k].th + suffix, { bold }), run("  " + L[k][lang], { size: 16, color: "555555" })], { align: AlignmentType.RIGHT }), tw[0]),
    cell(para(run(fmt(sat), { bold }), { align: AlignmentType.RIGHT }), tw[1])] });
  const totalRows = [trow("subtotal", sub)];
  if (vatOn) totalRows.push(trow("vat", vat, false, ` ${Math.round(rate * 100)}%`));
  totalRows.push(trow("total", total, true));
  out.push(new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: tw, rows: totalRows }));
  out.push(para([run(`${L.words.th}: `, { bold: true }), run(`(${bahttext(total)})`)], { before: 120 }));
  if (d.withholding_rate) {
    const w = Math.round(sub * d.withholding_rate);
    out.push(para(run(`${L.wht.th} ${d.withholding_rate * 100}%: ${fmt(w)}  |  ${L.net_pay.th}: ${fmt(total - w)}`, { size: 18 }), { before: 60 }));
    out.push(para(run(`${L.wht[lang]} ${d.withholding_rate * 100}%: ${fmt(w)}  |  ${L.net_pay[lang]}: ${fmt(total - w)}`, { size: 16, color: "555555", rtl: lang === "he" })));
  }
  if (d.notes) out.push(para(run(d.notes, { size: 18 }), { before: 120 }));

  // signatures
  const sw = W / 2;
  out.push(para(run(""), { after: 400 }));
  out.push(new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: [sw, sw], rows: [new TableRow({ children: ["sign_receiver", "sign_issuer"].map((k) =>
    new TableCell({ width: { size: sw, type: WidthType.DXA }, borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } },
      children: [para(run("______________________________"), { align: AlignmentType.CENTER }), para(run(`${L[k].th} / ${L[k][lang]}`, { size: 16 }), { align: AlignmentType.CENTER }),
        para(run(`${L.date.th} ____/____/______`, { size: 16 }), { align: AlignmentType.CENTER })] })) })] }));
  return out;
}

const SAMPLES = {
  tax_invoice: { type: "tax_invoice", second_language: "en", date: "2026-11-11", withholding_rate: 0.03,
    seller: { name: "บริษัท ตัวอย่าง จำกัด (Example Co., Ltd.)", address: "99/9 หมู่ 1 ต.บ่อผุด อ.เกาะสมุย จ.สุราษฎร์ธานี 84320", tax_id: "0845560000000", branch: "00000" },
    buyer: { name: "บริษัท สยามโคสต์ จำกัด (Siam Coast Co., Ltd.)", address: "1 ถ.สุขุมวิท กรุงเทพฯ 10110", tax_id: "0105560000000", branch: "00000" },
    items: [{ description: "ค่าบริการที่ปรึกษา ต.ค. 2569 / Consulting, October 2026", qty: 1, unit_price: 85000 }] },
  payslip: { type: "payslip", second_language: "en", period: "พฤศจิกายน 2569 (November 2026)",
    employer: { name: "บริษัท ตัวอย่าง จำกัด", address: "เกาะสมุย", tax_id: "0845560000000", branch: "00000" },
    employee: { name: "นางสาว ตัวอย่าง ใจดี", position: "พนักงานต้อนรับ / Receptionist" },
    earnings: [{ label: "เงินเดือน / Salary", amount: 18000 }, { label: "ค่าล่วงเวลา / Overtime", amount: 1687.5 }],
    deductions: [{ label: "ประกันสังคม / Social security", amount: 875 }, { label: "ภาษี ณ ที่จ่าย / Tax (PND.1)", amount: 0 }] },
};
SAMPLES.receipt = { ...SAMPLES.tax_invoice, type: "receipt", invoice_ref: "INV-2026-0042", payment_method: "โอนธนาคาร / Bank transfer" };
SAMPLES.quotation = { ...SAMPLES.tax_invoice, type: "quotation", valid_until: "2026-12-11", terms: "50% มัดจำ / 50% deposit", withholding_rate: undefined };
SAMPLES.billing_note = { ...SAMPLES.tax_invoice, type: "billing_note", due_date: "2026-12-15" };

(async () => {
  const a = process.argv.slice(2);
  if (a[0] === "--sample") { process.stdout.write(JSON.stringify(SAMPLES[a[1] || "tax_invoice"], null, 2) + "\n"); return; }
  if (a.length < 2) { console.error("usage: node make_document.js <input.json> <output.docx> | --sample <type>"); process.exit(2); }
  const d = JSON.parse(fs.readFileSync(a[0], "utf8"));
  if (!L[d.type]) { console.error("unknown type " + d.type); process.exit(2); }
  const doc = new Document({ styles: { default: { document: { run: { font: FONT, size: 20 } } } },
    sections: [{ properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 } } }, children: build(d) }] });
  fs.writeFileSync(a[1], await Packer.toBuffer(doc));
  console.log(JSON.stringify({ written: a[1], type: d.type, draft: !d.final }));
})();
