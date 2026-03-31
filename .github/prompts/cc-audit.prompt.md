---
name: cc-audit
description: Run a Claude-like audit for readiness, risks, and missing verification.
agent: cc-lead
argument-hint: "[goal or branch context] [ship criteria] [risk focus]"
---

Audit `${input:scope,current branch, feature, or codebase area}` for:

- missing validation
- risky assumptions
- obvious regressions
- incomplete implementation
- docs or configuration drift
- best next action

Use focused subagents where isolated research or verification helps. Return:

1. blockers
2. watch items
3. verified strengths
4. recommended next step
