# ISEYAA Launch 1.0 — Unified Startup Script
# This script launches both the AI Engine (Backend) and the Traveler Portal (Frontend)

Write-Host "🌿 Starting ISEYAA State Operating System..." -ForegroundColor Green

# 1. Start Backend (FastAPI)
Write-Host "📡 Launching ISEYAA AI Engine on http://localhost:8000..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python main.py"

# 2. Start Frontend (Next.js)
Write-Host "🎨 Launching ISEYAA Traveler Portal on http://localhost:3000..." -ForegroundColor Cyan
if (Test-Path "apps/web") {
    Set-Location "apps/web"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm run dev"
    Set-Location "..\.."
} else {
    Write-Host "⚠️ Warning: apps/web not found. Please ensure the monorepo structure is intact." -ForegroundColor Yellow
}

Write-Host "🚀 Launch Sequence Complete. Access your dashboard at http://localhost:3000" -ForegroundColor Green
Write-Host "Press any key to close this launcher (the servers will keep running in their own windows)."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
