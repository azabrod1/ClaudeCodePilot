---
name: cc-review
description: Review work with findings-first output and command-backed evidence.
agent: cc-review
argument-hint: "[what to review] [risk focus] [changed files]"
---

Review `${input:scope,implementation or change to review}`.

Requirements:

- lead with concrete findings, not summary
- validate behavior with real commands or explain the environment limitation precisely
- call out regressions, missing tests, risky assumptions, and verification gaps
- keep the closing summary short
