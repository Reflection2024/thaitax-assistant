# Withholding tax

Last verified: 2026-11-11. Re-verify before use (see `_index.md`). For arithmetic use `scripts/thaitax_calc.py`; its rates live in `scripts/rates.json`.

## Withholding tax (ภาษีหัก ณ ที่จ่าย)

The **payer** withholds, on the amount before VAT, then remits it and gives the payee a certificate (50 ทวิ).

| Payment to a Thai resident | Usual rate |
|---|---|
| Services, professional fees, contractors, commission | 3% |
| Rent of property | 5% |
| Advertising | 2% |
| Transport (not public passenger) | 1% |
| Non-life insurance premium | 1% |
| Prizes, promotions | 5% |
| Dividends | 10% |
| Salaries | progressive table, PND.1 |

- **Which form depends on who is paid.** PND.1 salaries · PND.3 Thai individuals · PND.53 Thai companies and partnerships · PND.54 non-residents (often 15%; a double-tax treaty may lower it) · PND.2 dividends or interest paid to individuals.
- Identify the payee's legal form before choosing the form. A certificate issued on the wrong form cannot be used by the payee.
- **e-Withholding:** the 5%, 3% and 2% rates drop to 1% when the payment goes through the banks' e-WHT system (extended to 31 Dec 2027). Apply this only if the payer actually uses e-WHT.
- **Deadlines:** PND.1, 2, 3, 53 and 54 are due the 7th on paper and the 15th online. The 8-day online extension (Ministry of Finance notice) covers filings due **1 Feb 2024 – 31 Jan 2027**; it has been renewed in rounds since 2014. From February 2027, check that a new notice is out before relying on the online dates.
- Withholding applies to a payment of **1,000 baht or more**, or to smaller instalments of one contract worth 1,000 baht or more. No withholding on goods, water, electricity or public transport.
- Record the rate and form for each supplier contract once (`contracts-and-payments`) and apply it before every payment.
- A withholding the payer missed is the payer's liability. List it; never ignore it.
