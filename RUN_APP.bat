@echo off
title AI Resume Analyzer & Career Copilot
cd /d "%~dp0"
echo ========================================================
echo   AI RESUME ANALYZER & CAREER COPILOT - BY ANUPAM CHATTERJEE
echo   Starting Local Application Server...
echo ========================================================
echo.
echo Opening browser at http://localhost:8501 ...
timeout /t 2 >nul
start http://localhost:8501
"%~dp0venvapp\Scripts\streamlit.exe" run App\App.py
pause
