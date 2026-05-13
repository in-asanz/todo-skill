# Complexity Levels

This skill supports three managed complexity levels per node. The levels describe real work scope, not just how much text a node contains.

## Level 1 - High complexity

Use for work that resembles creating or coordinating a complete project, new system, new repository, full program, or complex capability inside a larger program.

Expected characteristics:

- senior architect or senior lead engineer framing
- broad mission, explicit architecture boundaries, dependencies, and outputs
- child nodes for subsystems, milestones, risk areas, or implementation surfaces
- phased execution with integration and verification checkpoints
- broad validation evidence across the affected system

Examples:

- create a new service, repository, or end-to-end product module
- build a complete application workflow spanning several subsystems
- implement a complex capability that affects architecture, data flow, UI, API, and tests

## Level 2 - Medium complexity

Use for normal production work inside an existing project: a new feature, flow change, refactor, maintenance task, or structural improvement.

Expected characteristics:

- senior engineer framing
- concrete mission, affected surfaces, project conventions, integration points, and acceptance criteria
- practical roadmap with analysis, implementation, and verification
- focused validation for main behavior and regression risk
- child nodes only if the work grows into multiple coordinated surfaces

Examples:

- add a normal feature to an existing module
- change a user or data flow
- refactor a component, service, command, or integration
- perform maintainability or compatibility work

## Level 3 - Low complexity

Use for simple leaf work: a small fix, small function, local adjustment, or narrow task that should be completed directly.

Expected characteristics:

- senior engineer framing for precise, low-risk production changes
- one narrow objective
- no child nodes
- operative task description consolidated in `entrypoint.md`
- tight local validation with concrete evidence

Examples:

- fix a straightforward bug in one local surface
- add a small helper function
- adjust a local validation rule or message
- make a narrow compatibility correction

## Automatic recommendation

The skill recommends complexity automatically.

Current heuristic:

- recommend level 1 when a node is a `container`, already has children, has several dependencies, has several reference artifacts, or coordinates a broad system/program scope
- recommend level 2 for normal `task` nodes, feature work, flow changes, refactors, maintenance, or work with moderate integration surface
- recommend level 3 for simple `leaf` nodes with no children, no dependencies, and no supporting references

## Low-complexity leaf rule

Level 3 is the lowest task level. Level 3 nodes and `leaf` nodes must not have child nodes.

If a low-complexity task needs subtasks, raise it to level 2 before adding children. Do not hide multi-surface coordination inside a level 3 node.

## Managed migration

Complexity migration rewrites only managed blocks between these markers:

- `<!-- COMPLEXITY:ENTRYPOINT:START -->` / `<!-- COMPLEXITY:ENTRYPOINT:END -->`
- `<!-- COMPLEXITY:BRIEF:START -->` / `<!-- COMPLEXITY:BRIEF:END -->`
- `<!-- COMPLEXITY:EXECUTE:START -->` / `<!-- COMPLEXITY:EXECUTE:END -->`
- `<!-- COMPLEXITY:VALIDATE:START -->` / `<!-- COMPLEXITY:VALIDATE:END -->`
- `<!-- COMPLEXITY:ROADMAP:START -->` / `<!-- COMPLEXITY:ROADMAP:END -->`

Manual text outside those blocks is preserved.
