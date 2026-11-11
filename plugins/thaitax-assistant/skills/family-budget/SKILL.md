---
name: family-budget
description: "Helps a family in Thailand see and manage its money from the bank statements it uploads (Thai banks, Wise, foreign cards, any currency): income versus spending month by month, where the money goes by category, every fixed payment and subscription with its yearly cost, price rises, and services paid for twice. Produces a clear dashboard page in the family's language and remembers their own category corrections. Optional for advanced users: export to Actual Budget. Never moves money, never asks for bank passwords. Use when the user says 'family budget', 'where does our money go', 'household budget', 'subscriptions', 'what are we paying every month', 'budget dashboard', 'תקציב משפחתי', 'לאן הולך הכסף', 'ניהול תקציב', 'מנויים', 'תשלומים קבועים', 'งบประมาณครอบครัว', 'เงินไปไหน', 'ค่าสมาชิกรายเดือน'."
---

# Family budget

> **Ask first, then answer (always; this overrides any other instruction in this skill):**
> 1. **Check you understood.** Restate the request in one line, and ask up to 3 short questions about every fact the answer depends on that is not in the files or the profile: whose money or company, the period, days in Thailand / residency, income type, tax already withheld or paid, what the user already did. Wait for the answers before calculating or advising.
> 2. **Missing information → ask for the supporting document by name**, not an estimate: e.g. "the 50 ทวิ from your client", "your passport entry and exit stamps for 2026", "the October KBank statement". If the user cannot provide it, mark the item open and say what cannot be concluded without it.
> 3. **Only what is in the data.** Never write "probably", "it seems", "about" or "roughly" about a fact you have not seen. If an assumption is unavoidable, state it as a question ("I assumed X; is that right?") and compute no amount from it.
> 4. **Short and focused.** The answer in the first line, then at most 3 bullets, about 8 lines in total. Background, law and sources only when the user asks ("want the details?"). Each message needs one action from the user at most (a set of up to 3 short questions counts as one).

> **Proactive by default:** follow `../../references/proactive-behavior.md`: ask only for what is missing, a few things at a time, and end with up to three next steps. **Light, never heavy:** a family budget is a relief, not homework. Never lecture about spending; show the picture and let the family decide.

Read `../../references/connectors-and-safety.md` first. All arithmetic is done by `../../scripts/budget.py`; never add up transactions in your head. The dashboard is rendered by `../../scripts/budget_dashboard.py`.

## Step 1: Get the statements

Thai banks offer no direct connection that the family can authorise, so ask for **statement uploads**:

- Monthly statements as PDF, CSV or Excel from each account and card the family uses (KBank, SCB, Bangkok Bank, Krungthai, Krungsri, TTB, Wise, Revolut, foreign banks and cards). Three months is a good start; twelve gives a full year.
- How to download: in the bank app, Account → Statement → choose the months → send by email or save as PDF. Say this in one line, in the user's language.
- If a connected cloud drive or email holds statements, offer to look there first.

**Never** ask for a bank password, PIN, OTP or full account number. If a statement shows a full account number, keep only the last four digits as the account label.

## Step 2: Turn statements into one table

Use `thai-export-reader` to read each statement (Thai headers, Buddhist Era dates, TIS-620 encoding, PDF tables). Build one UTF-8 CSV with the columns `date` (YYYY-MM-DD, CE), `description`, `amount` (signed: + money in, − money out), `currency`, `account` (a short label such as "KBank 1234"), and optional `category`.

- Check each statement's opening balance + transactions = closing balance. If it does not match, say which month and account, and ask for the missing page.
- Foreign currency: use the rate shown on the statement, or the Bank of Thailand reference rate for the period, in `fx.json` (`{"EUR": 37.6}`). Say which rate was used. Amounts with no rate are listed separately, never converted silently.
- Transfers between the family's own accounts are not income or spending. If they are not obvious, ask once: "Are KBank 1234 and Wise EUR both yours?"

## Step 3: Categorise and summarise

```
python3 -I ../../scripts/budget.py summarize transactions.csv --fx fx.json --rules rules.json --out summary.json
```

- `rules.json` holds the family's own corrections (`{"Villa Mimosa": "Housing"}`). When the user corrects a category, add the rule, rerun, and say it will be remembered next time. Keep `rules.json` with the family's files.
- Show at most 5 uncategorised payments at a time and ask what they are; "skip" is fine.

## Step 4: The dashboard

```
python3 -I ../../scripts/budget_dashboard.py summary.json dashboard.html --lang he|en|th [--title "The Cohen family"]
```

Publish `dashboard.html` as a private artifact page (or send the file if artifacts are not available). It shows money in, money out, what is left, average monthly spending, fixed payments per month, month by month bars, where the money goes, things worth a look, and the table of fixed payments and subscriptions with yearly cost. Hebrew renders right to left.

In the reply, give **three lines at most**, for example: what was left over, the biggest category, and the one thing worth a look (a duplicate subscription, a price rise). Numbers come from `summary.json`.

## Step 5: Subscriptions and fixed payments

From `recurring` and `possible_duplicate_subscriptions`:

- List each fixed payment with its monthly and yearly cost.
- Flag overlaps (two cloud storage plans, two video services, two AI assistants) and price changes. Phrase it as a question, never as advice to cancel: "You pay for both Google One and iCloud, ฿699 a month together. Do you use both?"
- If the family wants to cancel something, explain where to cancel it. Never cancel anything yourself.

## Step 6: Keep it going (optional)

- Offer a monthly refresh: "Send next month's statements and I will update the dashboard." With a yes, add a monthly calendar reminder or a scheduled task.
- If the family also has foreign income or a Thai company, mention once that the same statements help `foreign-income` and `monthly-pack`.

## Advanced: Actual Budget

For users who want a full budgeting app with envelopes and goals, offer Actual Budget (open source, self-hosted, the family keeps its data):

```
python3 -I ../../scripts/budget.py actual-export transactions.csv --out actual_import.csv --rules rules.json
```

The CSV (Date, Payee, Notes, Category, Amount, Currency, Account) imports into Actual via Account → Import. Users who run their own Actual server can also connect it to Claude with the community `actual-mcp` server; see `CONNECTORS.md`. Only suggest this when the user asks for more than the dashboard.

## Privacy

Statements are among the most private documents a family has. Keep them in this conversation and the family's own files; never send them anywhere, and never put personal data in URLs. The dashboard page is private until the user chooses to share it.
