# Pilot kit: test ThaiTax Assistant before a wide release

Two stages: **(A)** synthetic data with planted mistakes, where the expected answer is known; **(B)** one real company and one real individual, reviewed by a Thai accountant.

## A. Synthetic run (about 30 minutes)

Install the plugin, then in a new chat upload each file from `sample-data/` with the prompt shown. Compare the answer with the **expected findings**. Every expected finding must appear; any number that differs is a bug.

| # | Upload | Prompt | Expected findings |
|---|---|---|---|
| 1 | `sales-tax-report-2569-10.csv` | "This is my sales export for October. Check it and give me the output VAT." | BE dates converted · **row 3:** tax ID has 12 digits · **INV2569-0105:** VAT 1,450 vs expected 1,400 · **gap:** INV2569-0104 missing · **duplicate:** INV2569-0106 twice · totals shown with and without the duplicate · nothing "repaired" silently |
| 2 | `purchases-2569-10.csv` | "Which input VAT can I claim, and what else should I file?" | Claimable: **A-5531 only (560)** · R-88 abbreviated invoice and entertainment: not claimable · T-221: buyer name does not match the registration · **S-19:** individual contractor, 3% WHT (900) on **PND.3**, not recorded · **Google:** PP.36 VAT 1,960 due the 15th; possible PND.54 flagged for the accountant |
| 3 | `payroll-2569-11.csv` | "Prepare November payroll." | Overtime for พนักงาน ก **1,125.00** · SSO capped at **875** for Staff C · **Staff C:** permit expires 22 Dec, within 60 days, pay held · **พนักงาน ง:** not SSO-registered · **ข and ง:** below the Ko Samui minimum wage, verified · nothing paid |
| 4 | `transfers-2026.csv` | "I live on Samui since January 2026; these are my transfers. What's taxable?" | Residency asked or counted · **A:** 302,400 savings before 2024 (needs the 31 Dec 2023 statement) · **B:** 472,920 from 2026 salary · **E:** 191,500 loan (evidence) · **F:** 114,000 unknown, asked and not assumed · German treaty credit explained · the draft relief called **not law** |
| 5 | (none) | "Draft a tax invoice in Thai and English for 85,000 consulting to Siam Coast, 3% withheld." | DOCX from the template · 5,950 VAT · 90,950 total · words "เก้าหมื่นเก้าร้อยห้าสิบบาทถ้วน" · WHT 2,550, net 88,400 · serial number blank · DRAFT line |
| 6 | 3 receipt photos (any) | "Add these receipts." | Each receipt read · claimable yes/no with the reason · no guessed digits on blurry fields |
| 7 | (none) | "Get started" | Welcome · short question rounds · connection walkthrough · phone-photo how-to · profile shown before saving · first task run |

Log results in `pilot/results.md`: prompt, pass/fail, what was wrong.

## B. Real pilot

1. **Company:** one client company for one closed month. Run "monthly pack". Give the pack to the company's Thai accountant together with the review form below.
2. **Individual:** one person with foreign income. Run "fill in my annual tax return" on their real documents. Same review.
3. Fix whatever the accountant marks, add each case to the synthetic set, and only then release version 1.0.

## Accountant review form / แบบประเมินโดยนักบัญชี

Reviewer · ผู้ตรวจ: ____________ Date · วันที่: ________ Entity · กิจการ: ____________ Period · งวด: ______

| Check · รายการตรวจ | ✓ / ✗ | Note · หมายเหตุ |
|---|---|---|
| Forms due and deadlines correct · แบบและกำหนดยื่นถูกต้อง | | |
| Output VAT / input VAT correct · ภาษีขาย/ภาษีซื้อถูกต้อง | | |
| Non-claimable invoices correctly identified · ระบุใบกำกับที่ใช้ไม่ได้ถูกต้อง | | |
| Withholding: right form (PND.3/53/54) and rate · แบบและอัตราหัก ณ ที่จ่ายถูกต้อง | | |
| Missing withholding detected · พบรายการที่ไม่ได้หัก ณ ที่จ่าย | | |
| PP.36 handled · ภ.พ.36 ถูกต้อง | | |
| SSO and payroll figures correct · ประกันสังคมและเงินเดือนถูกต้อง | | |
| Personal tax: income categories and expense deductions · ประเภทเงินได้และค่าใช้จ่ายถูกต้อง | | |
| Foreign income buckets and FTC reasonable · เงินได้ต่างประเทศและเครดิตภาษีสมเหตุสมผล | | |
| Usable as-is for filing? · ใช้ยื่นได้ทันทีหรือไม่ | | |
| Time saved vs. usual (estimate) · เวลาที่ประหยัดได้ | | |

Overall comments · ความเห็นเพิ่มเติม:
