# Automations the user can switch on

Each automation is a **scheduled task** in the user's own app (Claude: scheduled tasks; ChatGPT: Tasks), created only after the user picks it. Offer only the ones that fit the profile (company, individual, staff, foreign income, property, family). Every run follows the same rules as a chat: it prepares, drafts and reminds; it **never sends, files, pays, deletes or moves money**. Anything that would leave the user's account waits for their yes in the run's message.

Write each task's prompt as a complete standalone instruction in the user's language: who it is for (person or company name from the profile), what to prepare, which ThaiTax Assistant skill to use, and "nothing is sent without my yes". Pick a time outside the hour mark (for example 08:41) in the user's time zone (Asia/Bangkok unless the profile says otherwise).

| # | Automation | For | When | Skill it runs | What the user gets |
|---|---|---|---|---|---|
| 1 | **Deadline reminders** | everyone | 3 days before each filing deadline that applies to them (company: 7th/15th/23rd monthly, PND.50/51; person: PND.90/91, PND.94) | `thai-monthly-tax` / `thai-personal-tax` | "PP.30 due Monday (online 23rd). Ready: yes / missing: 2 tax invoices." Uses `scripts/thaitax_calc.py deadlines` with the year's holidays. |
| 2 | **Monthly pack** | companies, active individuals | 1st of each month | `monthly-pack` | The month's filings with figures, what is missing, who owes money, and a draft email to the accountant. |
| 3 | **Weekly email sweep** | anyone with email connected | Monday morning | `receipt-capture` + `what-do-you-need` | New tax invoices, receipts and 50 ทวิ found in the inbox, checked and filed in the month's folder; a list of what is still missing with draft requests in Thai (not sent). |
| 4 | **Send-your-documents nudge** | everyone | 25th of each month | `what-do-you-need` | One short list: "Before the month closes, send: KBank October statement, 3 receipts." |
| 5 | **Dashboard refresh** | anyone who built a dashboard | 2nd of each month | `dashboard-builder-thai-tax-payroll-cash-budget` | The same dashboards redrawn with the new month, same link. |
| 6 | **Payroll prep** | companies with staff | 3 working days before payday | `thai-payroll` | The run staged for approval, SSO and PND.1 figures, anomalies, work-permit flags. |
| 7 | **Cash and overdue invoices** | companies | Thursday | `cash-and-collections` | Who is overdue, polite reminders drafted in Thai/English (not sent), 30-day cash outlook. |
| 8 | **Supplier payments check** | companies with a contracts register | Before the 7th each month | `contracts-and-payments` | Payments without contract or tax invoice, wrong withholding, missing 50 ทวิ, contracts ending within 30 days. |
| 9 | **Accountant check** | companies | Quarterly (Jan, Apr, Jul, Oct, 10th) | `accountant-check` | Scorecard: everything filed, on time, paid to the Revenue Department; polite questions drafted. |
| 10 | **Visa and permits** | anyone who shared stamps or permits | 30 days before each date | `visa-reminders` | 90-day report, extension, work permit and passport reminders with the document list. |
| 11 | **180-day counter** | people with foreign income | Monthly from June to December | `foreign-income` | Days in Thailand so far and the date they cross 180; transfers to classify. |
| 12 | **Tax-year milestones** | individuals | 1 Oct (year-end saving), 5 Jan (annual return pack), 1 Jul (PND.94 if rental/business income) | `year-end-planning` / `thai-personal-tax` | The saving options in baht before 31 Dec; the annual return worksheet and document list; the half-year return. |
| 13 | **Property dates** | property owners | 1 Mar each year, and when the bill arrives | `property-tax` | Land and building tax due date, whether last year's bill looked right, rent tax set-aside. |
| 14 | **Family budget month** | families using the budget | 3rd of each month | `family-budget` | Last month in one page: in vs out, new subscriptions, price rises. |

## How to offer them

1. Pick the 3 to 5 that fit the profile best and show them as **one multi-select question** (clickable). Add "Show me all" as an option.
2. For each chosen one, say the day and time in one line and create the task. In Claude use the scheduled-task tool; in ChatGPT use Tasks. Calendar reminders (automation 1) can instead be calendar events with a reminder, if the user prefers their calendar.
3. Record in the profile: `- **Automations:** <names and days>`.
4. Changing later: the user can say "stop the email sweep", "move payroll prep to the 23rd", "what runs automatically?". List, change or remove the tasks accordingly; confirm each removal.

## If scheduling is not available

Say so in one line and offer the fallback: calendar events with reminders for dates (1, 4, 10, 12, 13), and "say *monthly pack* on the 1st" for the rest.
