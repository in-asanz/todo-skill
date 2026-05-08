#!/usr/bin/env python3
from __future__ import annotations

from datetime import date
import json
import os
from pathlib import Path
import re
import unicodedata

VALID_TYPES = {"container", "task", "leaf"}
VALID_STATUSES = {
    "backlog",
    "ready",
    "active",
    "paused",
    "blocked",
    "review",
    "witherror",
    "done",
    "archived",
}
USER_GATED_STATUSES = {"done", "archived"}
TERMINAL_STATUSES = USER_GATED_STATUSES
VALID_COMPLEXITIES = {1, 2, 3}
VALID_COMPLEXITY_MODES = {"auto", "manual"}
ID_RE = re.compile(r"^TASK-\d{3}(?:-\d{2})*$")
NODE_DIR_RE = re.compile(r"^(TASK-\d{3}(?:-\d{2})*)(?:_[a-z0-9]+(?:-[a-z0-9]+)*)?$")

REQUIRED_FILES = (
    "entrypoint.md",
    "meta.yaml",
    "brief.md",
    "execute.md",
    "validate.md",
    "handoff.md",
    "result.md",
    "plan/local-roadmap.md",
    "plan/current-step.md",
    "rules/local-rules.md",
    "rules/inheritance.yaml",
    "rules/effective-rules.md",
    "context/local-context.md",
)

REQUIRED_DIRS = ("plan", "rules", "context", "refs", "children")
MANAGED_MARKERS = {
    "brief": ("<!-- COMPLEXITY:BRIEF:START -->", "<!-- COMPLEXITY:BRIEF:END -->"),
    "execute": ("<!-- COMPLEXITY:EXECUTE:START -->", "<!-- COMPLEXITY:EXECUTE:END -->"),
    "validate": ("<!-- COMPLEXITY:VALIDATE:START -->", "<!-- COMPLEXITY:VALIDATE:END -->"),
    "roadmap": ("<!-- COMPLEXITY:ROADMAP:START -->", "<!-- COMPLEXITY:ROADMAP:END -->"),
}


def today_iso() -> str:
    return date.today().isoformat()


def ensure_valid_id(node_id: str) -> None:
    if not ID_RE.match(node_id):
        raise ValueError(
            f"Invalid node id '{node_id}'. Expected TASK-001 or nested TASK-001-01 pattern."
        )


def slugify_folder_name(name: str) -> str:
    normalized = unicodedata.normalize("NFKD", name.strip())
    normalized = normalized.encode("ascii", "ignore").decode("ascii").lower()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    normalized = normalized.strip("-")
    if not normalized:
        raise ValueError("Folder name must contain at least one ASCII letter or number.")
    return normalized


def node_dir_name(node_id: str, folder_name: str | None = None) -> str:
    ensure_valid_id(node_id)
    if folder_name is None or not folder_name.strip():
        return node_id
    return f"{node_id}_{slugify_folder_name(folder_name)}"


def dir_name_matches_id(directory_name: str, node_id: str) -> bool:
    ensure_valid_id(node_id)
    match = NODE_DIR_RE.match(directory_name)
    return bool(match and match.group(1) == node_id)


def compute_depth(node_id: str) -> int:
    ensure_valid_id(node_id)
    return len(node_id.split("-")) - 2


def node_meta_id(node: Path) -> str:
    meta = load_yaml(node / "meta.yaml")
    node_id = str(meta.get("id", ""))
    ensure_valid_id(node_id)
    return node_id


def parent_path(node: Path) -> Path | None:
    if node.parent.name != "children":
        return None
    candidate = node.parent.parent
    return candidate if is_node_dir(candidate) else None


def ancestor_nodes(node: Path) -> list[Path]:
    ancestors: list[Path] = []
    current = node.resolve()
    while True:
        parent = parent_path(current)
        if parent is None:
            return ancestors
        ancestors.append(parent)
        current = parent


def nearest_terminal_ancestor(node: Path) -> tuple[Path, dict] | None:
    for ancestor in ancestor_nodes(node):
        meta_path = ancestor / "meta.yaml"
        if not meta_path.exists():
            continue
        meta = load_yaml(meta_path)
        if meta.get("status") in TERMINAL_STATUSES:
            return ancestor, meta
    return None


def is_node_dir(path: Path) -> bool:
    return path.is_dir() and (path / "meta.yaml").exists()


