# CLI Contract

## `init_work_package.py`

Create a root node or a child node.

```text
python scripts/init_work_package.py --root <dir> --id <id> --title <title> [--folder-name <name>] [--parent <path>] [--type <type>] [--complexity <auto|1|2|3>]
```

- `--root`: directory that stores top-level nodes, usually `<project>/TODO/tasks`
- `--id`: hierarchical node ID
- `--title`: human-readable title
- `--folder-name`: optional human-readable folder suffix; creates names like `TASK-001_setup-auth-flow`
- `--parent`: existing parent node path; when present, create the new node under `children/`
- `--type`: `container`, `task`, or `leaf`; default is `task`
- `--complexity`: managed detail level; default is `auto`

Behavior:

- creates the full node structure
- bootstraps `TODO/config/todo-skill.json` and `TODO/rules/project-rules.md` when the root lives under `TODO/`
- creates or updates `TODO/tasks/entrypoint.md`
- writes template-driven source files
- selects or records the complexity level
- writes `inheritance.yaml`
- writes managed complexity blocks
- materializes `rules/effective-rules.md`
- validates the node before exiting successfully
- rejects child creation when the parent is a level 3 or `leaf` node

Directory naming:

- When `--folder-name` is omitted, the directory name is exactly the ID, for example `TASK-001`.
- When `--folder-name` is present, it is normalized to a lowercase ASCII suffix after the ID, for example `TASK-001_setup-auth-flow`.
- The stable node ID remains `meta.yaml.id`; the folder suffix is only for human scanning and does not affect hierarchy.

## `sync_complexity.py`

Review or migrate managed complexity level for a node.

```text
python scripts/sync_complexity.py --node <path> [--level <auto|1|2|3>]
```

Behavior:

- recommends complexity automatically when `--level auto`
- updates managed blocks in `entrypoint.md`, `brief.md`, `execute.md`, `validate.md`, and `plan/local-roadmap.md`
- updates complexity metadata in `meta.yaml`
- preserves manual text outside managed markers

## `sync_rules.py`

Regenerate `rules/effective-rules.md` from all rule sources.

```text
python scripts/sync_rules.py --node <path>
```

Behavior:

- reads `.agents/rules/user-global-rules.md` when present
- reads `TODO/rules/project-rules.md` when present
- reads parent `rules/effective-rules.md` when present
- reads local `rules/local-rules.md`
- rewrites `rules/effective-rules.md`

## `resolve_effective_state.py`

Compatibility wrapper that syncs complexity and effective rules after source edits.

```text
python scripts/resolve_effective_state.py --node <path>
```

Behavior:

- re-runs complexity synchronization in auto mode
- recalculates `rules/effective-rules.md`

## `update_handoff.py`

Refresh resume state without editing multiple files manually.

```text
python scripts/update_handoff.py --node <path> --status <status> --next-action "<text>" [--user-approved-terminal-status]
```

Behavior:

- re-runs complexity synchronization in auto mode
- updates `meta.yaml`
- rewrites `handoff.md`
- rewrites `plan/current-step.md`
- updates `TODO/tasks/entrypoint.md` when the node lives under `TODO/`
- accepts `backlog` for tasks that are not fully defined or still need better process definition
- accepts `paused` for tasks intentionally paused without an external blocker
- accepts `witherror` for implemented tasks with known errors that must be fixed
- rejects `done` and `archived` unless `--user-approved-terminal-status` is present

## `validate_work_package.py`

Validate node structure and metadata.

```text
python scripts/validate_work_package.py --node <path>
```

Checks:

- required files and directories exist
- `meta.yaml` has required keys and allowed values
- ID shape and depth are consistent
- directory names are either `<id>` or `<id>_<folder-name>`
- parent-child relationships are coherent
- `inheritance.yaml` points to real sources
- `rules/effective-rules.md` exists
- project rules exist when the node lives under `TODO/`
- complexity metadata exists and managed blocks are present
- level 3 and `leaf` nodes do not contain child nodes
