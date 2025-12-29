# AIweb Focused App Generator

[![fastapi_app tests](https://github.com/sarapriyain09/AIWEB/actions/workflows/fastapi_app_tests.yml/badge.svg)](https://github.com/sarapriyain09/AIWEB/actions/workflows/fastapi_app_tests.yml)

Product requirements and build constraints live in `COPILOT_INSTRUCTIONS.md`.

Minimal orchestrator for a “Focused AI App Generator” using 5 system prompts:
- `ARCHITECT_MODE` (idea → JSON spec)
- `BACKEND_GENERATOR` (spec → FastAPI files)
- `FRONTEND_GENERATOR` (spec → React/Vite files)
- `PATCH_MODE` (safe incremental diffs)
- `CODE_VALIDATOR` (quality gate JSON)

## Requirements
- Windows + PowerShell
- Python 3.10+ recommended

## Setup
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
```
If you don't want an editable install, use the helper script:
```powershell
.\\run.ps1 -h
```

## Configure LLM
Set environment variables (OpenAI-compatible API):
```powershell
$env:OPENAI_API_KEY = "..."
$env:OPENAI_MODEL = "gpt-5.2-mini"  # or your preferred model
# Optional if using a compatible proxy/server
# $env:OPENAI_BASE_URL = "https://api.openai.com/v1"
```

## Usage
### 1) Generate a new app (spec → backend → frontend)
```powershell
aiweb-gen generate --idea "Build a task management app for small teams" --out .\generated
# or: .\\run.ps1 generate --idea "..." --out .\\generated
```

### 2) Only produce the spec
```powershell
aiweb-gen architect --idea "..."
```

### 3) Apply a patch (unified diff) to an existing folder
```powershell
aiweb-gen patch --root .\generated\my-app --request "Add a dark mode toggle" 
```

Notes:
- The backend/frontend generators expect model output in `=== FILE: path ===` blocks.
- The validator is a model-based gate (JSON output) and can be enforced with `--strict`.

## Run frontend + backend together
This repo includes a minimal dev helper that opens two terminals:
```powershell
.\dev-all.ps1 -InitEnv
```
By default it runs the backend against SQLite (no Postgres required). To use Postgres, pass `-UsePostgres` and ensure your `fastapi_app/.env` points at Postgres (or run `docker compose up` in `fastapi_app`).

It starts:
- Backend on `http://127.0.0.1:8000`
- Frontend on `http://127.0.0.1:5173` (configured to call the backend)

### Running them individually (from repo root)
If you previously saw exit code `1`, it’s usually because `npm run dev` was executed from the repo root instead of `frontend/`, or `dev.ps1` was executed from the repo root instead of `fastapi_app/`.

Use these wrappers to avoid working-directory issues:
```powershell
.\dev-backend.ps1 -BindHost 127.0.0.1 -Port 8000
.\dev-frontend.ps1 -BindHost 127.0.0.1 -Port 5173 -ApiBaseUrl http://127.0.0.1:8000
```
