---
name: dashboards
description: "Builds a dashboard page from the user's own files and data, for a person or a company in Thailand: days in Thailand and money from abroad, tax still to save before 31 December, rental income and land tax, this month's taxes and deadlines, cash for the next 90 days and who owes money, payroll and staff with work-permit dates, or the family budget. Numbers come from the matching ThaiTax Assistant skill; the page is drawn by scripts/dashboard.py in the user's language and refreshed whenever asked. Always use this skill when the user asks to see, track or chart anything as a dashboard. Use when the user says 'dashboard', 'show me', 'build me a dashboard', 'chart', 'track', 'overview page', 'דשבורד', 'תבנה לי דשבורד', 'תראה לי', 'לוח בקרה', 'แดชบอร์ด', 'สรุปเป็นภาพ'."
---

# Dashboards

> **Ask first, then answer (always; this overrides any other instruction in this skill):**
> 1. **Check you understood.** Restate the request in one line, and ask **every** question needed to reach the best, complete result, about every fact the answer depends on that is not in the files or the profile (there is no limit on the number of questions): whose money or company, the period, days in Thailand / residency, income type, tax already withheld or paid, what the user already did. Ask in rounds of up to 4 questions (the most important first); after each round, ask the next round until nothing the result depends on is missing. Wait for the answers before calculating or advising. **Ask them as clickable questions:** use the interactive question tool (AskUserQuestion, ask_user_input or any tool that shows tappable choices), one question per fact, 2–4 short options each in the user's language, e.g. days in Thailand: "180 days or more" / "Less than 180" / "Not sure, I'll send my passport stamps". The user can always type another answer. Only if no such tool exists, ask as a short numbered list.
> 2. **Missing information → ask for the supporting document by name**, not an estimate: e.g. "the 50 ทวิ from your client", "your passport entry and exit stamps for 2026", "the October KBank statement". If the user cannot provide it, mark the item open and say what cannot be concluded without it.
> 3. **Only what is in the data.** Never write "probably", "it seems", "about" or "roughly" about a fact you have not seen. If an assumption is unavoidable, state it as a question ("I assumed X; is that right?") and compute no amount from it.
> 4. **Short and focused.** The answer in the first line, then at most 3 bullets, about 8 lines in total. Background, law and sources only when the user asks ("want the details?"). Questions are not limited; the final answer itself stays short.

> **Proactive by default:** follow `../../references/proactive-behavior.md`: ask for what is missing, run `document-check` on every document received, warn about deadlines and risks ahead, keep the request list, and end with up to three next steps. **Research before relying on any rule:** follow `../../references/research-protocol.md` (research connector or web search, official Thai sources first, Thai and English queries, cited sources).

Read `../../references/connectors-and-safety.md` and `../../references/language-and-documents.md` first.

A dashboard is a picture of numbers that another skill already worked out from the user's own files. This skill never invents a figure, never estimates a missing one, and never calculates tax itself.

## Step 1: Which dashboard, for whom

Ask (clickable) which one, for which person or company, and for which period, unless the request already says so.

| Dashboard | Numbers come from | Example spec |
|---|---|---|
| Days in Thailand and money from abroad | `foreign-income` (days, transfer classification) | `assets/dashboards/foreign-income.json` |
| Tax still to save before 31 December | `year-end-planning` + `scripts/thaitax_calc.py` | `assets/dashboards/year-end.json` |
| Rent from a condo or villa, land tax | `property-tax` + `thai-personal-tax` (Section 40(5)) | `assets/dashboards/rental.json` |
| This month's taxes and deadlines | `thai-monthly-tax` / `monthly-pack` | `assets/dashboards/monthly-tax.json` |
| Cash for 90 days, who owes money | `cash-and-collections` | `assets/dashboards/cash.json` |
| Payroll and staff | `thai-payroll` (+ work-permit dates) | `assets/dashboards/payroll.json` |
| Family budget | `family-budget` (`scripts/budget.py` → `scripts/budget_dashboard.py`) | (own renderer) |

Anything else the user asks for ("VAT threshold tracker", "suppliers by month", "my accountant's scorecard") is built the same way from the skill that owns those numbers.

## Step 2: Get the numbers

Run the owning skill's steps on the user's files and connected tools. Everything that skill requires still applies: ask its questions, request missing documents by name, check every document. A value that is not available is shown as "missing", never as zero or a guess.

## Step 3: Write the spec and draw

1. Copy the matching example spec and replace every value with the real ones. Write all labels in the user's language (any language; Hebrew, Arabic, Persian and Urdu draw right to left automatically). Keep Thai form names as they are.
2. Draw: `python3 -I ${CLAUDE_PLUGIN_ROOT}/scripts/dashboard.py spec.json dashboard.html`
   Section types: `bars`, `hbars`, `line`, `ring`, `table`, `list`; headline numbers go in `kpis`, with `tone` good / warn / bad.
3. Put the period and the source in `footer` ("From your October bank statement and FlowAccount, 12 Nov 2026").

## Step 4: Deliver

- Publish the page as a private artifact when an artifact tool is available, so the user can open it any time and share it if they want; otherwise send the HTML file. It opens in any browser and prints to PDF.
- Keep `spec.json` beside it (in the user's folder or Drive) so the next refresh only replaces the numbers.
- End with up to three next steps, for example the missing document that would complete the picture.

## Refresh

When the user says "update the dashboard", rerun Step 2 for the new period, update the spec, redraw, and republish the same page. Offer, once, a monthly refresh as a scheduled task; create it only on a yes.

## Privacy

The page is built in the user's own session from their own files. ThaiTax Assistant keeps no copy and has no server; the page lives in the user's Claude account, folder or Drive.
