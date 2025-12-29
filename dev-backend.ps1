param(
  [Alias('Host')]
  [string]$BindHost = "127.0.0.1",
  [int]$Port = 8000,
  [switch]$UsePostgres,
  [string]$DatabaseUrl
)

$ErrorActionPreference = 'Stop'

$repoRoot = $PSScriptRoot
$backendDir = Join-Path $repoRoot 'fastapi_app'

if (-not (Test-Path $backendDir)) {
  throw "Missing backend folder: $backendDir"
}

Push-Location $backendDir
try {
  if (-not $UsePostgres) {
    if (-not $DatabaseUrl) {
      $DatabaseUrl = "sqlite+aiosqlite:///./app.db"
    }
    $env:DATABASE_URL = $DatabaseUrl
  }

  .\\dev.ps1 run --host $BindHost --port $Port
} finally {
  Pop-Location
}
