@echo off
title Khmer Cartoon Pill Studio (Nano Banana)
echo =======================================================
echo   Checking for latest updates from GitHub...
echo =======================================================
git pull origin main
echo.
echo =======================================================
echo   Starting Khmer Cartoon Pill Studio Dashboard...
echo =======================================================
start http://localhost:5000
python web_ui.py
pause
