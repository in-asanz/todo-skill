#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from work_package_lib import VALID_STATUSES, generate_effective_files, is_node_dir, load_yaml, sync_complexity, today_iso, write_yaml


def rewrite_handoff(node: Path, status: str, next_action: str) -> None:
    content = f"""# Handoff

## Current state

- Node status: `{status}`
- Resume from disk using `entrypoint.md` and `rules/effective-rules.md`.

## Completed

- Existing progress should be summarized here by the active agent when real work starts.

## Remaining

- Follow the next action below.

## Next action

- {next_action}
"""
    (node / "handoff.md").write_text(content, encoding="utf-8")


def rewrite_current_step(node: Path, status: str, next_action: str) -> None:
    content = f"""# Current Step

## Status

- `{status}`

## Next action

- {next_action}
"""
    (node / "plan" / "current-step.md").write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Update resumable state for a node.")
    parser.add_argument("--node", required=True, help="Path to the work-package node.")
    parser.add_argument("--status", required=True, choices=sorted(VALID_STATUSES))
    parser.add_argument("--next-action", required=True, help="Exact next action for the next agent.")
    args = parser.parse_args()

    node = Path(args.node).resolve()
    if not is_node_dir(node):
        raise SystemExit(f"Not a work-package node: {node}")

    sync_complexity(node, "auto")
    generate_effective_files(node)
    meta = load_yaml(node / "meta.yaml")
    meta["status"] = args.status
    meta["updated_at"] = today_iso()
    meta["next_action"] = args.next_action
    write_yaml(node / "meta.yaml", meta)

    rewrite_handoff(node, args.status, args.next_action)
    rewrite_current_step(node, args.status, args.next_action)
    print(f"Updated resumable state for: {node}")


if __name__ == "__main__":
    main()
