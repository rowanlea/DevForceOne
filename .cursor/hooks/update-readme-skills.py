#!/usr/bin/env python3
"""
afterFileEdit hook: when a new skills/*/SKILL.md is written, append an entry
to the ## Skills Menu section in README.md.
"""
import json
import sys
import re
import os
import fnmatch


def main():
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        sys.exit(0)

    # Resolve the file path from whichever key the hook runtime populates
    path = (
        data.get("path")
        or data.get("input", {}).get("path")
        or ""
    )

    path_norm = path.replace("\\", "/")

    if not re.search(r"\.cursor/skills/[^/]+/SKILL\.md$", path_norm):
        sys.exit(0)

    # Read the SKILL.md contents (prefer hook payload, fall back to disk)
    contents = (
        data.get("contents")
        or data.get("input", {}).get("contents")
        or ""
    )
    if not contents:
        try:
            with open(path, "r", encoding="utf-8") as f:
                contents = f.read()
        except Exception:
            sys.exit(0)

    # Parse YAML frontmatter
    try:
        import yaml
        fm_match = re.match(r"^---\s*\n(.*?)\n---", contents, re.DOTALL)
        if not fm_match:
            sys.exit(0)
        frontmatter = yaml.safe_load(fm_match.group(1))
    except Exception:
        sys.exit(0)

    name = (frontmatter.get("name") or "").strip()
    description = (frontmatter.get("description") or "").strip()

    if not name or not description:
        sys.exit(0)

    # Drop the agent-facing "Use when..." tail so the README entry stays concise
    readme_desc = re.split(r"\.\s+Use when\b", description, maxsplit=1)[0].strip()
    if not readme_desc.endswith("."):
        readme_desc += "."

    new_entry = f"- `{name}` {readme_desc}"

    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(os.path.dirname(script_dir))  # hooks/ -> .cursor/ -> repo root
    readme_path = os.path.join(repo_root, "README.md")
    if not os.path.exists(readme_path):
        sys.exit(0)

    with open(readme_path, "r", encoding="utf-8") as f:
        readme = f.read()

    # Skip if this skill is already mentioned
    if f"`{name}`" in readme:
        sys.exit(0)

    # Locate the Skills Menu section
    section_start = readme.find("## Skills Menu\n")
    if section_start == -1:
        sys.exit(0)

    # Find where the next ## section begins (or end of file)
    next_section = readme.find("\n##", section_start + 1)

    if next_section == -1:
        # Skills Menu is the last section — append at the end
        new_readme = readme.rstrip("\n") + "\n" + new_entry + "\n"
    else:
        # Insert the entry just before the next section heading
        new_readme = readme[:next_section] + "\n" + new_entry + readme[next_section:]

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_readme)

    print("{}")


main()
