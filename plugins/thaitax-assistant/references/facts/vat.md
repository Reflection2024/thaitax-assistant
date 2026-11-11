# VAT and tax invoices

Last verified: 2026-11-11. Re-verify before use (see `_index.md`). For arithmetic use `scripts/thaitax_calc.py`; its rates live in `scripts/rates.json`.

## VAT (ภาษีมูลค่าเพิ่ม)

- Rate **7%** (a royal decree reduces the statutory 10%). The current decree runs to **30 Sep 2027**. Check the rate for any document dated after that.
- Registration is mandatory above THB 1.8 million of VAT-able annual revenue. A business that is not registered cannot charge VAT or issue a tax invoice.
- **PP.30 (ภ.พ.30)** is filed every month, including months with no sales. Due the 15th of the next month on paper, the 23rd online.
- **PP.36 (ภ.พ.36)** is reverse-charge VAT: self-assess 7% on services bought from a foreign provider and used in Thailand (Google Ads, Meta, AWS, SaaS). Due the 15th. The input credit is usually claimable.
- Input VAT can be claimed only with a valid tax invoice that carries the company's exact registered name, address and tax ID. Entertainment, passenger cars under 10 seats, and invoices missing a mandatory field cannot be claimed.
- Exports and services used abroad are 0%. Education, healthcare, residential rent and some land sales are exempt or fall under other taxes. Classify each item; never assume.

## Tax invoice (ใบกำกับภาษี): mandatory content

- The words "Tax Invoice / ใบกำกับภาษี".
- Seller: name, address, 13-digit tax ID, branch ("สำนักงานใหญ่" or a 5-digit branch code).
- Buyer: name and address, plus tax ID and branch if the buyer is VAT-registered.
- A running serial number from the issuer's system, and the date.
- Description, quantity and value of what was sold.
- VAT on its own line.

The invoice is issued at the tax point: payment for services, delivery for goods. e-Tax invoices are optional for most businesses.
