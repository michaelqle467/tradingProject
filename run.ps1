#!/usr/bin/env pwsh
# Convenience PowerShell script to activate venv and run the app
if (-not (Test-Path -Path .venv)) {
    Write-Host "Virtual environment not found. Creating .venv..."
    python -m venv .venv
}

Write-Host "Activating .venv..."
.\.venv\Scripts\Activate.ps1

Write-Host "Installing requirements (if needed)..."
python -m pip install --upgrade pip
pip install -r requirements.txt

Write-Host "Starting Flask app..."
python app.py
