# Thai tax facts: index and disclaimer

Read this before any Thai amount, rate or deadline goes into a deliverable.

**Facts change.** The figures below were compiled in November 2026. Before the owner acts on a rate or a deadline, check it against an official source (rd.go.th for the Revenue Department, sso.go.th for social security, mol.go.th for the minimum wage, the Royal Gazette) with web search. Write "verified on <date>, <source>" next to it. If the check fails, mark the figure **unverified**.

Every deliverable carries this line:
- EN: *Prepared for review by your Thai accountant. Not tax or legal advice. Nothing has been filed.*
- HE: *הוכן לבדיקת רואה החשבון התאילנדי שלך. אינו ייעוץ מס או ייעוץ משפטי. דבר לא הוגש.*
- TH: *จัดเตรียมเพื่อให้นักบัญชีของท่านตรวจสอบ ไม่ใช่คำแนะนำด้านภาษีหรือกฎหมาย และยังไม่มีการยื่นแบบใด ๆ*

## Files: load only what the task needs

| File | Covers | Used by |
|---|---|---|
| `vat.md` | VAT rate, registration, PP.30, PP.36, input-VAT rules, tax-invoice content | thai-monthly-tax, thai-documents, receipt-capture, cash-and-collections |
| `withholding.md` | WHT rates, forms PND.1/2/3/53/54, e-WHT, deadlines | thai-monthly-tax, thai-documents, receipt-capture, thai-personal-tax |
| `corporate.md` | CIT, SME rate, PND.50/51, DBD filing | thai-monthly-tax (annual) |
| `individuals.md` | Personal tax, residency, foreign income and remittance | thai-personal-tax, foreign-income |
| `payroll.md` | SSO, minimum wage, overtime, severance, work permits | thai-payroll, thai-monthly-tax |
| `calendar.md` | Buddhist Era, holidays, year end | all |
| `../pnd90-annual-return.md` | PND.90/91 line by line, foreign-income declaration, FTC | thai-personal-tax, foreign-income |

## Arithmetic

Never compute tax, VAT, SSO, withholding, overtime, BE dates, deadlines or baht-in-words in prose. Run the plugin's calculator and quote its output:

```
python3 -I <plugin>/scripts/thaitax_calc.py <command> '<json>'
```

Commands: `vat`, `vat_check`, `be`, `deadlines`, `sso`, `overtime`, `wht`, `pit`, `bahttext` (`help` lists them). `<plugin>` is two folders above the running skill's base directory. If Python cannot run, compute by hand, show every step, and label the result "unchecked".
