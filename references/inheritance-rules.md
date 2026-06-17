# Inheritance Rules

This skill uses materialized inheritance for rules only, not implicit inheritance at read time.

## Precedence

Effective execution state is built in this order:

1. User-global rules from `.agents/rules/user-global-rules.md`
2. Project rules from `TODO/rules/project-rules.md`
3. Direct parent effective rules
4. Local node rules

## Restrictive merge policy

Children may add tighter restrictions, narrower scope, and more specific next steps.
Children must not override inherited guarantees or contradict inherited constraints.

Because rules are stored as Markdown, the merge is structural rather than fully semantic:

- scripts materialize all inherited rule sources in the effective file
- validators enforce source presence, precedence metadata, and parent-child consistency
- humans and agents must still write local rules in a restrictive style

## User-global source

User-wide rules live in:

- `.agents/rules/user-global-rules.md`

## Project source

Project-wide rules live in:

- `TODO/rules/project-rules.md`

## Parent source

For non-root nodes, the direct parent contributes:

- `rules/effective-rules.md`

## Local source

Every node contributes:

- `rules/local-rules.md`

## Materialized output

Execution should use only:

- `rules/effective-rules.md`

That prevents deep nodes from depending on live traversal of parent rule files.

## Non-rule context

Context and roadmap stay local to the node:

- `context/local-context.md`
- `plan/local-roadmap.md`

If more context is needed, inspect only the direct parent node rather than materializing the whole tree recursively.
