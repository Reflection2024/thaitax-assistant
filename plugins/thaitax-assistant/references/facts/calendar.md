# Calendar and dates

Last verified: 2026-11-11. Re-verify before use (see `_index.md`). For arithmetic use `scripts/thaitax_calc.py`; its rates live in `scripts/rates.json`.

## Calendar

- Official Thai documents use the Buddhist Era: **BE = CE + 543** (2026 = 2569). Convert, and say that you did.
- A deadline that falls on a weekend or public holiday moves to the next working day. Check the current year's holiday list: `scripts/rates.json` → `holidays` (2026 as announced; 2027 is **provisional** until the cabinet publishes the official list, and lunar holy days can move). Pass them to `deadlines` with the `holidays` argument. Bank holidays differ slightly (1 May is a bank holiday, not a government one).
- The financial year is usually the calendar year, but read it from the profile.
