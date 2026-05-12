---
name: megalinter
description: Dynamically configures and runs an optimized MegaLinter scan on the current project.
---

# MegaLinter Global Skill

This skill triggers a smart, fast MegaLinter scan for the currently opened repository.

## How it works
1. **Dynamic Config**: It runs a pre-flight script to detect languages and exclude huge library folders.
2. **Local Mount**: it mounts the project currently open in Cursor into a Docker container.
3. **No Setup**: You don't need to configure `PROJECT_NAME` anymore; the skill handles it.

## Process
1. **Prepare**: Run `python3 ~/.cursor/skills-cursor/megalinter/scripts/preflight.py`
2. **Execute**: The script will automatically trigger the Docker scan once the configuration is ready.