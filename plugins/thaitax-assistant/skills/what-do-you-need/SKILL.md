---
name: what-do-you-need
description: "Tells the user exactly which documents and answers ThaiTax Assistant still needs from them, per company or person and per month, based on their profile and what has already arrived: bank statements, sales and purchase invoices, receipts, 50 ทวิ, payroll data, foreign transfers, allowance proofs. Keeps the request list up to date, drafts requests to third parties (suppliers, customers, payers), and offers calendar reminders. Use at the start of a month, when the user asks 'what do you need from me', 'what's missing', 'what should I send', 'מה אתה צריך ממני', 'מה חסר', 'מה לשלוח', 'ต้องส่งอะไรบ้าง', 'ขาดเอกสารอะไร', or whenever open requests exist."
---

# What do you need from me

> **Ask first, then answer (always; this overrides any other instruction in this skill):**
> 1. **Check you understood.** Restate the request in one line, and ask up to 3 short questions about every fact the answer depends on that is not in the files or the profile: whose money or company, the period, days in Thailand / residency, income type, tax already withheld or paid, what the user already did. Wait for the answers before calculating or advising. **Ask them as clickable questions:** use the interactive question tool (AskUserQuestion, ask_user_input or any tool that shows tappable choices), one question per fact, 2–4 short options each in the user's language, e.g. days in Thailand: "180 days or more" / "Less than 180" / "Not sure, I'll send my passport stamps". The user can always type another answer. Only if no such tool exists, ask as a short numbered list.
> 2. **Missing information → ask for the supporting document by name**, not an estimate: e.g. "the 50 ทวิ from your client", "your passport entry and exit stamps for 2026", "the October KBank statement". If the user cannot provide it, mark the item open and say what cannot be concluded without it.
> 3. **Only what is in the data.** Never write "probably", "it seems", "about" or "roughly" about a fact you have not seen. If an assumption is unavoidable, state it as a question ("I assumed X; is that right?") and compute no amount from it.
> 4. **Short and focused.** The answer in the first line, then at most 3 bullets, about 8 lines in total. Background, law and sources only when the user asks ("want the details?"). Each message needs one action from the user at most (a set of up to 3 short questions counts as one).

> **Research before relying on any rule:** follow `../../references/research-protocol.md`.

Read `../../references/proactive-behavior.md` and `../../references/intake-checklist.md` first.

## Step 1: Build the list

For each entity in the profile and each open period, list what the month normally needs.

**Company:**

- bank statements for every account;
- sales documents (or the FlowAccount sales report, if connected, which needs nothing from the user);
- purchase tax invoices and receipts;
- payments made to contractors, landlords and foreign providers (for withholding and PP.36);
- 50 ทวิ received from customers;
- payroll changes (new staff, leavers, overtime, leave);
- work-permit renewals.

**Individual:**

- 50 ทวิ from payers;
- foreign transfers into Thailand and what each one was;
- rent received;
- travel dates (days in Thailand);
- allowance proofs (from December to March).

Remove whatever a connected tool already supplies, and whatever already arrived (`[x]` items).

**Bank statements:** Thai banks offer no direct connection yet, so the monthly statement (PDF or Excel from the bank's app or internet banking) is a standing request for every account, every month. Ask for it once per month, together with the other items, and say in one line how to download it: in the bank app, open **Statement / e-Statement / ขอรายการเดินบัญชี**, choose the month, then share the PDF to Claude. Keep a note that a direct bank connection will be added when Thai banks make one available.

## Step 2: Ask

Group the list by how the user sends each item:

- **Upload or photo**
- **Forward the email**
- **Connect the tool once:** suggest this when the same item is requested every month.
- **Someone else must send it:** offer drafted requests in that person's language.

Keep each message to 5 items; continue in the next message if there are more. For every item, say in one line why it is needed.

## Step 3: Track and remind

- Update the document request list.
- Offer a calendar reminder for the date the user names, or the 25th by default. Show the event first and create it only on a yes.
- When documents arrive, run `document-check` on each one and tick the list.
- When everything for a period is `[x]`, say so and offer `monthly-pack`.
