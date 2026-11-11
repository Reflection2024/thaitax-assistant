---
name: year-end-planning
description: "Before 31 December, shows an individual how much personal tax they can legally save this year with the allowances still open to them (Thai life and health insurance, RMF, SSF, Thai ESG, provident fund, e-Donation, mortgage interest, parents' and children's allowances, and any temporary allowance for the year), computing the tax with and without each option so they see the real saving in baht, plus what to collect before year end. For companies: a short year-end checklist (stock count, bad debts, accruals, director fees, dividends) for the accountant. Facts and numbers only; the user decides. Use in October to December, or when the user says 'year-end tax planning', 'how can I pay less tax this year', 'RMF', 'Thai ESG', 'deductions before year end', 'תכנון מס לסוף השנה', 'איך לחסוך במס', 'ลดหย่อนภาษีปลายปี'."
---

# Year-end planning

> **Ask first, then answer (always; this overrides any other instruction in this skill):**
> 1. **Check you understood.** Restate the request in one line, and ask up to 3 short questions about every fact the answer depends on that is not in the files or the profile: whose money or company, the period, days in Thailand / residency, income type, tax already withheld or paid, what the user already did. Wait for the answers before calculating or advising.
> 2. **Missing information → ask for the supporting document by name**, not an estimate: e.g. "the 50 ทวิ from your client", "your passport entry and exit stamps for 2026", "the October KBank statement". If the user cannot provide it, mark the item open and say what cannot be concluded without it.
> 3. **Only what is in the data.** Never write "probably", "it seems", "about" or "roughly" about a fact you have not seen. If an assumption is unavoidable, state it as a question ("I assumed X; is that right?") and compute no amount from it.
> 4. **Short and focused.** The answer in the first line, then at most 3 bullets, about 8 lines in total. Background, law and sources only when the user asks ("want the details?"). Each message needs one action from the user at most (a set of up to 3 short questions counts as one).

> **Proactive by default:** follow `../../references/proactive-behavior.md`. **Research before relying on any rule:** follow `../../references/research-protocol.md`. Allowances change every year, so verify **this year's** list and caps first, including any temporary allowance (shopping or tourism schemes).

Read `../../references/pnd90-annual-return.md` §4 (allowances) and `../../references/facts/individuals.md`.

## Individuals

1. **Estimate this year so far.** Gather income to date plus the expected rest of the year (from `thai-personal-tax` data, payslips, foreign remittances via `foreign-income`). Run `../../scripts/thaitax_calc.py pit` for the **baseline**. If the person is unlikely to be tax resident (under 180 days), stop: foreign income is not taxed, so most planning does not apply. Say so.
2. **Allowances already used**, and the room left in each: life and health insurance, the retirement group (RMF, SSF, PVD, pension insurance, combined THB 500k), Thai ESG, mortgage interest, donations.
3. **Options:** for each open allowance that fits the person (Thai provider required, lock-up periods), run `pit` again with it applied and show:

   | Option | Put in | Tax saved | Cash locked until | Notes |
   |---|---|---|---|---|

   Rank by tax saved per baht. Mention the lock-up and the risk in plain words.
4. **Collect before 31 Dec:** certificates and receipts to request, and e-Donation through the RD system (double deduction for qualifying donations).
5. **Facts, not advice:** "These are the options and their effect. Whether to invest is your choice; for investment advice, speak to a licensed adviser."

## Companies (short)

A checklist for the accountant, before year end:

- stock count;
- write-off of bad debts (the conditions are strict);
- accrued expenses and invoices;
- director remuneration resolutions;
- assets to depreciate;
- donations;
- the SME-rate thresholds;
- withholding on year-end payments;
- planning the dividend and its timing.

Prepare questions, not decisions.

## Reminders

Offer, once, a calendar reminder around 1 December ("Last month to use your tax allowances"), and on 20 December for documents.
