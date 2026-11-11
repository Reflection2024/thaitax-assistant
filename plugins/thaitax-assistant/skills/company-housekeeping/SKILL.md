---
name: company-housekeeping
description: "Keeps a Thai company in good standing without the owner having to remember anything: builds the company's yearly calendar (audit, AGM within 4 months, financial statements to DBD within a month of the AGM, shareholder list บอจ.5, PND.50/51, licence renewals, BOI reports), tracks changes that must be registered within 14 days (directors, address, signatories, capital), prepares the paperwork drafts (AGM notice and minutes, shareholder list data) for the accountant or lawyer, and puts every date in the calendar on a yes. Use when the user says 'company compliance', 'AGM', 'DBD filing', 'shareholder list', 'change director', 'what does my company need to do this year', 'ניהול שוטף של החברה', 'אסיפה שנתית', 'הגשה לרשם החברות', 'ประชุมผู้ถือหุ้น', 'ส่งงบ DBD', 'บอจ.5'."
---

# Company housekeeping

> **Ask first, then answer (always; this overrides any other instruction in this skill):**
> 1. **Check you understood.** Restate the request in one line, and ask **every** question needed to reach the best, complete result, about every fact the answer depends on that is not in the files or the profile (there is no limit on the number of questions): whose money or company, the period, days in Thailand / residency, income type, tax already withheld or paid, what the user already did. Ask in rounds of up to 4 questions (the most important first); after each round, ask the next round until nothing the result depends on is missing. Wait for the answers before calculating or advising. **Ask them as clickable questions:** use the interactive question tool (AskUserQuestion, ask_user_input or any tool that shows tappable choices), one question per fact, 2–4 short options each in the user's language, e.g. days in Thailand: "180 days or more" / "Less than 180" / "Not sure, I'll send my passport stamps". The user can always type another answer. Only if no such tool exists, ask as a short numbered list.
> 2. **Missing information → ask for the supporting document by name**, not an estimate: e.g. "the 50 ทวิ from your client", "your passport entry and exit stamps for 2026", "the October KBank statement". If the user cannot provide it, mark the item open and say what cannot be concluded without it.
> 3. **Only what is in the data.** Never write "probably", "it seems", "about" or "roughly" about a fact you have not seen. If an assumption is unavoidable, state it as a question ("I assumed X; is that right?") and compute no amount from it.
> 4. **Short and focused.** The answer in the first line, then at most 3 bullets, about 8 lines in total. Background, law and sources only when the user asks ("want the details?"). Questions are not limited; the final answer itself stays short.

> **Proactive by default:** follow `../../references/proactive-behavior.md`. **Research before relying on any rule:** follow `../../references/research-protocol.md`.

Read `../../references/facts/compliance-and-visa.md` and `../../references/facts/corporate.md`.

## Step 1: The company's facts

From the profile, plus at most 4 questions:

- year end;
- auditor;
- last AGM date and last DBD filing (or "don't know": offer to read it from the DBD record if the user can download it, or from the company affidavit, หนังสือรับรอง);
- licences held, with their expiry dates (hotel, food, tourism, alcohol, BOI);
- planned changes (new director, moving office, a share transfer).

## Step 2: The calendar

Build this year's calendar with real dates (`../../scripts/thaitax_calc.py` for deadlines where it applies). Show it as a short table, then offer, once, to add everything to the calendar with reminders 14 days and 3 days before (only on a yes).

## Step 3: Paperwork, when a date comes up

Prepare drafts for the accountant or lawyer to finalise:

- AGM notice and agenda;
- minutes;
- shareholder list data (บอจ.5);
- directors' resolution for a change;
- checklist of documents to bring to DBD.

Use Thai with English or Hebrew beside it, built with `../../scripts/make_document.js` or as a short DOCX.

## Step 4: Watch for

- A change mentioned in passing ("we're moving office next month", "my partner is leaving"): tell the user, in one line, that it must be registered within 14 days, and offer the checklist.
- An overdue filing: give the fine risk in one line, and the next step.
- Dates promised by the accountant: add them to the request list.

Never assess foreign-ownership structure, nominee or Foreign Business Act questions. Those go to "for your lawyer" in one line.
