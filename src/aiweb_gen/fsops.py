from __future__ import annotations

import os
from pathlib import Path


class WriteError(RuntimeError):
    pass


def safe_write_files(root: Path, files: list[tuple[str, str]], *, dry_run: bool = False) -> list[str]:
    """Write files under root, preventing path traversal.

    If dry_run=True, validates paths and returns the list of files that would be written
    without creating directories or writing content.
    """
    written: list[str] = []
    root = root.resolve()
    if not dry_run:
        root.mkdir(parents=True, exist_ok=True)

    for rel_path, content in files:
        target = (root / rel_path).resolve()
        if root not in target.parents and target != root:
            raise WriteError(f"Refusing to write outside root: {rel_path}")
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8", newline="\n")
        written.append(os.path.relpath(str(target), str(root)))

    return written
