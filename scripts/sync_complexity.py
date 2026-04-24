#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from work_package_lib import is_node_dir, sync_complexity


def main() -> None:
    parser = argparse.ArgumentParser(description="Review or migrate node complexity.")
    parser.add_argument("--node", required=True, help="Path to the work-package node.")
    parser.add_argument(
        "--level",
        default="auto",
        choices=("auto", "1", "2", "3"),
        help="Target complexity level or auto recommendation.",
    )
    args = parser.parse_args()

    node = Path(args.node).resolve()
    if not is_node_dir(node):
        raise SystemExit(f"Not a work-package node: {node}")

    level, reason = sync_complexity(node, args.level)
    print(f"Synchronized complexity for {node}")
    print(f"Level: {level}")
    print(f"Reason: {reason}")


if __name__ == "__main__":
    main()
