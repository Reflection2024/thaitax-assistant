# Document templates

Build every Thai business document with the plugin generator. It gives every document the same layout and keeps the numbers reconciled.

```
node <plugin>/scripts/make_document.js --sample tax_invoice > doc.json   # start from a sample
node <plugin>/scripts/make_document.js doc.json output.docx
```

Types: `tax_invoice`, `receipt`, `quotation`, `billing_note`, `payslip`.

- **Layout:** Thai first, with the second language (`"second_language": "en"` or `"he"`) under each label. A4. Tahoma font (Thai-capable on Windows and macOS).
- **Computed in the script, in satang:** totals, VAT (`vat_rate`, default 0.07; `"vat": false` for a non-VAT document), withholding note (`withholding_rate`), Thai amount in words, and Thai dates (BE with CE).
- **Draft by default:** the serial number stays blank and a DRAFT line is printed. Set `number` and `"final": true` only when the user confirms the number comes from their registered system. A legal tax invoice is issued from FlowAccount or the user's own system.
- **If `docx` is missing:** run `npm install docx` in a scratch folder. If Node is not available, build the same layout with the docx skill.

**Fields:**

- Seller, buyer or employer blocks: `name`, `address`, `tax_id`, `branch` (`"00000"` = head office).
- Items: `description`, `qty`, `unit_price`.
- Quotation: `valid_until`, `terms`.
- Billing note: `due_date`.
- Receipt: `invoice_ref`, `payment_method`.
- Payslip: `period`, `employee {name, position}`, `earnings[]`, `deductions[]`, each as `{label, amount}`.
- All documents: optional `notes`.

Dates in JSON are ISO `YYYY-MM-DD` (CE).

**After generating:** render the file once (convert to PDF and look at it). Check:

- the Thai renders;
- the totals match `thaitax_calc.py vat`;
- blank legal fields are visible.

Then send the file.
