# DevForceOne

## Setup (one-time)

1. `pip install pyyaml`
2. Copy any skills you want from the `skills/` folder into your Cursor skills folder (e.g. `megalinter`):
   ```
   .cursor/
     └── skills-cursor/
        └── megalinter/
            ├── SKILL.md
            └── scripts/
                └── preflight.py
   ```
3. Start the Grafana stack: `docker compose up -d`
4. Open Grafana at [http://localhost:3000](http://localhost:3000) — dashboards are provisioned automatically

## Running a scan

Open the project you want to scan in Cursor and invoke the MegaLinter skill.

## Skills Menu
- Use Cursor's in-built `split-to-prs` to convert a large change set into small, understandable pull requests. - _I had an idea to create exactly this skill, and then found that cursor already did it, so I'm not going to reinvent the wheel._
- `commit-auto` will figure out an appropriate commit message for all the changes you currently have. It will add everything currently unstaged, so make sure you manually review changes first.
- `code-coverage` Detects and runs code coverage tools for the current project. Checks if a coverage tool is already installed for the project's programming language; if one is found, runs it immediately. If none is found, installs the most popular free tool for that language first and then runs it. If the choice of tool is ambiguous, presents the user with a list of options.
- `run-local` Figures out how to run a project locally, installs dependencies, sets up virtual environments (Python etc.), resolves dependency conflicts, verifies the project runs correctly, and writes or updates a concise "Running locally" README section.

## Additional Force Multiplying Tools
- [OpenWhispr](https://openwhispr.com/) - a free alternative to WisprFlow. It can be clunky to use sometimes, but the results are just as good, if not occasionally better than WisprFlow.