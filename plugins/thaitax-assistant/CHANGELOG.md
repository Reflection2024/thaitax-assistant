# Changelog

## 1.0.0-rc.2 (2026-11-11): annual facts update
No rate in `rates.json` changed; all 2026 figures re-verified 2026-11-11.
- **Expiring:** online 8-day filing extension (MoF notice 12 Jan 2024) covers returns due up to 31 Jan 2027; renewal not yet published. Flagged in withholding, VAT, individuals, PND.90 guide; `deadlines.online_extension_valid_until` added.
- **New, unverified:** Employee Welfare Fund from 1 Jan 2027, 0.25% + 0.25% (employers with 10+ staff); regulations not yet gazetted (Tilleke & Gibbins, HLB, Oct 2026). Added to payroll.md and `rates.json` → `ewf`.
- Minimum wage: Koh Samui THB 400, rest of Surat Thani incl. Koh Phangan THB 352 (Notification No. 14, 1 Jul 2025); 2027 review pending (Thaiger, 6 Nov 2026).
- e-WHT 1% to 31 Dec 2027 confirmed: Ministerial Regulation No. 402, gazetted Oct 2026, retroactive to 1 Jan 2026.
- VAT 7% to 30 Sep 2027 confirmed: Royal Decree No. 807 (BDO, Aug 2026).
- SSO ceiling THB 17,500 confirmed (Ministerial Regulation gazetted 12 Dec 2025).
- Allowances tax year 2026: solar rooftop up to THB 200,000 (Royal Decree, Mar 2026) and artwork up to THB 100,000 added; no Easy E-Receipt for 2026; Thai ESG 300k window ends 31 Dec 2026; house-construction allowance marked unverified.
- Foreign income: remittance relief still not law; FTC tool (July 2026) and foreign-income declaration form (RD forms page, 10 Sep 2026) confirmed.
- Public holidays added to `rates.json`: 2026 as announced, 2027 provisional.

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
