$ErrorActionPreference = "Stop"

if (-not (Test-Path ".venv")) {
    Write-Host "Creando entorno virtual..." -ForegroundColor Cyan
    python -m venv .venv
}

Write-Host "Activando entorno virtual..." -ForegroundColor Cyan
. .\.venv\Scripts\Activate.ps1

Write-Host "Instalando dependencias..." -ForegroundColor Cyan
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if (-not $env:OPENAI_API_KEY) {
    Write-Host ""
    Write-Host "Falta OPENAI_API_KEY." -ForegroundColor Yellow
    Write-Host 'Configúrala con: $env:OPENAI_API_KEY="TU_API_KEY"'
    exit 1
}

Write-Host ""
Write-Host "Iniciando JARVIS..." -ForegroundColor Green
python app.py
