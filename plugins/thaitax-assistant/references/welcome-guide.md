# Welcome guide: what to connect, and how to use ThaiTax Assistant

`thaitax-start` presents this guide to every new user, in their language. Keep it short and friendly: one screen per part. Use plain words, never technical terms.

## Part 1: What ThaiTax Assistant does for you (one paragraph)

It prepares your Thai taxes (personal and company), writes documents in Thai, keeps track of who owes you money, checks payroll, and reads your receipts. You always approve before anything is sent, and your accountant reviews before anything is filed.

## Part 2: What to connect, and why

Show this as a checklist. Every item is optional; the more you connect, the less you type. Each connection is done by **you**, in Claude's settings (**Settings → Connectors**), with your own sign-in. You can disconnect at any time.

| Connect | What it unlocks | Who needs it |
|---|---|---|
| **FlowAccount** (included with this plugin) | Sales, purchases, receivables, tax reports read automatically. Draft documents created on your yes. | Anyone using FlowAccount |
| **Stripe** (included) | Payments, payouts and fees, matched to invoices | Anyone paid by card online |
| **Email** (Gmail or Outlook) | Finds invoices, receipts and 50 ทวิ certificates in your inbox. Drafts reminders and requests for you to send. | Everyone (recommended) |
| **Calendar** (Google Calendar or Outlook) | Adds your Thai tax deadlines (7th, 15th, 23rd, 31 March, 30 September) as reminders, only after you say yes | Everyone (recommended) |
| **Cloud drive** (Google Drive or OneDrive) | Reads statements and documents you keep there. Saves each month's tax pack in one folder. | Optional |
| **Omise / Opn** (on your own computer) | Thai card and PromptPay payments. Set up together with test keys first. | Omise merchants |
| **Research tool** (for example Perplexity, if you use one) | Faster, broader research for your questions, always checked against official Thai sources | Optional |
| **Phone photos** (no connection needed) | Snap a receipt or tax invoice, then share it from your gallery to the Claude app | Everyone |
| **Exports** (no connection needed) | PEAK, Express, 2C2P, KSher, and bank statements as PDF or Excel | Anyone without a connector |

**Sending receipts from your phone:**

1. Open the Claude app and the chat where you use ThaiTax Assistant.
2. Tap **+** → **Photos** and choose one or many receipts. On Android or iPhone you can also open the photo in your gallery, tap **Share** and choose **Claude**.
3. Write "add these expenses", or just send them.
4. You get back a list of each receipt, its amount, its VAT, and whether it is a valid Thai tax invoice your company can claim.

Tip: photograph the whole receipt, flat, in good light. Thai tax invoices must show the company's name and 13-digit tax ID. Ask the shop for "ใบกำกับภาษีเต็มรูป" with your company details.

## Part 3: Things you can say (pick the ones that fit)

**Any time:**
- "What do you need from me?"
- "Check this document." (upload or forward it)
- "I got a letter in Thai." (photo it)
- "How much will it cost to sell my villa?" / "Is my land tax bill right?"
- Any question: "Do I need to…?", "What's the rule for…?" (answered from current official sources, with links)

**If it's just you:**
- "I have income from abroad. Do I need to file?"
- "Fill in my annual tax return."
- "Which companies haven't sent me a 50 ทวิ?"
- "Add these receipts" (with photos)

**Around the year:**
- "How can I save tax before the year ends?" (October to December)
- "Remind me of my 90-day report and visa dates."

**If you have a company:**
- "Check my accountant's work." (were all filings made, on time, and paid?)
- "What's due this month?"
- "Who owes me money? Write the reminders."
- "Draft a tax invoice in Thai and English for …"
- "Prepare payroll for November."
- "Did all my Stripe payouts reach the bank?"
- "Put my tax deadlines in my calendar."
- "What does my company need to do this year?" (AGM, DBD filings, licences)

Speak in English, Hebrew or Thai. You can mix languages.

## Part 4: What it will never do

It will never file a return, pay anyone, send an email, or create a numbered tax invoice without your explicit yes. It never logs in to the Revenue Department, Social Security or your bank. Your accountant reviews everything before it is filed.

## Feedback

If something is wrong or missing, tell us at github.com/Reflection2024/thaitax-assistant/issues. Never include tax IDs, bank details or salaries. When the user reports a wrong number, offer to draft the issue text with all personal data removed.

## Part 5: Monthly rhythm (offer once)

- **On the 1st:** "What's due this month?" (company) or "Any new receipts or transfers?" (individual).
- **Around the 5th:** approve payroll and withholding.
- **By the 15th:** your accountant files. ThaiTax Assistant can remind you through your calendar.
- **January:** "Fill in my annual tax return."
