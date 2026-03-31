#!/usr/bin/env python3
"""Audit this pack's tool usage against the latest official VS Code and GitHub docs."""

from __future__ import annotations

import ast
import json
import re
import sys
import time
from pathlib import Path
from typing import Any
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "config" / "tool-policy.json"
VSCODE_TOOLS_URL = "https://code.visualstudio.com/docs/copilot/reference/copilot-vscode-features"
GITHUB_AGENT_CONFIG_URL = "https://docs.github.com/en/copilot/reference/custom-agents-configuration"


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def fetch(url: str, retries: int = 3, delay_s: float = 1.0) -> str:
    last_exc: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            with urlopen(url, timeout=20) as response:
                return response.read().decode("utf-8", "ignore")
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            if attempt < retries:
                time.sleep(delay_s * attempt)
    raise RuntimeError(f"Failed to fetch {url}: {last_exc}")


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
        return {}
    _, fm, _ = text.split("---\n", 2)
    data: dict[str, Any] = {}
    for line in fm.splitlines():
        if not line.strip():
            continue
        if line.startswith("  "):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key in data:
            fail(f"{path} has duplicate frontmatter key {key!r}")
        if value:
            data[key] = parse_scalar(value)
    return data


def extract_vs_code_top_level_tools(html: str) -> list[str]:
    marker = "The following table lists the VS Code built-in tools:"
    start = html.find(marker)
    if start == -1:
        fail("Could not locate the VS Code built-in tools table in the fetched docs.")
    end = html.find("## Slash commands", start)
    if end == -1:
        # HTML source has raw <h2> tags rather than markdown headers.
        end = html.find("<h2", start + len(marker))
    snippet = html[start:end]
    raw_tools = re.findall(r"<code>#([^<]+)</code>", snippet)
    top_level = sorted({tool.split("/")[0] for tool in raw_tools})
    return top_level


def extract_github_aliases(html: str) -> list[str]:
    marker = 'id="tool-aliases"'
    start = html.find(marker)
    if start == -1:
        fail("Could not locate the GitHub tool aliases table in the fetched docs.")
    end = html.find('id="tool-names-for-out-of-the-box-mcp-servers"', start)
    snippet = html[start:end]
    aliases = re.findall(r"<td><code>([A-Za-z][A-Za-z0-9-]*)</code></td>", snippet)
    # The table repeats several code cells; keep the well-known primary alias order.
    primary = []
    for alias in aliases:
        if alias not in primary:
            primary.append(alias)
    return primary


def collect_used_tools() -> tuple[list[str], list[str]]:
    used: set[str] = set()
    implicit_all: list[str] = []
    for path in sorted((ROOT / ".github").rglob("*.md")):
        meta = parse_frontmatter(path)
        if path.name.endswith(".agent.md") and "tools" not in meta:
            implicit_all.append(path.relative_to(ROOT).as_posix())
            continue
        value = meta.get("tools")
        if not value:
            continue
        if isinstance(value, str):
            used.add(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str):
                    used.add(item)
    return sorted(used), implicit_all


def main() -> int:
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    accounted = policy["accountedVsCodeTopLevelTools"]

    vs_code_html = fetch(VSCODE_TOOLS_URL)
    github_html = fetch(GITHUB_AGENT_CONFIG_URL)

    current_vs_code = extract_vs_code_top_level_tools(vs_code_html)
    current_aliases = extract_github_aliases(github_html)
    used_tools, implicit_all = collect_used_tools()

    unaccounted_top_level = [tool for tool in current_vs_code if tool not in accounted]
    if unaccounted_top_level:
        fail(
            "New VS Code top-level tools are not yet accounted for in config/tool-policy.json: "
            + ", ".join(unaccounted_top_level)
        )

    invalid_used_tools = []
    for tool in used_tools:
        if tool == "*":
            continue
        if "/" in tool:
            head = tool.split("/", 1)[0]
            if head in current_vs_code or head in current_aliases:
                continue
            invalid_used_tools.append(tool)
            continue
        if tool in current_vs_code or tool in current_aliases:
            continue
        invalid_used_tools.append(tool)

    if invalid_used_tools:
        fail(
            "This repo uses tools that are not in the current VS Code top-level list or GitHub alias list: "
            + ", ".join(invalid_used_tools)
        )

    used_top_level = sorted({tool.split("/", 1)[0] for tool in used_tools if tool != "*"})
    omitted = sorted(tool for tool in current_vs_code if tool not in used_top_level)

    print("Current VS Code top-level tools:")
    print(", ".join(current_vs_code))
    print()
    print("Current GitHub custom-agent aliases:")
    print(", ".join(current_aliases))
    print()
    print("Tools used by this pack:")
    print(", ".join(used_tools))
    print()
    if implicit_all:
        print("Files with implicit all-tools access:")
        for item in implicit_all:
            print(f"- {item}")
        print()
    print("Top-level tools currently pinned explicitly by this pack:")
    print(", ".join(used_top_level))
    print()
    if implicit_all:
        print("Top-level tools reachable through implicit-all agents:")
        print(", ".join(current_vs_code))
        print()
    print("Accounted but currently omitted top-level tools:")
    for tool in omitted:
        print(f"- {tool}: {accounted[tool]}")
    print()
    print("Tool coverage audit passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
