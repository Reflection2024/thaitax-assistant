# Official forms: give the user the real form

Every return or certificate you prepare is delivered **on the official Revenue Department form**, filled in, so the user can send it straight to the accountant. The user gets two files:

1. **`<FORM>-<period>.pdf`**: the official form, filled. This is the file to send to the accountant.
2. **`<FORM>-<period>-explained.pdf`**: a short sheet with each filled line and what it means (English and Thai). For Hebrew speakers, also explain the main lines in the chat in Hebrew.

## Bundled forms

`python3 -I ../../scripts/official_forms.py list` shows them, with the official source link:

| ID | Form |
|---|---|
| PND90, PND91, PND94 | Personal income tax returns |
| PND90_FOREIGN | Income Declaration for Foreign-Sourced Income |
| PND1, PND3, PND3_ATTACH, PND53 | Monthly withholding returns and the payee list |
| PP30, PP36 | VAT return and reverse-charge VAT |
| (more when added) | PND50, PND51, PND53 attachment, 50 ทวิ certificate, SSO 1-10 |

If the form you need is not bundled, or rd.go.th has a newer version for the tax year, say so in one line. Download the official PDF into the session when the network allows, and fill it the same way (pass the file path instead of the ID). Never redraw a form by hand.

## How to fill

1. **Boxes:** `official_forms.py fields <FORM> --named` lists the boxes that have plain names (`taxpayer_tin`, `line5_output_vat`, `chk_month_10`...). `fields <FORM> --page N` lists every box on a page with the Thai text printed next to it, for lines that have no plain name yet.
2. **values.json:**
   ```json
   {"form": "PP30", "values": {
     "tin": "0845566001234", "year_be": "2569", "chk_month_10": true,
     "line5_output_vat": {"value": "33775.00", "note": "7% of taxable sales 482,500"}}}
   ```
   - Amounts as plain numbers (`12345.50`): baht and satang go into their own boxes automatically.
   - 13-digit tax IDs without dashes; they are spread into the boxes.
   - Tick boxes: `true`. Radio groups: tick only one option.
   - Dates and years in Buddhist Era, as the form expects.
   - Every figure comes from the calculator or the user's documents, never typed from memory.
3. **Fill:** `official_forms.py fill <FORM> values.json <out>.pdf`. A small grey "Draft for review" line is printed in the bottom margin. Use `--final` only when the user asks for a clean copy, after they have checked it.
4. **Check by looking:** `official_forms.py preview <out>.pdf <dir>` and open every page image. Every value must sit in the right box, inside it, on the right line. If anything is off, fix values.json and fill again. Do not deliver before this check.
5. **Explanation:** `official_forms.py explain values.json <out>-explained.pdf` (uses the `note` of each value; add `"line": "5. ภาษีขาย"` for a clearer first column).
6. **Deliver** both files. One line in the reply: what the form is, the period, the bottom line (tax to pay or refund), and that it is a draft for the accountant to check and file.

## Limits

- The forms are the RD's own PDFs for the 2568 (2025) tax year or the latest monthly version. The annual personal forms for tax year 2569 (2026) are published by the RD around January 2027: replace them then (the `tax-facts-update` skill does this).
- Filling a form is not filing it. The user or accountant files through e-Filing or at the office.
