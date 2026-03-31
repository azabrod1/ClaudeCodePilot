#!/usr/bin/env python3
"""Validate the customizations shipped by this repository without external dependencies."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

ALLOWED_TOOL_ALIASES = {
    "*",
    "agent",
    "browser",
    "edit",
    "execute",
    "read",
    "search",
    "todo",
    "web",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def warn(message: str) -> None:
    print(f"WARNING: {message}")


def parse_scalar(raw: str) -> Any:
    raw = raw.strip()
    if raw in {"true", "false"}:
        return raw == "true"
    if raw.startswith("[") and raw.endswith("]"):
        return ast.literal_eval(raw)
    if (raw.startswith('"') and raw.endswith('"')) or (
        raw.startswith("'") and raw.endswith("'")
    ):
        return ast.literal_eval(raw)
    return raw


def parse_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(f"{path} is missing YAML frontmatter")
    try:
        _, fm, _ = text.split("---\n", 2)
    except ValueError as exc:
        fail(f"{path} has malformed frontmatter separators: {exc}")

    data: dict[str, Any] = {}
    lines = fm.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("  "):
            fail(f"{path} has unexpected indentation at top level: {line!r}")
        if ":" not in line:
            fail(f"{path} has malformed frontmatter line: {line!r}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key in data:
            fail(f"{path} has duplicate frontmatter key {key!r}")
        if value:
            data[key] = parse_scalar(value)
            i += 1
            continue

        i += 1
        items: list[Any] = []
        current_obj: dict[str, Any] | None = None
        while i < len(lines):
            nested = lines[i]
            if not nested.strip():
                i += 1
                continue
            if not nested.startswith("  "):
                break
            stripped = nested.strip()
            if stripped.startswith("- "):
                payload = stripped[2:]
                if payload and ":" in payload:
                    current_obj = {}
                    sub_key, sub_value = payload.split(":", 1)
                    current_obj[sub_key.strip()] = parse_scalar(sub_value.strip())
                    items.append(current_obj)
                elif payload:
                    items.append(parse_scalar(payload))
                    current_obj = None
                else:
                    current_obj = {}
                    items.append(current_obj)
            else:
                if current_obj is None:
                    fail(f"{path} has malformed nested block near: {nested!r}")
                if ":" not in stripped:
                    fail(f"{path} has malformed nested property near: {nested!r}")
                sub_key, sub_value = stripped.split(":", 1)
                current_obj[sub_key.strip()] = parse_scalar(sub_value.strip())
            i += 1
        data[key] = items
    return data


def collect_files(base: Path, pattern: str) -> list[Path]:
    if not base.exists():
        return []
    return sorted(base.rglob(pattern))


def validate_tools(path: Path, value: Any) -> None:
    if value in (None, "*"):
        return
    if isinstance(value, str):
        tool_values = [value]
    elif isinstance(value, list):
        tool_values = value
    else:
        fail(f"{path} has a non-list tools value")

    for tool in tool_values:
        if not isinstance(tool, str):
            fail(f"{path} has a non-string tool entry: {tool!r}")
        if tool in ALLOWED_TOOL_ALIASES:
            continue
        if "/" in tool:
            continue
        warn(f"{path} uses a non-standard tool name that will be trusted as product-specific: {tool}")


def validate_agent_files(agent_files: list[Path]) -> dict[str, dict[str, Any]]:
    agents: dict[str, dict[str, Any]] = {}
    for path in agent_files:
        meta = parse_frontmatter(path)
        name = meta.get("name") or path.stem.replace(".agent", "")
        if not meta.get("description"):
            fail(f"{path} is missing description")
        if name in agents:
            fail(f"Duplicate agent name: {name}")
        validate_tools(path, meta.get("tools"))
        if "agents" in meta and not isinstance(meta["agents"], list):
            fail(f"{path} must use a list for agents")
        handoffs = meta.get("handoffs", [])
        if handoffs and not isinstance(handoffs, list):
            fail(f"{path} handoffs must be a list")
        agents[name] = {
            "path": path,
            "meta": meta,
        }
    return agents


def validate_agent_relationships(agents: dict[str, dict[str, Any]]) -> None:
    hidden = {"cc-research", "cc-test"}
    for name, payload in agents.items():
        meta = payload["meta"]
        path = payload["path"]

        if name in hidden and meta.get("user-invocable", True) is not False:
            fail(f"{path} should be hidden with user-invocable: false")
        if name not in hidden and meta.get("disable-model-invocation") is not True:
            fail(f"{path} should set disable-model-invocation: true")

        allowed_agents = meta.get("agents")
        if name in {"cc-lead", "cc-plan", "cc-build", "cc-review"}:
            if not isinstance(allowed_agents, list) or not allowed_agents:
                fail(f"{path} should define an explicit non-empty agents allow-list")
        if isinstance(allowed_agents, list):
            tools = meta.get("tools")
            if tools is not None:
                if tools == "*":
                    tool_values = ["*"]
                elif isinstance(tools, str):
                    tool_values = [tools]
                else:
                    tool_values = tools
                if "*" not in tool_values and "agent" not in tool_values:
                    fail(
                        f"{path} defines subagents but does not expose the agent tool. "
                        "Either include `agent` in tools or omit tools to allow all available tools."
                    )
        if isinstance(allowed_agents, list):
            for allowed in allowed_agents:
                if allowed not in agents:
                    fail(f"{path} references unknown subagent {allowed!r}")

        for handoff in meta.get("handoffs", []):
            if not isinstance(handoff, dict):
                fail(f"{path} has malformed handoff entry: {handoff!r}")
            target = handoff.get("agent")
            label = handoff.get("label")
            if not label or not target:
                fail(f"{path} has a handoff missing label or agent")
            if target not in agents:
                fail(f"{path} handoff points to unknown agent {target!r}")


def validate_prompt_files(prompt_files: list[Path], agents: dict[str, dict[str, Any]]) -> None:
    for path in prompt_files:
        meta = parse_frontmatter(path)
        if not meta.get("description"):
            fail(f"{path} is missing description")
        validate_tools(path, meta.get("tools"))
        agent = meta.get("agent")
        if agent and agent not in {"ask", "agent", "plan"} and agent not in agents:
            fail(f"{path} references unknown agent {agent!r}")
        if agent in agents and "tools" in meta:
            warn(
                f"{path} overrides the referenced custom agent tool budget; "
                "prefer leaving tools unset in prompt files unless this is intentional"
            )


def validate_instruction_files(instruction_files: list[Path]) -> None:
    for path in instruction_files:
        meta = parse_frontmatter(path)
        if not meta.get("description"):
            fail(f"{path} is missing description")


def validate_skill_dirs(skill_root: Path) -> None:
    if not skill_root.exists():
        return
    for skill_dir in sorted(p for p in skill_root.iterdir() if p.is_dir()):
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            fail(f"{skill_dir} is missing SKILL.md")
        meta = parse_frontmatter(skill_file)
        if meta.get("name") != skill_dir.name:
            fail(
                f"{skill_file} must set name to match the directory name ({skill_dir.name})"
            )
        if not meta.get("description"):
            fail(f"{skill_file} is missing description")


def main() -> int:
    roots = [
        ROOT / ".github",
        ROOT / "templates" / "project-overlay" / ".github",
    ]

    agent_files = []
    prompt_files = []
    instruction_files = []

    for base in roots:
        agent_files.extend(collect_files(base / "agents", "*.agent.md"))
        prompt_files.extend(collect_files(base / "prompts", "*.prompt.md"))
        instruction_files.extend(collect_files(base / "instructions", "*.instructions.md"))

    if not agent_files:
        fail("No agent files found")
    if not prompt_files:
        fail("No prompt files found")

    agents = validate_agent_files(agent_files)
    validate_agent_relationships(agents)
    validate_prompt_files(prompt_files, agents)
    validate_instruction_files(instruction_files)
    validate_skill_dirs(ROOT / ".github" / "skills")

    print(f"Validated {len(agent_files)} agent files")
    print(f"Validated {len(prompt_files)} prompt files")
    print(f"Validated {len(instruction_files)} instruction files")
    print("Validated skill directories")
    print("All customization checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
