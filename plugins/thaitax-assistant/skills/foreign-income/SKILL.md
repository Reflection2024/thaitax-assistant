---
name: foreign-income
description: "Tracks money brought into Thailand from abroad by an individual (foreign salary, remote work for an overseas employer, overseas business or freelance income, foreign rent, dividends, pensions, savings), counts days in Thailand for residency, separates savings from before 2024 from taxable income earned since 2024, flags Thai-source income paid into foreign accounts, lists foreign tax already paid for a treaty credit, flags LTR and DTV visa points, and prepares the foreign-income part of the personal tax file with the proof the accountant will need. Prepares; never files or decides. Use when the owner says 'income from abroad', 'foreign income', 'remittance', 'bringing money into Thailand', 'transfer from overseas', 'am I tax resident', '180 days', 'LTR tax', 'DTV tax', 'הכנסה מחו\"ל', 'העברות לתאילנד', 'תושבות מס', '180 יום', 'เงินได้จากต่างประเทศ', 'นำเงินเข้าประเทศ', 'ผู้มีถิ่นที่อยู่ในประเทศไทย'."
---

# Income from abroad

> **Ask first, then answer (always; this overrides any other instruction in this skill):**
> 1. **Check you understood.** Restate the request in one line, and ask up to 3 short questions about every fact the answer depends on that is not in the files or the profile: whose money or company, the period, days in Thailand / residency, income type, tax already withheld or paid, what the user already did. Wait for the answers before calculating or advising.
> 2. **Missing information → ask for the supporting document by name**, not an estimate: e.g. "the 50 ทวิ from your client", "your passport entry and exit stamps for 2026", "the October KBank statement". If the user cannot provide it, mark the item open and say what cannot be concluded without it.
> 3. **Only what is in the data.** Never write "probably", "it seems", "about" or "roughly" about a fact you have not seen. If an assumption is unavoidable, state it as a question ("I assumed X; is that right?") and compute no amount from it.
> 4. **Short and focused.** The answer in the first line, then at most 3 bullets, about 8 lines in total. Background, law and sources only when the user asks ("want the details?"). Each message needs one action from the user at most (a set of up to 3 short questions counts as one).

> **Proactive by default:** follow `../../references/proactive-behavior.md`: ask for what is missing, run `document-check` on every document received, warn about deadlines and risks ahead, keep the request list, and end with up to three next steps. **Research before relying on any rule:** follow `../../references/research-protocol.md` (research connector or web search, official Thai sources first, Thai and English queries, cited sources).

Read `../../references/facts/individuals.md` (section **Foreign income and remittance**), `../../references/pnd90-annual-return.md` §6 and `../../references/connectors-and-safety.md` first. Do every calculation with the plugin calculator, `../../scripts/thaitax_calc.py` (see `../../references/facts/_index.md` § Arithmetic), and quote its output.

This area changes and the stakes are high. Before every run, verify the current rule with web search against rd.go.th and at least one recent professional source (a Big-Four, HLB or law-firm note). Check in particular:

- whether the draft "remit within the same or following year, tax-free" relief has become law;
- any new Revenue Department form or guidance for foreign-source income;
- the current status of the treaty-credit tool.

Write "verified <date>, <sources>" on the deliverable. Never plan on a draft rule.

## Step 1: Residency for each year

For each tax year in scope, count the days in Thailand from passport stamps, a travel list, or the person's own count. Any part of a day counts.

- **180 days or more in a calendar year:** Thai tax resident for that year.
- **Under 180 days:** non-resident. Foreign income brought in that year is not taxed in Thailand, but Thai-source income still is.

Show a short table of year, days and status. If the days are near 180, say how many days are left this year.

## Step 2: Build the remittance ledger

Collect every transfer into Thailand for the year:

- bank statements of the Thai account(s), Wise or Revolut statements;
- foreign card spending and ATM withdrawals in Thailand. In practice these are treated as bringing money in; flag them as **possible remittance**.
- money paid directly to Thai sellers from abroad (a property purchase, school fees, rent).

For each transfer record: date, amount and currency, THB equivalent at the rate on the source document (or the Bank of Thailand reference rate for that date, stating which), the account it came from, and **what the money was**. Ask the person; never guess.

Then classify each transfer into one bucket:

| Bucket | Typical Thai treatment (verify) |
|---|---|
| **A. Savings or income earned before 1 Jan 2024** | Generally outside the remittance charge under Por.162/2566. Needs proof that the money existed before 2024 (statement balance at 31 Dec 2023). |
| **B. Foreign income earned from 1 Jan 2024, in a year the person was resident** | Assessable in the year it is brought in, at progressive rates. A treaty credit may reduce it. |
| **C. Foreign income earned in a year the person was not resident** | Usually outside the charge. Confirm with the accountant. |
| **D. Income for work done while in Thailand, paid abroad** | Thai-source income, taxable whether or not it is transferred. Also a **work permit** question: flag it to the lawyer. |
| **E. Loans, gifts, return of capital, sale of an asset bought before 2024** | Depends on facts and documents. List it for the accountant with the evidence. Never decide it. |
| **F. Unknown** | Stays unknown until the person explains it. Never put it in A. |

If one foreign account mixes old savings and new income, show the mix. Do not pick an ordering rule on the person's behalf. List it as a question for the accountant.

## Step 3: Foreign tax already paid

For bucket B items, record the country, the tax paid abroad on that income, and the proof. Check whether Thailand has a double-tax treaty with that country (about 61 treaties), and list the treaty article for the accountant.

Compute the indicative credit with the Revenue Department method in `../../references/pnd90-annual-return.md` §6. The RD's Foreign Tax Credit Calculation Tool (manual Nov 2025) does this inside e-Filing.

Evidence the RD expects, in English or Thai:

- the foreign tax return or foreign withholding certificate (or the contract or lease);
- a foreign tax receipt or payment certificate;
- proof of the transfer into Thailand.

Also map every bucket B line to its Section 40 category and the tax year it was earned. This is exactly what the RD's **Income Declaration for Foreign-Sourced Income** form asks for.

## Step 4: Visa points (flag, never apply)

- **LTR visa:** some LTR categories carry an exemption for foreign income brought into Thailand. Record the category and the visa start date, and flag it for the accountant to confirm.
- **DTV and other visas:** no special income-tax treatment is known; the normal rules apply. Verify.
- **US citizens:** remind them that the US taxes worldwide income regardless of what Thailand does. Coordination is for their US preparer.

## Step 5: Deliver

A file for the person and their accountant, in the person's language:

1. **Residency table:** days per year and the resulting status.
2. **Remittance ledger:** every transfer with bucket, THB value and evidence status, plus totals per bucket.
3. **Possibly assessable this year:** the bucket B total, gross, with foreign tax paid beside it. Mark it as an estimate. The final figure belongs to the accountant.
4. **Evidence checklist:** what is still missing (31 Dec 2023 balances, foreign returns, loan agreements, sale documents).
5. **Questions for the accountant:** mixed accounts, bucket E items, LTR status, treaty points.
6. **Disclaimer** in three languages.

Feed the bucket B total into `thai-personal-tax` so the year's estimate includes it.

## Rules

- Never suggest ways to hide, structure or delay transfers to avoid tax. If asked about timing, explain the current rule, note any pending draft as **not law**, and send the planning question to the accountant.
- Keep account numbers and balances inside the deliverable. Never paste them into web searches.
- A company is different: a Thai company is taxed on its worldwide profit. Send company questions to `thai-monthly-tax` and the accountant.
