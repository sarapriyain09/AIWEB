from __future__ import annotations

import json
import re
from dataclasses import dataclass


class ParseError(ValueError):
    pass


def parse_json_strict(text: str) -> dict:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ParseError(f"Invalid JSON output: {exc}") from exc


_FILE_HEADER_RE = re.compile(r"^=== FILE: (?P<path>[^=\n\r]+) ===\s*$")


@dataclass(frozen=True)
class FileBlock:
    path: str
    content: str


def parse_file_blocks(text: str) -> list[FileBlock]:
    lines = text.splitlines()
    blocks: list[FileBlock] = []
    current_path: str | None = None
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_path, current_lines
        if current_path is None:
            return
        blocks.append(FileBlock(path=current_path.strip(), content="\n".join(current_lines).rstrip() + "\n"))
        current_path = None
        current_lines = []

    for line in lines:
        m = _FILE_HEADER_RE.match(line.strip())
        if m:
            flush()
            current_path = m.group("path")
            continue
        if current_path is not None:
            current_lines.append(line)

    flush()
    if not blocks:
        raise ParseError("No file blocks found. Expected one or more '=== FILE: <path> ===' sections.")

    bad = [b.path for b in blocks if not b.path or b.path.startswith("/") or ":" in b.path]
    if bad:
        raise ParseError(f"Invalid relative paths in file blocks: {bad}")

    return blocks
