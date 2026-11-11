---
name: accountant-check
description: "A second pair of eyes on the work of the user's accountant: checks that every required filing (PP.30, PP.36, PND.1/3/53/54, SSO, PND.50/51, DBD financial statements, audit) was actually submitted, on time, with Revenue Department and SSO receipts; that the filed figures match the books, invoices, payroll and bank statements; that tax money given to the accountant actually reached the Revenue Department; that penalties and surcharges are explained; that the owner holds their own e-Filing and DBD access; and that the financial statements and fees make sense. Produces a scorecard and polite, factual questions for the accountant in Thai or English. Use when the user says 'check my accountant', 'did my accountant file everything', 'audit my accountant', 'are my taxes really paid', 'בקרה על רואה החשבון', 'תבדוק את רואה החשבון', 'האם המסים באמת שולמו', 'ตรวจงานนักบัญชี', 'ยื่นภาษีครบไหม', or quarterly from monthly-pack."
---

# Accountant check

> **Proactive by default:** follow `../../references/proactive-behavior.md`. **Research before relying on any rule:** follow `../../references/research-protocol.md`.

Read first:

- `../../references/facts/_index.md`, `vat.md`, `withholding.md`, `payroll.md`, `corporate.md`, `calendar.md`;
- `../../references/connectors-and-safety.md`.

Use `../../scripts/thaitax_calc.py` for deadlines and arithmetic.

**Tone:** this is a check, not an accusation. Most findings have an innocent explanation (a timing difference, a filing made under another reference, a correction already planned). Report facts, never motives. Every question to the accountant is polite and specific, and offers the chance to explain.

## Step 1: Scope

Choose the entity (one per run) and the period: by default the last 12 months, or the last quarter when called from `monthly-pack`. Ask who the accountant is (firm name; never collect their credentials) and what the agreement covers: bookkeeping, monthly filings, payroll, annual statements, audit coordination, paying taxes on the owner's behalf.

## Step 2: Ask for the evidence

Ask in batches, and say where the owner can download each item themselves:

1. **Revenue Department filing history and receipts.** The owner logs in to RD e-Filing with **their own** account and downloads the list of filed returns and the receipts (ใบเสร็จรับเงิน / ใบยืนยันการยื่นแบบ) for PP.30, PP.36, PND.1/3/53/54, PND.50/51. If the owner has no login of their own, that is finding #1 (Step 3.6).
2. **SSO:** contribution receipts (SPS 1-10) for each month, or the employer e-service history.
3. **DBD:** the company's filing history from DBD e-Filing or DataWarehouse (financial statements, the shareholder list บอจ.5), plus the audited statements and auditor's report.
4. **Bank statements** for the period: the debits for tax payments, and any transfers to the accountant.
5. **The books:** the sales and purchase tax reports, payroll, trial balance or general ledger (FlowAccount if connected).
6. **Accountant's invoices** and the service agreement.

Run `document-check` on every item received.

## Step 3: Check

1. **Completeness:** build the expected filing calendar for the period from the profile (VAT-registered? staff? foreign services? withholding payments?). For each month, match each required return to a receipt. PP.30 is due **every** month, including nil months. Missing receipt → `missing`.
2. **On time:** compare the filing date with the deadline (`deadlines`). Late → note the surcharge (1.5% per month on tax) and the penalty, and whether the owner was charged for it.
3. **Figures match:**
   - PP.30 output and input VAT against the sales and purchase registers or FlowAccount;
   - PND.3/53/54 totals against withholdable payments in the books;
   - SSO against payroll (`sso`);
   - PND.1 against payslips;
   - PND.50 profit against the audited statements;
   - PP.36 against foreign service payments.

   Tolerance: 1 THB per line. Differences are listed with both figures.
4. **Money reached the Revenue Department.** For each tax payment, the amount on the RD receipt must equal a debit on the company's bank statement, or the owner's transfer to the accountant for that purpose. Money sent to the accountant **without a matching RD receipt** is the most serious finding. Report it factually: "Transfer of THB X on <date>, no matching Revenue Department receipt found yet."
5. **50 ทวิ issued:** for each withholding filed, a certificate should have gone to the payee. Spot-check.
6. **Access and control:**
   - The owner has their own RD e-Filing and DBD logins, and receives RD and SSO notices.
   - Bank and accounting-software admin rights are with the owner, with the accountant as a user.
   - The original documents are returned or kept accessible.
7. **Annual statements** (if in scope):
   - audit report signed by a licensed auditor (check the CPA number format);
   - statements filed with DBD within the deadline;
   - red flags to explain: very large "cash on hand", growing director or shareholder loans, unexplained "other receivables", inventory on a services company, losses year after year with tax paid anyway.
8. **Fees and scope:** invoices against the agreement; services billed but not delivered (for example "audit coordination" with no audit filed).

## Step 4: Report

**Scorecard**, in the owner's language:

| Area | Status | Detail |
|---|---|---|
| Filings complete | ✅ / ⚠️ / ❌ | n of N months with receipts |
| On time | | late filings, surcharges |
| Figures match books | | differences |
| Payments reached RD | | unmatched transfers |
| Access and control | | |
| Annual statements | | |
| Fees vs. scope | | |

Then:

1. **Questions for your accountant:** polite and numbered, in Thai (with English) or English. Each one cites the document and the period, and asks for the receipt or an explanation. Example (Thai first): "รบกวนขอสำเนาใบเสร็จการยื่นแบบ ภ.พ.30 เดือนสิงหาคม 2569 ด้วยครับ ไม่พบในประวัติการยื่นแบบออนไลน์ ขอบคุณครับ"
2. **What you can do yourself today:** set up your own e-Filing login, request read access, keep a copy of every receipt.
3. **When to escalate:** an unmatched tax payment, or a missing filing confirmed after the accountant replies. Suggest asking a second accountant or a lawyer to review. Never advise confronting anyone or making allegations.
4. **Disclaimer.** This check compares documents. It is not an audit, and it does not judge anyone's conduct.

## Step 5: Follow up

- Add each open question to the request list. Offer a calendar reminder 7 days later.
- On a yes, send the questions as an email draft for the owner to review. Never send them directly.
- Offer to repeat the check every quarter (`monthly-pack` runs it in January, April, July and October).
