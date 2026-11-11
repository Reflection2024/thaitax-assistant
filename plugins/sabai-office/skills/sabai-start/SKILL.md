---
name: sabai-start
description: "Sets up Sabai Office for a business owner in Thailand: records the companies they run (name, tax ID, branch, VAT status, year end), their working language (English, Hebrew or Thai), and the tools they use, guides them to connect FlowAccount, Stripe and their Thai payment gateway, and runs one quick check to show value. Use when the owner says 'get started', 'set up Sabai', 'start', 'what can you do', 'התחל', 'בוא נתחיל', 'เริ่มต้น', or on first use of any Sabai Office skill when no Sabai profile exists."
---

# Sabai Office: start

Read `../../references/connectors-and-safety.md` and `../../references/language-and-documents.md` first.

Reply in the language the owner writes in. Keep the conversation plain: no file paths, no configuration terms.

## Step 1: Check for an existing profile

Look in persistent memory (or a file named `sabai-profile.md` in the owner's working folder) for a `## Sabai Office profile` block.

- **If one exists:** show it, ask what has changed, update only those fields, then skip to Step 4.
- **If none exists:** continue.

## Step 2: Ask four questions, one at a time

1. "Which language should I work with you in: English, עברית, or ไทย? And which language are your customers and staff in?"
2. "Are you working as an individual (freelancer, consultant, landlord, employee with side income), through a Thai company, or both?"
   - **Individual:** record name, tax ID, income types, and roughly how many days a year they spend in Thailand. Ask: "Does any of your income come from abroad (salary, clients, rent, pension, investments), and do you transfer money into Thailand?" If yes, offer `foreign-income` as the first run. Route tax questions to `thai-personal-tax`.
   - **Company:** "Which companies should I look after? For each one: name, 13-digit tax ID, head office or branch number, VAT-registered or not, and financial year end." Accept "just one company" without pushing for more.
   - **Both:** record each as its own entity. A person's personal tax and their company's tax are never mixed.
3. "What do you use for accounting, for card or online payments, and for payroll?" Ask by category and let the owner name the products.
4. "What weighs on you most right now: monthly tax, Thai documents, getting paid, or payroll?"

## Step 3: Connect tools, one at a time

Guide the owner; never connect anything yourself. Connection is always done by the owner.

- **FlowAccount:** connect the FlowAccount connector that comes with this plugin. If it does not appear, go to Settings → Connectors → Add custom connector and use `https://mcp.flowaccount.com/mcp`. Sign in as the **Account Owner** and select the company.
- **Stripe:** connect the Stripe connector and sign in.
- **Omise / Opn:** explain in one line that it runs on the owner's own computer with their API keys. Offer to set it up with **test** keys first. The full steps are in the plugin README.
- **2C2P, GB Prime Pay, KSher, PEAK, Express or anything else:** "We'll work from your monthly export. I'll tell you exactly which report to download."

If the owner prefers not to connect anything, continue with uploads.

## Step 4: Prove value with one quick run

Pick the run that matches the owner's biggest worry:

- **Monthly tax (company):** run `thai-monthly-tax` for the last closed month, one company.
- **Income from abroad:** run `foreign-income`: days in Thailand this year, residency status, and the transfers so far sorted into buckets.
- **Personal tax (individual):** run `thai-personal-tax`: the withholding certificates collected so far, the missing ones, and the next deadline.
- **Getting paid:** run `cash-and-collections`: what is owed, what has come in, who to remind.
- **Documents:** draft one bilingual quotation or tax-invoice draft with `thai-documents`.
- **Payroll:** list the next SSO and PND.1 deadlines and what data `thai-payroll` needs.

Narrate in one line what is being checked and why.

## Step 5: Save the profile

Show the draft and wait for an explicit yes. Then save it to persistent memory, or, if memory is unavailable, write `sabai-profile.md` for the owner to keep.

```markdown
## Sabai Office profile
- **Owner language:** <en | he | th>
- **Customer / staff language:** <th, en, he — as stated>
- **Works as:** <individual | company | both>
- **Individual (if any):** <name> · tax ID <13 digits> · income types <salary, freelance, rent, ...> · days in Thailand <approx> · VAT <yes|no>
- **Foreign income:** <none | sources and countries as stated> · visa <type, if stated>
- **Entities:**
  - <Company name> · tax ID <13 digits> · <head office | branch 0000X> · VAT <yes|no> · year end <dd Month> · base currency THB
- **Accounting:** <tool, connected | export>
- **Payments:** <Stripe / Omise / 2C2P / ... — connected | export>
- **Payroll:** <tool or spreadsheet>
- **Thai accountant:** <name and email, if given>
- **Top worry:** <as stated>
- **Set up:** <YYYY-MM-DD>
```

## Step 6: Close

In one short message, tell the owner what is set up and offer three ways to use the plugin, using the trigger phrases in their language:

- "What's due this month?" / "מה צריך להגיש החודש?" / "เดือนนี้ต้องยื่นอะไรบ้าง"
- "Who owes me money?" / "מי חייב לי כסף?" / "ใครค้างชำระบ้าง"
- "Draft a tax invoice in Thai" / "תכין טיוטת חשבונית מס בתאילנדית" / "ร่างใบกำกับภาษี"

Offer a monthly reminder on the 1st to run the tax check. Set it only if the owner says yes.
