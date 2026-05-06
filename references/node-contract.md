# Node Contract

Each work-package node uses the same layout, regardless of depth.

```text
<NODE>/
  entrypoint.md
  meta.yaml
  brief.md
  execute.md
  validate.md
  handoff.md
  result.md
  plan/
    local-roadmap.md
    current-step.md
  rules/
    local-rules.md
    inheritance.yaml
    effective-rules.md
  context/
    local-context.md
  refs/
  children/
```

## File meanings

- `entrypoint.md`: exact read order for execution.
- `meta.yaml`: stable machine-readable state for the node.
- `brief.md`: goal, scope, and non-goals for this node only.
- `execute.md`: implementation instructions for the next agent.
- `validate.md`: checks and acceptance criteria.
- `handoff.md`: current factual state, blockers, next move.
- `result.md`: final summary once the node closes.
- `plan/local-roadmap.md`: node-local plan written by humans or agents.
- `plan/current-step.md`: exact resume cursor.
- `rules/local-rules.md`: node-local constraints.
- `rules/inheritance.yaml`: declared rule inheritance model and source files.
- `rules/effective-rules.md`: materialized rules for isolated execution.
- `context/local-context.md`: node-local context that does not belong in rules.
- `refs/`: optional supporting artifacts.
- `children/`: nested nodes with the same contract.

## Required `meta.yaml` keys

- `id`
- `title`
- `type`
- `status`
- `priority`
- `parent`
- `depends_on`
- `depth`
- `updated_at`
- `next_action`
- `complexity_level`
- `complexity_mode`
- `complexity_reason`
- `complexity_last_reviewed_at`

## Allowed values

- `type`: `container`, `task`, `leaf`
- `status`: `backlog`, `ready`, `active`, `blocked`, `review`, `witherror`, `done`, `archived`
- Agent-driven progression stops at `review`; `done` and `archived` are user-gated terminal statuses.

## Effective Closure

- Persisted status is the literal value in a node's own `meta.yaml.status`.
- Effective closure is inherited from ancestors: if any parent or ancestor has persisted status `done` or `archived`, treat every descendant as closed for reporting and execution decisions.
- Do not update descendant `meta.yaml.status` values merely because an ancestor closed.
- When status detail matters, report both values, for example: persisted `active`, effectively closed by ancestor `TASK-001` status `done`.

## ID format

- Root: `TASK-001`
- Child: `TASK-001-01`
- Grandchild: `TASK-001-01-01`

Depth equals the number of suffix segments after the root pair:

- `TASK-001` -> depth `0`
- `TASK-001-01` -> depth `1`
- `TASK-001-01-01` -> depth `2`
