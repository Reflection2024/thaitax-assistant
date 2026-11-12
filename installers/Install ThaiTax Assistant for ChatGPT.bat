@echo off
chcp 65001 >nul
title ThaiTax Assistant - install for ChatGPT
echo ThaiTax Assistant - installing for ChatGPT
echo ------------------------------------------
rem Adds the ThaiTax Assistant plugin list from GitHub and installs or updates the plugin.
rem Nothing else on your computer is changed. Run it again any time to update.

set "CODEX="
for /f "delims=" %%i in ('where codex 2^>nul') do if not defined CODEX set "CODEX=%%i"
if not defined CODEX for /f "delims=" %%i in ('dir /b /s "%LOCALAPPDATA%\Programs\ChatGPT\codex.exe" 2^>nul') do if not defined CODEX set "CODEX=%%i"
if not defined CODEX (
  where npx >nul 2>nul && set "CODEX=npx -y @openai/codex"
)
if not defined CODEX (
  echo.
  echo Codex was not found. Install the ChatGPT desktop app from https://openai.com/chatgpt/download
  echo and open it once, or install Node.js from https://nodejs.org, then run this file again.
  echo.
  pause
  exit /b 1
)

call %CODEX% plugin marketplace add Reflection2024/thaitax-assistant || goto :fail
call %CODEX% plugin marketplace upgrade thaitax-assistant >nul 2>nul
call %CODEX% plugin add thaitax-assistant@thaitax-assistant || goto :fail

echo.
echo Done. ThaiTax Assistant is installed.
echo Close ChatGPT completely, open it again, start a new chat and type "Get started".
echo.
pause
exit /b 0

:fail
echo.
echo Something went wrong. Please send a screenshot of this window to the ThaiTax Assistant team.
pause
exit /b 1
