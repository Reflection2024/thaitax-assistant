# ThaiTax Assistant 🌴

**A back office in Thailand for foreign business owners, inside Claude. In English, עברית and ไทย.**

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
| **thai-export-reader** | Reads PEAK / Express / gateway / bank files with Thai headers and BE dates | (upload a file) |

### Connectors

- **FlowAccount**: included (official connector, OAuth). Sign in as the Account Owner and pick the company. Works with every FlowAccount package.
- **Stripe**: included (official connector, OAuth).
- **Omise / Opn Payments**: optional, runs locally. See *Omise setup* below.
- **2C2P, GB Prime Pay, KSher, PEAK, Express**: work from the monthly export file.

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
