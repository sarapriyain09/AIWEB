param(
  [Parameter(Mandatory=$true, Position=0)]
  [ValidateSet('init-env','install','run','test','migrate-init','migrate-up','migrate-current','docker-up','docker-db')]
  [string]$Task,

  [Parameter(ValueFromRemainingArguments=$true)]
  [string[]]$Args
)

$ErrorActionPreference = 'Stop'

function Ensure-Venv {
  if (Test-Path -Path (Join-Path $PSScriptRoot '.venv\Scripts\Activate.ps1')) {
    . (Join-Path $PSScriptRoot '.venv\Scripts\Activate.ps1')
  }
}

Push-Location $PSScriptRoot
try {
  switch ($Task) {
    'init-env' {
      if (-not (Test-Path '.env')) {
        Copy-Item '.env.example' '.env'
        Write-Host 'Created .env from .env.example'
      } else {
        Write-Host '.env already exists'
      }
    }

    'install' {
      if (-not (Test-Path '.venv')) {
        python -m venv .venv
      }
      Ensure-Venv
      pip install -r requirements.txt
    }

    'run' {
      Ensure-Venv
      # Uses .env via pydantic-settings
      uvicorn main:app --reload @Args
    }

    'test' {
      Ensure-Venv
      pytest -q @Args
    }

    'migrate-init' {
      Ensure-Venv
      if (-not (Test-Path '.env')) {
        throw 'Missing .env. Run: .\dev.ps1 init-env'
      }
      python -m alembic revision --autogenerate -m "init" @Args
    }

    'migrate-up' {
      Ensure-Venv
      if (-not (Test-Path '.env')) {
        throw 'Missing .env. Run: .\dev.ps1 init-env'
      }
      python -m alembic upgrade head @Args
    }

    'migrate-current' {
      Ensure-Venv
      python -m alembic current @Args
    }

    'docker-up' {
      docker compose up --build @Args
    }

    'docker-db' {
      docker compose up -d db @Args
    }

    default {
      throw "Unknown task: $Task"
    }
  }
} finally {
  Pop-Location
}
