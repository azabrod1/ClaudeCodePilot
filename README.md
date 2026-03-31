# ClaudeCodePilot

`ClaudeCodePilot` is a researched, Copilot-native customization pack for GitHub Copilot in VS Code that aims to make Copilot behave more like Claude Code where that actually helps. It uses the current native customization surface only: custom agents, experimental subagents, prompt files, instructions, handoffs, and a small skills layer.

The goal is not to copy Claude Code literally. The goal is to bring over the parts that improve real coding workflows inside Copilot:

- specialized planner, builder, researcher, tester, and reviewer roles
- explicit delegation rules for when isolated context helps
- findings-first review and verification discipline
- prompt and instruction hygiene so one file does not try to do everything

It intentionally does **not** try to recreate Claude Code's background workers, task mailboxes, transcript resume, or remote orchestration runtime. Copilot does not expose those same primitives today, so this pack stays inside what Copilot can actually do well.

One important implementation choice: `cc-lead` and `cc-build` intentionally leave their `tools` frontmatter unset. In Copilot, that means they can use the currently available tool surface instead of a pinned list, so they track new built-in, extension, and MCP tools more naturally over time.

## What's inside

- `.github/agents`: four user-facing agents and two hidden subagents
- `.github/instructions`: reusable orchestration, planning, edit, and review rules
- `.github/prompts`: slash-command entry points for plan, build, review, and audit flows
- `.github/skills`: lightweight reusable verify and debug workflows
- `docs/research-memo.md`: the implementation research basis and design decisions
- `docs/session-workflow.md`: the recommended day-to-day operating loop for this pack
- `docs/agent-lineage.md`: how each agent maps back to Claude Code ideas and where it intentionally diverges
- `templates/project-overlay`: optional repo-local overlays for `CLAUDE.md`, `AGENTS.md`, `.github/copilot-instructions.md`, and path-specific instructions
- `scripts/install.py`: prints a ready-to-paste VS Code settings block for this repo path
- `scripts/validate_customizations.py`: no-dependency validator for agent, prompt, skill, and handoff wiring
- `scripts/audit_tool_coverage.py`: fetches the latest official docs and checks whether new built-in tool sets need a deliberate decision

## Quick start

1. Load this repo into VS Code using the settings block from `python scripts/install.py`.
2. Start with `/cc-plan` for larger or unclear tasks.
3. Hand off to `cc-build` for implementation.
4. Run `cc-review` before you trust the result.
5. Use `/cc-brief` or `/compact` when the thread gets bloated.

If you want one main entry point, use `cc-lead`. It is the closest thing in this pack to a Claude Code-style top-level coordinator.

## Recommended workflow

1. Use `cc-lead` when you want a single orchestrating agent that can route work and keep the overall thread aligned.
2. Use `/cc-plan` or the `cc-plan` agent when the task is ambiguous, risky, or likely to touch multiple files.
3. Hand off to `cc-build` to implement with targeted research and validation helpers.
4. Hand off to `cc-review` before declaring work complete.
5. Use `/cc-audit`, `cc-research`, `cc-test`, `cc-verify`, and `cc-debug` when you want a structured audit, a focused research pass, or a debugging loop.
6. Use `/cc-brief` when a task has grown large and you want a compact handoff summary for a fresh session.

The practical operating guide is in [docs/session-workflow.md](docs/session-workflow.md).

## What "Claude Code-like" means here

This repo tries to reproduce the useful workflow shape of Claude Code inside Copilot:

- a coordinator that explores before editing
- role-specialized helpers instead of one overloaded assistant
- explicit plan, build, and review phases
- delegation only when it reduces context clutter
- strong verification and findings-first review

It does **not** try to mimic runtime features Copilot does not really have, such as durable background task workers, transcript-native resume semantics, or a full remote subagent execution model.

There is also no supported custom-agent frontmatter for "inherit the built-in Plan agent's exact tool config." When you specifically want the native Plan agent's evolving behavior, the best approach is to use the built-in Plan agent directly or ask `cc-lead` to use Plan as a subagent.

## Context and performance

Copilot handles context differently from Claude Code, so this pack now leans into Copilot-native context hygiene instead of assuming a long-lived rich worker transcript.

The main rules:

- use subagents for discovery and targeted validation so intermediate tool output stays out of the main thread
- keep prompt files thin and let the agent own its tool budget
- leave `cc-lead` and `cc-build` unpinned so they can see the live Copilot tool surface
- split large work across plan, build, and review phases instead of forcing one giant session
- use `/compact` when a thread gets noisy
- use `/cc-brief` when you want a paste-ready handoff into a fresh session

