---
name: thai-monthly-tax
description: "Prepares the monthly Thai tax package for one company at a time: VAT return PP.30, reverse-charge PP.36, withholding returns PND.3, PND.53 and PND.54, the social security total, and the half-year PND.51 or annual PND.50 working papers, with the due dates and a list of what is missing. Works from FlowAccount or an uploaded export. Prepared for the owner's Thai accountant; nothing is filed. Use when the owner asks 'what's due this month', 'monthly tax', 'VAT return', 'withholding', 'PP.30', 'PND.53', 'מה צריך להגיש החודש', 'דוחות מס', 'מע\"מ תאילנד', 'ภาษี', 'ภ.พ.30', 'ภ.ง.ด.3', 'ภ.ง.ด.53', 'ภาษีหัก ณ ที่จ่าย'."
---

# Thai monthly tax

Read `../../references/facts/_index.md`, `../../references/facts/vat.md`, `../../references/facts/withholding.md`, `../../references/facts/calendar.md` and `../../references/connectors-and-safety.md` before anything else; add `../../references/facts/corporate.md` only for PND.50/51 and `../../references/facts/payroll.md` for SSO. Do every calculation with the plugin calculator, `../../scripts/thaitax_calc.py` (see `../../references/facts/_index.md` § Arithmetic), and quote its output. (commands `vat`, `vat_check`, `wht`, `deadlines`)

## Step 0: Scope

1. Read the ThaiTax Assistant profile. If there is none, run `thaitax-start` first, or ask for the company name and tax ID.
2. **One company per run.** For "all my companies", repeat the steps for each one and produce one section per company. Never blend totals.
3. Choose the period: by default the last completed month. Use "half-year" or "annual" for PND.51 / PND.50.
4. With web search, verify on rd.go.th the VAT rate for the period, whether the online filing extension is still in force, and any new holiday that moves a deadline. Note the source and date.

## Step 1: Get the data

- **FlowAccount connected:** confirm the selected company matches. Pull for the period: sales tax invoices and receipts, credit and debit notes, purchases and expenses with VAT, withholding recorded on payments made, and payments to foreign providers.
- **Not connected:** ask for the sales tax report (รายงานภาษีขาย), the purchase tax report (รายงานภาษีซื้อ), and the expense and withholding registers, then read them with `thai-export-reader`.
- **Payments from Stripe or Omise:** use them only to cross-check that every payment received has a sales document. Never use them as the VAT base.

If the books for the month are not closed, say so and ask whether to continue on a provisional basis. Mark every page "provisional".

## Step 2: Prepare each return

**PP.30 (VAT).** Output VAT from sales documents and input VAT from purchase tax invoices give the net payable or the amount carried forward. Check every purchase line: supplier tax ID and branch present, buyer name and tax ID exactly the company's, category creditable. List non-creditable lines with the reason. Never drop them silently. Nil months still need a filing.

**PP.36 (reverse charge).** Find payments to foreign providers used in Thailand (ads platforms, cloud, SaaS, foreign consultants). Self-assess 7% and note whether the input credit is claimable.

**PND.3 / PND.53 / PND.54 (withholding).** For each withholdable payment, decide the payee's legal form first (Thai individual → PND.3, Thai company → PND.53, non-resident → PND.54). Then apply the rate from the table to the amount before VAT. Produce one register per form: payee, tax ID, date, income type, amount, rate, tax. Then list payments that look withholdable but have no withholding recorded. The payer carries that liability.

**SSO.** Take the total from `thai-payroll` if it has run this month. Otherwise show it as "pending payroll" with the 15th deadline.

**PND.51 / PND.50 (on request).** Prepare profit before tax from the trial balance, a list of likely adjustments (entertainment caps, non-deductible items, depreciation differences, provisions), the SME-status question, and the statutory dates. Do not compute the final tax due. That belongs to the accountant.

## Step 3: Deliver

Produce one packet per company, in the owner's language, with Thai form names alongside. Deliver it as a document or spreadsheet the owner can forward.

1. **What's due and when:** form, period, paper deadline, online deadline (moved past weekends and holidays), amount.
2. **The numbers:** VAT summary, the withholding registers, the SSO total. Each comes with its source.
3. **Needs a human:** missing or invalid tax invoices, unclear payees, unrecorded withholding, anything unverified.
4. **Disclaimer** in all three languages.

Then offer to draft a short email to the Thai accountant with the packet attached, in Thai or English. Send it only on an explicit yes.

Never file, pay, or log in to the Revenue Department system.
