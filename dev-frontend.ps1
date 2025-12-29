param(
  [int]$Port = 5173,
  [Alias('Host')]
  [string]$BindHost = "127.0.0.1",
  [string]$ApiBaseUrl = "http://127.0.0.1:8000",
  [switch]$MockApi
)

$ErrorActionPreference = 'Stop'

$repoRoot = $PSScriptRoot
$frontendDir = Join-Path $repoRoot 'frontend'

if (-not (Test-Path $frontendDir)) {
  throw "Missing frontend folder: $frontendDir"
}

if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
  throw "npm not found on PATH. Install Node.js and ensure npm is available."
}

Push-Location $frontendDir
try {
  if ($MockApi) {
    $env:VITE_MOCK_API = '1'
  } else {
    $env:VITE_MOCK_API = '0'
    $env:VITE_API_BASE_URL = $ApiBaseUrl
  }

  npm run dev -- --host $BindHost --port $Port
} finally {
  Pop-Location
}
