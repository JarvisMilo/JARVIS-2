$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Test-Path ".venv")) {
    Write-Host "Creando entorno virtual..." -ForegroundColor Cyan
    python -m venv .venv
}

Write-Host "Activando entorno virtual..." -ForegroundColor Cyan
. .\.venv\Scripts\Activate.ps1

Write-Host "Instalando/verificando dependencias..." -ForegroundColor Cyan
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if (-not $env:OPENAI_API_KEY) {
    Write-Host ""
    Write-Host "Falta OPENAI_API_KEY." -ForegroundColor Yellow
    Write-Host 'Puedes usar un archivo .env con OPENAI_API_KEY=TU_API_KEY'
    Write-Host 'o configurar PowerShell con: $env:OPENAI_API_KEY="TU_API_KEY"'
    exit 1
}

Write-Host ""
Write-Host "Iniciando JARVIS Nivel 1..." -ForegroundColor Green
python main.py
