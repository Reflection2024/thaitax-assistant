---
name: cash-and-collections
description: "Shows a business in Thailand where its cash stands and who owes it money: receivables and payables from FlowAccount, card and online payments and payouts from Stripe and Omise (or exports from 2C2P, GB Prime Pay, KSher), a matching of payments to invoices, a 30/60/90-day cash outlook including upcoming tax and SSO payments, and overdue reminders in Thai, English or Hebrew for the owner to send. Use when the owner asks 'who owes me money', 'cash flow', 'overdue invoices', 'did the payout arrive', 'match payments', 'מי חייב לי', 'תזרים', 'חובות לקוחות', 'ใครค้างชำระ', 'กระแสเงินสด', 'ทวงหนี้'."
---

# Cash and collections

> **Ask first, then answer (always; this overrides any other instruction in this skill):**
> 1. **Check you understood.** Restate the request in one line, and ask up to 3 short questions about every fact the answer depends on that is not in the files or the profile: whose money or company, the period, days in Thailand / residency, income type, tax already withheld or paid, what the user already did. Wait for the answers before calculating or advising. **Ask them as clickable questions:** use the interactive question tool (AskUserQuestion, ask_user_input or any tool that shows tappable choices), one question per fact, 2–4 short options each in the user's language, e.g. days in Thailand: "180 days or more" / "Less than 180" / "Not sure, I'll send my passport stamps". The user can always type another answer. Only if no such tool exists, ask as a short numbered list.
> 2. **Missing information → ask for the supporting document by name**, not an estimate: e.g. "the 50 ทวิ from your client", "your passport entry and exit stamps for 2026", "the October KBank statement". If the user cannot provide it, mark the item open and say what cannot be concluded without it.
> 3. **Only what is in the data.** Never write "probably", "it seems", "about" or "roughly" about a fact you have not seen. If an assumption is unavoidable, state it as a question ("I assumed X; is that right?") and compute no amount from it.
> 4. **Short and focused.** The answer in the first line, then at most 3 bullets, about 8 lines in total. Background, law and sources only when the user asks ("want the details?"). Each message needs one action from the user at most (a set of up to 3 short questions counts as one).

> **Proactive by default:** follow `../../references/proactive-behavior.md`: ask for what is missing, run `document-check` on every document received, warn about deadlines and risks ahead, keep the request list, and end with up to three next steps. **Research before relying on any rule:** follow `../../references/research-protocol.md` (research connector or web search, official Thai sources first, Thai and English queries, cited sources).

Read `../../references/connectors-and-safety.md` and `../../references/language-and-documents.md` first.

Work one company at a time, in THB unless the company's base currency is different.

## Step 1: Gather

- **FlowAccount:** open receivables (invoice, customer, issue date, due date, amount, paid to date), open payables, and the cash and bank balances if exposed.
- **Stripe:** charges, refunds, disputes and payouts for the period, plus the current balance.
- **Omise** (if set up) or **gateway export** (2C2P, GB Prime Pay, KSher and others, read with `thai-export-reader`): transactions, fees and settlements.
- **Bank statement** (optional upload): to confirm payouts actually landed.

Anything not available is listed as unknown, never as zero.

## Step 2: Match

- Match each gateway payment to a FlowAccount invoice or receipt by amount, reference and date. Show three lists:
  - matched;
  - paid but no sales document, which is a VAT risk: a document is needed;
  - invoice marked unpaid but money received.
- Reconcile gateway payouts to bank deposits: gross − fees − refunds = payout. Show fees per gateway for the period.
- Flag disputes or chargebacks with their response deadline.

## Step 3: Outlook

Build a 30/60/90-day view:

- **Money in:** open receivables weighted by each customer's past payment behaviour. Expected gateway payouts.
- **Money out:** open payables, payroll, and **tax and SSO due dates** (PP.30, PND, SSO from `thai-monthly-tax` / `thai-payroll` where known).

Flag any week where the balance falls below the buffer the owner names. If they have not named one, ask once.

## Step 4: Collections

Rank overdue customers by amount × days overdue. For each, draft a reminder:

- in the **customer's** language (Thai by default for Thai customers);
- at the right tone step for how late they are and how they have paid before;
- with the invoice number, the amount, and a payment link (Stripe or Omise) if one exists. Never create a payment link without a yes.

Show all drafts together. **Nothing is sent without an explicit yes, message by message or as an approved batch.** Customers who have been chased three times go to the owner as a decision, not a fourth email.

## Deliver

A one-page summary: cash today, owed to you, you owe, the tight weeks, the top five to chase, and the missing sales documents. Attach a spreadsheet with the detail. Write it in the owner's language.
