---
name: cc-verify
description: Structured verification workflow for targeted commands, edge checks, and evidence-backed PASS/PARTIAL/FAIL summaries. Use after implementation, before review, or whenever you need to prove what was actually verified.
argument-hint: "[what changed] [commands or entrypoints] [risk focus]"
---

# cc-verify

Use this skill when the main agent needs a repeatable, evidence-based verification pass without bloating the base prompt.

## Workflow

1. Restate the scope and the success signal.
2. Discover existing build, test, lint, or repro commands before inventing new ones.
3. Run the narrowest meaningful checks first.
4. Add at least one edge, boundary, or adversarial check when it materially improves confidence.
5. Summarize the results using [the evidence template](./evidence-template.md) and [the verification checklist](./verification-checklist.md).

## Guardrails

- Prefer real command output over code-reading claims.
- If the environment blocks execution, record the exact blocker and the resulting confidence gap.
- Treat passing tests as evidence, not the whole argument.
- Keep the final summary concise and explicit about verified versus unverified behavior.
