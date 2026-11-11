---
name: monthly-pack
description: "Runs the whole month in one go for each company or person in the ThaiTax Assistant profile: deadlines for the month, the tax package (VAT, withholding, SSO), who owes money, receipts and missing tax invoices, payroll status, and for individuals the transfers and personal-tax checkpoints. Ends with one summary and a draft email to the Thai accountant. Built to run automatically on the 1st of each month as a scheduled task, or on demand. Nothing is sent, filed or paid without a yes. Use when the user says 'monthly pack', 'run the month', 'month close', 'prepare everything for my accountant', 'what do I need to do this month', 'חבילה חודשית', 'תכין הכל לרואה החשבון', 'סגירת חודש', 'สรุปประจำเดือน', 'เตรียมเอกสารส่งนักบัญชี'."
---

# Monthly pack

> **Proactive by default:** follow `../../references/proactive-behavior.md`: ask for what is missing, run `document-check` on every document received, warn about deadlines and risks ahead, keep the request list, and end with up to three next steps.

Read `../../references/facts/_index.md` and `../../references/connectors-and-safety.md` first.

## Step 0: Scope

- Read the ThaiTax Assistant profile. If there is none, run `thaitax-start`.
- **Period:** the month that just ended (on the 1st, the previous month).
- Run once **per entity** (each company, and the individual if any). Never blend entities.
- **If running unattended** (a scheduled task, no one watching): prepare everything, ask nothing, and put every question into the "Needs you" list. Never send, file, post or pay.

## Step 1: Deadlines

Run `../../scripts/thaitax_calc.py deadlines` for the period, with this year's Thai public holidays (verify them with web search on the first run of each year). List what is due, and when, for this entity.

## Step 2: Company entities

Run these in order and keep only their summaries:

1. `thai-monthly-tax` for the period: VAT, PP.36, withholding registers, SSO, missing or invalid tax invoices.
2. `cash-and-collections`: cash position, top 5 overdue customers, and reminders drafted (not sent).
3. `receipt-capture` on anything new: receipt photos shared during the month, and invoices or receipts found in the connected inbox for the period.
4. `document-check` on the period's journal or trial balance, if the books are available: debits and credits, VAT and WHT accounts against the returns, unusual entries.
5. `what-do-you-need`: everything still open for the period, with requests drafted.
6. `thai-payroll` status: whether payroll has been run and approved for the period. If it has not, say so and list what is needed. Do not run payroll unattended.

## Step 3: Individuals

1. New transfers into Thailand this month, sorted into buckets (`foreign-income`) and days in Thailand year to date. Warn when the person is within 20 days of 180.
2. 50 ทวิ received this month, and any still missing.
3. **Checkpoints:**
   - September: PND.94 is due on the 30th; prepare it with `thai-personal-tax`.
   - January to March: annual return season; offer `thai-personal-tax`.
   - December: remind the person to collect year-end certificates and allowance documents.

## Step 4: Deliver

One message, in the user's language, with one section per entity:

1. **Due this month:** form, date, estimated amount.
2. **Ready:** what was prepared, with the files attached.
3. **Needs you:** decisions, missing documents, reminders waiting for a yes.
4. **Numbers at a glance:** VAT payable, withholding, SSO, cash today, total owed to you.

Then the actions waiting for a yes (show each one exactly):

- **Draft email to the accountant**, in Thai or English per the profile, with the pack attached. If the mail connector is available, create it as a **draft** only after a yes; never send.
- **Save to the cloud drive** in `<Entity>/<YYYY-MM>/`, on a yes.
- **Customer reminders** drafted in Step 2: send each one only on a yes.

End with the disclaimer.

## Scheduling

When the user asks for it, or accepts the offer in `thaitax-start`, create a **monthly scheduled task** with the session's scheduling tool:

- the 1st of each month, 09:00 Asia/Bangkok;
- prompt: "Run the ThaiTax Assistant monthly-pack skill for all entities in my profile, for the month that just ended. Unattended: prepare only; send, file, post or pay nothing."

If no scheduling tool exists, offer a recurring calendar event instead, titled "Run ThaiTax monthly pack".
