---
name: thai-personal-tax
description: "Prepares an individual's annual Thai income tax return (PND.90 or PND.91) line by line, and the half-year PND.94: freelance, consulting, rental, dividend, salary and foreign income sorted into the Section 40 categories, standard versus actual expense deductions, every allowance, the 0.5% minimum-tax test, Thai withholding credits from 50 ทวิ, the Income Declaration for Foreign-Sourced Income, and the Foreign Tax Credit. Produces a filled-in worksheet that mirrors the form and an e-Filing walkthrough for the person or their accountant. Prepares; never files. Use when the owner says 'annual tax return', 'PND.90', 'PND.91', 'PND.94', 'personal tax', 'freelancer tax Thailand', 'rental income tax', 'fill in my tax return', 'דוח שנתי', 'מס אישי בתאילנד', 'למלא את הדוח', 'ภ.ง.ด.90', 'ภ.ง.ด.91', 'ภ.ง.ด.94', 'ยื่นภาษี'."
---

# Thai personal tax: annual return (PND.90 / 91) and half-year (PND.94)

> **Ask first, then answer (always; this overrides any other instruction in this skill):**
> 1. **Check you understood.** Restate the request in one line, and ask **every** question needed to reach the best, complete result, about every fact the answer depends on that is not in the files or the profile (there is no limit on the number of questions): whose money or company, the period, days in Thailand / residency, income type, tax already withheld or paid, what the user already did. Ask in rounds of up to 4 questions (the most important first); after each round, ask the next round until nothing the result depends on is missing. Wait for the answers before calculating or advising. **Ask them as clickable questions:** use the interactive question tool (AskUserQuestion, ask_user_input or any tool that shows tappable choices), one question per fact, 2–4 short options each in the user's language, e.g. days in Thailand: "180 days or more" / "Less than 180" / "Not sure, I'll send my passport stamps". The user can always type another answer. Only if no such tool exists, ask as a short numbered list.
> 2. **Missing information → ask for the supporting document by name**, not an estimate: e.g. "the 50 ทวิ from your client", "your passport entry and exit stamps for 2026", "the October KBank statement". If the user cannot provide it, mark the item open and say what cannot be concluded without it.
> 3. **Only what is in the data.** Never write "probably", "it seems", "about" or "roughly" about a fact you have not seen. If an assumption is unavoidable, state it as a question ("I assumed X; is that right?") and compute no amount from it.
> 4. **Short and focused.** The answer in the first line, then at most 3 bullets, about 8 lines in total. Background, law and sources only when the user asks ("want the details?"). Questions are not limited; the final answer itself stays short.

> **Deliver on the official form:** every return or certificate this skill prepares goes to the user as the Revenue Department's own PDF form, filled in with `../../scripts/official_forms.py`, plus a short explanation sheet. Follow `../../references/official-forms.md` (fill, then look at every page of the preview before delivering).

> **Proactive by default:** follow `../../references/proactive-behavior.md`: ask for what is missing, run `document-check` on every document received, warn about deadlines and risks ahead, keep the request list, and end with up to three next steps. **Research before relying on any rule:** follow `../../references/research-protocol.md` (research connector or web search, official Thai sources first, Thai and English queries, cited sources).

Read first:

- `../../references/pnd90-annual-return.md`, the line-by-line guide. **It is the backbone of this skill.**
- `../../references/facts/individuals.md` and `../../references/facts/calendar.md`
- the calculator `../../scripts/thaitax_calc.py`: run `pit` for the whole computation (expenses, allowances, donations, progressive and 0.5% minimum tax, credits, foreign tax credit) and quote its output; never compute the tax in prose
- `../../references/connectors-and-safety.md`

The person is one taxpayer. Never mix their figures with a company's, even one they own.

## Step 0: Scope and verification

