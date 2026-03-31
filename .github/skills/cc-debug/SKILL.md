---
name: cc-debug
description: Structured reproduce-isolate-fix-regression workflow for debugging tasks. Use when a failure is unclear, intermittent, environment-sensitive, or likely to need tighter triage before editing.
argument-hint: "[bug or failure] [how to reproduce] [suspected area]"
---

# cc-debug

Use this skill when the main agent needs a disciplined debugging loop instead of jumping straight to edits.

## Workflow

1. Clarify the symptom, environment, and success signal.
2. Reproduce the issue with the smallest reliable command or interaction you can find.
3. Isolate the likely scope using file search, code paths, logs, and targeted checks.
4. Form a short ranked hypothesis list.
5. After a fix, run a regression pass using [the debug loop template](./debug-loop.md).

## Guardrails

- Do not treat a guess as a root cause.
- Prefer narrowing the repro over broad speculative edits.
- Record commands, observed output, and confidence changes after each meaningful step.
- If the bug cannot be reproduced, say that explicitly and list the strongest remaining hypotheses.
