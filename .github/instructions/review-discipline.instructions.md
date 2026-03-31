---
name: review-discipline
description: Use when reviewing, auditing, or verifying code changes.
---

# Review Discipline

- Put findings first, ordered by severity.
- Back claims with evidence from real checks, repro steps, browser actions, or precise file references.
- Reading code is useful, but it is not a substitute for a command or tool check when one is available.
- Call out residual risks and missing coverage even when no bug is confirmed.
- Prefer targeted checks over noisy full-suite runs when a narrower command answers the question faster.
- Include at least one edge or adversarial check when it materially improves confidence.
- Distinguish confirmed issue, likely issue, and unverified suspicion.
- Do not fix code during review unless the task explicitly changes from review to implementation.
