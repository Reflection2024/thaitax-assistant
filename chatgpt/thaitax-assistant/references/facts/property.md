# Property taxes and Land Office costs

Last verified: 2026-11-11. Re-verify before use (see `_index.md` and `../research-protocol.md`). All arithmetic: `scripts/thaitax_calc.py` commands `land_building_tax`, `property_sale`, `lease_registration`. Rates live in `scripts/rates.json` → `property`.

## Annual land and building tax (ภาษีที่ดินและสิ่งปลูกสร้าง)

- Owner on **1 January** pays. The local authority (อบต. / เทศบาล) sends the assessment, usually February–April. By law payment is due by **30 April** (s.46; often extended, for example to June–August in 2026), with instalments allowed from THB 3,000 (s.52, apply first). **Appeal** to the local executive within **30 days** of receiving the notice (s.73). Always use the dates on the notice.
- The base is the **official appraised value** of land plus building (Treasury Department lists; a new valuation cycle starts in 2027, so expect changes).
- Classified by **actual use:** main home, other residential, commercial / other, agricultural, vacant. The tax is computed **in tiers** (ขั้นบันได, s.42 para 1): each slice of value is taxed at its band rate. Some bank and press summaries apply one rate to the whole value; the plugin follows the Act and compares against the notice.
- **Main home** (owner of land and building, registered in the house book on 1 Jan): exempt up to THB 50m. If the owner owns the building only: exempt up to THB 10m.
- **Other residential** (second homes, condos held by individuals): 0.02% up to THB 50m, then 0.03% / 0.05% / 0.1%.
- **Commercial, other use, vacant:** 0.3% up to 50m, then 0.4% / 0.5% / 0.6% / 0.7%. Land left vacant for 3 years gets an extra 0.3% every 3 years (cap 3%).
- **Rental property.** Villas and condos rented to tourists, and Bangkok rental condos, may be treated as "other use" at commercial rates. Bangkok proposed this reclassification in July 2026. Flag it; the local authority decides.
- Companies get **no** main-home exemption.

## Selling property: costs at the Land Office

| Item | Rate | Base | Usually paid by |
|---|---|---|---|
| Transfer fee | 2% (0.01% for qualifying residential ≤ THB 7m, 1 Jul 2026 – 30 Jun 2027; buyer must be a **Thai-national individual**; transfer and mortgage registered together for the mortgage fee; confirmed by Ministry of Interior notifications of 1 Jul 2026 and multiple sources) | Appraised value | Split by contract |
| Specific business tax (SBT) | 3.3% | Higher of price and appraised | Seller |
| Stamp duty | 0.5%, only when SBT does not apply | Higher of price and appraised | Seller |
| Withholding tax | Company 1%; individual: progressive (below) | Company: higher of price and appraised; individual: appraised | Seller |

- **SBT applies** when a company sells, or an individual sells within **5 years** of acquiring. It does **not** apply if the individual was registered in the house book for 1+ year, or inherited the property. Otherwise stamp duty applies instead.
- **Individual withholding** (RD method):
  1. Take the appraised value and deduct the holding-period expense (1 yr 92%, 2 yrs 84%, 3 yrs 77%, 4 yrs 71%, 5 yrs 65%, 6 yrs 60%, 7 yrs 55%, 8+ yrs 50%; inherited or gifted 50%).
  2. Divide by the years held (max 10).
  3. Apply the progressive table.
  4. Multiply by the years held.
  5. For property not acquired for trade or profit, the result is capped at **20% of the sale price** stated at registration (RD Order Por.100/2543).

  Inherited or gifted property located in a **Tambon Administrative Organisation (อบต.) area**, outside municipalities: the first THB 200,000 of sale income in the year is exempt (s.42(17); RD ruling 1998).

  Confirm the table each year.
- The seller may choose to include the sale in the annual return instead; that is the accountant's call.
- Foreign buyers of condos need the foreign-exchange transaction form (FET / bank credit advice) for the funds. Flag it; the plugin does not handle the transfer.

## Leases (over 3 years must be registered)

- Registration fee 1% plus stamp duty 0.1% of the **total rent** over the term. Maximum 30 years per registration.
- Rent received by an individual is 40(5) income (30% expense for buildings). Companies paying rent withhold 5%.

## Not handled here

Ownership structure (nominees, Thai company holding land, leasehold vs. freehold), Foreign Business Act and Land Code questions. Flag them to a lawyer.
