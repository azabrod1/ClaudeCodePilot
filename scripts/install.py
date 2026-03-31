#!/usr/bin/env python3
"""Emit a ready-to-paste VS Code settings block for this customization pack."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def build_settings(repo_root: Path) -> dict:
    github_root = repo_root / ".github"
    return {
        "chat.customAgentInSubagent.enabled": True,
        "chat.useAgentSkills": True,
        "github.copilot.chat.summarizeAgentConversationHistory.enabled": True,
        "chat.includeReferencedInstructions": True,
        "github.copilot.chat.codeGeneration.useInstructionFiles": True,
        "chat.useClaudeMdFile": True,
        "chat.agentFilesLocations": {
            str((github_root / "agents").resolve()): True,
        },
        "chat.instructionsFilesLocations": {
            str((github_root / "instructions").resolve()): True,
        },
        "chat.promptFilesLocations": {
            str((github_root / "prompts").resolve()): True,
        },
        "chat.agentSkillsLocations": {
            str((github_root / "skills").resolve()): True,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print the VS Code settings block for this repo."
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Write the generated JSONC to a file instead of stdout.",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    payload = build_settings(repo_root)
    rendered = json.dumps(payload, indent=2)

    header = (
        "// Paste these settings into your VS Code settings.json (JSONC is fine).\n"
        "// Optional: also enable \"workbench.browser.enableChatTools\" if you want browser-backed verification.\n"
    )
    output = header + rendered + "\n"

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
