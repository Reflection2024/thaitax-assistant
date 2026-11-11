# ThaiTax Assistant

**Every Thai tax report, ready for your accountant.** Personal or company: ThaiTax Assistant gathers your numbers, prepares your monthly and annual reports, and hands your accountant a clean file. You just approve. English, עברית, ไทย. Free.

**Website:** https://reflection2024.github.io/thaitax-assistant/

## Install

**Claude Code**
```
/plugin marketplace add Reflection2024/thaitax-assistant
/plugin install thaitax-assistant@thaitax-assistant
```

**Claude desktop app:** download [`thaitax-assistant.plugin`](https://reflection2024.github.io/thaitax-assistant/thaitax-assistant.plugin), drag it into a Claude chat, and press **Install**.

Then say **"Get started"**.

## What's inside

Every return comes back **on the official Revenue Department form**, filled in and ready to send to your accountant, with a short explanation sheet.


| Skill | For | Say |
|---|---|---|
| thaitax-start | Everyone | "Get started" |
| thai-personal-tax | Individuals: annual PND.90/91 and PND.94, line by line, with an e-Filing walkthrough | "Fill in my annual tax return" |
| foreign-income | Individuals: income from abroad, 180-day residency, remittance ledger, treaty credit | "I have income from abroad" |
| thai-monthly-tax | Companies: PP.30, PP.36, PND.3/53/54, SSO, PND.50/51 | "What's due this month?" |
| thai-documents | Both: bilingual tax-invoice drafts, quotations, 50 ทวิ, payslips | "Draft a tax invoice in Thai" |
| cash-and-collections | Both: FlowAccount, Stripe, Omise, cash outlook, reminders | "Who owes me money?" |
| thai-payroll | Employers: salary, overtime, SSO, PND.1, work permits | "Prepare payroll" |
| receipt-capture | Both: receipt photos from the phone gallery → expense list with VAT checks | (share photos) "Add these receipts" |
| ask-thai-tax | Both: any tax question answered from current official Thai sources, with links | "Do I need to…?" |
| accountant-check | Companies: second pair of eyes on your accountant: every filing made, on time, figures match, payments reached the Revenue Department | "Check my accountant's work" |
| what-do-you-need | Both: asks for exactly the documents still missing, tracks them, reminds you | "What do you need from me?" |
| document-check | Both: checks any document or journal for errors and says what to fix | "Check this document" |
| official-letter | Everyone: a Thai letter from any authority explained, deadline, reply drafted | (photo the letter) |
| year-end-planning | Individuals: tax you can still save before 31 December, in baht | "How can I save tax before year end?" |
| property-tax | Owners: land and building tax, sale costs, lease registration | "What will it cost to sell my villa?" |
| company-housekeeping | Companies: AGM, DBD filings, บอจ.5, 14-day changes, licences, all in the calendar | "What does my company need to do this year?" |
| visa-reminders | Everyone: 90-day reports, extensions, work permits, TM30 (reminders only) | "Remind me of my visa dates" |
| contracts-and-payments | Companies: suppliers & contracts register, right withholding before every payment, 50 ทวิ, monthly check | "I need to pay a supplier" |
| family-budget | Families: bank statements → a dashboard of money in vs. out, where it goes, subscriptions and fixed payments; optional Actual Budget export | "Where does our money go?" |
| monthly-pack | Both: the whole month in one go, optional automatic run on the 1st | "Run the month" |
| thai-export-reader | Both: PEAK / Express / gateway / bank files | (upload a file) |

Feedback and bug reports: [open an issue](https://github.com/Reflection2024/thaitax-assistant/issues/new/choose). Pilot kit for testers: [`pilot/`](pilot/).

Full documentation: [`plugins/thaitax-assistant/README.md`](plugins/thaitax-assistant/README.md).

> Prepared for review by your Thai accountant. Not tax or legal advice. Nothing is filed without your explicit yes.

© Reflection Thailand
