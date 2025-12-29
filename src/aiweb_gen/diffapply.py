from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path


class PatchError(RuntimeError):
    pass


@dataclass(frozen=True)
class PatchResult:
    applied_files: list[str]
    total_hunks: int


_DIFF_FILE_RE = re.compile(r"^\+\+\+\s+(?P<path>.+)$")


def _normalize_diff_path(path: str) -> str:
    p = path.strip()
    if p.startswith("a/") or p.startswith("b/"):
        p = p[2:]
    if p in ("/dev/null", "dev/null"):
        return ""
    return p


def apply_unified_diff(root: Path, diff_text: str, *, dry_run: bool = False) -> PatchResult:
    """Apply unified diff by shelling out to 'git apply' if available.

    Falls back to error if git isn't present. This is intentional: implementing a robust
    patch engine is non-trivial, and git's patcher is reliable.
    """
    root = root.resolve()
    if not root.exists():
        raise PatchError(f"Root directory does not exist: {root}")

    # Basic sanity: ensure the diff only targets paths under root.
    applied_files: list[str] = []
    total_hunks = diff_text.count("@@")

    for line in diff_text.splitlines():
        m = _DIFF_FILE_RE.match(line)
        if not m:
            continue
        p = _normalize_diff_path(m.group("path"))
        if not p:
            continue
        if p.startswith("/") or ":" in p:
            raise PatchError(f"Absolute/drive path in diff not allowed: {p}")
        target = (root / p).resolve()
        if root not in target.parents and target != root:
            raise PatchError(f"Path traversal in diff not allowed: {p}")
        applied_files.append(os.path.relpath(str(target), str(root)))

    # Use git apply for correctness.
    import subprocess  # noqa: PLC0415

    cmd = ["git", "apply"]
    if dry_run:
        cmd.append("--check")

    proc = subprocess.run(
        cmd,
        input=diff_text,
        text=True,
        cwd=str(root),
        capture_output=True,
    )
    if proc.returncode != 0:
        raise PatchError((proc.stderr or proc.stdout or "git apply failed").strip())

    if dry_run:
        return PatchResult(applied_files=sorted(set(applied_files)), total_hunks=total_hunks)

    # Now apply for real (we already checked):
    proc2 = subprocess.run(
        ["git", "apply"],
        input=diff_text,
        text=True,
        cwd=str(root),
        capture_output=True,
    )
    if proc2.returncode != 0:
        raise PatchError((proc2.stderr or proc2.stdout or "git apply failed").strip())

    return PatchResult(applied_files=sorted(set(applied_files)), total_hunks=total_hunks)
