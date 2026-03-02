# Stellar-Journal dev startup - single script, no sub-scripts
$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
$backendDir = Join-Path $root "backend"
$frontendDir = Join-Path $root "frontend"

Write-Host "Checking environment..." -ForegroundColor Cyan
if (!(Get-Command node -ErrorAction SilentlyContinue)) { Write-Host "Node.js not found." -ForegroundColor Red; exit 1 }
if (!(Get-Command python -ErrorAction SilentlyContinue)) { Write-Host "Python not found." -ForegroundColor Red; exit 1 }

# Backend: cd, venv, uvicorn (run in new window)
$backendCmd = "Set-Location '" + $backendDir + "'; if (Test-Path venv) { & .\venv\Scripts\Activate.ps1 } else { python -m venv venv; & .\venv\Scripts\Activate.ps1; pip install -r requirements.txt }; uvicorn app.main:app --reload"
Write-Host "Starting backend..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCmd

Start-Sleep -Seconds 3

# Frontend: cd, npm install if needed, npm run dev (run in new window)
$frontendCmd = "Set-Location '" + $frontendDir + "'; if (!(Test-Path node_modules)) { npm install }; npm run dev"
Write-Host "Starting frontend..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendCmd

Write-Host "Done. Frontend: http://localhost:3000  Backend: http://localhost:8000" -ForegroundColor Cyan
