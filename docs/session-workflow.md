# Session Workflow

This is the default way to use `ClaudeCodePilot` day to day in VS Code.

## Default loop

1. Start with `/cc-plan` when the task is ambiguous, risky, cross-cutting, or likely to touch multiple files.
2. Switch to `cc-build` when the plan is good enough to execute.
3. Switch to `cc-review` before you trust a non-trivial change.
4. Use `/cc-brief` when the session has become noisy and you want a clean restart with only the important facts.

If the task is small and obvious, skip straight to `cc-build`.

## Which agent to start with

### Start with `cc-plan`

Use this when:

- you do not yet know the right implementation shape
- the task spans several files or systems
- you need a clear validation plan before changing code
- you want to compare approaches before committing

Good prompt:

```text
/cc-plan Add audit logging to user-role changes. Reuse existing logging patterns, avoid schema churn if possible, and include the test/verification plan.
```

### Start with `cc-build`

Use this when:

- the task is already well-scoped
- you know roughly where the change belongs
- the repo pattern is clear enough to implement directly

Good prompt:

```text
/cc-build Fix the retry backoff bug in the API client. Keep the public interface unchanged and run the narrowest meaningful validation afterward.
```

### Start with `cc-review`

Use this when:

- code already exists and you want confidence
- you want a second opinion before shipping
- you suspect missing tests, risky assumptions, or regressions

Good prompt:

```text
/cc-review Review the recent auth refresh changes with a focus on race conditions, stale token handling, and missing verification.
```

## When to use subagents

Let the main agent use `cc-research` and `cc-test` for:

- broad code discovery
- framework or tooling lookup
- targeted repro work
- narrow command-based validation
- independent second-opinion checks

Do **not** ask the main agent to delegate everything. The main thread should still own:

- the chosen approach
- the final synthesis
- the final user-facing explanation

## Context hygiene rules

Copilot handles long sessions differently than Claude Code. Treat the main thread as something that can get compacted and partially summarized.

### Use `/compact` when

- the chat has accumulated dead ends or exploratory noise
- the implementation direction is already decided
- you are about to move from research to implementation
- you are about to move from implementation to review

Useful examples:

```text
/compact keep only the chosen approach, changed files, verified facts, and remaining blockers
```

```text
/compact focus on the implementation state and unresolved verification gaps
```

### Start a fresh session when

- the thread has crossed several phases and no longer feels crisp
- you want a high-signal review without implementation noise
- the task changed materially from the original goal
- the current session includes too much unrelated context

### Use `/cc-brief` before a fresh session

This is the cleanest handoff path for longer work.

Recommended pattern:

1. Run `/cc-brief`
2. Copy the brief into a new chat
3. Start the next phase with the right agent

Example:

```text
/cc-brief Summarize the current state of the feature flag rollout work for a fresh review session.
```

Then in the new session:

```text
/cc-review [paste brief here]
```

## Best phase boundaries

### Research -> Build

Good boundary when:

- you know the approach
- you know the likely files
- open questions are down to implementation details

### Build -> Review

Good boundary when:

- code changes are in place
- at least narrow validation has run
- you want findings that are not anchored to the build thread's reasoning

### Review -> Build

Good boundary when:

- the review found concrete issues
- the next step is implementation, not more speculation

## Anti-patterns

- Doing research, implementation, and review in one giant session if the task is medium or large
- Repeating stable repo conventions in every prompt instead of storing them in instructions or overlays
- Letting prompt files override the custom agent's tool budget unless there is a very specific reason
- Delegating “figure this out” instead of giving subagents a narrow, explicit task
- Using `cc-review` as a disguised implementation agent

## Simple default for most coding work

If you want one reliable workflow, use this:

1. `/cc-plan` for 5-10 minutes
2. `cc-build` for the implementation
3. `/compact` or `/cc-brief`
4. `cc-review` in a cleaner session

That pattern fits Copilot's context model better than trying to keep one huge conversation alive indefinitely.
