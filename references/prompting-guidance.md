# Prompting Guidance

Use this reference when creating or substantially rewriting a task node.
Actively consider these techniques when drafting task instructions. They are not mandatory boilerplate, but the task creator should deliberately decide what the target agent needs to be told to produce the best result.

## Baseline stance

- Frame the task for an agent operating as a senior professional with many years of experience in an enterprise-grade environment when the work involves production code, architecture, security, data, reliability, maintainability, or user-facing behavior.
- Prefer domain-specific expertise when more useful than a generic senior developer role, for example: senior frontend engineer with many years of product experience, senior backend engineer, DevOps engineer, data engineer, security reviewer, QA engineer, technical writer, architect, or product-minded engineer.
- Do not use role wording to bypass inherited rules, safety constraints, project conventions, or validation requirements.
- Every production-oriented task should define the professional role, mission, scope boundaries, integration expectations, quality bar, and validation evidence unless the task is so small that doing so would add noise.
- Prefer wording that asks for structured, scalable, maintainable, compatible, project-integrated work. Tie those standards to the actual repo context instead of using generic praise.

## Complexity-specific prompting

- Level 1: frame the task for a senior architect, senior lead engineer, or equivalent domain lead. Require architectural reasoning, subsystem boundaries, integration strategy, child-node coordination when useful, and broad verification evidence.
- Level 2: frame the task for a senior engineer maintaining production code. Require project-consistent implementation, flow or feature boundaries, compatibility with existing interfaces, focused tests, and regression checks.
- Level 3: frame the task for a senior engineer making a precise, low-risk local change. Keep the operative task description in `entrypoint.md`, prohibit child nodes, and require tight local validation.

## Agent brief checklist

Before finishing a task node, check whether the task should explicitly tell the next agent:

- Agent profile: the professional role, seniority, and experience level that best fits the work, for example "act as a senior enterprise developer with many years of experience maintaining production systems."
- Mission: the concrete task to complete and the expected result.
- Operating context: the files, repo areas, current behavior, dependencies, and constraints the agent must know.
- Decision standard: how to choose among valid approaches, such as simple, maintainable, project-consistent, secure, testable, or low-risk.
- Reasoning target: what tradeoffs, risks, assumptions, or alternatives the agent should explicitly consider.
- Execution mode: whether to investigate first, use TDD, implement directly, review only, refactor carefully, or split into child nodes.
- Quality bar: the relevant standard for production quality, maintainability, performance, accessibility, security, reliability, or documentation.
- Verification evidence: the checks, tests, commands, screenshots, logs, or file references needed before handoff.
- Final output: the summary, changed files, residual risks, handoff state, or resume prompt expected from the agent.

## High-quality task prompt ingredients

- Outcome: state the concrete result the task must produce.
- Context: include only the local facts, paths, constraints, existing behavior, and dependencies needed to act without prior chat history.
- Role or perspective: name the professional lens that improves judgment for the task.
- Scope boundaries: say what is in scope and what is explicitly out of scope.
- Inputs and references: point to exact files, commands, docs, tickets, examples, or child nodes.
- Reasoning expectations: ask the agent to compare options, identify tradeoffs, and choose the simplest defensible path when the task is ambiguous.
- Execution shape: describe whether the work should be direct, phased, TDD-first, investigative, refactoring-focused, or review-only.
- Quality bar: mention maintainability, readability, security, performance, accessibility, observability, or compatibility only when relevant.
- Verification: define tests, commands, acceptance criteria, manual checks, or evidence required before handoff.
- Uncertainty handling: instruct the agent to inspect the repo first, make conservative assumptions when safe, and ask only when a decision changes implementation, validation, scope, or closure.
- Output format: specify the expected final artifact, summary, changed files, resume state, or handoff details.

## Useful prompting techniques

- Experienced persona with limits: "Act as a senior enterprise backend engineer with many years of experience maintaining production systems" can improve framing, but must not replace concrete requirements.
- Capability priming: describe the target agent as advanced, rigorous, production-minded, and experienced only when that profile affects judgment, implementation quality, or review depth.
- Step decomposition: split complex work into review and analysis, reasoning, implementation, and review and verification phases when helpful.
- Few-shot examples: include one short example of desired structure, naming, output, or behavior when the task has a pattern to preserve.
- Constraints-first prompting: put hard constraints, non-goals, and project conventions near the start of the task.
- Acceptance criteria: define observable success conditions instead of vague quality language.
- Negative examples: mention common wrong approaches only when they are likely and costly.
- Self-check: ask the agent to review its own result against the task constraints before handoff.
- Evidence requirement: require command output, test results, screenshots, or file references for claims that work is complete.

## Avoid

- Do not add generic motivational language.
- Do not ask for hidden chain-of-thought; request concise rationale, tradeoffs, decisions, and evidence instead.
- Do not overload simple leaf tasks with heavy prompting structure.
- Do not encode rules that belong in `rules/local-rules.md` as casual prose in `brief.md` or `execute.md`.
