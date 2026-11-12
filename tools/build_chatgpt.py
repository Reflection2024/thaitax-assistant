#!/usr/bin/env python3
"""Build the ChatGPT edition of ThaiTax Assistant from the Claude plugin.

    python3 tools/build_chatgpt.py

Source of truth: plugins/thaitax-assistant (the Claude plugin). This script copies it to
chatgpt/thaitax-assistant, swaps Claude-specific wording for ChatGPT wording, writes the
ChatGPT plugin manifests, and zips docs/thaitax-assistant-chatgpt.zip. Run it after every
change to the Claude plugin so both editions stay identical in substance.
"""
from __future__ import annotations

import json
import re
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "plugins" / "thaitax-assistant"
OUT = ROOT / "chatgpt" / "thaitax-assistant"
ZIP = ROOT / "docs" / "thaitax-assistant-chatgpt.zip"

# Ordered: specific phrases first, the generic "Claude" -> "ChatGPT" last.
SWAPS = [
    ("AskUserQuestion, ask_user_input or any tool that shows tappable choices", "ChatGPT's tappable choice buttons or any tool that shows tappable choices"),
    ("${CLAUDE_PLUGIN_ROOT}/", ""),
    ("Claude's settings (**Settings → Connectors**)", "ChatGPT's settings (**Settings → Apps**)"),
    ("Publish `dashboard.html` as a private artifact page (or send the file if artifacts are", "Show `dashboard.html` in canvas or as a downloadable page (or send the file if that is"),
    ("Publish the page as a private artifact when an artifact tool is available, so the user can open it any time and share it if they want; otherwise send the HTML file.",
     "Give the page as a downloadable HTML file (or show it in canvas), so the user can open it any time and share it if they want."),
    ("a Sheets artifact or an .xlsx the user keeps", "an .xlsx the user keeps"),
    ("(chats, artifacts, memory)", "(chats, files, memory)"),
    ("connect it to Claude with the community `actual-mcp` server", "connect it with the community `actual-mcp` server"),
    ("does not make Claude the user's tax adviser", "does not make the assistant the user's tax adviser"),
    ("Claude reads saved preferences in every new chat", "ChatGPT reads saved memories in every new chat"),
    ("`.claude-plugin/plugin.json`", "`plugin.json`"),
    ("in **Settings → Connectors**, with their own sign-in", "in ChatGPT, with their own sign-in: **Plugins → + → Add custom MCP server** for FlowAccount (`https://mcp.flowaccount.com/mcp`) and Stripe (`https://mcp.stripe.com`), or the ready-made app in **Settings → Apps** when one exists"),
    ("Open **Settings → Connectors**, find *X*, press **Connect** and sign in.", "Open **Plugins → + → Add custom MCP server** (or **Settings → Apps** if *X* is listed there), enter its MCP address, press **Connect** and sign in."),
    ("In Claude use the scheduled-task tool; in ChatGPT use Tasks.", "Use ChatGPT Tasks."),
    ("(Claude: scheduled tasks; ChatGPT: Tasks)", "(ChatGPT Tasks)"),
    ("(Claude scheduled tasks / ChatGPT Tasks)", "(ChatGPT Tasks)"),
    ("(Claude scheduled tasks, ChatGPT Tasks)", "(ChatGPT Tasks)"),
    ("Claude Code", "Codex"),
    ("Claude", "ChatGPT"),
]

CHATGPT_NOTE = """
> **ChatGPT edition.** Same assistants, same rules, built from the Claude plugin. FlowAccount and Stripe connect as MCP servers (declared in `mcp.json`; in ChatGPT: Plugins → + → Add custom MCP server, then sign in). Without a connection, upload exports and statements: every skill also works from files.
"""


def build() -> dict:
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(SRC, OUT, ignore=shutil.ignore_patterns(".claude-plugin", ".mcp.json", "__pycache__", "*.pyc", ".DS_Store"))
    changed = 0
    for p in OUT.rglob("*.md"):
        s = p.read_text(encoding="utf-8")
        t = s
        for a, b in SWAPS:
            t = t.replace(a, b)
        if t != s:
            p.write_text(t, encoding="utf-8")
            changed += 1
    readme = OUT / "README.md"
    readme.write_text(readme.read_text(encoding="utf-8").replace("\n", "\n" + CHATGPT_NOTE, 1), encoding="utf-8")

    src_manifest = json.loads((SRC / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    manifest = {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        "name": src_manifest["name"],
        "version": src_manifest["version"],
        "description": src_manifest["description"],
        "author": src_manifest.get("author", {}),
        "keywords": src_manifest.get("keywords", []),
    }
    (OUT / "plugin.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    src_mcp = json.loads((SRC / ".mcp.json").read_text(encoding="utf-8"))["mcpServers"]
    mcp = {"$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
           "mcpServers": {k: {"type": "streamable-http", "url": v["url"]} for k, v in src_mcp.items()}}
    (OUT / "mcp.json").write_text(json.dumps(mcp, indent=2) + "\n", encoding="utf-8")
    (OUT / ".codex-plugin").mkdir(exist_ok=True)
    compat = {k: v for k, v in manifest.items() if k != "$schema"}
    compat["skills"] = "./skills/"
    (OUT / ".codex-plugin" / "plugin.json").write_text(json.dumps(compat, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Checks: nothing Claude-specific left in instructions, every skill well formed.
    leftovers = [str(p.relative_to(OUT)) for p in OUT.rglob("*.md") if p.name != "README.md" and re.search(r"\bClaude\b|AskUserQuestion|CLAUDE_PLUGIN_ROOT|\bartifact", p.read_text(encoding="utf-8"))]
    skills = sorted(OUT.glob("skills/*/SKILL.md"))
    for sk in skills:
        head = sk.read_text(encoding="utf-8").split("---")[1]
        name = re.search(r"^name: (.+)$", head, re.M).group(1).strip()
        desc = re.search(r'^description: "(.*)"$', head, re.M).group(1)
        assert name == sk.parent.name, sk
        assert re.fullmatch(r"[a-z0-9-]{1,64}", name), name
        assert 0 < len(desc) <= 1024, (sk, len(desc))

    ZIP.unlink(missing_ok=True)
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(OUT.rglob("*")):
            if p.is_file():
                z.write(p, p.relative_to(OUT))
    return {"skills": len(skills), "files_reworded": changed, "leftovers": leftovers, "zip": str(ZIP.relative_to(ROOT)), "zip_mb": round(ZIP.stat().st_size / 1e6, 1)}


if __name__ == "__main__":
    r = build()
    print(json.dumps(r, ensure_ascii=False, indent=1))
    sys.exit(1 if r["leftovers"] else 0)
