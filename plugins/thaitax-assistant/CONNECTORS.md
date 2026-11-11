# Connectors

| Category | Included | Notes |
|---|---|---|
| Accounting | FlowAccount (official MCP, `https://mcp.flowaccount.com/mcp`) | OAuth. The Account Owner signs in; access is per company. |
| Card / online payments | Stripe (official MCP) | OAuth. |
| Thai payment gateway | Omise / Opn (local MCP, optional) | API keys on the owner's computer. Start with test keys. |
| Other gateways and accounting tools | 2C2P, GB Prime Pay, KSher, PEAK, Express, SMLSoft | Monthly export, read by `thai-export-reader`. PEAK offers an API on Pro Plus and above. |
| Bank | (none) | Statement PDF or Excel upload. |

ThaiTax Assistant works with whatever the owner already uses and never recommends switching tools.
