# Todo Skill

Portable agent skill for simple file-based TODO plans that can be resumed from
disk without relying on chat history.

## What It Does

- Creates or updates `TODO.md`.
- Uses optional `TODO/TASK-001.md` files for detailed tasks.
- Tracks status, checklist, notes, and handoff in Markdown.
- Avoids scripts, config, and recursive task frameworks.

## Installation

Place this folder in any agent skills directory that supports `SKILL.md`.

```text
skills/todo-skill
```

Invoke it as:

```text
$todo-skill
```

## Typical Layout

The skill keeps project task state in the target repository:

```text
TODO/
  TASK-001.md
  TASK-002.md
TODO.md
```

## Task Format

```markdown
# TASK-001 - Short Title

Status: backlog | active | blocked | review | done

## Goal
...

## Checklist
- [ ] ...

## Notes
...

## Handoff
...
```

## Status Rules

- `backlog`: not started or not fully shaped.
- `active`: being worked now.
- `blocked`: waiting on external input.
- `review`: implementation is done and needs review or validation.
- `done`: complete and validated.
