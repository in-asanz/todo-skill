# CLI Contract

## `init_work_package.py`

Create a root node or a child node.

```text
python scripts/init_work_package.py --root <dir> --id <id> --title <title> [--parent <path>] [--type <type>] [--complexity <auto|1|2|3>]
```

- `--root`: directory that stores top-level nodes, usually `<project>/TODO/tasks`
- `--id`: hierarchical node ID
- `--title`: human-readable title
- `--parent`: existing parent node path; when present, create the new node under `children/`
- `--type`: `container`, `task`, or `leaf`; default is `task`
- `--complexity`: managed detail level; default is `auto`

Behavior:

- creates the full node structure
- bootstraps `TODO/config/recursive-task-authoring.json` and `TODO/rules/project-rules.md` when the root lives under `TODO/`
- writes template-driven source files
- selects or records the complexity level
- writes `inheritance.yaml`
- writes managed complexity blocks
- materializes `rules/effective-rules.md`
- validates the node before exiting successfully

## `sync_complexity.py`

Review or migrate managed complexity level for a node.

```text
python scripts/sync_complexity.py --node <path> [--level <auto|1|2|3>]
```

Behavior:

- recommends complexity automatically when `--level auto`
- updates managed blocks in `brief.md`, `execute.md`, `validate.md`, and `plan/local-roadmap.md`
- updates complexity metadata in `meta.yaml`
- preserves manual text outside managed markers

## `sync_rules.py`

Regenerate `rules/effective-rules.md` from all rule sources.

```text
python scripts/sync_rules.py --node <path>
```

Behavior:

- reads `.codex/rules/user-global-rules.md` when present
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
python scripts/update_handoff.py --node <path> --status <status> --next-action "<text>"
```

Behavior:

- re-runs complexity synchronization in auto mode
- updates `meta.yaml`
- rewrites `handoff.md`
- rewrites `plan/current-step.md`

## `validate_work_package.py`

Validate node structure and metadata.

```text
python scripts/validate_work_package.py --node <path>
```

Checks:

- required files and directories exist
- `meta.yaml` has required keys and allowed values
- ID shape and depth are consistent
- parent-child relationships are coherent
- `inheritance.yaml` points to real sources
- `rules/effective-rules.md` exists
- project rules exist when the node lives under `TODO/`
- complexity metadata exists and managed blocks are present
