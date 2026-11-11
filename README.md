# ThaiTax Assistant

A Thai back office inside Claude, for foreign individuals and companies in Thailand. Works in English, עברית and ไทย. Free.

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

| Skill | For | Say |
|---|---|---|
| sabai-start | Everyone | "Get started" |
| thai-personal-tax | Individuals: annual PND.90/91 and PND.94, line by line, with an e-Filing walkthrough | "Fill in my annual tax return" |
| foreign-income | Individuals: income from abroad, 180-day residency, remittance ledger, treaty credit | "I have income from abroad" |
| thai-monthly-tax | Companies: PP.30, PP.36, PND.3/53/54, SSO, PND.50/51 | "What's due this month?" |
| thai-documents | Both: bilingual tax-invoice drafts, quotations, 50 ทวิ, payslips | "Draft a tax invoice in Thai" |
| cash-and-collections | Both: FlowAccount, Stripe, Omise, cash outlook, reminders | "Who owes me money?" |
| thai-payroll | Employers: salary, overtime, SSO, PND.1, work permits | "Prepare payroll" |
| receipt-capture | Both: receipt photos from the phone gallery → expense list with VAT checks | (share photos) "Add these receipts" |
| thai-export-reader | Both: PEAK / Express / gateway / bank files | (upload a file) |

Full documentation: [`plugins/thaitax-assistant/README.md`](plugins/thaitax-assistant/README.md).

> Prepared for review by your Thai accountant. Not tax or legal advice. Nothing is filed without your explicit yes.

© Reflection Thailand
