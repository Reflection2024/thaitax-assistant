# Intake checklist: everything ThaiTax Assistant needs from the user

`thaitax-start` collects these details **in short rounds** (up to 4 clickable questions per round, as many rounds as needed, in the user's language). Ask only the rounds that apply. Accept "I don't know" or "later": mark the item as missing and move on. Never ask for passwords, card numbers or full bank-account numbers.

## Round 1: About you (everyone)

1. Preferred language for the user (English, Hebrew, Thai), and the language of customers and staff.
2. Full name, and whether a male or female polite form should be used in Thai letters (ครับ / ค่ะ).
3. Working as: an **individual**, through a **Thai company**, or **both**.
4. Thai accountant: name and email, if there is one. The user says whether ThaiTax Assistant may prepare packs for them.
5. Preferred way to receive work: spreadsheet, Word or PDF, in chat, or saved to the cloud drive.

## Round 2: Individual (if applicable)

1. Thai tax ID (13 digits), or "not registered yet".
2. Nationality(ies) and visa type (LTR, DTV, retirement, work and so on). Visa start date if LTR.
3. Roughly how many days in Thailand this year and last year, or permission to count from a travel list the user provides.
4. Marital status. Spouse: Thai or foreign, has income or not, lives in Thailand or not. Number of children (and birth years). Parents aged 60+ supported.
5. **Income types:** Thai salary, freelance or consulting fees, rent (property type and location), Thai dividends or interest, business, **income from abroad** (salary, clients, rent, pension, investments: which countries).
6. Transfers into Thailand: which foreign accounts or services (bank, Wise, Revolut), and whether savings from before 2024 exist.
7. Thai bank used for refunds (PromptPay linked to the tax ID: yes or no).
8. Allowance items: Thai life or health insurance, RMF/SSF/Thai ESG, Thai mortgage, donations, social security (if employed).
9. Last return filed (year and form), and any PND.94 filed this year.

## Round 3: Each company (if applicable; repeat per company)

1. Company name (Thai and English), 13-digit tax ID, head office or branch code, registered address exactly as on the certificate.
2. VAT registered (yes/no, since when). SME (paid-up capital ≤ THB 5m and revenue ≤ THB 30m): yes, no, or unknown.
3. Financial year end; who audits; DBD filing done for last year.
4. Business activity in a sentence, and BOI or Treaty of Amity status, if any (recorded, not assessed).
5. **Tools:** accounting (FlowAccount, PEAK, Express, other), card and online payments (Stripe, Omise, 2C2P, GB Prime Pay, KSher), payroll (tool or spreadsheet), bank(s).
6. Customers: mostly Thai companies, Thai individuals, or foreigners? This decides withholding and language.
7. Regular payments: rent, contractors, foreign services (Google, Meta, AWS, SaaS). This decides PND.3/53/54 and PP.36.
8. Staff: number, Thai or foreign, work-permit expiry dates for foreigners, SSO registered (yes/no), province and district of work.
9. Whether e-Withholding Tax and e-Tax Invoice are used (yes, no, or unknown).
10. Who files today, and how (the accountant, online or paper). Does the user have **their own** RD e-Filing and DBD logins? Does the accountant pay taxes on the user's behalf? This decides whether `accountant-check` is offered.

## Round 3b: Optional extras (ask in one line, skip if not wanted)

- Properties owned in Thailand (type, use, owner): for land-tax reminders and sale costs.
- Visa and work-permit dates for the user and family: for reminders only.
- Company licences with expiry dates.

## Round 4: Connections (everyone)

Walk through the table in `welcome-guide.md` Part 2. For each item record **connected**, **will connect later**, **not used**, or **export instead**. For phone photos, show the 4-step how-to once.

## Round 5: Automations and permissions

1. Which automations to switch on (one multi-select question; options and rules in `automations.md`): deadline reminders, monthly pack, weekly email sweep, the 25th nudge, dashboard refresh, payroll prep, and the others that fit the profile. Calendar reminders: which calendar.
2. Where documents come from for the runs: Gmail, a Google Drive folder (which one), FlowAccount, uploads. Which bank sends the monthly e-statement. Which family members to track for visas.
3. Times: keep the suggested day and time or pick another.
3. Standing permissions are **never** assumed. Every send, post, create or pay still needs a yes at the time. State this once, plainly.

## What gets saved

Save only what the user gave, in the profile block in `thaitax-start` Step 5. **Never save:** passport numbers, ID-card numbers of staff, full bank-account numbers, salaries, or anything the user asks not to keep. Those stay in the working files for the task in hand. The 13-digit tax ID of the user or their company may be saved, because every form needs it; ask first.
