# Resume Protocol

A node is resumable when another agent can continue from disk without prior chat memory.

## Minimum resumable state

Keep these files aligned:

- `meta.yaml`
- `handoff.md`
- `plan/current-step.md`

## Required behaviors

- Never encode progress as a percentage only.
- Always state what is done, what is still missing, and the exact next action.
- Keep the next action executable in one step when possible.
- Update `updated_at` whenever the resume state changes.

## Status guidance

- `ready`: no work started or re-opened and ready to start
- `active`: implementation in progress
- `blocked`: waiting on a real blocker
- `review`: implementation done, validation or review still pending
- `done`: fully closed, but only after the user explicitly asks to close the node
- `archived`: intentionally retired from active use, but only after the user explicitly asks to retire the node
- The default agent-owned flow ends at `review`.

## Resume read order

When resuming a node, read:

1. `entrypoint.md`
2. `meta.yaml`
3. `rules/effective-rules.md`
4. `context/local-context.md`
5. `plan/local-roadmap.md`
6. `plan/current-step.md`
7. `execute.md`
8. `validate.md`
9. `handoff.md`

## Recommended write-back

At the end of an unfinished session, update:

- `meta.yaml.status`
- `meta.yaml.updated_at`
- `meta.yaml.next_action`
- `handoff.md`
- `plan/current-step.md`
