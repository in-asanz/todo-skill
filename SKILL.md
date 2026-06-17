---
name: todo-skill
description: "Create and maintain simple file-based TODO task plans that can be resumed by any agent. Use when an agent needs to break work into tasks, record status, leave handoff notes, or resume later without relying on chat history."
---

# Todo Skill

Use this skill to keep task state in plain Markdown files inside the target project.

## Layout

```text
TODO.md
TODO/
  TASK-001.md
  TASK-002.md
```

Use `TODO.md` as the index. Use one file per task only when the work needs details, handoff notes, or subtasks.

## Task File

Use this format:

```markdown
# TASK-001 - Short Title

Status: backlog | active | blocked | review | done

## Goal
One or two sentences describing the outcome.

## Checklist
- [ ] Concrete step
- [ ] Concrete validation

## Notes
Important context, links, decisions, or blockers.

## Handoff
Current state and next action for another agent.
```

## Workflow

1. Inspect existing `TODO.md` and `TODO/*.md` before creating anything.
2. Use stable IDs: `TASK-001`, `TASK-002`, `TASK-003`.
3. Keep task text self-contained enough to resume from disk.
4. Prefer a short checklist over nested task systems.
5. Update status and handoff notes before stopping.
6. Mark `done` only when the work and validation are complete.

## Rules

- Do not rely on prior chat history for task execution.
- Do not create deep recursive task trees unless the user asks.
- Do not add scripts, config files, or generated frameworks for simple planning.
- Ask only when missing information changes scope, implementation, or validation.
- Keep output short: changed task files, current status, and next action.
