# ThaiTax Assistant

**Every Thai tax report, ready for your accountant.** Personal or company, in English, עברית and ไทย. Free.

By Reflection Thailand.

---

## English

ThaiTax Assistant takes care of the Thai admin that usually needs an accountant, a translator and a spreadsheet. It works for **individuals** (freelancers, consultants, landlords, expats with side income) and for **companies**, or both at once, always keeping each taxpayer separate.

| Skill | What it does | Say |
|---|---|---|
| **thaitax-start** | Sets up your companies, language and tools | "Get started" |
| **thai-personal-tax** | Your annual return (PND.90/91) and half-year PND.94, line by line, with a worksheet that mirrors the form and an e-Filing walkthrough | "Fill in my annual tax return" |
| **foreign-income** | Income from abroad: 180-day residency, remittance ledger (pre-2024 savings vs. taxable income), Foreign-Sourced Income Declaration, Foreign Tax Credit | "I have income from abroad" |
| **thai-monthly-tax** | Prepares PP.30, PP.36, PND.3/53/54, SSO, and PND.50/51 working papers, with deadlines | "What's due this month?" |
| **thai-documents** | Bilingual tax-invoice drafts, quotations, receipts, billing notes, 50 ทวิ, payslips, letters | "Draft a tax invoice in Thai" |
| **cash-and-collections** | Receivables, payments and payouts, a 90-day cash outlook, polite reminders | "Who owes me money?" |
| **thai-payroll** | Salaries, overtime, social security, PND.1, work-permit flags | "Prepare payroll" |
| **receipt-capture** | Photos of receipts from your phone gallery → an expense list, with VAT claimability checked | (share photos) "Add these receipts" |
| **ask-thai-tax** | Any question, researched in current official sources (rd.go.th, Royal Gazette, SSO) and answered with links | "Do I need to…?" |
| **accountant-check** | A second pair of eyes on your accountant: filings complete and on time, figures match your books, tax payments really reached the Revenue Department, your own access in place | "Check my accountant's work" |
| **what-do-you-need** | Asks for exactly what is missing, keeps the list, reminds you | "What do you need from me?" |
| **document-check** | Checks every document (invoices, 50 ทวิ, forms, payslips, statements, journals) and says what to fix | "Check this" |
| **official-letter** | A Thai letter from the Revenue Department, SSO, DBD, a bank or the land office: translated, what they want, deadline, reply drafted | (photo the letter) |
| **year-end-planning** | How much tax you can still save before 31 December, with each option computed | "How can I save tax before year end?" |
| **property-tax** | Land and building tax, the full cost of selling, lease registration | "What will it cost to sell my villa?" |
| **company-housekeeping** | Your company's yearly calendar: AGM, DBD, บอจ.5, changes, licences | "What does my company need to do this year?" |
| **visa-reminders** | 90-day reports, extensions, work permits, TM30: reminders only | "Remind me of my visa dates" |
| **family-budget** | Your bank statements → a family dashboard: money in vs. out, where it goes, every fixed payment and subscription, services paid twice. Optional export to Actual Budget | "Where does our money go?" |
| **monthly-pack** | Everything for the month in one go, automatically on the 1st if you want, with a draft email to your accountant | "Run the month" |
| **thai-export-reader** | Reads PEAK / Express / gateway / bank files with Thai headers and BE dates | (upload a file) |

### Built-in tools

- `scripts/thaitax_calc.py`: every tax, VAT, SSO, withholding and overtime figure is calculated here, never estimated (tested; rates in `scripts/rates.json`).
- `scripts/make_document.js`: Thai + English/Hebrew tax invoices, receipts, quotations, billing notes and payslips with the same layout every time.
- `scripts/official_forms.py` + `assets/forms/`: the Revenue Department's own PDF forms (ภ.ง.ด.90/91/94, foreign-income declaration, ภ.ง.ด.1/3/53 and their attachments, ภ.พ.30, ภ.พ.36, ภ.ง.ด.50/51, 50 ทวิ) filled in with your figures, checked by preview, plus a one-page explanation. Send the form straight to your accountant.
- `scripts/budget.py` + `scripts/budget_dashboard.py`: family budget engine (categories, recurring payments, duplicates, FX) and a self-contained dashboard page in English, Hebrew or Thai (tested).
- `skills/tax-facts-update`: annual re-verification of every rate and deadline.

### Getting started

After installing, say **"Get started"**. ThaiTax Assistant welcomes you, asks for the details it needs in short rounds, walks you through each connection one at a time, and shows you something useful straight away.

### What to connect (all optional)

