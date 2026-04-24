# Project Layout

Keep the skill global in `.codex`, but keep project-local operating files under the project's `TODO/` folder.

Recommended layout:

```text
<project>/
  TODO/
    AGENTS.md
    config/
      recursive-task-authoring.json
    rules/
      project-rules.md
    tasks/
      TASK-001/
      TASK-002/
```

## Responsibilities

- `.codex/skills/recursive-task-authoring/`: reusable global skill logic
- `.codex/rules/user-global-rules.md`: user-wide rules source
- `TODO/config/recursive-task-authoring.json`: optional project-local config for this skill
- `TODO/rules/project-rules.md`: project-level rules source
- `TODO/tasks/`: actual task trees and nodes

## Default behavior

When the target root is inside a `TODO/` tree, the skill should:

- create `TODO/config/recursive-task-authoring.json` if missing
- create `TODO/rules/project-rules.md` if missing
- create task nodes under `TODO/tasks/`

This keeps project-local task assets together and avoids spreading task system files across unrelated folders.
