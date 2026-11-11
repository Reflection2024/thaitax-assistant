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
- **Deadlines:** PND.1, 2, 3, 53 and 54 are due the 7th on paper and the 15th online. The online extension is renewed by Ministry of Finance notice, so confirm it is still in force.
- No withholding on water, electricity or public transport.
- A withholding the payer missed is the payer's liability. List it; never ignore it.
