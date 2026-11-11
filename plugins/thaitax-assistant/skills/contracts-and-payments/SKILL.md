---
name: contracts-and-payments
description: "Keeps a Thai company's suppliers and contracts in order: a register that links every expense to its contract and its tax invoice, flags payments with no contract, amounts that differ from the contract, missing tax invoices and contracts about to end, and makes sure withholding tax is taken at the right rate for each type of service (3% services, 5% rent, 2% advertising, 1% transport...) on the right form (PND.3, 53, 54), with the 50 ทวิ certificate drafted on the official form. Runs before every supplier payment, when a new contract is signed, and in the monthly check. Use when the user says 'pay a supplier', 'how much do I transfer', 'new contract', 'withholding', 'which rate', 'contracts register', 'match invoices to contracts', 'תשלום לספק', 'כמה לנכות', 'ניכוי במקור', 'חוזה חדש', 'טבלת חוזים', 'ภาษีหัก ณ ที่จ่าย', 'สัญญา', 'จ่ายเงินผู้ขาย'."
---

# Contracts and payments

> **Ask first, then answer (always; this overrides any other instruction in this skill):**
> 1. **Check you understood.** Restate the request in one line, and ask **every** question needed to reach the best, complete result, about every fact the answer depends on that is not in the files or the profile (there is no limit on the number of questions): who the supplier is (individual, company, foreign), what the service is, the contract, the amount before VAT, whether the company uses e-WHT. Ask in rounds of up to 4 questions (the most important first); after each round, ask the next round until nothing the result depends on is missing. Wait for the answers before calculating or advising. **Ask them as clickable questions:** use the interactive question tool (AskUserQuestion, ask_user_input or any tool that shows tappable choices), one question per fact, 2–4 short options each in the user's language. The user can always type another answer. Only if no such tool exists, ask as a short numbered list.
> 2. **Missing information → ask for the supporting document by name**, not an estimate: "the signed contract with Clean Service Co.", "their tax invoice for October", "their company certificate or ID card copy". If the user cannot provide it, mark the item open and say what cannot be concluded without it.
> 3. **Only what is in the data.** Never write "probably", "it seems", "about" or "roughly" about a fact you have not seen. If an assumption is unavoidable, state it as a question and compute no amount from it.
> 4. **Short and focused.** The answer in the first line, then at most 3 bullets, about 8 lines in total. Details only when asked. Questions are not limited; the final answer itself stays short.

> **Deliver on the official form:** the 50 ทวิ certificate and the PND.3 / PND.53 lists go out on the Revenue Department's own forms, filled with `../../scripts/official_forms.py` (forms `WHT_CERT`, `PND3_ATTACH`, `PND53_ATTACH`). Follow `../../references/official-forms.md`.

> **Proactive by default:** follow `../../references/proactive-behavior.md`. Read `../../references/facts/withholding.md` first. All withholding arithmetic comes from `../../scripts/thaitax_calc.py wht` or `../../scripts/contracts.py`, never from memory.

## The register

Keep one **Suppliers & contracts** table per company, in the company's own drive (Google Drive or OneDrive when connected; otherwise a Sheets artifact or an .xlsx the user keeps). Create it on a yes. Two sheets:

- **Contracts:** contract_id, supplier, tax ID and branch, legal form (individual / company / foreign), service type, withholding rate and form, VAT-registered (yes/no), amount before VAT and schedule, start, end, link to the signed contract file.
- **Payments:** date, supplier, amount paid, invoice number, invoice amount before VAT, VAT, withholding taken, 50 ทวิ number, contract_id, status.

Export both as CSV with the column names in `../../scripts/contracts.py` to run the checks.

## 1. Before every payment to a supplier

When the user uploads an invoice, asks "how much do I transfer", or a payment is about to go out:

1. Find the contract in the register. None on file → ask for it (or confirm there is none, for a one-off purchase) and add the supplier.
2. Check the invoice against the contract: amount, period, supplier name and tax ID, full tax invoice if the supplier is VAT-registered (`document-check`).
3. Withholding: `python3 -I ../../scripts/thaitax_calc.py wht '{"amount_before_vat": 25000, "kind": "services"}'` (add `"e_wht": true` only if the company pays through e-WHT). Applies to payments of 1,000 baht or more. No withholding on goods, water, electricity or public transport. Foreign supplier → PND.54: research the rate and the treaty before paying (`ask-thai-tax`).
4. Answer in three lines: **transfer this amount** (invoice total minus withholding), withhold X (rate, form), due date of the form (7th, or 15th online).
5. Draft the 50 ทวิ on the official form (`WHT_CERT`) for the supplier, and add the payment to this month's PND.3 or PND.53 list.
6. Record the payment in the register.

## 2. When a new contract is signed

From the contract (photo, PDF, or the user's description):

- Record it in the register: parties, legal form, service type, amount, schedule, term.
- Say in one line what withholding applies to every payment under it, on which form, and whether the price is stated before or including VAT. If the contract is silent on VAT or withholding, point it out and suggest the standard wording ("price excludes VAT; the client withholds tax as required by law") for the user to agree with the supplier.
- Offer a calendar reminder 30 days before the contract ends.

## 3. Monthly check (also from `monthly-pack`)

Export the month's supplier payments (bank statement, FlowAccount, or the register), then:

```
python3 -I ../../scripts/contracts.py check contracts.csv payments.csv --as-of <last day of month>
```

Report only what needs action, most money first: withholding not taken (with the amount the company now owes itself), payments with no contract or no invoice, amounts that differ from the contract, missing 50 ทวิ, contracts ending within 30 days. Everything in order → say so in one line.

## Safety

Never send money, issue a numbered certificate in the RD system, or sign anything. Supplier tax IDs and bank details stay in the company's files; do not repeat them in the chat beyond what the task needs.
