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