1. Identify the person (name, 13-digit Thai tax ID or "not yet registered") and the tax year. If they are married, ask about the spouse's income and whether they would file jointly or separately.
2. If the person has any income from abroad, or brings money into Thailand, **run `foreign-income` first**. It returns residency, the remittance ledger, and the foreign tax paid.
3. With web search, verify for **this** tax year on rd.go.th and recent professional notes: tax bands, every allowance amount (especially the temporary ones), filing deadlines, the social security deduction cap, the Foreign Tax Credit tool, and the current foreign-income declaration form. Write "verified <date>, <sources>".

## Step 1: Collect

Work through the checklist in section 7 of the guide. Ask for the documents in batches, in the person's language. Sources:

- Thai: 50 ทวิ from every payer, FlowAccount (if the person invoices through it), Stripe or Omise payouts, Thai bank statements, leases.
- Foreign: from `foreign-income`.
- Allowances: certificates and receipts. **Ask; never assume** a spouse, a child or an insurance policy.

Missing items stay missing and go on the list. Never zero them.

If a payer withheld tax but no 50 ทวิ has arrived, draft a polite request in Thai through `thai-documents`. Send it only on a yes.

## Step 2: Classify income into Section 40 items

For each income line, assign the PND.90 item (No. 1–8) using the table in the guide. For each line show:

- source (Thai or the foreign country) and payer;
- gross amount in THB, with the FX method for foreign items;
- Thai tax withheld;
- the expense method: standard rate, or actual (only if the person has documents).

**Ambiguous classifications** (for example consulting fees as 40(2), 40(6) or 40(8), or furnished villa rent as 40(5) or 40(8)): compute each option side by side and mark the decision for the accountant. Never pick silently.

## Step 3: Compute (mirror the form)

Build the computation in the order of the form's No. 11:

1. income after expenses → minus allowances → minus double-rate donations → minus general donations → **net income**;
2. **progressive tax**, and separately the **0.5% minimum-tax test** on non-employment income before expenses (THB 120k income and THB 5k tax thresholds). Tax payable = the higher of the two;
3. **credits:** Thai withholding (sum of the 50 ทวิ), PND.94 or PND.93 already paid, the Thai dividend credit if the person elects it, and the **Foreign Tax Credit** (RD formula: foreign income brought in ÷ total assessable income before expenses × Thai tax, capped at the foreign tax actually paid; treaty countries only);
4. **result:** payable or refundable. If payable and at least THB 3,000, note the instalment option.

Show every formula. Label the result **an estimate for the accountant's review**.

Where the spouse has income, compute **joint versus separate** and show both outcomes.

## Step 4: PND.94 (half-year), when relevant

If the person had 40(5)–(8) income from January to June (rent, business, freelance outside 40(2)), prepare PND.94 the same way on six months of income: the half-year allowances, due 30 September (online about a week later). The PND.94 tax paid becomes a credit on the annual return.

## Step 5: Deliver

Produce one file in the person's language, with the Thai form labels alongside:

1. **Form-mirror worksheet:** page 1 details, then each PND.90 item No. 1–8 with the amounts and the expense method, the allowances attachment, and the No. 11 computation line by line. Where the person files on e-Filing, these are the numbers to type in, in the same order.
2. **Foreign-Sourced Income Declaration worksheet:** for each line, the Section 40 category, country, tax year earned, and amount brought in (taxpayer / spouse).
3. **Foreign Tax Credit sheet:** country, treaty, foreign tax paid, the RD limit and the credit claimed, with the list of evidence.
4. **Decisions for the accountant:** classifications, joint or separate, actual or standard expenses, mixed foreign accounts.
5. **Missing documents.**
6. **Deadlines** for this year (moved past weekends and holidays), and the payment or refund method (PromptPay or ค.21).
7. **e-Filing walkthrough:** the screens in order (log in with the tax ID → choose PND.90 → income categories → allowances → foreign tax credit → review → submit), with the worksheet numbers for each screen. The person or accountant files; **never log in for them**.
8. **Disclaimer** in three languages.

Deliver it as a spreadsheet (worksheet tabs) plus a one-page summary document. Offer to draft the cover email to the accountant.

Never file, pay, or log in to the Revenue Department system.
