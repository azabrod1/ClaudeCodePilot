---
name: context-hygiene
description: Use when trying to keep Copilot sessions fast, focused, and resilient to history compaction.
---

# Context Hygiene

- Prefer focused prompts over broad narrative prompts.
- Assume older history may be compacted into a lossy summary. Before a phase change, restate the current goal, constraints, changed files, and next step in a short recap.
- Use subagents for exploration, comparison, and targeted validation so intermediate tool output does not crowd the main thread.
- Prefer search before large file reads, and read only the files or ranges that materially affect the decision.
- Avoid attaching many files manually unless the automatic workspace context misses something important.
- Use `/compact` when the session becomes noisy. Good prompts for compaction include:
  - `/compact keep only the current goal, chosen approach, changed files, and remaining blockers`
  - `/compact focus on the implementation plan and unresolved verification gaps`
- Start a fresh session when switching from broad research to implementation, or from implementation to a high-stakes review, if the prior history is no longer helping.
- Put stable repo knowledge in repo-local instructions, overlays, or memory rather than repeating it in every chat.
