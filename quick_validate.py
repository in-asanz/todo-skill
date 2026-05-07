#!/usr/bin/env python3
from __future__ import annotations

import compileall
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def fail(message: str) -> None:
    raise SystemExit(f"quick validation failed: {message}")


def run_command(args: list[str], cwd: Path = ROOT) -> None:
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True)
    if result.returncode != 0:
        details = (result.stdout + result.stderr).strip()
        fail(f"{' '.join(args)}\n{details}")


def validate_skill_frontmatter() -> None:
    text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail("SKILL.md must start with YAML frontmatter.")
    match = re.match(r"---\n(.*?)\n---\n", text, flags=re.DOTALL)
    if not match:
        fail("SKILL.md frontmatter is not closed.")
    frontmatter = match.group(1)
    for key in ("name:", "description:"):
        if key not in frontmatter:
            fail(f"SKILL.md frontmatter is missing {key}")


def validate_references_exist() -> None:
    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    referenced_paths = re.findall(r"\]\((references/[^)]+)\)", skill_text)
    missing = [path for path in referenced_paths if not (ROOT / path).exists()]
    if missing:
        fail("missing referenced docs: " + ", ".join(sorted(missing)))


def validate_complexity_profiles() -> None:
    required_keys = {"brief", "execute", "validate", "roadmap"}
    for path in sorted((ROOT / "assets" / "complexity").glob("level-*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        missing = required_keys - set(data)
        if missing:
            fail(f"{path.relative_to(ROOT)} is missing keys: {', '.join(sorted(missing))}")


def validate_scripts_compile() -> None:
    ok = compileall.compile_dir(ROOT / "scripts", quiet=1)
    if not ok:
        fail("scripts do not compile.")


def smoke_test_work_package() -> None:
    with tempfile.TemporaryDirectory(prefix="todo-skill-") as temp_dir:
        tasks_root = Path(temp_dir) / "TODO" / "tasks"
        node = tasks_root / "TASK-001"
        named_node = tasks_root / "TASK-002_named-smoke-task"
        named_child = named_node / "children" / "TASK-002-01_named-child"
        run_command(
            [
                sys.executable,
                "scripts/init_work_package.py",
                "--root",
                str(tasks_root),
                "--id",
                "TASK-001",
                "--title",
                "Quick validation smoke task",
                "--type",
                "task",
                "--complexity",
                "auto",
            ]
        )
        run_command([sys.executable, "scripts/validate_work_package.py", "--node", str(node)])
        run_command([sys.executable, "scripts/sync_complexity.py", "--node", str(node)])
        run_command([sys.executable, "scripts/sync_rules.py", "--node", str(node)])
        run_command(
            [
                sys.executable,
                "scripts/update_handoff.py",
                "--node",
                str(node),
                "--status",
                "review",
                "--next-action",
                "Review smoke-test output.",
            ]
        )
        run_command([sys.executable, "scripts/validate_work_package.py", "--node", str(node)])
        run_command(
            [
                sys.executable,
                "scripts/init_work_package.py",
                "--root",
                str(tasks_root),
                "--id",
                "TASK-002",
                "--title",
                'Named "smoke" task',
                "--folder-name",
                "Named smoke task",
            ]
        )
        run_command(
            [
                sys.executable,
                "scripts/init_work_package.py",
                "--root",
                str(tasks_root),
                "--id",
                "TASK-002-01",
                "--title",
                "Named child",
                "--parent",
                str(named_node),
                "--folder-name",
                "Named child",
            ]
        )
        run_command([sys.executable, "scripts/validate_work_package.py", "--node", str(named_node)])
        run_command([sys.executable, "scripts/validate_work_package.py", "--node", str(named_child)])


def main() -> None:
    validate_skill_frontmatter()
    validate_references_exist()
    validate_complexity_profiles()
    validate_scripts_compile()
    smoke_test_work_package()
    print("quick validation passed.")


if __name__ == "__main__":
    main()
