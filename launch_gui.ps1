# Database Migration POC - PowerShell GUI Launcher
# This script activates the virtual environment and launches the GUI

Write-Host "🚀 Starting Database Migration POC GUI..." -ForegroundColor Yellow
Write-Host ""

# Change to the project directory
Set-Location -Path $PSScriptRoot

# Activate virtual environment
Write-Host "📦 Activating virtual environment..." -ForegroundColor Cyan
& ".\db-venv\Scripts\Activate.ps1"

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Virtual environment activated" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "🖥️ Launching GUI application..." -ForegroundColor Cyan
    & python gui.py
    
    Write-Host ""
    Write-Host "👋 GUI application closed." -ForegroundColor Yellow
} else {
    Write-Host "❌ Failed to activate virtual environment" -ForegroundColor Red
    Write-Host "Please ensure the db-venv folder exists and contains a valid Python virtual environment."
}

Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