def find_root(node: Path) -> Path:
    current = node.resolve()
    while True:
        parent = parent_path(current)
        if parent is None:
            return current
        current = parent


def find_child_node_by_id(container: Path, node_id: str) -> Path | None:
    if not container.exists():
        return None
    for child in container.iterdir():
        if not is_node_dir(child):
            continue
        try:
            if node_meta_id(child) == node_id:
                return child
        except (ValueError, FileNotFoundError):
            continue
    return None


def find_todo_root(path: Path) -> Path | None:
    current = path.resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if candidate.name == "TODO":
            return candidate
    return None


def load_yaml(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML file must contain a mapping: {path}")
    return data


def write_yaml(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def quote_or_null(value: str | None) -> str:
    return "null" if value is None else f'"{value}"'


def render_template(template_path: Path, output_path: Path, context: dict[str, str]) -> None:
    text = template_path.read_text(encoding="utf-8")
    for key, value in context.items():
        text = text.replace(f"{{{{{key}}}}}", value)
    output_path.write_text(text, encoding="utf-8")


def load_complexity_profile(skill_dir: Path, level: int) -> dict[str, str]:
    profile_path = skill_dir.parent / "assets" / "complexity" / f"level-{level}.json"
    data = json.loads(profile_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Invalid complexity profile: {profile_path}")
    return {str(k): str(v) for k, v in data.items()}


def os_relative(node_dir: Path, target: Path | None) -> str:
    if target is None:
        return "null"
    return Path(os.path.relpath(target, node_dir)).as_posix()


def read_optional(path: Path | None, default: str) -> str:
    if path is None or not path.exists():
        return default
    return path.read_text(encoding="utf-8").strip()


def ensure_user_global_rules() -> Path:
    rules_dir = Path.home() / ".codex" / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)
    rules_path = rules_dir / "user-global-rules.md"
    if not rules_path.exists():
        rules_path.write_text(
            "# User Global Rules\n\n"
            "- Add user-wide task-system rules here.\n"
            "- These rules apply above project rules and node-local rules.\n",
            encoding="utf-8",
        )
    return rules_path


def ensure_project_todo_files(root: Path) -> None:
    todo_root = find_todo_root(root)
    if todo_root is None:
        return

    config_dir = todo_root / "config"
    rules_dir = todo_root / "rules"
    tasks_dir = todo_root / "tasks"
    config_dir.mkdir(parents=True, exist_ok=True)
    rules_dir.mkdir(parents=True, exist_ok=True)
    tasks_dir.mkdir(parents=True, exist_ok=True)

    config_path = config_dir / "todo-skill.json"
    if not config_path.exists():
        config_path.write_text(
            json.dumps(
                {
                    "tasks_root": "TODO/tasks",
                    "project_rules": "TODO/rules/project-rules.md",
                    "user_rules": str(Path.home() / ".codex" / "rules" / "user-global-rules.md"),
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    project_rules_path = rules_dir / "project-rules.md"
    if not project_rules_path.exists():
        project_rules_path.write_text(
            "# Project Rules\n\n"
            "- Add project-wide task-system rules here.\n"
            "- These rules apply below user-global rules and above node-local rules.\n"
            "- Keep them focused on how tasks should be structured and executed in this repository.\n",
            encoding="utf-8",
        )

    update_tasks_entrypoint(todo_root)


def build_inheritance_context(node_dir: Path, parent_id: str | None) -> dict[str, str]:
    root_dir = find_root(node_dir)
    parent_dir = parent_path(node_dir)
    todo_root = find_todo_root(node_dir)
    user_rules = ensure_user_global_rules()
    project_rules = todo_root / "rules" / "project-rules.md" if todo_root else None
    return {
        "tree_root": root_dir.name,
        "parent": quote_or_null(parent_id),
        "user_global_rules": os_relative(node_dir, user_rules),
        "project_global_rules": quote_or_null(
            os_relative(node_dir, project_rules) if project_rules else None
        ),
        "parent_effective_rules": quote_or_null(
            os_relative(node_dir, parent_dir / "rules" / "effective-rules.md") if parent_dir else None
        ),
    }


def count_refs(node_dir: Path) -> int:
    refs_dir = node_dir / "refs"
    if not refs_dir.exists():
        return 0
    return sum(1 for item in refs_dir.rglob("*") if item.is_file())


def count_children(node_dir: Path) -> int:
    children_dir = node_dir / "children"
    if not children_dir.exists():
        return 0
    return sum(1 for item in children_dir.iterdir() if is_node_dir(item))


def recommend_complexity(node_dir: Path, meta: dict) -> tuple[int, str]:
    child_count = count_children(node_dir)
    depends_count = len(meta.get("depends_on", [])) if isinstance(meta.get("depends_on"), list) else 0
    refs_count = count_refs(node_dir)
    node_type = str(meta.get("type", "task"))

    if node_type == "container" or child_count > 0 or depends_count >= 2 or refs_count >= 3:
        return 1, (
            f"container_or_coordinated_scope(type={node_type}, children={child_count}, "
            f"depends_on={depends_count}, refs={refs_count})"
        )
    if node_type == "task" or depends_count == 1 or refs_count >= 1:
        return 2, (
            f"medium_scope(type={node_type}, children={child_count}, "
            f"depends_on={depends_count}, refs={refs_count})"
        )
    return 3, (
        f"simple_scope(type={node_type}, children={child_count}, "
        f"depends_on={depends_count}, refs={refs_count})"
    )


def replace_managed_block(text: str, block_key: str, replacement: str) -> str:
    start_marker, end_marker = MANAGED_MARKERS[block_key]
    start = text.find(start_marker)
    end = text.find(end_marker)
    if start == -1 or end == -1 or end < start:
        raise ValueError(f"Managed complexity block '{block_key}' is missing or malformed.")
    start_content = start + len(start_marker)
    return text[:start_content] + "\n" + replacement.strip() + "\n" + text[end:]


def sync_complexity(node_dir: Path, requested_level: int | str = "auto") -> tuple[int, str]:
    meta_path = node_dir / "meta.yaml"
    meta = load_yaml(meta_path)
    if requested_level == "auto":
        level, reason = recommend_complexity(node_dir, meta)
        mode = "auto"
    else:
        level = int(requested_level)
        if level not in VALID_COMPLEXITIES:
            raise ValueError(f"Invalid complexity level: {level}")
        reason = f"manual_override(level={level})"
        mode = "manual"

    skill_dir = Path(__file__).resolve().parent
    profile = load_complexity_profile(skill_dir, level)
    file_map = {
        "brief": node_dir / "brief.md",
        "execute": node_dir / "execute.md",
        "validate": node_dir / "validate.md",
        "roadmap": node_dir / "plan" / "local-roadmap.md",
    }
    for key, path in file_map.items():
        text = path.read_text(encoding="utf-8")
        path.write_text(replace_managed_block(text, key, profile[key]), encoding="utf-8")

    meta["complexity_level"] = level
    meta["complexity_mode"] = mode
    meta["complexity_reason"] = reason
    meta["complexity_last_reviewed_at"] = today_iso()
    write_yaml(meta_path, meta)
    return level, reason


def effective_doc(title: str, intro: str, sections: tuple[tuple[str, str, str], ...]) -> str:
    lines = [f"# {title}", "", intro, ""]
    for heading, source, body in sections:
        lines.append(f"## {heading}")
        lines.append("")
        lines.append(f"Source: `{source}`")
        lines.append("")
        lines.append(body if body else "_Empty._")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def sync_rules(node_dir: Path) -> None:
    user_rules = ensure_user_global_rules()
    todo_root = find_todo_root(node_dir)
    project_rules = todo_root / "rules" / "project-rules.md" if todo_root else None
    parent_dir = parent_path(node_dir)
    parent_rules = parent_dir / "rules" / "effective-rules.md" if parent_dir else None
    local_rules = node_dir / "rules" / "local-rules.md"
    local_meta = load_yaml(node_dir / "meta.yaml")
    terminal_ancestor = nearest_terminal_ancestor(node_dir)
    if terminal_ancestor is None:
        inherited_closure = (
            f"- This node's persisted status is `{local_meta.get('status', 'unknown')}`.\n"
            "- No terminal ancestor status was detected when these effective rules were generated.\n"
            "- If this node is `done` or `archived`, treat this node and every descendant as effectively closed."
        )
    else:
        ancestor_dir, ancestor_meta = terminal_ancestor
        inherited_closure = (
            f"- Treat this node as effectively closed because ancestor "
            f"`{ancestor_meta.get('id', ancestor_dir.name)}` has persisted status "
            f"`{ancestor_meta.get('status', 'unknown')}`.\n"
            "- Do not rewrite this node's own `meta.yaml.status` solely to mirror the ancestor closure.\n"
            "- Report the persisted status and the inherited effective closure separately when status detail matters."
        )

    rules_text = effective_doc(
        "Effective Rules",
        "Use this file during execution. Precedence is user-global, then project-global, then parent effective rules, then local node rules. Local rules may only tighten inherited constraints.",
        (
            ("Closure status interpretation", "meta.yaml ancestry", inherited_closure),
            ("User-global rules", os_relative(node_dir, user_rules), read_optional(user_rules, "_Missing user-global rules._")),
            ("Project rules", os_relative(node_dir, project_rules) if project_rules and project_rules.exists() else "(none)", read_optional(project_rules, "_No project rules._")),
            ("Parent effective rules", os_relative(node_dir, parent_rules) if parent_rules else "(none)", read_optional(parent_rules, "_No parent effective rules._")),
            ("Local rules", "rules/local-rules.md", read_optional(local_rules, "_Missing local rules._")),
        ),
    )
    (node_dir / "rules" / "effective-rules.md").write_text(rules_text, encoding="utf-8")


def generate_effective_files(node_dir: Path) -> None:
    sync_rules(node_dir)


def list_top_level_nodes(tasks_root: Path) -> list[Path]:
    if not tasks_root.exists():
        return []
    return sorted(
        [item for item in tasks_root.iterdir() if is_node_dir(item)],
        key=lambda path: path.name,
    )


def update_tasks_entrypoint(todo_root: Path) -> None:
    tasks_root = todo_root / "tasks"
    tasks_root.mkdir(parents=True, exist_ok=True)
    entrypoint = tasks_root / "entrypoint.md"
    nodes = list_top_level_nodes(tasks_root)

    lines = [
        "# Tasks Entrypoint",
        "",
        "Use this file when the user wants to execute all tasks in the project TODO tree.",
        "",
        "## Global order",
        "",
    ]

    if nodes:
        for index, node in enumerate(nodes, start=1):
            meta = load_yaml(node / "meta.yaml")
            lines.append(
                f"{index}. `{(node / 'entrypoint.md').relative_to(todo_root).as_posix()}`"
                f" - status `{meta.get('status', 'unknown')}`, type `{meta.get('type', 'unknown')}`"
            )
    else:
        lines.append("- No task nodes exist yet.")

    lines.extend(
        [
            "",
            "## Rules",
            "",
            "- Execute tasks from this file only when the user asks for the whole queue or whole tree.",
            "- Respect task status and dependencies before starting execution.",
            "- Update node handoff and status after meaningful progress.",
        ]
    )
    entrypoint.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate_meta(meta: dict) -> list[str]:
    errors: list[str] = []
    required = {
        "id",
        "title",
        "type",
        "status",
        "priority",
        "parent",
        "depends_on",
        "depth",
        "updated_at",
        "next_action",
        "complexity_level",
        "complexity_mode",
        "complexity_reason",
        "complexity_last_reviewed_at",
    }
    missing = sorted(required - set(meta))
    if missing:
        errors.append(f"Missing meta keys: {', '.join(missing)}")
        return errors

    try:
        ensure_valid_id(str(meta["id"]))
    except ValueError as exc:
        errors.append(str(exc))

    if meta["type"] not in VALID_TYPES:
        errors.append(f"Invalid type '{meta['type']}'.")
    if meta["status"] not in VALID_STATUSES:
        errors.append(f"Invalid status '{meta['status']}'.")
    if not isinstance(meta["depends_on"], list):
        errors.append("depends_on must be a list.")
    if meta["complexity_level"] not in VALID_COMPLEXITIES:
        errors.append(f"Invalid complexity_level '{meta['complexity_level']}'.")
    if meta["complexity_mode"] not in VALID_COMPLEXITY_MODES:
        errors.append(f"Invalid complexity_mode '{meta['complexity_mode']}'.")

    expected_depth = compute_depth(str(meta["id"]))
    if meta["depth"] != expected_depth:
        errors.append(f"Depth {meta['depth']} does not match id-derived depth {expected_depth}.")

    return errors
