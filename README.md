# Todo Skill

Codex skill for creating recursive, self-contained TODO task trees that can be resumed from disk without relying on chat history.

## What It Does

- Creates root tasks and nested subtasks with a consistent node layout.
- Materializes inherited rules into each node's `rules/effective-rules.md`.
- Keeps project-local task data under `TODO/`.
- Tracks resumable state through `meta.yaml`, `handoff.md`, and `plan/current-step.md`.
- Supports managed task complexity levels for simple, medium, and coordination-heavy work.

## Installation

Place this repository in your Codex skills directory:

```text
~/.codex/skills/todo-skill
```

Then invoke it as:

```text
$todo-skill
```

## Typical Layout

The skill keeps reusable logic in the skill folder and project-specific task data in the target project's `TODO/` folder:

```text
TODO/
  config/
    todo-skill.json
  rules/
    project-rules.md
  tasks/
    entrypoint.md
    TASK-001/
```

## Main Commands

Create a root task:

```powershell
python scripts/init_work_package.py --root TODO/tasks --id TASK-001 --title "Example task"
```

Create a child task:

```powershell
python scripts/init_work_package.py --root TODO/tasks --id TASK-001-01 --title "Example child" --parent TODO/tasks/TASK-001
```

Refresh complexity and rules:

```powershell
python scripts/resolve_effective_state.py --node TODO/tasks/TASK-001
```

Update resumable state:

```powershell
python scripts/update_handoff.py --node TODO/tasks/TASK-001 --status review --next-action "Review the result."
```

Validate a node:

```powershell
python scripts/validate_work_package.py --node TODO/tasks/TASK-001
```

Validate the skill itself:

```powershell
python quick_validate.py
```

## Status Rules

Agents may move a task through `backlog`, `ready`, `active`, `blocked`, `review`, and `witherror`.
Use `backlog` when a task is not fully defined or still needs better execution or validation process definition.
Use `witherror` when a task was executed and implemented, but validation or review found errors that must be fixed.

Terminal statuses are user-gated:

- `done`
- `archived`

Use `--user-approved-terminal-status` only when the user explicitly approves closing or retiring a node.
When a parent task is `done` or `archived`, all descendants are considered effectively closed, but their own `meta.yaml.status` values are not changed automatically.

## Publishing Notes

Generated project task state lives under `TODO/` and is ignored by this repository. Publish the reusable skill files, not local task instances.
