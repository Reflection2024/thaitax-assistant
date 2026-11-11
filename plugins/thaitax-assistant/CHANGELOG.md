# Changelog

## 1.0.0-rc.3 (2026-11-11)
- Research protocol for every skill: research connector / web / deep research, official Thai sources first, Thai + English queries, cross-checks, cited sources.
- New skill `ask-thai-tax` for any question.

## 1.0.0-rc.2 (2026-11-11)
- Proactive by default: asks for missing documents, checks every document on arrival, warns ahead, keeps a request list, calendar reminders (on a yes).
- New skills: `document-check` (incl. journals and trial balance), `what-do-you-need`.

## 1.0.0-rc.1 (2026-11-11)
- Calculator `scripts/thaitax_calc.py` (VAT, BE dates, SSO, overtime, withholding, PND.90 tax incl. 0.5% minimum tax and foreign tax credit, deadlines, baht in words) with tests; rates in `scripts/rates.json`.
- Fact files split by topic (`references/facts/`); skills load only what they need.
- Document generator `scripts/make_document.js`: tax invoice, receipt, quotation, billing note, payslip (Thai + English/Hebrew).
- New skills: `monthly-pack` (runs on the 1st), `tax-facts-update` (annual).
- All facts last verified 2026-11-11.

## 0.4.0 (2026-11-11)
- Renamed to ThaiTax Assistant. Guided onboarding with intake checklist; receipt capture from phone photos.

## 0.3.0
- PND.90 line-by-line guide; foreign income and treaty credit.

## 0.2.0
- Individuals supported (personal tax).

## 0.1.0
- First version: monthly tax, documents, collections, payroll, export reader.