Good times to start a fresh session:

- after broad exploration, before implementation starts
- after implementation, before a high-stakes review
- when the current thread has drifted across multiple unrelated ideas or dead ends

## Install in VS Code

This repo is designed to stay in its own folder and be loaded into Copilot from settings.

1. Clone or keep this repo somewhere stable on disk.
2. Run:

```bash
python scripts/install.py
```

3. Copy the emitted JSONC block into your VS Code settings.
4. Reload VS Code.

The generated settings turn on the important pieces for this pack:

- `chat.agentFilesLocations`
- `chat.instructionsFilesLocations`
- `chat.promptFilesLocations`
- `chat.agentSkillsLocations`
- `chat.customAgentInSubagent.enabled`
- `chat.useAgentSkills`
- `github.copilot.chat.tools.memory.enabled`
- `chat.includeReferencedInstructions`
- `github.copilot.chat.summarizeAgentConversationHistory.enabled`

`browser` tools are included in several agents because they help with web verification, but they are optional. If the browser tool is unavailable, VS Code ignores it. If you want that capability, also enable `workbench.browser.enableChatTools`.

After reloading VS Code, check that you can see:

- agents: `cc-lead`, `cc-plan`, `cc-build`, `cc-review`
- prompts: `/cc-plan`, `/cc-build`, `/cc-review`, `/cc-audit`, `/cc-brief`
- skills available to agents: `cc-verify`, `cc-debug`

## Why the files are split this way

The repo follows the current Copilot guidance:

- agents are for persistent personas and handoffs
- prompt files are for lightweight entry points
- skills are for portable, multi-file workflows
- instructions hold reusable rules instead of duplicating them across every prompt

That split keeps the agent files focused while still giving the system enough structure to feel more like a disciplined agent workflow and less like one giant prompt.

## Validate the pack

Run the validator locally:

```bash
python scripts/validate_customizations.py
```

It checks:

- frontmatter presence and basic structure
- agent names and duplicate definitions
- handoff targets
- prompt-to-agent references
- hidden-agent visibility
- explicit subagent allow-lists
- prompt files that accidentally override a custom agent's tool budget
- skill folder and `SKILL.md` naming consistency

## Tool maintenance

Two things make the tool story safer over time.

First, the agents mostly use broad top-level tool names such as `search`, `read`, `edit`, `execute`, `agent`, and `web`. That means if VS Code adds new subtools under an existing top-level tool set, the pack generally benefits automatically without any file changes here.

Second, `cc-lead` and `cc-build` intentionally leave `tools` unset, so they can use whatever tools are currently available in Copilot rather than a frozen list.

Third, this repo includes a tool-audit script:

```bash
python scripts/audit_tool_coverage.py
```

It fetches the latest official VS Code and GitHub docs, then checks:

- the current VS Code top-level built-in tools
- the current GitHub custom-agent aliases
- the tools used by this pack
- whether any newly documented top-level tool set is not yet accounted for in [config/tool-policy.json](config/tool-policy.json)

That means if Copilot adds a **new top-level tool set**, we do not silently miss it. The audit fails until we explicitly decide whether to use it or intentionally omit it.

There is also a scheduled GitHub Action at [.github/workflows/tool-audit.yml](.github/workflows/tool-audit.yml) so the repo can catch tool-surface drift weekly once it is pushed to GitHub.

To verify the real tool surface in your own VS Code session:

- type `#` in the chat input to see the currently available tools and tool sets
- use the Agent Debug Log and Chat Debug views to inspect the exact tools and context that were sent to the model

## Research basis

The implementation is grounded in current official documentation plus live community examples. The detailed memo is in [docs/research-memo.md](docs/research-memo.md).

If you want the direct Claude Code mapping, see [docs/agent-lineage.md](docs/agent-lineage.md).

Key sources:

- [VS Code customization overview](https://code.visualstudio.com/docs/copilot/concepts/customization)
- [Custom agents in VS Code](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
- [Subagents in VS Code](https://code.visualstudio.com/docs/copilot/agents/subagents)
- [Prompt files in VS Code](https://code.visualstudio.com/docs/copilot/customization/prompt-files)
- [Custom instructions in VS Code](https://code.visualstudio.com/docs/copilot/customization/custom-instructions)
- [Agent skills in VS Code](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [GitHub custom agents configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
- [awesome-copilot](https://github.com/github/awesome-copilot)
