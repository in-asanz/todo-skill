# Complexity Levels

This skill supports three managed detail levels per node.

## Level 1

Highest detail level.
Use when the node has children, multiple dependencies, multiple supporting references, or broad coordination scope.

Expected characteristics:

- richer brief sections
- explicit execution phases
- broader validation checklist
- more detailed roadmap wording

## Level 2

Medium detail level.
Use for regular task nodes that need a meaningful plan and validation surface but do not coordinate a large subtree.

Expected characteristics:

- balanced brief
- short execution checklist
- moderate validation checklist
- practical roadmap

## Level 3

Simplest detail level.
Use for small leaf tasks with narrow scope and low orchestration overhead.

Expected characteristics:

- compact brief
- minimal execution instructions
- tight validation list
- concise roadmap

## Automatic recommendation

The skill recommends complexity automatically.

Current heuristic:

- recommend level 1 when a node has children, is a `container`, has at least 2 dependencies, or has several refs artifacts
- recommend level 2 for normal `task` nodes with moderate surface
- recommend level 3 for simple `leaf` nodes or narrow tasks without extra coordination

## Managed migration

Complexity migration rewrites only managed blocks between these markers:

- `<!-- COMPLEXITY:BRIEF:START -->` / `<!-- COMPLEXITY:BRIEF:END -->`
- `<!-- COMPLEXITY:EXECUTE:START -->` / `<!-- COMPLEXITY:EXECUTE:END -->`
- `<!-- COMPLEXITY:VALIDATE:START -->` / `<!-- COMPLEXITY:VALIDATE:END -->`
- `<!-- COMPLEXITY:ROADMAP:START -->` / `<!-- COMPLEXITY:ROADMAP:END -->`

Manual text outside those blocks is preserved.
