$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot

Write-Host "Stopping PostgreSQL container..." -ForegroundColor Cyan
Push-Location $ProjectRoot
try {
    docker compose stop postgres
}
finally {
    Pop-Location
}

Write-Host "PostgreSQL stopped. Close backend/frontend terminal windows manually if they are still open." -ForegroundColor Green
