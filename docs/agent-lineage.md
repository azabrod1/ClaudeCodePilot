# Agent Lineage

Short answer: yes, the `.agent.md` files are based on Claude Code equivalents in **concept and role design**, but they are **not** copied line-by-line from Claude Code prompts.

They are Claude-inspired, then adapted to Copilot's customization surface and context model.

## Mapping

### `cc-lead`

Closest Claude Code sources:

- coordinator mode prompt
- general-purpose agent prompt
- agent-tool guidance about when to delegate and when not to

What carried over:

- delegate for isolated research or validation
- never delegate final understanding
- keep worker prompts narrow and explicit
- treat orchestration as a disciplined workflow, not “spawn agents all the time”

What changed for Copilot:

- much smaller tool surface
- no durable task runtime, mailboxes, output files, or background notifications
- more emphasis on phase transitions, `/compact`, and fresh-session handoffs

### `cc-plan`

Closest Claude Code sources:

- built-in plan agent
- coordinator planning guidance

What carried over:

- read-only planning mode
- explore before deciding
- produce an actionable plan with validation and risks

What changed for Copilot:

- plan output is intentionally shorter and more compaction-friendly
- uses handoffs instead of Claude Code's richer orchestration/runtime model

### `cc-build`

Closest Claude Code sources:

- general-purpose agent
- coordinator implementation phase guidance

What carried over:

- implement directly once the shape is clear
- use helpers for narrow research or validation
- prefer minimal, coherent edits over sprawling changes

What changed for Copilot:

- subagents are used mainly for context isolation, not as durable workers
- the main agent is expected to survive a summarized history, so recaps matter more

### `cc-review`

Closest Claude Code sources:

- verification agent

What carried over:

- findings-first output
- skepticism toward “looks correct”
- command-backed evidence over pure code-reading claims

What changed for Copilot:

- tuned to work well as a cleaner second-phase review session
- avoids assuming Claude Code's specific task/task-notification workflow

### `cc-research`

Closest Claude Code sources:

- explore agent
- fork/subagent guidance

What carried over:

- read-heavy discovery
- keep output concise so the parent only gets the useful summary

What changed for Copilot:

- broader built-in read/search/web tool access because Copilot workers are otherwise too weak if overly constrained
- explicit emphasis on not narrating every search step

### `cc-test`

Closest Claude Code sources:

- verification agent
- task/test-running helper role

What carried over:

- gather evidence from real commands
- summarize only the useful result back to the parent

What changed for Copilot:

- positioned as a narrow validation worker rather than a durable task runner
- designed to help the main thread stay small instead of acting like a long-lived subprocess

## Why they are not literal Claude Code copies

Claude Code and Copilot differ in important ways:

- Claude Code has a richer subagent runtime and transcript model.
- Copilot uses prompt files, handoffs, skills, and conversation summarization differently.
- Prompt-file tool priority and session compaction matter much more in Copilot customization work.

So the right move was:

1. preserve the strong Claude Code ideas
2. drop the runtime-specific assumptions
3. rebuild the roles around Copilot-native mechanisms

That is why these agent files are best described as **Claude Code equivalents adapted for Copilot**, not as ports.
