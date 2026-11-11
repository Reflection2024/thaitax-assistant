# Changelog

## 1.0.0-rc.9 (2026-11-11)
- `family-budget` and `ask-thai-tax` now trigger whenever statements are uploaded or any Thai tax question is asked, so their ask-first rules always apply.

## 1.0.0-rc.8 (2026-11-11): ask first, answer short
- Every user-facing skill now starts with the same rule: confirm the request, ask up to 3 short questions for any fact the answer depends on, and ask for the supporting document by name instead of estimating.
- No assumed facts: no "probably / it seems / about" for anything not in the data; an unavoidable assumption is asked as a question and no amount is computed from it.
- Short answers: the answer first, at most 3 bullets, about 8 lines; details only on request.
- Replaced the "defaults over questions" rule; defaults now only for things that change no money.

## 1.0.0-rc.7 (2026-11-11): family budget
- New skill `family-budget`: bank statements from any bank or currency → money in vs. out per month, where the money goes, fixed payments and subscriptions with yearly cost, price rises, services paid for twice; remembers the family's own category corrections.
- `scripts/budget.py` (standard library; own-account transfers excluded, FX never silent) and `scripts/budget_dashboard.py` (one self-contained page, EN/HE/TH, right-to-left for Hebrew, light and dark).
- Advanced option: export to Actual Budget, and setup notes for the community `actual-mcp` server.
- `scripts/test_budget.py` (7 tests); sample family statements in `pilot/sample-data`.

## 1.0.0-rc.6 (2026-11-11): verification pass
- PIT bands confirmed on rd.go.th (30% to THB 5m, 35% above).
- Online filing extension: valid for filings due to 31 Jan 2027; the calculator now warns for later periods and PND.90 for tax year 2026.
- SSO: ceiling 17,500 / 875 confirmed; rounding rule (50 satang up) confirmed; PIT deduction 10,500.
- Minimum wage: Notification No. 14 still current; Koh Samui 400, rest of Surat Thani incl. Koh Phangan 352; hotels types 2-4 and entertainment venues 400 nationwide.
- Severance 400 days after 20 years confirmed (Act No. 7, 2019).
- Land & building tax: tiered computation (s.42), payment by 30 April (s.46), appeal within 30 days (s.73).
- Property sale: individual WHT capped at 20% of the sale price (Por.100/2543); THB 200,000 exemption for inherited or gifted property in Tambon areas; 0.01% transfer fee confirmed for Thai-national individual buyers only.
- 90-day report windows by channel (in person, online, post).

## 1.0.0-rc.5 (2026-11-11)
- Lightness rule: never ask what can be found, defaults over questions, one batch of requests per conversation.
- Monthly bank-statement upload request (no Thai bank connection available yet).
- New skills: `official-letter`, `year-end-planning`, `property-tax` (with calculator: land & building tax, sale costs, lease registration), `company-housekeeping`, `visa-reminders`.

## 1.0.0-rc.4 (2026-11-11)
- New skill `accountant-check`: completeness, timeliness, figures vs. books, payments reached the RD, access and control, annual statements, fees; polite questions for the accountant. Runs quarterly from `monthly-pack`.

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
