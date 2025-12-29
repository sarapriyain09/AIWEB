from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from .flow import (
    apply_patch_flow,
    architect_flow,
    generate_flow,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="aiweb-gen")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_arch = sub.add_parser("architect", help="Idea → JSON spec")
    p_arch.add_argument("--idea", required=True)
    p_arch.add_argument("--prompts", default="prompts")
    p_arch.add_argument(
        "--auto-retry",
        action="store_true",
        help="Retry once if the model output cannot be parsed/validated",
    )

    p_gen = sub.add_parser("generate", help="Idea → spec → backend → validate → frontend → validate")
    p_gen.add_argument("--idea", required=True)
    p_gen.add_argument("--out", default="generated")
    p_gen.add_argument("--prompts", default="prompts")
    p_gen.add_argument("--strict", action="store_true", help="Fail if CODE_VALIDATOR reports issues")
    p_gen.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not write any files; only show what would be written",
    )
    p_gen.add_argument(
        "--auto-retry",
        action="store_true",
        help="Retry once if the model output cannot be parsed/validated (or fails strict validation)",
    )

    p_patch = sub.add_parser("patch", help="Generate unified diff and apply it")
    p_patch.add_argument("--root", required=True, help="Root folder of the existing codebase")
    p_patch.add_argument("--request", required=True, help="Change request")
    p_patch.add_argument("--prompts", default="prompts")
    p_patch.add_argument("--dry-run", action="store_true")

    args = parser.parse_args(argv)

    try:
        if args.cmd == "architect":
            spec = architect_flow(
                idea=args.idea,
                prompts_dir=Path(args.prompts),
                auto_retry=args.auto_retry,
            )
            sys.stdout.write(json.dumps(spec, indent=2))
            sys.stdout.write("\n")
            return 0

        if args.cmd == "generate":
            out_dir = Path(args.out)
            result = generate_flow(
                idea=args.idea,
                out_dir=out_dir,
                prompts_dir=Path(args.prompts),
                strict=args.strict,
                dry_run=args.dry_run,
                auto_retry=args.auto_retry,
            )
            sys.stdout.write(json.dumps(result, indent=2))
            sys.stdout.write("\n")
            return 0 if result.get("ok", False) else 1

        if args.cmd == "patch":
            root = Path(args.root)
            result = apply_patch_flow(
                root_dir=root,
                change_request=args.request,
                prompts_dir=Path(args.prompts),
                dry_run=args.dry_run,
            )
            sys.stdout.write(json.dumps(result, indent=2))
            sys.stdout.write("\n")
            return 0

        raise RuntimeError(f"Unknown command: {args.cmd}")
    except KeyboardInterrupt:
        return 130
    except Exception as exc:  # noqa: BLE001
        sys.stderr.write(f"ERROR: {exc}\n")
        if os.environ.get("AIWEB_DEBUG") == "1":
            raise
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
