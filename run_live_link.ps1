# Helper script to launch Streamlit and the public Cloudflare tunnel
$projectDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $projectDir

Write-Host "1. Starting Streamlit server in background..." -ForegroundColor Cyan
Start-Process -FilePath "$projectDir\venvapp\Scripts\streamlit.exe" -ArgumentList "run App/App.py --server.headless true" -WindowStyle Hidden

Start-Sleep -Seconds 3

Write-Host "2. Starting Cloudflare Public Tunnel..." -ForegroundColor Green
Write-Host "Look for the public HTTPS URL (e.g. https://*.trycloudflare.com) below:`n" -ForegroundColor Yellow

& "$projectDir\cloudflared.exe" tunnel --url http://localhost:8501
