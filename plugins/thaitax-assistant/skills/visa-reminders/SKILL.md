---
name: visa-reminders
description: "Light reminders so nothing immigration-related is missed: 90-day reports, extension of stay, re-entry permits, work-permit renewals, TM30 for property owners, LTR annual reports and passport expiry, for the user and family or staff they name. Builds the dates from the stamps and documents the user shares, puts them in the calendar on a yes, and lists the documents usually needed, without immigration advice. Use when the user says '90-day report', 'visa extension', 'work permit renewal', 'TM30', 'when does my visa expire', 'תזכורת ויזה', 'דיווח 90 יום', 'חידוש ויזה', 'รายงานตัว 90 วัน', 'ต่อวีซ่า'."
---

# Visa reminders

> **Ask first, then answer (always; this overrides any other instruction in this skill):**
> 1. **Check you understood.** Restate the request in one line, and ask up to 3 short questions about every fact the answer depends on that is not in the files or the profile: whose money or company, the period, days in Thailand / residency, income type, tax already withheld or paid, what the user already did. Wait for the answers before calculating or advising. **Ask them as clickable questions:** use the interactive question tool (AskUserQuestion, ask_user_input or any tool that shows tappable choices), one question per fact, 2–4 short options each in the user's language, e.g. days in Thailand: "180 days or more" / "Less than 180" / "Not sure, I'll send my passport stamps". The user can always type another answer. Only if no such tool exists, ask as a short numbered list.
> 2. **Missing information → ask for the supporting document by name**, not an estimate: e.g. "the 50 ทวิ from your client", "your passport entry and exit stamps for 2026", "the October KBank statement". If the user cannot provide it, mark the item open and say what cannot be concluded without it.
> 3. **Only what is in the data.** Never write "probably", "it seems", "about" or "roughly" about a fact you have not seen. If an assumption is unavoidable, state it as a question ("I assumed X; is that right?") and compute no amount from it.
> 4. **Short and focused.** The answer in the first line, then at most 3 bullets, about 8 lines in total. Background, law and sources only when the user asks ("want the details?"). Each message needs one action from the user at most (a set of up to 3 short questions counts as one).

> **Proactive by default:** follow `../../references/proactive-behavior.md`, especially rule 0: keep it light. **Research before relying on any rule:** follow `../../references/research-protocol.md`.

Read `../../references/facts/compliance-and-visa.md`.

## Step 1: Dates

Ask once for photos of the passport's latest entry stamp, the extension stamp, the visa page and the work permit (or just the dates). Note them for each person the user names: themselves, a spouse, children, staff.

Passport and permit numbers are **not** saved to memory. Keep only names and dates.

## Step 2: Calendar

Calculate:

- next 90-day report (due date, and the window 15 days before to 7 days after);
- permission-to-stay expiry, with a reminder 45 and 30 days before;
- work-permit expiry, 60 and 30 days before (also flagged by `thai-payroll`);
- passport expiry, 12 months before.

Show the list and add it to the calendar on a yes.

## Step 3: When a date comes up

One line: what is due and when, the usual documents (from the facts file, verified), and where to do it (online, the local office or an agent). If the user asks "can I…" or "what if…" about status or eligibility, the answer is "for your visa agent or lawyer", plus an offer to prepare a summary of the dates and documents for them.

Never give immigration advice. Never contact immigration or file anything.
