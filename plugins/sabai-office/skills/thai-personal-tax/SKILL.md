---
name: thai-personal-tax
description: "Helps an individual in Thailand (freelancer, consultant, sole trader, landlord renting out a condo or villa, or a salaried expat with side income) keep track of income, collect withholding certificates, see what is due (PND.90 / PND.91 annual, PND.94 half-year), and prepare a personal tax working file for their accountant, with flags for tax residency, foreign income brought into Thailand, and VAT registration. Prepares; never files. Use when the owner says 'personal tax', 'freelancer tax Thailand', 'rental income tax', 'PND.90', 'PND.94', 'tax residency', 'remittance', 'מס אישי בתאילנד', 'פרילנסר', 'הכנסה משכירות', 'ภาษีเงินได้บุคคลธรรมดา', 'ภ.ง.ด.90', 'ภ.ง.ด.94', 'ฟรีแลนซ์'."
---

# Thai personal tax (individuals)

Read `../../references/thai-tax-facts.md` (the individuals section) and `../../references/connectors-and-safety.md` first. The person is one taxpayer: never mix their figures with a company's, even one they own.

## Step 0: Who and which year

From the Sabai Office profile, or by asking once:

- the person's name and 13-digit tax ID (Thai ID or the tax ID issued to a foreigner);
- the tax year (the calendar year);
- the kinds of income: salary, freelance and professional fees, business, rent, dividends and interest, foreign income;
- the days spent in Thailand this year: 180 or more means tax resident;
- visa type, if relevant (some visas, such as LTR, carry special treatment: flag it, never apply it).

With web search, verify on rd.go.th the current bands, the allowances, the expense deductions for each income type, and the PND.90/91/94 deadlines. Note the source and date.

## Step 1: Collect

- **Income records:** FlowAccount if the person invoices through it, Stripe or Omise payouts, bank statements, rental agreements, payslips (50 ทวิ from employers).
- **Withholding certificates (50 ทวิ)** from every company that paid them. Build a register: payer, tax ID, date, income type, amount, tax withheld. List payers with no certificate yet, and draft a polite request in Thai through `thai-documents` (sent only on a yes).
- **Allowances the person states:** spouse, children, parents, insurance, provident or retirement funds, donations, mortgage interest. Ask; never assume.

## Step 2: Prepare

- **Income by type.** Group income into the Revenue Code categories (salary; professional and contractor fees; rent; business; dividends and interest). Show which expense deduction each category allows, as verified in Step 0. Where a category lets the person choose between a flat deduction and actual expenses, show both, and let the person and the accountant choose.
- **Estimate (labelled as an estimate):** net income → tax by band → minus tax already withheld = estimated payable or refund. Only if the person has supplied the allowances. Otherwise show the gross figures and stop.
- **What's due:** PND.90 (several income types) or PND.91 (salary only) by 31 March, about a week later online. PND.94 by 30 September for the first half's non-salary income (such as rent or business). Move dates past weekends and holidays.

## Step 3: Flags (never decide these)

- **Foreign income brought into Thailand** by a resident: taxable when remitted, with limited treaty credit. List the transfers into Thailand the person shows you and hand them to a specialist.
- **VAT:** if VAT-able income from freelance work, rent of commercial space, or business exceeds THB 1.8 million a year, the person must register for VAT. Flag it as the threshold approaches.
- **Rent paid by companies:** the tenant company withholds 5%. Check that a 50 ทวิ exists for every month.
- **Working legally:** a foreigner earning from work in Thailand generally needs a work permit for that work. Flag it to the person's lawyer; never assess it.
- **Changing to a company:** if the person asks whether to incorporate, list the factors (income level, expenses, VAT, foreign-ownership rules) and send the decision to the accountant and lawyer.

## Step 4: Deliver

A one-page summary in the person's language:

- income by type;
- the withholding register and missing certificates;
- the estimate, if one was made;
- what's due and when;
- the flags;
- the trilingual disclaimer.

Attach a spreadsheet with the detail. Offer to draft a cover email to the accountant. Never file, pay, or log in to the Revenue Department system.
