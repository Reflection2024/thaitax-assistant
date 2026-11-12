# Monthly update check (runs on the 1st of every month)

Goal: find out whether anything ThaiTax Assistant relies on has changed, prepare the update, and **wait for the owner's approval**. Nothing reaches users until the owner says yes.

## 1. Official forms

```
python3 tools/check_forms.py
```

- `changed`: the Revenue Department / SSO republished a form. If `map_still_fits` is true, the new PDF can replace the old one as is. If boxes are missing, the map needs updating (see `references/official-forms.md`).
- `errors`: rd.go.th often resets connections; rerun once. Anything still failing is listed in the report as "could not check".
- Also look for **new tax-year forms** not yet in the catalog: the rd.go.th download pages for personal income tax (ภ.ง.ด.90, 91, 94, foreign-income declaration) and corporate tax (ภ.ง.ด.50, 51) for the current Buddhist-Era year. In December–January the new ภ.ง.ด.90/91 usually appear.

## 2. Rates, thresholds and deadlines

Re-verify each item against an official source first (rd.go.th, ratchakitcha.soc.go.th, sso.go.th, mol.go.th, dol.go.th), then a professional note. Follow `plugins/thaitax-assistant/skills/tax-facts-update/SKILL.md`.

| What | Where it lives |
|---|---|
| VAT 7% and decree expiry | `scripts/rates.json` → vat; `references/facts/vat.md` |
| e-WHT 1% (Cabinet approval vs. gazetted regulation) | rates.json → wht_resident; `facts/withholding.md` |
| Online filing 8-day extension (current notice ends 31 Jan 2027) | rates.json → deadlines; `facts/calendar.md` |
| SSO ceiling and floor | rates.json → sso; `facts/payroll.md` |
| Minimum wage (provinces used: Koh Samui, Surat Thani, Bangkok, Phuket…) | rates.json → minimum_wage |
| PIT bands, allowances, temporary allowances for the year (Easy e-Receipt, Thai ESG…) | rates.json → pit; `facts/individuals.md` |
| Foreign income remittance (is the draft relief law yet?) | `facts/individuals.md`; `skills/foreign-income` |
| Land and building tax rates, payment month, reductions | rates.json → property; `facts/property.md` |
| Transfer fee 0.01% measure (current: to 30 Jun 2027) | rates.json → property.sale; `facts/property.md` |
| Public holidays for the coming months (deadline shifts) | `facts/calendar.md` |

## 3. If something changed

1. Create a branch `monthly-update-YYYY-MM` from `main`.
2. Apply the changes: replace PDFs, update `rates.json` and the fact files with the new value, the source and `verified` date; bump the version in both `plugin.json` and `.claude-plugin/marketplace.json`; add a CHANGELOG entry.
3. Run every test in `plugins/thaitax-assistant/scripts/test_*.py`, `claude plugin validate` if available, and `python3 tools/build_chatgpt.py`. Rebuild `docs/thaitax-assistant.plugin`.
4. Push the branch and open a pull request titled `Monthly update YYYY-MM`. **Do not merge.**
5. Send the owner a short summary in Hebrew: what changed, the source for each change, the PR link, and "reply yes to publish". After `python3 tools/check_forms.py --record` is run on approval, the new hashes become the baseline.

## 4. If nothing changed

Send one line in Hebrew: "בדיקה חודשית: הכול עדכני", with the date and what could not be checked, if anything. No branch, no PR.
