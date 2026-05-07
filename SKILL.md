---
name: todo-skill
description: Create, split, normalize, and resume recursive self-contained TODO task trees with materialized effective rules per node. Use when Codex needs to create a root task, add a child task/subtask, sync inherited rules, or leave a task resumable without relying on prior chat memory. Prefer storing project-local task assets, project rules, and skill config under the project's TODO folder.
---

# Todo Skill

## Overview

Use this skill to build recursive work-package trees where every node is executable in isolation.
Prefer this workflow when tasks must survive context compression, handoffs, or deep nesting without losing inherited rules, resume state, or the right level of task-detailing.

## Read Order

1. Read [references/node-contract.md](references/node-contract.md).
2. Read [references/inheritance-rules.md](references/inheritance-rules.md).
3. Read [references/resume-protocol.md](references/resume-protocol.md) when resuming or leaving a partially completed task.
4. Read [references/complexity-levels.md](references/complexity-levels.md).
5. Read [references/project-layout.md](references/project-layout.md).
6. Read [references/question-template.md](references/question-template.md) when the repo cannot answer a decision that changes implementation, validation, scope, or closure.
7. Read [references/cli-contract.md](references/cli-contract.md) before running scripts directly.

## Workflow

### 1. Inspect the current tree

- Identify whether the request needs a new root node, a child node, or a rules refresh.
- Read the target node's `entrypoint.md`, `meta.yaml`, and `rules/effective-rules.md` before deciding anything.
- Treat the project-local operating surface as `TODO/` whenever the project has one.
- Treat `TODO/tasks/entrypoint.md` as the global tree entrypoint when the user wants to execute all tasks.
- Treat legacy layouts as out of scope for v1; do not migrate them silently.
- When asked about task status, report only the general/top-level tasks by default. Include subtasks only when the user asks for more detail, asks about tasks and subtasks, or asks to increase the tree detail level.

### 2. Create or extend the tree

- Use `scripts/init_work_package.py` to create a root node or child node.
- Keep IDs hierarchical: `TASK-001`, `TASK-001-01`, `TASK-001-01-01`.
- Task directories may append an optional descriptive suffix after the ID, using `TASK-001_descriptive-name`; the ID prefix remains the source of ordering and hierarchy.
- Keep one node contract for every depth level; do not invent alternate layouts for subtasks.
- Let the skill choose complexity automatically unless a user asks for a specific level.
- Keep project-local config and project rules under `TODO/`, not inside the global skill folder.
- Keep the global task entrypoint inside `TODO/tasks/entrypoint.md`.
- After finishing the task description, give the user a ready-to-use resume prompt that references the node's base file, `entrypoint.md`.
- Format the prompt as: `Use $todo-skill and execute the task described in <absolute-or-project-relative-path-to-node>/entrypoint.md`.

### 3. Review complexity and migrate if needed

- Use `scripts/sync_complexity.py` to review the current node shape and align it to complexity level 1, 2, or 3.
- Complexity level 3 is the simplest layout, level 1 is the most detailed layout.
- Preserve manual content outside managed complexity blocks when migrating between levels.

### 4. Materialize effective rules

- Use `scripts/sync_rules.py` whenever inherited or local rules change.
- Complexity review runs before rules synchronization so the node always keeps the right detail level.
- Always execute tasks from `rules/effective-rules.md`, not by re-reading all parent rule files.
- Preserve precedence: user-global rules, project rules from `TODO/rules/project-rules.md`, parent effective rules, then local node rules.
- Do not recursively materialize roadmap or context files.

### 5. Leave resumable state

- Use `scripts/update_handoff.py` when a task remains open after a session.
- Keep `meta.yaml`, `handoff.md`, and `plan/current-step.md` aligned so another agent can resume from disk only.
- Use explicit statuses: `backlog`, `ready`, `active`, `blocked`, `review`, `witherror`, `done`, `archived`.
- Use `backlog` when the task is not fully defined, needs a better definition, or lacks complete and advanced execution or validation processes.
- Use `witherror` when the task has been executed and implemented, but validation or review found errors that must be fixed.
- Treat `review` or `witherror` as the last status an agent may set on its own.
- Set `done` or `archived` only after the user explicitly says to close or retire the node.
- Treat closure as inherited for interpretation: when a parent or ancestor is `done` or `archived`, every descendant is considered effectively closed even if the descendant's own `meta.yaml.status` still says `ready`, `active`, `blocked`, `review`, or `witherror`.
- Do not rewrite a child status just because an ancestor closed; report persisted child status and inherited effective closure separately when that distinction matters.
- Do not execute an effectively closed descendant unless the user explicitly asks to reopen or continue that descendant despite the ancestor closure.

### 6. Validate before handing off

- Run `scripts/validate_work_package.py --node <path>` on changed nodes.
- Run `quick_validate.py` on the skill itself after editing the skill assets.
- Do not leave nodes without `rules/effective-rules.md`, with inconsistent parent-child metadata, or with stale complexity metadata.

### 7. Ask only when the repo cannot answer

- Ask the user only when the missing information materially changes implementation, validation, scope, or closure and cannot be recovered from the repo, docs, or existing task tree.
- When asking, use the template in `references/question-template.md`.
- Each question must have 3 to 5 mutually exclusive options and exactly one recommended option.
- Keep questions grouped under the affected task or subtask name.
- Do not ask questions for facts the environment can answer.
## Guardrails

- Do not depend on prior chat history to execute a node.
- Do not encode task state in folder names.
- Do not let children contradict inherited rules; children may only add tighter restrictions.
- Do not skip rule synchronization after editing local rules, project rules, or user-global rules.
- Do not downgrade or upgrade complexity by manually rewriting whole files when managed blocks can be migrated automatically.
- Do not migrate legacy trees automatically in v1.
- Do not ask the user open-ended implementation questions when a structured multi-option question can close the decision faster.
- Do not set `done` or `archived` unless the user explicitly authorizes terminal closure; stop at `review` by default, or `witherror` when implemented work has known errors to fix.
- Do not mutate descendant statuses when closing a parent; inherited closure is an interpretation rule, not a metadata cascade.

## Script Entry Points

- `scripts/init_work_package.py --root <dir> --id <id> --title <title> [--folder-name <name>] [--parent <path>] [--type <type>] [--complexity <auto|1|2|3>]`
- `scripts/sync_complexity.py --node <path> [--level <auto|1|2|3>]`
- `scripts/sync_rules.py --node <path>`
- `scripts/resolve_effective_state.py --node <path>`
- `scripts/update_handoff.py --node <path> --status <status> --next-action "<text>" [--user-approved-terminal-status]`
- `scripts/validate_work_package.py --node <path>`
- `quick_validate.py`

## Node Execution Rule

When using a generated node, read only:

- `entrypoint.md`
- `meta.yaml`
- `rules/effective-rules.md`
- `context/local-context.md`
- `plan/local-roadmap.md`
- `plan/current-step.md`
- `execute.md`
- `validate.md`
- `handoff.md`

If that local material is still insufficient, inspect only the direct parent node for extra context. Do not reconstruct the whole tree by default.
