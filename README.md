# DevForceOne

## Setup (one-time)

1. `pip install pyyaml`
2. Copy `SKILL.md` and `preflight.py` into your Cursor skills folder:
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
