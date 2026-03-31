# Research Memo

Date: 2026-03-31

This memo records the current Copilot customization surface that informed `ClaudeCodePilot`, the patterns adopted from that surface, and the Claude Code patterns that were intentionally not copied.

## Sources consulted

### Official VS Code documentation

- [Customization overview](https://code.visualstudio.com/docs/copilot/concepts/customization)
  - Used to decide where to place agents, prompts, instructions, and skills.
- [Custom agents in VS Code](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
  - Confirmed `.github/agents` support, frontmatter fields, and handoff behavior.
- [Subagents in VS Code](https://code.visualstudio.com/docs/copilot/agents/subagents)
  - Confirmed `user-invocable`, `disable-model-invocation`, `agents` allow-lists, and the guidance to define subagent usage in agent instructions.
- [Prompt files in VS Code](https://code.visualstudio.com/docs/copilot/customization/prompt-files)
  - Confirmed `.prompt.md` format, prompt-to-agent wiring, input variables, tool priority, and the recommendation to link instructions rather than duplicate them.
- [Custom instructions in VS Code](https://code.visualstudio.com/docs/copilot/customization/custom-instructions)
  - Confirmed `.github/copilot-instructions.md`, `.instructions.md`, linkable instruction files, and compatibility with Claude-style rules.
- [Agent skills in VS Code](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
  - Confirmed `SKILL.md` structure, naming, and the role of skills as portable multi-file capabilities.
- [VS Code Copilot settings reference](https://code.visualstudio.com/docs/copilot/reference/copilot-settings)
  - Confirmed the real settings names used by this repo:
    - `chat.agentFilesLocations`
    - `chat.instructionsFilesLocations`
    - `chat.promptFilesLocations`
    - `chat.agentSkillsLocations`
    - `chat.customAgentInSubagent.enabled`
    - `chat.useAgentSkills`
    - `chat.includeReferencedInstructions`

### Official GitHub documentation

- [Custom agents configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
  - Confirmed shared frontmatter behavior across Copilot surfaces, tool aliases, and the fact that unrecognized tools are ignored.
- [Invoking custom agents in Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli-agents/invoke-custom-agents)
  - Useful for portability decisions and for understanding the built-in CLI agent lineup.

### Community examples

- [awesome-copilot](https://github.com/github/awesome-copilot)
  - Reviewed the repository-level `agentic-workflows.agent.md`
  - Reviewed the general agent authoring guidance in `instructions/agents.instructions.md`
  - Reviewed several plan, review, and test-focused examples to understand current community patterns
  - Reviewed the `context-engineering` skills examples to confirm that reusable workflows fit better as skills than as giant agent prompts

## Patterns adopted

### 1. Use `.github/agents` as the canonical home

Reason:

- VS Code documents `.github/agents` as the workspace-level location.
- GitHub docs use the same repo-level location.
- This gives one canonical structure that works for VS Code first and still ports reasonably to other Copilot surfaces.

### 2. Keep user-facing agents separate from hidden subagents

Reason:

- VS Code now supports `user-invocable: false` and `disable-model-invocation`.
- Hidden agents make the system more predictable than a free-for-all pool of similarly named helpers.
- Subagent allow-lists reduce accidental selection of the wrong helper.

Implementation:

- `cc-lead`, `cc-plan`, `cc-build`, and `cc-review` are visible in the picker and protected from accidental subagent use.
- `cc-research` and `cc-test` are hidden helpers used through explicit allow-lists.

### 3. Use explicit subagent allow-lists

Reason:

- The subagents docs explicitly warn that unrestricted subagent pools can lead the model to choose unintended helpers.
- Claude Code's strongest orchestration lesson is not “spawn many agents,” but “spawn the right narrow worker with a clear job.”

Implementation:

- Main agents use `agents: [...]` instead of `agents: "*"`.
- No nested subagent chains are required in v1.

### 4. Give workers enough tools to be useful

Reason:

- GitHub's agent config docs confirm that tool lists are filters, and over-constraining them often makes workers ineffective.
- Community examples increasingly use role-based tool breadth rather than ultra-minimal lists.
- The user explicitly requested that subagents have enough tools.

Implementation:

- `cc-research` and `cc-test` are read-only in intent, not starved of capability.
- Read-heavy agents can search, read, inspect command output, and use web tools when available.
- Editing authority remains concentrated in `cc-build` and `cc-lead`.

### 5. Keep prompts lean and move reusable behavior into instructions and skills

Reason:

- VS Code prompt-file guidance explicitly recommends linking instruction files rather than duplicating guidance.
- Skills are designed for portable, multi-file workflows, which is a better fit for structured verify/debug flows than bloated agent prompts.

Implementation:

- Reusable orchestration, planning, edit, and review rules live in `.github/instructions`.
- Repeatable workflows live in `.github/skills/cc-verify` and `.github/skills/cc-debug`.
- Prompt files stay short and act as entry points into the agent pack.

### 5a. Do not override custom-agent tool budgets from prompt files unless absolutely necessary

Reason:

- VS Code prompt files take tool priority over the referenced custom agent.
- If a prompt file re-declares a broad tool list, it can silently undo the tighter tool surface chosen for performance and focus.

Implementation:

- Prompt files in this repo no longer declare `tools` when they reference a custom agent.
- The validator warns on future regressions in this area.

### 6. Use handoffs as the Copilot-native replacement for parts of Claude Code's workflow progression

Reason:

- VS Code handoffs provide a native way to move through planning, implementation, and review without inventing a custom protocol.
- This is a better fit for Copilot than trying to fake a durable worker notification system.

Implementation:

- `cc-plan` hands off to `cc-build`
- `cc-build` hands off to `cc-review`
- `cc-review` hands back to `cc-build` or `cc-plan`

### 7. Treat main-thread context as lossy over time

Reason:

- VS Code documents automatic conversation summarization and manual `/compact`, which is a different operating model than Claude Code's worker transcript flow.
- Subagents in VS Code return only the final result, which is good for context cleanliness, but the main thread still needs explicit hygiene when tasks become long or multi-phase.

Implementation:

- Added a dedicated `context-hygiene` instruction file.
- Reduced tool surfaces on the main agents to lower decision noise.
- Added `/cc-brief` for generating a compact handoff summary into a fresh session.
- Documented phase splitting and fresh-session guidance in the README.

## Patterns rejected or intentionally diverged

### 1. No attempt to clone Claude Code's task runtime

Rejected:

- background worker lifecycle
- output files and task notifications
- transcript-based resume
- remote worker orchestration

Reason:

- Copilot customizations do not expose equivalent primitives.
- Faking them in prompt text would add ceremony without real capability.

### 2. No giant “do everything” agent

Rejected:

- one oversized agent with every tool and every workflow embedded in a single prompt

Reason:

- Community examples and the official docs both point toward role separation.
- Claude Code itself works best when planner, implementer, researcher, and reviewer responsibilities are split.

### 3. No MCP in v1

Rejected:

- adding GitHub or browser MCP servers to force parity with Claude Code features

Reason:

- The user explicitly asked for built-ins only.
- This pack is meant to improve a stock VS Code Copilot setup first.

### 4. No dependence on `.github/copilot-instructions.md` for the shared pack

Reason:

- That file is automatically discovered only from the active workspace, not from an arbitrary external repo path.
- A global pack loaded from settings needs `.instructions.md` files and explicit location settings.

Implementation:

- The central pack uses `chat.instructionsFilesLocations`.
- `templates/project-overlay/.github/copilot-instructions.md` is provided for repo-local overlays.

## Claude Code ideas that *did* transfer well

- “Explore before editing”
- “Never delegate final understanding”
- Findings-first review
- Specialized plan/build/review roles
- Narrow worker prompts with explicit scope and expected output
- Use delegation to reduce context clutter, not as a reflex
- Isolate exploratory work so the main thread only receives the useful summary

## Notes and corrections from the research pass

- The earlier draft plan used `chat.skillsLocations`. The current VS Code setting name is `chat.agentSkillsLocations`.
- VS Code allows `agents` allow-lists for custom subagents, but that capability is still experimental. This repo is therefore “preview-friendly,” not “stable-only.”
- Tool aliases are intentionally broad and tolerant. GitHub docs state that unrecognized tool names are ignored, which lets this pack stay VS Code-first without breaking other Copilot surfaces outright.
- Prompt-file tool priority matters. In this repo, prompt files intentionally avoid redeclaring tools for custom agents so the agent remains the source of truth for its tool budget.
