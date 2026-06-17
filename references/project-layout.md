# Project Layout

Keep the skill global in the agent's skills directory, but keep project-local operating files under the project's `TODO/` folder.

Recommended layout:

```text
<project>/
  TODO/
    AGENTS.md
    config/
      todo-skill.json
    rules/
      project-rules.md
    tasks/
      entrypoint.md
      TASK-001/
      TASK-002_descriptive-name/
      TASK-003/
```

## Responsibilities

- `.agents/skills/todo-skill/`: reusable global skill logic
- `.agents/rules/user-global-rules.md`: user-wide rules source
- `TODO/config/todo-skill.json`: optional project-local config for this skill
- `TODO/rules/project-rules.md`: project-level rules source
- `TODO/tasks/entrypoint.md`: global execution index for all active tasks
- `TODO/tasks/`: actual task trees and nodes

## Default behavior

When the target root is inside a `TODO/` tree, the skill should:

- create `TODO/config/todo-skill.json` if missing
- create `TODO/rules/project-rules.md` if missing
- create `TODO/tasks/entrypoint.md` if missing
- create task nodes under `TODO/tasks/`

This keeps project-local task assets together and avoids spreading task system files across unrelated folders.
