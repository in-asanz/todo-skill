#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from work_package_lib import (
    build_inheritance_context,
    compute_depth,
    ensure_project_todo_files,
    ensure_valid_id,
    find_root,
    generate_effective_files,
    is_node_dir,
    quote_or_null,
    render_template,
    sync_complexity,
    today_iso,
)
from validate_work_package import validate_node


SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = SCRIPT_DIR.parent / "assets" / "templates"

TEMPLATE_MAP = {
    "entrypoint.md.tmpl": "entrypoint.md",
    "meta.yaml.tmpl": "meta.yaml",
    "brief.md.tmpl": "brief.md",
    "execute.md.tmpl": "execute.md",
    "validate.md.tmpl": "validate.md",
    "handoff.md.tmpl": "handoff.md",
    "result.md.tmpl": "result.md",
    "plan/local-roadmap.md.tmpl": "plan/local-roadmap.md",
    "plan/current-step.md.tmpl": "plan/current-step.md",
    "rules/local-rules.md.tmpl": "rules/local-rules.md",
    "rules/inheritance.yaml.tmpl": "rules/inheritance.yaml",
    "context/local-context.md.tmpl": "context/local-context.md",
}


def build_context(
    node_id: str,
    title: str,
    node_type: str,
    parent_id: str | None,
    node_dir: Path,
    complexity_mode: str,
) -> dict[str, str]:
    return {
        "id": node_id,
        "title": title,
        "type": node_type,
        "parent": quote_or_null(parent_id),
        "depth": str(compute_depth(node_id)),
        "updated_at": today_iso(),
        "complexity_level": "2" if complexity_mode == "auto" else complexity_mode,
        "complexity_mode": "auto" if complexity_mode == "auto" else "manual",
        "complexity_reason": "awaiting_initial_review",
        "complexity_brief": "- Initial managed complexity block. Run complexity review after creation.",
        "complexity_execute": "- Initial managed complexity block. Run complexity review after creation.",
        "complexity_validate": "- Initial managed complexity block. Run complexity review after creation.",
        "complexity_roadmap": "## Managed complexity guidance\n\n- Initial managed complexity block. Run complexity review after creation.",
        **build_inheritance_context(node_dir, parent_id),
    }


def create_node(
    root: Path,
    node_id: str,
    title: str,
    node_type: str,
    parent: Path | None,
    complexity: str,
) -> Path:
    ensure_valid_id(node_id)
    root.mkdir(parents=True, exist_ok=True)
    ensure_project_todo_files(root)

    if parent is not None:
        if not is_node_dir(parent):
            raise ValueError(f"Parent path is not a work-package node: {parent}")
        expected_prefix = f"{parent.name}-"
        if not node_id.startswith(expected_prefix):
            raise ValueError(f"Child id '{node_id}' must start with '{expected_prefix}'.")
        node_dir = parent / "children" / node_id
        parent_id = parent.name
    else:
        node_dir = root / node_id
        parent_id = None

    if node_dir.exists():
        raise ValueError(f"Node directory already exists: {node_dir}")

    for relative_dir in ("plan", "rules", "context", "refs", "children"):
        (node_dir / relative_dir).mkdir(parents=True, exist_ok=True)

    context = build_context(node_id, title, node_type, parent_id, node_dir, complexity)
    for template_rel, output_rel in TEMPLATE_MAP.items():
        render_template(TEMPLATE_DIR / template_rel, node_dir / output_rel, context)

    sync_complexity(node_dir, requested_level=complexity)
    generate_effective_files(node_dir)

    errors = validate_node(node_dir)
    if errors:
        raise ValueError("Validation failed after node creation:\n- " + "\n- ".join(errors))

    return node_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a recursive work-package node.")
    parser.add_argument("--root", required=True, help="Directory that stores top-level nodes.")
    parser.add_argument("--id", required=True, help="Node id, e.g. TASK-001 or TASK-001-01.")
    parser.add_argument("--title", required=True, help="Human-readable node title.")
    parser.add_argument("--parent", help="Existing parent node path.")
    parser.add_argument(
        "--type",
        default="task",
        choices=("container", "task", "leaf"),
        help="Node type.",
    )
    parser.add_argument(
        "--complexity",
        default="auto",
        choices=("auto", "1", "2", "3"),
        help="Managed task-detail level.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    parent = Path(args.parent).resolve() if args.parent else None
    node_dir = create_node(root, args.id, args.title, args.type, parent, args.complexity)
    print(f"Created node: {node_dir}")
    print(f"Root node: {find_root(node_dir)}")


if __name__ == "__main__":
    main()
