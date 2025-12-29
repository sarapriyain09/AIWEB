from __future__ import annotations

from pathlib import Path


class PromptError(RuntimeError):
    pass


def load_prompt(prompts_dir: Path, name: str) -> str:
    path = prompts_dir / f"{name}.txt"
    if not path.exists():
        raise PromptError(f"Missing prompt file: {path}")
    return path.read_text(encoding="utf-8")
