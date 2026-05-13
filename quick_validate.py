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
    required_keys = {"entrypoint", "brief", "execute", "validate", "roadmap"}
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
        high_node = tasks_root / "TASK-001_high-complexity-system"
        medium_node = tasks_root / "TASK-002_medium-feature-flow"
        low_node = tasks_root / "TASK-003_low-complexity-fix"
        run_command(
            [
                sys.executable,
                "scripts/init_work_package.py",
                "--root",
                str(tasks_root),
                "--id",
                "TASK-001",
                "--title",
                "Build a new production analytics system",
                "--folder-name",
                "High complexity system",
                "--type",
                "container",
                "--complexity",
                "auto",
            ]
        )
        run_command([sys.executable, "scripts/validate_work_package.py", "--node", str(high_node)])
        high_meta = json.loads((high_node / "meta.yaml").read_text(encoding="utf-8"))
        if high_meta["complexity_level"] != 1:
            fail("container node should resolve to complexity level 1.")
        high_brief = (high_node / "brief.md").read_text(encoding="utf-8")
        if "senior" not in high_brief.lower() or "production" not in high_brief.lower():
            fail("level 1 brief should include senior production-quality framing.")

        run_command(
            [
                sys.executable,
                "scripts/init_work_package.py",
                "--root",
                str(tasks_root),
                "--id",
                "TASK-002",
                "--title",
                "Refactor checkout flow",
                "--folder-name",
                "Medium feature flow",
                "--type",
                "task",
                "--complexity",
                "auto",
            ]
        )
        run_command([sys.executable, "scripts/validate_work_package.py", "--node", str(medium_node)])
        medium_meta = json.loads((medium_node / "meta.yaml").read_text(encoding="utf-8"))
        if medium_meta["complexity_level"] != 2:
            fail("task node should resolve to complexity level 2.")

        run_command(
            [
                sys.executable,
                "scripts/init_work_package.py",
                "--root",
                str(tasks_root),
                "--id",
                "TASK-003",
                "--title",
                "Fix local input trimming helper",
                "--folder-name",
                "Low complexity fix",
                "--type",
                "leaf",
                "--complexity",
                "3",
            ]
        )
        run_command([sys.executable, "scripts/validate_work_package.py", "--node", str(low_node)])
        low_entrypoint = (low_node / "entrypoint.md").read_text(encoding="utf-8")
        for expected in ("Professional profile", "Mission", "Context", "Scope", "Execution", "Validation", "Handoff"):
            if expected not in low_entrypoint:
                fail(f"level 3 entrypoint is missing compact section: {expected}")

        blocked_child = subprocess.run(
            [
                sys.executable,
                "scripts/init_work_package.py",
                "--root",
                str(tasks_root),
                "--id",
                "TASK-003-01",
                "--title",
                "Invalid low-level child",
                "--parent",
                str(low_node),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        if blocked_child.returncode == 0:
            fail("level 3 leaf nodes must reject child creation.")
        if "cannot have child nodes" not in (blocked_child.stdout + blocked_child.stderr):
            fail("level 3 child rejection should explain that low-level nodes cannot have child nodes.")

        run_command([sys.executable, "scripts/sync_complexity.py", "--node", str(medium_node)])
        run_command([sys.executable, "scripts/sync_rules.py", "--node", str(medium_node)])
        run_command(
            [
                sys.executable,
                "scripts/update_handoff.py",
                "--node",
                str(medium_node),
                "--status",
                "paused",
                "--next-action",
                "Resume smoke-test work.",
            ]
        )
        run_command(
            [
                sys.executable,
                "scripts/update_handoff.py",
                "--node",
                str(medium_node),
                "--status",
                "review",
                "--next-action",
                "Review smoke-test output.",
            ]
        )
        run_command([sys.executable, "scripts/validate_work_package.py", "--node", str(medium_node)])
        run_command(
            [
                sys.executable,
                "scripts/init_work_package.py",
                "--root",
                str(tasks_root),
                "--id",
                "TASK-002-01",
                "--title",
                "Valid medium child",
                "--parent",
                str(medium_node),
                "--folder-name",
                "Valid medium child",
            ]
        )
        medium_child = medium_node / "children" / "TASK-002-01_valid-medium-child"
        run_command([sys.executable, "scripts/validate_work_package.py", "--node", str(medium_child)])

        run_command([sys.executable, "scripts/sync_complexity.py", "--node", str(medium_node), "--level", "3"])
        invalid_level3 = subprocess.run(
            [sys.executable, "scripts/validate_work_package.py", "--node", str(medium_node)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        if invalid_level3.returncode == 0:
            fail("validation should reject level 3 nodes that contain children.")


def main() -> None:
    validate_skill_frontmatter()
    validate_references_exist()
    validate_complexity_profiles()
    validate_scripts_compile()
    smoke_test_work_package()
    print("quick validation passed.")


if __name__ == "__main__":
    main()
