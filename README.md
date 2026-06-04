# DevForceOne

A grab-bag of Claude Code commands and supporting scripts. Take whatever is useful — nothing here is wired into an active `.claude/` folder, so cloning this repo won't override or conflict with your own user- or project-level Claude config.

## Installing a command

Copy the command you want from `commands/` into your own Claude Code commands folder:

- **User-level (available everywhere):** `~/.claude/commands/`
- **Project-level (just one repo):** `<project>/.claude/commands/`

It's then available as a slash command, e.g. `/code-coverage`. Some commands also need a script from `scripts/` — see the menu below.

## Commands Menu
- `/commit-auto` — figures out an appropriate commit message for all your current changes, then adds, commits, and pushes. It stages everything unstaged, so review your changes first.
- `/code-coverage` — detects and runs the right code coverage tool for the project; installs the most popular free one if none is present, and asks you to choose when ambiguous.
- `/run-local` — figures out how to run a project locally: installs dependencies, sets up virtualenvs, resolves conflicts, verifies it runs, and writes a concise "Running locally" README section.
- `/html-doc` — creates a polished, self-contained HTML presentation document from a prompt.
- `/analyse-file` — analyses a single file to help you decide how to refactor it: inventory, external-call usage, a 30-second summary, and coupling/cohesion with brief tips.
- `/split-to-prs` — splits your current work into small, reviewable PRs: proposes a reviewer-aligned split plan, waits for approval, snapshots your work, then creates the branches/PRs.
- `/megalinter` — configures and runs an optimised MegaLinter scan. **Requires** `scripts/megalinter-preflight.py` copied to your `.claude/scripts/`, plus `pip install pyyaml`, Docker, and the Grafana stack below.

## MegaLinter scans

The `/megalinter` command runs a smart, fast scan of the open repo:

1. Copy `scripts/megalinter-preflight.py` into your `.claude/scripts/` and `pip install pyyaml`.
2. Start the Grafana stack so results can be reported: `docker compose up -d`, then open Grafana at [http://localhost:3000](http://localhost:3000) (dashboards are provisioned automatically). The scan still runs if the stack is down — results stay in the console output and MegaLinter logs.
3. Run `/megalinter` in the project you want to scan.

## Optional: auto-maintain your Commands Menu

`scripts/update-readme-commands.py` is a Claude Code `PostToolUse` hook that appends an entry to a `## Commands Menu` section in your README whenever you write a new `.claude/commands/<name>.md`. To use it, copy the script into your `.claude/scripts/` and add this to your `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          { "type": "command", "command": "python .claude/scripts/update-readme-commands.py" }
        ]
      }
    ]
  }
}
```

## Additional Force Multiplying Tools
- [OpenWhispr](https://openwhispr.com/) - a free alternative to WisprFlow. It can be clunky to use sometimes, but the results are just as good, if not occasionally better than WisprFlow.
