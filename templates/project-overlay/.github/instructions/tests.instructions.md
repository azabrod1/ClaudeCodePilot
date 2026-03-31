---
name: project-test-conventions
description: Apply to this repository's test files and test-related edits.
applyTo: "**/tests/**"
---

# Project Test Conventions

- Place new tests next to the existing test structure used by this repo.
- Match the current naming, fixtures, and helper patterns before introducing new ones.
- Prefer deterministic tests with clear failure messages.
- Cover the main path first, then the highest-value edge cases.
