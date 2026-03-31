---
name: orchestration-discipline
description: Use when coordinating multi-step work with agents, subagents, prompt files, or skills.
---

# Orchestration Discipline

- Explore current state before proposing edits or delegation.
- Use subagents when isolated context clearly helps: read-heavy discovery, independent second opinions, parallel analysis, or targeted verification.
- Keep subagent briefs self-contained: goal, scope, out-of-scope, expected output, and success signal.
- Never delegate final understanding. The parent agent must merge findings, choose tradeoffs, and communicate the final recommendation.
- Prefer narrow delegation over generic prompts like "figure this out."
- If a worker returns ambiguous findings, tighten the scope and rerun instead of guessing.
- Prefer the sequence `plan -> build -> review` unless the user explicitly wants to skip a phase.
- Keep main-thread summaries decision-oriented and explicit about what is verified versus inferred.
