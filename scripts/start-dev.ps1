param(
    [switch]$SkipAppStart
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$BackendDir = Join-Path $ProjectRoot "backend"
$FrontendDir = Join-Path $ProjectRoot "frontend"
$DatabaseUrl = "postgresql+psycopg://postgres:postgres@localhost:5432/ai_learning_platform"

function Write-Step($Message) {
    Write-Host "`n==> $Message" -ForegroundColor Cyan
}

function Test-DockerReady {
    docker info *> $null
    return $LASTEXITCODE -eq 0
}

function Start-DockerDesktop {
    if (Test-DockerReady) {
        Write-Host "Docker is already running." -ForegroundColor Green
        return
    }

    Write-Step "Starting Docker Desktop"
    $dockerDesktopPaths = @(
        "C:\Program Files\Docker\Docker\Docker Desktop.exe",
        "$env:LOCALAPPDATA\Docker\Docker Desktop.exe"
    )
    $dockerDesktopPath = $dockerDesktopPaths | Where-Object { Test-Path $_ } | Select-Object -First 1

    if (-not $dockerDesktopPath) {
        throw "Docker Desktop was not found. Install Docker Desktop or start it manually once."
    }

    Start-Process -FilePath $dockerDesktopPath | Out-Null

    $maxAttempts = 60
    for ($attempt = 1; $attempt -le $maxAttempts; $attempt++) {
        if (Test-DockerReady) {
            Write-Host "Docker is ready." -ForegroundColor Green
            return
        }
        Write-Host "Waiting for Docker... $attempt/$maxAttempts"
        Start-Sleep -Seconds 2
    }

    throw "Docker did not become ready in time. Open Docker Desktop and try again."
}

function Start-Postgres {
    Write-Step "Starting PostgreSQL"
    Push-Location $ProjectRoot
    try {
        docker compose up -d postgres
    }
    finally {
        Pop-Location
    }
}

function Start-Backend {
    Write-Step "Starting backend"
    $pythonPath = Join-Path $BackendDir ".venv-py\Scripts\python.exe"
    if (-not (Test-Path $pythonPath)) {
        $pythonPath = Join-Path $BackendDir ".venv\Scripts\python.exe"
    }
    if (-not (Test-Path $pythonPath)) {
        throw "Backend virtual environment was not found. Expected .venv-py or .venv in backend/."
    }

    $command = "`$env:DATABASE_URL='$DatabaseUrl'; & '$pythonPath' -m uvicorn app.main:app --reload"
    Start-Process powershell.exe -WorkingDirectory $BackendDir -ArgumentList @(
        "-NoExit",
        "-ExecutionPolicy", "Bypass",
        "-Command", $command
    ) | Out-Null
}

function Start-Frontend {
    Write-Step "Starting frontend"
    Start-Process powershell.exe -WorkingDirectory $FrontendDir -ArgumentList @(
        "-NoExit",
        "-ExecutionPolicy", "Bypass",
        "-Command", "npm.cmd run dev -- --host 127.0.0.1"
    ) | Out-Null
}

Start-DockerDesktop
Start-Postgres

if (-not $SkipAppStart) {
    Start-Backend
    Start-Frontend
}

Write-Host "`nSkillWay dev environment is ready." -ForegroundColor Green
Write-Host "Frontend: http://127.0.0.1:5173/"
Write-Host "Backend:  http://127.0.0.1:8000/api/v1/health"
Write-Host "Docs:     http://127.0.0.1:8000/docs"