- **FlowAccount**: included. Sign in as the Account Owner and pick the company.
- **Stripe**: included.
- **Email** (Gmail or Outlook): finds invoices, receipts and 50 ทวิ in your inbox.
- **Calendar**: deadline reminders, added only after you say yes.
- **Cloud drive**: statements in, monthly packs out.
- **Omise / Opn**: optional, runs on your computer. See *Omise setup* below.
- **Phone photos**: no connection. In the Claude app, tap **+ → Photos**, or **Share → Claude** from your gallery.
- **PEAK, Express, 2C2P, KSher, banks**: send the export file.

### Omise setup (optional)

Omise publishes an MCP server that runs on your computer with your API keys. Start with **test** keys:

1. In the Omise dashboard, copy your test public and secret keys.
2. Install Omise's MCP server following Omise's own instructions, with `OMISE_PUBLIC_KEY`, `OMISE_SECRET_KEY` and `OMISE_ENVIRONMENT=test`.
3. Add it to Claude Desktop. Switch to live keys only once you are comfortable.

The secret key can charge and refund. ThaiTax Assistant always asks before any write.

### Safety rules (built in)

- Nothing is filed, paid, sent or created without your explicit yes.
- ThaiTax Assistant never issues a numbered legal tax invoice. It drafts the document; you issue it from FlowAccount.
- It never logs in to the Revenue Department, SSO or bank portals.
- Each company is handled separately and amounts are never added across currencies.
- Rates and deadlines are checked against official Thai sources before use.

> **Prepared for review by your Thai accountant. Not tax or legal advice. Nothing is filed.**

---

## עברית

ThaiTax Assistant מטפל בכל מה שחוזר כל חודש בעסק בתאילנד: דוחות מס, מסמכים בתאילנדית, גבייה ותזרים, ומשכורות. הוא מתאים גם לאדם פרטי (פרילנסר, יועץ, משכיר נכס) וגם לחברה.

- **"תמלא לי את הדוח השנתי"**: הדוח השנתי (PND.90/91) והחצי-שנתי (PND.94), שורה אחר שורה. גיליון עבודה שבנוי כמו הטופס עצמו, עם הדרכה למילוי במערכת ה-e-Filing.
- **"יש לי הכנסות מחו"ל"**: ספירת ימים לצורך תושבות מס (180 יום), מעקב אחרי העברות כסף לתאילנד (הפרדה בין חסכונות מלפני 2024 לבין הכנסה חייבת), טופס הצהרה על הכנסות מחו"ל, וזיכוי בגין מס ששולם בחו"ל.

- **"בוא נתחיל"**: הגדרת החברות, השפה והכלים.
- **"מה צריך להגיש החודש?"**: מע"מ (PP.30), מע"מ על שירותים מחו"ל (PP.36), ניכוי במקור (PND.3/53/54) וביטוח לאומי, עם מועדי ההגשה.
- **"תכין טיוטת חשבונית מס בתאילנדית"**: מסמכים דו-לשוניים עם כל שדות החובה.
- **"מי חייב לי כסף?"**: חובות פתוחים, תשלומים מ-Stripe ומ-Omise, תחזית תזרים ותזכורות מנומסות.
- **"תכין משכורות"**: שכר, שעות נוספות, ביטוח לאומי ו-PND.1, עם התראות על היתרי עבודה.

שום דבר לא מוגש, לא משולם ולא נשלח בלי אישור מפורש שלך. הכל מוכן לבדיקת רואה החשבון התאילנדי שלך.

---

## ภาษาไทย

ThaiTax Assistant ช่วยเตรียมงานเอกสารประจำเดือนสำหรับธุรกิจในประเทศไทย ได้แก่ ภาษีมูลค่าเพิ่ม ภาษีหัก ณ ที่จ่าย ประกันสังคม เอกสารสองภาษา ติดตามหนี้ และเงินเดือน

เหมาะทั้งบุคคลธรรมดา (ฟรีแลนซ์ ผู้ให้เช่า) และนิติบุคคล

- "ช่วยกรอก ภ.ง.ด.90": เตรียมแบบ ภ.ง.ด.90/91/94 ทีละบรรทัด
- "มีรายได้จากต่างประเทศ": ถิ่นที่อยู่ทางภาษี เงินได้ที่นำเข้าประเทศ และเครดิตภาษีต่างประเทศ
- "เดือนนี้ต้องยื่นอะไรบ้าง": ภ.พ.30, ภ.พ.36, ภ.ง.ด.3/53/54
- "ร่างใบกำกับภาษี": ร่างเอกสารภาษาไทยคู่ภาษาอังกฤษ
- "ใครค้างชำระบ้าง": ลูกหนี้ค้างชำระและจดหมายทวงถามอย่างสุภาพ
- "เตรียมเงินเดือน": เงินเดือน ประกันสังคม และ ภ.ง.ด.1

ไม่มีการยื่นแบบ ชำระเงิน หรือส่งเอกสารใด ๆ โดยไม่ได้รับการยืนยันจากท่าน จัดเตรียมเพื่อให้นักบัญชีของท่านตรวจสอบ
