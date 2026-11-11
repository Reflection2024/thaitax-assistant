---
name: ask-thai-tax
description: "Answers any question about Thai tax, payroll, company reporting or foreign income that is not a fixed workflow, by researching current official sources (Revenue Department, Royal Gazette, SSO, DBD, BOI) and recent professional notes in Thai and English, cross-checking them, and replying with a clear answer, the figures, what is uncertain, and cited sources. Uses a connected research tool (such as Perplexity) or deep research for complex questions. Always use this skill before answering any question about tax for a person or company in Thailand, including 'what tax will I pay this month' or 'how much tax do I owe', even when it comes with other requests or files. Use for questions like 'do I need to…', 'is it true that…', 'what's the rule for…', 'how is X taxed', 'what changed this year', 'האם אני צריך…', 'מה הכלל לגבי…', 'מה השתנה השנה', 'ต้อง…ไหม', 'กฎเรื่อง…คืออะไร'."
---

# Ask a Thai tax question

> **Ask first, then answer (always; this overrides any other instruction in this skill):**
> 1. **Check you understood.** Restate the request in one line, and ask up to 3 short questions about every fact the answer depends on that is not in the files or the profile: whose money or company, the period, days in Thailand / residency, income type, tax already withheld or paid, what the user already did. Wait for the answers before calculating or advising.
> 2. **Missing information → ask for the supporting document by name**, not an estimate: e.g. "the 50 ทวิ from your client", "your passport entry and exit stamps for 2026", "the October KBank statement". If the user cannot provide it, mark the item open and say what cannot be concluded without it.
> 3. **Only what is in the data.** Never write "probably", "it seems", "about" or "roughly" about a fact you have not seen. If an assumption is unavoidable, state it as a question ("I assumed X; is that right?") and compute no amount from it.
> 4. **Short and focused.** The answer in the first line, then at most 3 bullets, about 8 lines in total. Background, law and sources only when the user asks ("want the details?"). Each message needs one action from the user at most (a set of up to 3 short questions counts as one).

Read `../../references/research-protocol.md` and `../../references/facts/_index.md` first. Use the fact file for the topic as the starting point, never as the final word.

## Step 1: Understand the situation

Restate the question in one line. If the answer depends on facts you don't have, ask for them, up to 3 questions:

- individual or company;
- resident days;
- VAT-registered or not;
- the type of income;
- the country involved;
- BOI status.

Use the profile first; ask only what is missing.

## Step 2: Research

Follow the research protocol: research connector, then web search and fetching the pages, then deep research for multi-part questions. Search in Thai and English, and open the official page for every figure. Run independent searches in parallel.

## Step 3: Answer

- **Answer:** 2–4 sentences, in the user's language and in plain words.
- **Figures and conditions:** rates, thresholds and dates, each with its source and date. Run the numbers with `../../scripts/thaitax_calc.py` when there is a calculation.
- **What it means for you:** apply the answer to the user's profile, if relevant.
- **Uncertain or depends on:** who confirms it (accountant, lawyer, RD 1161).
- **Next steps:** up to 3 (per `../../references/proactive-behavior.md`).
- **Sources:** a list of titles and links.
- **Disclaimer.**

If the answer shows that a plugin fact file is out of date, say so and offer to record it for `tax-facts-update`.
