---
name: thai-documents
description: "Drafts Thai business documents in Thai with English or Hebrew alongside: tax invoice drafts (ใบกำกับภาษี), receipts, quotations, billing notes, withholding certificate (50 ทวิ) data, payslips, overdue-payment letters and short business letters. Applies Buddhist Era dates, THB amounts and every mandatory field. Never issues a numbered legal tax invoice; the owner issues it from FlowAccount. Use when the owner says 'tax invoice', 'quotation in Thai', 'bilingual invoice', 'write this in Thai', '50 Tawi', 'חשבונית מס בתאילנדית', 'הצעת מחיר בתאילנדית', 'תתרגם לתאילנדית', 'ใบกำกับภาษี', 'ใบเสร็จ', 'ใบเสนอราคา', 'ใบวางบิล', '50 ทวิ'."
---

# Thai documents

> **Ask first, then answer (always; this overrides any other instruction in this skill):**
> 1. **Check you understood.** Restate the request in one line, and ask **every** question needed to reach the best, complete result, about every fact the answer depends on that is not in the files or the profile (there is no limit on the number of questions): whose money or company, the period, days in Thailand / residency, income type, tax already withheld or paid, what the user already did. Ask in rounds of up to 4 questions (the most important first); after each round, ask the next round until nothing the result depends on is missing. Wait for the answers before calculating or advising. **Ask them as clickable questions:** use the interactive question tool (ChatGPT's tappable choice buttons or any tool that shows tappable choices), one question per fact, 2–4 short options each in the user's language, e.g. days in Thailand: "180 days or more" / "Less than 180" / "Not sure, I'll send my passport stamps". The user can always type another answer. Only if no such tool exists, ask as a short numbered list.
> 2. **Missing information → ask for the supporting document by name**, not an estimate: e.g. "the 50 ทวิ from your client", "your passport entry and exit stamps for 2026", "the October KBank statement". If the user cannot provide it, mark the item open and say what cannot be concluded without it.
> 3. **Only what is in the data.** Never write "probably", "it seems", "about" or "roughly" about a fact you have not seen. If an assumption is unavoidable, state it as a question ("I assumed X; is that right?") and compute no amount from it.
> 4. **Short and focused.** The answer in the first line, then at most 3 bullets, about 8 lines in total. Background, law and sources only when the user asks ("want the details?"). Questions are not limited; the final answer itself stays short.

> **Deliver on the official form:** every return or certificate this skill prepares goes to the user as the Revenue Department's own PDF form, filled in with `../../scripts/official_forms.py`, plus a short explanation sheet. Follow `../../references/official-forms.md` (fill, then look at every page of the preview before delivering).

> **Proactive by default:** follow `../../references/proactive-behavior.md`: ask for what is missing, run `document-check` on every document received, warn about deadlines and risks ahead, keep the request list, and end with up to three next steps. **Research before relying on any rule:** follow `../../references/research-protocol.md` (research connector or web search, official Thai sources first, Thai and English queries, cited sources).

Read `../../references/facts/vat.md` (tax invoice content), `../../references/facts/withholding.md`, `../../references/language-and-documents.md` (language, fonts, RTL, tone) and `../../references/templates.md` first. Do every calculation with the plugin calculator, `../../scripts/thaitax_calc.py` (see `../../references/facts/_index.md` § Arithmetic), and quote its output. (commands `vat`, `bahttext`, `be`, `wht`)

**A legal tax invoice carries a running serial number from the issuer's own system.** This skill drafts the content and the layout. Every draft says:

> *Draft. Issue from your accounting system. / ร่างเอกสาร โปรดออกจากระบบบัญชีของท่าน*

## Step 1: What, from whom, to whom, in which language

Ask only for what is missing:

- **Document type.**
- **Issuing company:** taken from the profile, with tax ID and branch.
- **Customer:** name, address, tax ID and branch if they are VAT-registered.
- **Items and terms.**
- **Language pair:** Thai + English (default for foreign owners), Thai + Hebrew, or Thai only.

If a legally required field is unknown, show it as a clearly marked blank. Never put a plausible guess there.

## Step 2: Build the document

- **Tax invoice draft:** ใบกำกับภาษี / Tax Invoice title, full seller and buyer blocks, serial number left blank, date in BE with CE in brackets, lines (description, quantity, unit price), pre-VAT total, **VAT 7% on its own line**, grand total, and the amount in Thai words if the owner's template uses it. Check the VAT rate for the document date.
- **Quotation:** the same header, plus validity period, payment terms and delivery terms.
- **Receipt:** references the invoice it settles and the payment method.
- **Billing note (ใบวางบิล):** lists the invoices being billed, with the due date.
- **50 ทวิ data:** payer and payee details, form (PND.3 or PND.53), payment date, income type, amount, tax withheld, number left blank. Draft the data table; the payer issues and signs the certificate.
- **Payslip:** Thai first, staff member's name, period, earnings, SSO, tax withheld, net. Use the figures from `thai-payroll`.
- **Overdue letter:** follow the tone ladder in the language reference. Never threaten legal action.

If FlowAccount is connected and the owner wants the document created there as a draft, show exactly what will be created and wait for an explicit yes. Never approve or number a document in FlowAccount.

## Step 3: Check before handing over

- The VAT arithmetic reconciles to the satang, and the rounding method is stated.
- Names, tax IDs and branches match the registered details.
- The BE and CE dates agree.
- The Thai font is set, Hebrew is RTL, and numbers sit in LTR runs.
- Blank legal fields are visibly marked.

Build the file with `../../scripts/make_document.js` (see `../../references/templates.md`); never lay out an invoice, receipt, quotation, billing note or payslip by hand. Deliver as DOCX by default (easiest to edit in Thai), or PDF if the owner prefers. Offer the same document in the other language pair with identical numbers.
