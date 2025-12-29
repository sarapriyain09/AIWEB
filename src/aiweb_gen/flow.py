from __future__ import annotations

import json
from pathlib import Path

from .diffapply import apply_unified_diff
from .fsops import safe_write_files
from .llm import chat_completion
from .parsing import ParseError, parse_file_blocks, parse_json_strict
from .prompts import load_prompt


def architect_flow(*, idea: str, prompts_dir: Path, auto_retry: bool = False) -> dict:
    system = load_prompt(prompts_dir, "ARCHITECT_MODE")

    last_err: Exception | None = None
    attempts = 2 if auto_retry else 1
    for _ in range(attempts):
        try:
            out = chat_completion(system=system, user=idea, temperature=0.0)
            spec = parse_json_strict(out)

            required = [
                "app_name",
                "description",
                "tech_stack",
                "pages",
                "components",
                "database_models",
                "api_endpoints",
                "non_functional_requirements",
            ]
            missing = [k for k in required if k not in spec]
            if missing:
                raise ValueError(f"Spec missing required keys: {missing}")
            return spec
        except (ParseError, ValueError) as exc:
            last_err = exc

    raise ValueError(f"Failed to produce a valid spec: {last_err}")


def validate_code_flow(*, code_bundle_text: str, prompts_dir: Path, auto_retry: bool = False) -> dict:
    system = load_prompt(prompts_dir, "CODE_VALIDATOR")

    last_err: Exception | None = None
    attempts = 2 if auto_retry else 1
    for _ in range(attempts):
        try:
            out = chat_completion(system=system, user=code_bundle_text, temperature=0.0)
            report = parse_json_strict(out)
            if "valid" not in report or "issues" not in report:
                raise ValueError("Validator output missing required keys")
            return report
        except (ParseError, ValueError) as exc:
            last_err = exc

    raise ValueError(f"Failed to parse validator output: {last_err}")


def backend_flow(*, spec: dict, prompts_dir: Path, auto_retry: bool = False) -> tuple[list[tuple[str, str]], dict]:
    system = load_prompt(prompts_dir, "BACKEND_GENERATOR")

    last_err: Exception | None = None
    attempts = 2 if auto_retry else 1
    for _ in range(attempts):
        try:
            out = chat_completion(system=system, user=json.dumps(spec), temperature=0.0)
            blocks = parse_file_blocks(out)

            code_bundle_for_validator = out
            report = validate_code_flow(
                code_bundle_text=code_bundle_for_validator,
                prompts_dir=prompts_dir,
                auto_retry=auto_retry,
            )

            files = [(b.path, b.content) for b in blocks]
            return files, report
        except (ParseError, ValueError) as exc:
            last_err = exc

    raise ValueError(f"Backend generation failed: {last_err}")


def frontend_flow(*, spec: dict, prompts_dir: Path, auto_retry: bool = False) -> tuple[list[tuple[str, str]], dict]:
    system = load_prompt(prompts_dir, "FRONTEND_GENERATOR")

    last_err: Exception | None = None
    attempts = 2 if auto_retry else 1
    for _ in range(attempts):
        try:
            out = chat_completion(system=system, user=json.dumps(spec), temperature=0.0)
            blocks = parse_file_blocks(out)

            code_bundle_for_validator = out
            report = validate_code_flow(
                code_bundle_text=code_bundle_for_validator,
                prompts_dir=prompts_dir,
                auto_retry=auto_retry,
            )

            files = [(b.path, b.content) for b in blocks]
            return files, report
        except (ParseError, ValueError) as exc:
            last_err = exc

    raise ValueError(f"Frontend generation failed: {last_err}")


def generate_flow(
    *,
    idea: str,
    out_dir: Path,
    prompts_dir: Path,
    strict: bool,
    dry_run: bool = False,
    auto_retry: bool = False,
) -> dict:
    spec = architect_flow(idea=idea, prompts_dir=prompts_dir, auto_retry=auto_retry)
    app_name = str(spec.get("app_name", "app")).strip() or "app"

    root = out_dir / app_name
    backend_root = root / "backend"
    frontend_root = root / "frontend"

    backend_files, backend_report = backend_flow(spec=spec, prompts_dir=prompts_dir, auto_retry=auto_retry)
    if strict and not backend_report.get("valid", False) and auto_retry:
        backend_files, backend_report = backend_flow(spec=spec, prompts_dir=prompts_dir, auto_retry=False)
    if strict and not backend_report.get("valid", False):
        return {
            "ok": False,
            "stage": "backend_validation_failed",
            "dry_run": dry_run,
            "app_root": str(root),
            "backend_root": str(backend_root),
            "frontend_root": str(frontend_root),
            "report": backend_report,
        }

    written_backend = safe_write_files(backend_root, backend_files, dry_run=dry_run)

    frontend_files, frontend_report = frontend_flow(spec=spec, prompts_dir=prompts_dir, auto_retry=auto_retry)
    if strict and not frontend_report.get("valid", False) and auto_retry:
        frontend_files, frontend_report = frontend_flow(spec=spec, prompts_dir=prompts_dir, auto_retry=False)
    if strict and not frontend_report.get("valid", False):
        return {
            "ok": False,
            "stage": "frontend_validation_failed",
            "dry_run": dry_run,
            "app_root": str(root),
            "backend_root": str(backend_root),
            "frontend_root": str(frontend_root),
            "report": frontend_report,
        }

    written_frontend = safe_write_files(frontend_root, frontend_files, dry_run=dry_run)

    safe_write_files(root, [("spec.json", json.dumps(spec, indent=2) + "\n")], dry_run=dry_run)

    return {
        "ok": True,
        "dry_run": dry_run,
        "app_root": str(root),
        "backend": {
            "root": str(backend_root),
            "files_written": written_backend,
            "validator": backend_report,
        },
        "frontend": {
            "root": str(frontend_root),
            "files_written": written_frontend,
            "validator": frontend_report,
        },
    }


def apply_patch_flow(*, root_dir: Path, change_request: str, prompts_dir: Path, dry_run: bool) -> dict:
    system = load_prompt(prompts_dir, "PATCH_MODE")

    # For PATCH_MODE we need "current file content". Keep it simple: pack all text files.
    # This is intentionally conservative; for larger repos, you would add a file selector.
    file_blobs: list[str] = []
    for path in root_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.name.startswith("."):
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".zip"}:
            continue
        try:
            rel = path.relative_to(root_dir).as_posix()
            content = path.read_text(encoding="utf-8")
        except Exception:  # noqa: BLE001
            continue
        file_blobs.append(f"=== FILE: {rel} ===\n{content}\n")

    user = "CURRENT CODEBASE FILES:\n" + "\n".join(file_blobs) + "\n\nCHANGE REQUEST:\n" + change_request
    diff_text = chat_completion(system=system, user=user, temperature=0.0)

    if not diff_text.strip():
        return {"ok": True, "changed": False, "reason": "Model returned empty diff"}

    result = apply_unified_diff(root_dir, diff_text, dry_run=dry_run)
    return {
        "ok": True,
        "changed": True,
        "dry_run": dry_run,
        "applied_files": result.applied_files,
        "total_hunks": result.total_hunks,
    }
