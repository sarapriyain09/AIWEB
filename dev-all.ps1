param(
  [switch]$InitEnv,
  [switch]$UsePostgres,
  [int]$FrontendPort = 5173,
  [string]$BackendHost = "127.0.0.1",
  [int]$BackendPort = 8000
)

$ErrorActionPreference = 'Stop'

$repoRoot = $PSScriptRoot
$backendDir = Join-Path $repoRoot 'fastapi_app'
$frontendDir = Join-Path $repoRoot 'frontend'

if (-not (Test-Path $backendDir)) {
  throw "Missing backend folder: $backendDir"
}
if (-not (Test-Path $frontendDir)) {
  throw "Missing frontend folder: $frontendDir"
}

if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
  throw "npm not found on PATH. Install Node.js and ensure npm is available."
}

if (-not (Test-Path (Join-Path $frontendDir 'node_modules'))) {
  Write-Host "Warning: frontend dependencies not installed. Run: cd frontend; npm install" -ForegroundColor Yellow
}

if (-not (Test-Path (Join-Path $backendDir '.venv'))) {
  Write-Host "Warning: backend venv not found. Run: cd fastapi_app; .\\dev.ps1 install" -ForegroundColor Yellow
}

if ($InitEnv) {
  Write-Host "Initializing backend .env..."
  & (Join-Path $backendDir 'dev.ps1') init-env
}

$apiBaseUrl = "http://$BackendHost`:$BackendPort"

$dbUrl = if ($UsePostgres) { $null } else { "sqlite+aiosqlite:///./app.db" }

Write-Host "Starting backend: $apiBaseUrl"
Start-Process -FilePath powershell -ArgumentList @(
  '-NoExit',
  '-Command',
  (
    "Set-Location -Path '$backendDir'; " +
    $(if ($dbUrl) { "`$env:DATABASE_URL='$dbUrl'; " } else { "" }) +
    ".\\dev.ps1 run --host $BackendHost --port $BackendPort"
  )
)

Write-Host "Starting frontend: http://127.0.0.1:$FrontendPort (API=$apiBaseUrl)"
Start-Process -FilePath powershell -ArgumentList @(
  '-NoExit',
  '-Command',
  "Set-Location -Path '$frontendDir'; `$env:VITE_MOCK_API='0'; `$env:VITE_API_BASE_URL='$apiBaseUrl'; npm run dev -- --host 127.0.0.1 --port $FrontendPort"
)

Write-Host "Done. If the backend fails to start, run: cd fastapi_app; .\\dev.ps1 init-env; .\\dev.ps1 install"
Write-Host "If the frontend fails to start, run: cd frontend; npm install"
