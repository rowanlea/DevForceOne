#!/usr/bin/env python3
"""
Claude Code PostToolUse hook: when a `.claude/commands/<name>.md` file is
written or edited, append an entry to the `## Commands Menu` section in
README.md.

Reads the Claude hook payload from stdin (tool_name, tool_input.file_path,
tool_input.content). The command name is derived from the filename; the
description is read from the markdown frontmatter.
"""
import json
import sys
import re
import os


def main():
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        sys.exit(0)

    tool_input = data.get("tool_input", {}) or {}

    # Resolve the edited file path from the Claude hook payload
    path = tool_input.get("file_path") or tool_input.get("path") or ""
    path_norm = path.replace("\\", "/")

    # Only react to command definitions under .claude/commands/
    m = re.search(r"(?:^|/)\.claude/commands/([^/]+)\.md$", path_norm)
    if not m:
        sys.exit(0)

    name = m.group(1)

    # Read the file contents (prefer hook payload, fall back to disk)
    contents = tool_input.get("content") or ""
    if not contents:
        try:
            with open(path, "r", encoding="utf-8") as f:
                contents = f.read()
        except Exception:
            sys.exit(0)

    # Parse the description out of the YAML frontmatter
    fm_match = re.match(r"^---\s*\n(.*?)\n---", contents, re.DOTALL)
    if not fm_match:
        sys.exit(0)
    desc_match = re.search(r"^description:\s*(.+)$", fm_match.group(1), re.MULTILINE)
    if not desc_match:
        sys.exit(0)
    description = desc_match.group(1).strip().strip("\"'")

    # Drop any agent-facing "Use when..." tail so the README entry stays concise
    readme_desc = re.split(r"\.\s+Use when\b", description, maxsplit=1)[0].strip()
    if not readme_desc.endswith("."):
        readme_desc += "."

    new_entry = f"- `/{name}` {readme_desc}"

    # README lives at the project root (hook command runs from cwd)
    repo_root = data.get("cwd") or os.getcwd()
    readme_path = os.path.join(repo_root, "README.md")
    if not os.path.exists(readme_path):
        sys.exit(0)

    with open(readme_path, "r", encoding="utf-8") as f:
        readme = f.read()

    # Skip if this command is already mentioned
    if f"`/{name}`" in readme:
        sys.exit(0)

    # Locate the Commands Menu section
    section_start = readme.find("## Commands Menu\n")
    if section_start == -1:
        sys.exit(0)

    # Find where the next ## section begins (or end of file)
    next_section = readme.find("\n##", section_start + 1)

    if next_section == -1:
        new_readme = readme.rstrip("\n") + "\n" + new_entry + "\n"
    else:
        new_readme = readme[:next_section] + "\n" + new_entry + "\n" + readme[next_section:]

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_readme)


main()
