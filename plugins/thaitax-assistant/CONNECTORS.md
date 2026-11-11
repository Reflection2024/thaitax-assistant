# Connectors

Every connection is made by the user, in **Settings → Connectors**, with their own sign-in. All are optional.

| Category | Tool | Status | What it unlocks |
|---|---|---|---|
| Accounting | FlowAccount (official MCP, `https://mcp.flowaccount.com/mcp`) | Included | Sales, purchases, receivables, tax reports; draft documents on a yes |
| Card / online payments | Stripe (official MCP) | Included | Payments, payouts, fees, disputes |
| Email | Gmail or Outlook | User connects | Invoices, receipts and 50 ทวิ found in the inbox; reminder drafts |
| Calendar | Google Calendar or Outlook | User connects | Thai tax deadline reminders (on a yes) |
| Cloud drive | Google Drive or OneDrive | User connects | Statements and documents read; monthly packs saved |
| Thai payment gateway | Omise / Opn (local MCP) | Optional, on the user's computer | Thai card and PromptPay payments (test keys first) |
| Phone photos | Claude mobile app: share from gallery | No connection needed | Receipt and tax-invoice capture (`receipt-capture`) |
| Family budget, advanced | Actual Budget (self-hosted) via community `actual-mcp` | Optional, for advanced users | Transactions, categories and budgets in your own Actual server |
| Other tools | PEAK, Express, SMLSoft, 2C2P, GB Prime Pay, KSher, banks | Export file | Read by `thai-export-reader` |

ThaiTax Assistant works with whatever the user already uses and never recommends switching tools.

## Actual Budget (advanced, optional)

`family-budget` works without it. For a full budgeting app you host yourself:

1. Run an Actual server ([actualbudget.org](https://actualbudget.org)).
2. Import: `python3 -I scripts/budget.py actual-export transactions.csv --out actual_import.csv`, then in Actual: Account → Import.
3. To let Claude read it directly, add the community MCP server (MIT, [s-stefanov/actual-mcp](https://github.com/s-stefanov/actual-mcp)) to your Claude settings on your own computer:

```json
{"mcpServers":{"actual":{"command":"npx","args":["-y","actual-mcp","--enable-write"],
  "env":{"ACTUAL_SERVER_URL":"https://your-actual-server","ACTUAL_PASSWORD":"…","ACTUAL_BUDGET_SYNC_ID":"…"}}}}
```

Leave out `--enable-write` to keep it read-only. It is a community project, not part of ThaiTax Assistant; review it before use.
