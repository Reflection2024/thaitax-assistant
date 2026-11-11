---
name: what-do-you-need
description: "Tells the user exactly which documents and answers ThaiTax Assistant still needs from them, per company or person and per month, based on their profile and what has already arrived: bank statements, sales and purchase invoices, receipts, 50 ทวิ, payroll data, foreign transfers, allowance proofs. Keeps the request list up to date, drafts requests to third parties (suppliers, customers, payers), and offers calendar reminders. Use at the start of a month, when the user asks 'what do you need from me', 'what's missing', 'what should I send', 'מה אתה צריך ממני', 'מה חסר', 'מה לשלוח', 'ต้องส่งอะไรบ้าง', 'ขาดเอกสารอะไร', or whenever open requests exist."
---

# What do you need from me

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
