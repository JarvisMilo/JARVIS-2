$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    Write-Host ""
    Write-Host "No encuentro Ollama en Windows." -ForegroundColor Yellow
    Write-Host "Instálalo desde https://ollama.com/download/windows y vuelve a ejecutar este script."
    exit 1
}

if (-not (Test-Path ".venv")) {
    Write-Host "Creando entorno virtual..." -ForegroundColor Cyan
    python -m venv .venv
}

Write-Host "Activando entorno virtual..." -ForegroundColor Cyan
. .\.venv\Scripts\Activate.ps1

Write-Host "Instalando/verificando dependencias..." -ForegroundColor Cyan
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

Write-Host ""
Write-Host "Comprobando modelo Ollama: llama3.2" -ForegroundColor Cyan
$models = ollama list
if ($models -notmatch "(?m)^llama3\.2\s") {
    Write-Host "El modelo llama3.2 no está descargado." -ForegroundColor Yellow
    Write-Host "Descárgalo con: ollama pull llama3.2"
    exit 1
}

Write-Host ""
Write-Host "Iniciando JARVIS Nivel 1 con Ollama local..." -ForegroundColor Green
python main.py
