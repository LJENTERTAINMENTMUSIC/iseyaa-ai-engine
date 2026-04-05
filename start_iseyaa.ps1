# ISEYAA Launch 2.0 — Unified Automatic Startup
# One-click setup and launch for the ISEYAA State Operating System

Clear-Host
Write-Host "🌿 Starting ISEYAA State Operating System Suite..." -ForegroundColor Green
Write-Host "----------------------------------------------------" -ForegroundColor Gray

# 1. Verification & Auto-Installation
Write-Host "📡 Verifying dependencies..." -ForegroundColor Cyan
if (Get-Command pnpm -ErrorAction SilentlyContinue) {
    Write-Host "✓ pnpm detected. Updating local packages..." -ForegroundColor Gray
    pnpm install --silent
} else {
    Write-Host "⚠ pnpm not found. Please install pnpm (npm install -g pnpm)." -ForegroundColor Red
    exit 1
}

# 2. Environment Synchronization
Write-Host "🔑 Syncing environment variables from Vercel..." -ForegroundColor Cyan
if (Test-Path ".vercel\project.json") {
    pnpm env:pull
} else {
    Write-Host "⚠ Local project not linked to Vercel. Skipping secret sync." -ForegroundColor Yellow
}

# 3. Database Synchronization (Optional/Automatic)
Write-Host "🗄️ Checking Supabase Schema..." -ForegroundColor Cyan
pnpm db:sync

# 4. Unified Startup Sequence
Write-Host "🎨 Launching Unified Development Suite (Turbo)..." -ForegroundColor Green
Write-Host "----------------------------------------------------" -ForegroundColor Gray
Write-Host "AI Engine:     http://localhost:8000" -ForegroundColor Gray
Write-Host "Traveler Hub:  http://localhost:3000" -ForegroundColor Gray
Write-Host "Dashboard:     http://localhost:3001" -ForegroundColor Gray
Write-Host "----------------------------------------------------" -ForegroundColor Gray

# Launch everything in a single, unified terminal session
pnpm dev
