# Project TODO (High-level)

Last updated: 2025-12-28

## Core decisions
- [ ] Define project deliverable scope (generator tool vs `fastapi_app` template vs both)
- [ ] Lock target versions (Python/Postgres) and supported OS targets

## Orchestrator (AIweb generator)
- [ ] Add an end-to-end command: Architect → Backend → Frontend → Validator
- [ ] Harden output handling: strict validation, clear failures, optional single auto-retry
- [ ] Add `--dry-run` mode to preview planned file writes/patches
- [ ] Add unit tests for parsing and patch safety (JSON, file blocks, path traversal, absolute paths)

## `fastapi_app` hardening
- [ ] Replace deprecated FastAPI `on_event` hooks with lifespan handlers
- [ ] Review production defaults (SECRET_KEY, token expiry, CORS, AUTO_CREATE_TABLES)
- [ ] Document Alembic workflow (create/apply migrations + example first migration)

## DevOps / quality
- [ ] Add CI pipeline (install deps, run tests; optionally lint/format and Docker build)
- [ ] Add lint/format tooling (keep minimal, e.g., ruff)
- [ ] Add dependency pin/lock strategy (constraints/lockfile) for reproducible installs

## Documentation
- [ ] Update root README with Getting Started (generator + `fastapi_app`) and troubleshooting
