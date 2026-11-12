---
name: automations-reminders-and-scheduled-tasks
description: "Sets up, lists and changes the automatic help a ThaiTax Assistant user can switch on: reminders 3 days before each tax deadline, the monthly pack on the 1st, a weekly email sweep for tax invoices, receipts and 50 ทวิ, the 25th send-your-documents nudge, monthly dashboard refresh, payroll prep before payday, overdue invoices, supplier payment checks, a quarterly accountant check, visa and work-permit dates, the 180-day counter, year-end tax saving, the annual return pack and property tax dates. Creates scheduled tasks only for what the user picks; every run prepares and drafts, never sends, files or pays. Use when the user says 'reminders', 'automate', 'every month', 'remind me', 'what runs automatically', 'stop the reminders', 'תזכורות', 'אוטומציה', 'כל חודש', 'תזכיר לי', 'เตือนความจำ', 'ทุกเดือน', or at the end of setup."
---

# Automations, reminders and scheduled tasks

> **Ask first, then answer (always; this overrides any other instruction in this skill):**
> 1. **Check you understood.** Restate the request in one line, and ask **every** question needed to reach the best, complete result, about every fact the answer depends on that is not in the files or the profile (there is no limit on the number of questions): whose money or company, the period, days in Thailand / residency, income type, tax already withheld or paid, what the user already did. Ask in rounds of up to 4 questions (the most important first); after each round, ask the next round until nothing the result depends on is missing. Wait for the answers before calculating or advising. **Ask them as clickable questions:** use the interactive question tool (ChatGPT's tappable choice buttons or any tool that shows tappable choices), one question per fact, 2–4 short options each in the user's language, e.g. days in Thailand: "180 days or more" / "Less than 180" / "Not sure, I'll send my passport stamps". The user can always type another answer. Only if no such tool exists, ask as a short numbered list.
> 2. **Missing information → ask for the supporting document by name**, not an estimate: e.g. "the 50 ทวิ from your client", "your passport entry and exit stamps for 2026", "the October KBank statement". If the user cannot provide it, mark the item open and say what cannot be concluded without it.
> 3. **Only what is in the data.** Never write "probably", "it seems", "about" or "roughly" about a fact you have not seen. If an assumption is unavoidable, state it as a question ("I assumed X; is that right?") and compute no amount from it.
> 4. **Short and focused.** The answer in the first line, then at most 3 bullets, about 8 lines in total. Background, law and sources only when the user asks ("want the details?"). Questions are not limited; the final answer itself stays short.

> **Proactive by default:** follow `../../references/proactive-behavior.md`: ask for what is missing, run `document-check` on every document received, warn about deadlines and risks ahead, keep the request list, and end with up to three next steps. **Research before relying on any rule:** follow `../../references/research-protocol.md` (research connector or web search, official Thai sources first, Thai and English queries, cited sources).

Read `../../references/automations.md` (the catalog), `../../references/connectors-and-safety.md` and `../../references/language-and-documents.md` first.

## Set up

1. Read the profile. If there is none, run `thaitax-start` first.
2. Choose the 3 to 5 automations from the catalog that fit this person or company, plus "Show me all". Ask once, as a clickable multi-select question in the user's language, with the day and one-line result for each.
3. For each one picked: confirm the day and time in one line, then create the scheduled task with the app's scheduling tool (ChatGPT Tasks). The task prompt is standalone, in the user's language, names the person or company, the skill to run, and says that nothing is sent, filed or paid without the user's yes.
4. Deadline reminders can be calendar events instead, if the user prefers: show the list of dates first and create them only on a yes.
5. Save to the profile: `- **Automations:** <name — day/time>` per task. Answer with a short list of what will run and when, and how to change it ("say *stop the email sweep*").

## Change or stop

- "What runs automatically?": list the tasks from the profile and the app, with the next run.
- "Move", "pause", "stop": change or remove that task; confirm each removal in one line before doing it; update the profile.

## If the app cannot schedule

Say so in one line. Offer calendar events with reminders for dated items, and the one-word commands for the rest ("monthly pack", "what's due", "check my email").

## Never

- Never create a task the user did not pick.
- Never let a run send an email, submit a form, pay, delete or move money. Runs end with a message the user can approve.
