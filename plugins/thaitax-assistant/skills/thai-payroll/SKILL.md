---
name: thai-payroll
description: "Prepares Thai payroll for the owner to approve: gross pay, overtime and holiday pay under the Labour Protection Act, social security (5% each side up to the wage ceiling), income tax withheld for PND.1, net pay, employer cost, payslip data in Thai, and flags for minimum wage, SSO registration and foreign staff work permits. Stages the run; never pays anyone or submits anything. Use when the owner says 'payroll', 'pay my staff', 'social security', 'SSO', 'PND.1', 'work permit expiring', 'משכורות', 'ביטוח לאומי תאילנד', 'תלושים', 'เงินเดือน', 'ประกันสังคม', 'ภ.ง.ด.1', 'สลิปเงินเดือน'."
---

# Thai payroll

> **Proactive by default:** follow `../../references/proactive-behavior.md`: ask for what is missing, run `document-check` on every document received, warn about deadlines and risks ahead, keep the request list, and end with up to three next steps. **Research before relying on any rule:** follow `../../references/research-protocol.md` (research connector or web search, official Thai sources first, Thai and English queries, cited sources).

Read `../../references/facts/payroll.md`, `../../references/facts/withholding.md` (PND.1) and `../../references/facts/calendar.md` first. Do every calculation with the plugin calculator, `../../scripts/thaitax_calc.py` (see `../../references/facts/_index.md` § Arithmetic), and quote its output. (commands `sso`, `overtime`, `deadlines`) A wrong payslip is a person who cannot pay rent: assemble and check, and let the owner decide.

## Step 1: Verify the moving numbers

With web search, confirm against sso.go.th and mol.go.th:

- the SSO rate and wage ceiling for the month;
- the minimum wage for the **district** where each employee works.

Write "verified <date>, <source>".

## Step 2: Collect

Take the data from the owner's payroll tool, spreadsheet, or last month's payroll:

- name, Thai ID or passport number, position, Thai or foreign;
- monthly salary or daily rate, days worked, overtime hours, holiday work, leave;
- bonus, commission, allowances, deductions, advances;
- SSO registration date;
- for foreign staff, work permit number and expiry;
- tax allowances on file.

Anything missing stays missing and goes on the list. Never assume a figure.

## Step 3: Compute (show the formula per person)

- **Gross** = salary + overtime (1.5x working day; holiday work 1x or 2x; overtime on a holiday 3x) + allowances. Hourly rate = monthly ÷ (30 × normal daily hours).
- **SSO** = 5% × min(wage, ceiling), with the floor applied. The employer pays the same. State the rounding.
- **PND.1 tax withheld:** use the figure from the owner's payroll system or accountant. If there is none and the allowances are known, show an **estimate** from the progressive table, labelled as an estimate.
- **Net** = gross − SSO − tax − other deductions.
- **Employer cost** = gross + employer SSO.

## Step 4: Flag, never quietly fix

- Pay below the district minimum wage, or overtime hours without overtime pay.
- A foreign employee with no permit on file, or one expiring within 60 days. **Do not stage that person's pay until the owner decides.**
- Not registered with the SSO within 30 days of hire.
- A rate or hours change from last month, a mid-month start or exit, or negative net pay.
- A termination: list years of service and stop. Severance goes to the owner's lawyer.

## Step 5: Stage and hand off

Show the run line by line and wait for an explicit yes. Then deliver:

- payslip data per person, in Thai with English or Hebrew, generated through `thai-documents`;
- the SSO total and the **15th** deadline (form SPS 1-10);
- the PND.1 total, with the **7th** (paper) and **15th** (online) deadlines;
- a payroll journal summary for the accountant;
- a bank-transfer list for the owner to key in. Never execute transfers.

Never pay, submit SSO or PND.1, or post to the books without an explicit yes. Keep ID numbers and salaries inside the deliverable; never send them to outside services.
