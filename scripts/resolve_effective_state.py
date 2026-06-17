#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from work_package_lib import generate_effective_files, is_node_dir, sync_complexity


def main() -> None:
    parser = argparse.ArgumentParser(description="Rebuild effective rules for a node.")
    parser.add_argument("--node", required=True, help="Path to the work-package node.")
    args = parser.parse_args()

    node = Path(args.node).resolve()
    if not is_node_dir(node):
        raise SystemExit(f"Not a work-package node: {node}")

    sync_complexity(node, "auto")
    generate_effective_files(node)
    print(f"Rebuilt effective rules for: {node}")


if __name__ == "__main__":
    main()
