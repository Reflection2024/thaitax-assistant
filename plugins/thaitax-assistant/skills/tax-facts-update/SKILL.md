---
name: tax-facts-update
description: "Maintainer skill: re-verifies every rate, threshold, allowance and deadline that ThaiTax Assistant relies on (VAT rate and decree expiry, withholding rates and e-WHT, SSO ceiling, minimum wage, PIT bands and allowances, PND.90/91/94 dates and online extensions, foreign-income remittance rules, foreign tax credit tool, public holidays) against official Thai sources, then updates the fact files and rates.json with new last-verified dates, re-runs the calculator tests, and reports what changed. Run every January, after a royal decree or budget announcement, or when the user says 'update tax facts', 'annual update', 'check rates are current', 'עדכון שנתי', 'לעדכן שיעורי מס', 'อัปเดตอัตราภาษี'."
---

# Tax facts update (maintainer)

Applies to the plugin's own files:

- `../../references/facts/*.md`
- `../../references/pnd90-annual-return.md`
- `../../scripts/rates.json`

## Step 1: Inventory

List every dated or numeric fact in those files: each `rates.json` block, each "Last verified" line, every rate, threshold, cap, deadline and "valid until" date, and every item marked UNVERIFIED.

## Step 2: Verify

For each fact, search official sources first: rd.go.th (English and Thai), sso.go.th, mol.go.th, the Royal Gazette (ratchakitcha.soc.go.th), and dbd.go.th. Then use one recent professional note (Big-Four, Forvis Mazars, HLB, Luther, a Thai law firm) to confirm interpretation. Record for each fact: the old value, the current value, the source URL, the date read, and a status of **unchanged**, **changed**, **expiring** (within 6 months) or **unverified**.

Priority checks every January:

- VAT rate decree expiry; e-WHT reduced-rate expiry;
- online filing extension notices;
- SSO ceiling;
- minimum wage notifications (Surat Thani, Koh Samui, Koh Phangan);
- **temporary personal allowances for the new tax year** (e-Receipt, tourism, construction);
- the remittance rule (Por.161/162 and the status of any relief draft);
- the foreign-income declaration form and the foreign-tax-credit tool;
- the year's public holidays (add them as a `holidays` list per year in `rates.json`).

## Step 3: Update

- Edit only facts whose status changed. Update every "Last verified" line and the `verified` / `source` fields in `rates.json`.
- If a rate in `rates.json` changed, update or add tests in `../../scripts/test_thaitax_calc.py` and run `python3 -I test_thaitax_calc.py`. All tests must pass.
- Bump the plugin version (minor for rate changes, patch for date-only refreshes) in `.claude-plugin/plugin.json`, and in the marketplace file if one exists.
- Add an entry at the top of `CHANGELOG.md` at the plugin root (create it if missing): date, version, and the list of changed facts with sources.

## Step 4: Report

Produce a short table: fact, old value, new value, source. Put **expiring** and **unverified** items first. If working in the repository, commit on a branch named `facts-update-<YYYY-MM-DD>` and push the branch; never push to `main` without the maintainer's yes.
