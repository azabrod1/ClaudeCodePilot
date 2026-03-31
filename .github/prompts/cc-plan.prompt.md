---
name: cc-plan
description: Turn a request into a decision-ready implementation plan with the cc-plan agent.
agent: cc-plan
argument-hint: "[goal] [constraints] [definition of done]"
---

Create a decision-complete implementation plan for `${input:task,feature or refactor to plan}`.

Requirements:

- stay read-only
- inspect the current implementation before deciding
- reuse existing patterns and commands when possible
- use a focused subagent only if a specific unknown remains after local inspection
- return sections for Summary, Current State, Proposed Changes, Validation, Risks, Critical Files, and Assumptions
