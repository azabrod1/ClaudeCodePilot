---
name: project-audit
description: Run a repo-specific audit that assumes the shared ClaudeCodePilot pack is installed.
agent: cc-review
argument-hint: "[feature, branch, or risk focus]"
---

Use the repository's `.github/copilot-instructions.md` plus any matching instruction files.

Audit `${input:scope,current branch or feature}` for:

- correctness risks
- missing tests or missing verification
- config or docs drift
- likely regressions

Return findings first, then a short summary and the best next action.
