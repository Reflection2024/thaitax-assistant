#!/bin/bash
# ThaiTax Assistant: one-click install for the ChatGPT desktop app (macOS).
# Adds the ThaiTax Assistant plugin list from GitHub, installs or updates the plugin,
# then restarts ChatGPT. Nothing else on your Mac is changed. Run it again any time to update.
clear
echo "ThaiTax Assistant · installing for ChatGPT"
echo "------------------------------------------"

CODEX=""
for c in "/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex" \
         "$HOME/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex"; do
  [ -x "$c" ] && CODEX="$c" && break
done
[ -z "$CODEX" ] && command -v codex >/dev/null 2>&1 && CODEX="$(command -v codex)"

if [ -z "$CODEX" ]; then
  echo
  echo "The ChatGPT desktop app was not found."
  echo "Install it from https://openai.com/chatgpt/download, open it once, then run this file again."
  echo
  read -n 1 -s -r -p "Press any key to close."
  exit 1
fi

set -e
"$CODEX" plugin marketplace add Reflection2024/thaitax-assistant
"$CODEX" plugin marketplace upgrade thaitax-assistant >/dev/null 2>&1 || true
"$CODEX" plugin add thaitax-assistant@thaitax-assistant
set +e

echo
echo "Done. ThaiTax Assistant is installed."
if pgrep -xq "ChatGPT"; then
  echo "Restarting ChatGPT so it loads the plugin..."
  osascript -e 'quit app "ChatGPT"' >/dev/null 2>&1
  sleep 3
fi
open -a "ChatGPT" >/dev/null 2>&1
echo
echo "In ChatGPT: open a new chat and type \"Get started\" (or in your own language)."
echo
read -n 1 -s -r -p "Press any key to close this window."
