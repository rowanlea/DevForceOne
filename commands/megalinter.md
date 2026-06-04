---
description: Configure and run an optimised MegaLinter scan on the current project.
---

# MegaLinter

Triggers a smart, fast MegaLinter scan for the currently open repository.

## How it works
1. **Dynamic Config**: a pre-flight script detects languages and excludes huge library/vendor folders.
2. **Local Mount**: it mounts the currently open project into a Docker container.
3. **No Setup**: you don't need to configure `PROJECT_NAME`; the script handles it.

## Process
1. **Prepare & Execute**: Run `python .claude/scripts/megalinter-preflight.py` from the project root. The script writes a tailored `.mega-linter.yml`, ensures the `megalinter-net` Docker network exists, checks whether the Grafana stack (Loki + VictoriaMetrics) is reachable for API reporting, and then automatically triggers the Docker scan.
2. **Report**: Summarise the scan results for the user once it completes. Results are always available in the console output and MegaLinter's log files even if API reporting is disabled.
