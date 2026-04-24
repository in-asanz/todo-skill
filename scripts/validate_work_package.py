#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from work_package_lib import (
    MANAGED_MARKERS,
    REQUIRED_DIRS,
    REQUIRED_FILES,
    compute_depth,
    find_todo_root,
    is_node_dir,
    load_yaml,
    parent_path,
    validate_meta,
)


def validate_node(node: Path) -> list[str]:
    errors: list[str] = []

    if not node.exists():
        return [f"Node path does not exist: {node}"]
    if not node.is_dir():
        return [f"Node path is not a directory: {node}"]

    for relative_dir in REQUIRED_DIRS:
        if not (node / relative_dir).is_dir():
            errors.append(f"Missing required directory: {relative_dir}")

    for relative_file in REQUIRED_FILES:
        if not (node / relative_file).is_file():
            errors.append(f"Missing required file: {relative_file}")

    meta_path = node / "meta.yaml"
    if meta_path.exists():
        meta = load_yaml(meta_path)
        errors.extend(validate_meta(meta))

        expected_depth = compute_depth(str(meta.get("id", ""))) if meta.get("id") else None
        if expected_depth is not None and node.name != meta.get("id"):
            errors.append(f"Directory name '{node.name}' does not match meta id '{meta.get('id')}'.")

        parent = parent_path(node)
        if parent is None:
            if meta.get("parent") is not None:
                errors.append("Root node must have parent: null.")
        else:
            if meta.get("parent") != parent.name:
                errors.append(
                    f"Meta parent '{meta.get('parent')}' does not match actual parent '{parent.name}'."
                )
            if not str(meta.get("id", "")).startswith(f"{parent.name}-"):
                errors.append("Child id must begin with the parent id prefix.")

    inheritance_path = node / "rules" / "inheritance.yaml"
    if inheritance_path.exists():
        inheritance = load_yaml(inheritance_path)
        sources = inheritance.get("sources")
        if not isinstance(sources, dict):
            errors.append("inheritance.yaml must contain a sources mapping.")
        else:
            for key, value in sources.items():
                if value is None:
                    continue
                source_path = (node / value).resolve()
                if not source_path.exists():
                    errors.append(f"Missing inheritance source for {key}: {value}")

    managed_targets = {
        "brief": node / "brief.md",
        "execute": node / "execute.md",
        "validate": node / "validate.md",
        "roadmap": node / "plan" / "local-roadmap.md",
    }
    for key, path in managed_targets.items():
        if path.exists():
            text = path.read_text(encoding="utf-8")
            start_marker, end_marker = MANAGED_MARKERS[key]
            if start_marker not in text or end_marker not in text:
                errors.append(f"Missing managed complexity markers in {path.relative_to(node)}")

    todo_root = find_todo_root(node)
    if todo_root is not None:
        project_rules = todo_root / "rules" / "project-rules.md"
        if not project_rules.exists():
            errors.append("Missing project rules file: TODO/rules/project-rules.md")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a recursive work-package node.")
    parser.add_argument("--node", required=True, help="Path to the work-package node.")
    args = parser.parse_args()

    node = Path(args.node).resolve()
    errors = validate_node(node)
    if errors:
        print("Work-package validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print("Work-package is valid.")


if __name__ == "__main__":
    main()
