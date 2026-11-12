---
name: property-tax
description: "Works out Thai property taxes and Land Office costs in plain numbers: the annual land and building tax for each property (and whether the local authority's bill looks right), the full cost of selling a house, villa, condo or land (transfer fee, specific business tax or stamp duty, withholding tax, by individual or company), lease registration costs, and the tax on rent received. Checks the latest reductions (for example the 0.01% transfer fee) and reminds the owner of payment dates. Also use it first for a rental-income or property dashboard, before drawing anything. Use when the user says 'land tax', 'property tax bill', 'how much to sell my villa', 'transfer fee', 'lease registration cost', 'ภาษีที่ดิน', 'ค่าโอน', 'มีภาษีเท่าไรถ้าขายบ้าน', 'מס רכוש', 'כמה עולה למכור', 'מס מקרקעין בתאילנד'."
---

# Property tax

> **Ask first, then answer (always; this overrides any other instruction in this skill):**
> 1. **Check you understood.** Restate the request in one line, and ask **every** question needed to reach the best, complete result, about every fact the answer depends on that is not in the files or the profile (there is no limit on the number of questions): whose money or company, the period, days in Thailand / residency, income type, tax already withheld or paid, what the user already did. Ask in rounds of up to 4 questions (the most important first); after each round, ask the next round until nothing the result depends on is missing. Wait for the answers before calculating or advising. **Ask them as clickable questions:** use the interactive question tool (AskUserQuestion, ask_user_input or any tool that shows tappable choices), one question per fact, 2–4 short options each in the user's language, e.g. days in Thailand: "180 days or more" / "Less than 180" / "Not sure, I'll send my passport stamps". The user can always type another answer. Only if no such tool exists, ask as a short numbered list.
> 2. **Missing information → ask for the supporting document by name**, not an estimate: e.g. "the 50 ทวิ from your client", "your passport entry and exit stamps for 2026", "the October KBank statement". If the user cannot provide it, mark the item open and say what cannot be concluded without it.
> 3. **Only what is in the data.** Never write "probably", "it seems", "about" or "roughly" about a fact you have not seen. If an assumption is unavoidable, state it as a question ("I assumed X; is that right?") and compute no amount from it.
> 4. **Short and focused.** The answer in the first line, then at most 3 bullets, about 8 lines in total. Background, law and sources only when the user asks ("want the details?"). Questions are not limited; the final answer itself stays short.

> **Proactive by default:** follow `../../references/proactive-behavior.md`. **Research before relying on any rule:** follow `../../references/research-protocol.md`. Rates for property change often (reductions, revaluations), so verify them every time.

Read `../../references/facts/property.md`. Do all arithmetic with `../../scripts/thaitax_calc.py` (`land_building_tax`, `property_sale`, `lease_registration`).

## Step 1: Which property and what question

Use the profile first. Ask only for what is missing, up to 4 items:

- owner (individual or company, and which one);
- property type and actual use (home, rental, commercial, vacant, farm);
- appraised value (from the title deed office, the tax notice, or the Treasury Department's online lookup), or ask for a photo of the notice or title deed;
- for a sale: price, date acquired, how acquired (bought, inherited, gift), years in the house book, buyer type.

## Step 2: Calculate

- **Annual tax:** run `land_building_tax` per property. If the user has the local authority's notice, run `document-check` on it and compare. A different use classification or value is the usual cause; say which, and how to ask for a review (deadline: 30 days from the notice, verify).
- **Sale:** run `property_sale`. Show who usually pays what, and the seller's net. If the sale is within a few months of the 5-year mark, or of the reduced-fee expiry, say so in one line with the saving. This is a fact, not advice.
- **Lease:** run `lease_registration`. Rent received goes to `thai-personal-tax` (individual) or `thai-monthly-tax` (company, including withholding by tenants).

## Step 3: Deliver

A short table per property: tax or cost lines, amounts, who pays, due date. One line on what is uncertain. Sources. The disclaimer. Offer calendar reminders for the payment dates (only on a yes).

Ownership-structure or Land Code questions go to "for your lawyer" in one line; never assess them.
