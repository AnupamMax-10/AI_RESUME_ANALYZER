@echo off
cd /d "%~dp0"

echo 1. Starting Streamlit application in background...
start "" /b "%~dp0venvapp\Scripts\streamlit.exe" run App\App.py --server.headless true

timeout /t 3 >nul

echo 2. Starting Cloudflare Public Tunnel...
echo Look for your public HTTPS link (https://*.trycloudflare.com) below:
echo.

"%~dp0cloudflared.exe" tunnel --url http://localhost:8501
pause
