# Question Template

Use this template when the repo, docs, and current task tree cannot answer a decision that materially changes implementation, validation, scope, or closure.

## Rules

- Use the task or subtask name as the section title.
- Number the questions.
- Each question must have 3 to 5 options.
- Options must be mutually exclusive.
- Mark exactly one option as `(Recommended)`.
- Ask only what the repo cannot answer.
- Keep wording concrete enough that the answer changes a real implementation decision.

## Compact template

```md
## <Task name>

1. <Concrete question>
a. <Option 1>
b. <Option 2> `(Recommended)`
c. <Option 3>
d. <Option 4>
e. <Option 5>

2. <Concrete question>
a. <Option 1> `(Recommended)`
b. <Option 2>
c. <Option 3>
```

## Extended template

```md
## <Task name>

1. <Concrete question that changes implementation, validation, scope, or closure>
a. <Option 1>
b. <Option 2> `(Recommended)`
c. <Option 3>
d. <Option 4>

Impact:
- <Why this question matters and what the answer changes>

2. <Concrete question>
a. <Option 1>
b. <Option 2>
c. <Option 3> `(Recommended)`

Impact:
- <What changes if another option is selected>
```

## Example

```md
## Drawing prompt refinement

1. What should the prompt prioritize if visual style conflicts with technical fidelity?
a. Improve visual style
b. Preserve geometry and technical content `(Recommended)`
c. Reduce inference cost
d. Simplify the prompt

Impact:
- This decision changes the acceptance criteria for refinement and the expected fallback.
```
