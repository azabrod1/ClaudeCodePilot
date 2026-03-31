---
name: cc-brief
description: Create a compact handoff summary for a fresh Copilot session.
agent: cc-lead
argument-hint: "[current task or session]"
---

Create a compact new-session brief for `${input:scope,current task}`.

Output only these sections:

1. Goal
2. Fixed constraints
3. Current approach
4. Changed files or likely files
5. Verified facts
6. Open questions
7. Next best action

Keep the brief short enough to paste into a fresh session after `/compact` or when starting a new chat.
