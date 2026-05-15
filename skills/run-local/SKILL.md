---
name: run-local
description: Figures out how to run a project locally, installs dependencies, sets up virtual environments (Python etc.), resolves dependency conflicts, verifies the project runs correctly, and writes or updates a concise "Running locally" README section. Use when the user wants to get a project running locally, set up a dev environment, fix dependency issues, or document how to run the project.
---

# Local Dev Setup

## Workflow

### 1. Identify the project type

Scan the repo root for signal files:

| Signal file | Stack |
|---|---|
| `requirements.txt` / `pyproject.toml` / `setup.py` / `Pipfile` | Python |
| `package.json` | Node.js / JS / TS |
| `go.mod` | Go |
| `Cargo.toml` | Rust |
| `pom.xml` / `build.gradle` | Java / Kotlin |
| `*.csproj` / `*.sln` | .NET |
| `composer.json` | PHP |
| `Gemfile` | Ruby |
| `mix.exs` | Elixir |
| `docker-compose.yml` / `Dockerfile` | Container-based |

Check for multiple stacks (monorepo) and handle each.

### 2. Install dependencies

#### Python
1. Determine minimum Python version from `pyproject.toml`, `.python-version`, or code.
2. Create a virtual environment in the repo root:
   ```bash
   python -m venv .venv
   ```
3. Activate (show both platforms):
   - macOS/Linux: `source .venv/bin/activate`
   - Windows: `.venv\Scripts\activate`
4. Install:
   - `pip install -r requirements.txt` or
   - `pip install -e ".[dev]"` (editable + extras) or
   - `pip install -e .` for `pyproject.toml`
5. If `requirements.txt` is absent, check `setup.py`/`pyproject.toml` and generate one if needed.

#### Node.js
1. Check for `.nvmrc` / `engines.node` in `package.json`; flag version mismatches.
2. Detect lockfile: `package-lock.json` → npm, `yarn.lock` → yarn, `pnpm-lock.yaml` → pnpm.
3. Run the appropriate install command (`npm ci` preferred over `npm install` when lockfile exists).

#### Other stacks
Use the idiomatic install command for the detected stack (`go mod download`, `cargo build`, `bundle install`, etc.).

### 3. Resolve dependency issues

Common patterns and fixes:

| Problem | Fix |
|---|---|
| Version conflict | Pin the conflicting package to a compatible version |
| Missing system dependency (e.g. `libpq`, `node-gyp`) | Document the system-level install step |
| `.env` / secrets required | Create `.env.example`, note what values are needed |
| Database or external service required | Document with `docker-compose` snippet or connection string format |
| Port conflict | Note how to change the default port |

After each fix, re-run the install command to confirm it resolves cleanly.

### 4. Find and run the start command

Check in order:
1. `Makefile` targets (`make dev`, `make run`, `make start`)
2. `package.json` `scripts` field (`dev`, `start`, `serve`)
3. `Procfile`
4. Framework conventions (`uvicorn`, `flask run`, `rails s`, `cargo run`, etc.)
5. README (existing, may be stale — verify)
6. Entrypoint files (`main.py`, `index.js`, `cmd/main.go`, etc.)

### 5. Verify it's running

After starting the project, confirm it is healthy using the first applicable method:

- **HTTP service**: `curl -f http://localhost:<PORT>/` (or the health endpoint if one exists). A 2xx/3xx response is a pass.
- **CLI tool**: Run `<tool> --version` or `<tool> --help` and check exit code 0.
- **Background worker / daemon**: Check process is alive (`ps`, task manager) and logs contain no fatal errors within 10 seconds.
- **Test suite as smoke test**: Run the project's own tests (`pytest`, `npm test`, etc.) if startup verification isn't otherwise possible.

Report the result clearly: either "running at http://localhost:PORT" or the specific error to fix next.

### 6. Write or update the README

Find the README (`README.md`, `README.rst`, `docs/README.md`, etc.). Look for an existing "Running locally", "Development", "Getting started", or "Setup" section.

**If a correct section already exists**: skip or note it is up to date.

**If the section is missing or outdated**: insert/replace it. Keep it as short as possible — only what is genuinely needed to reproduce the setup from scratch. Use this template:

```markdown
## Running locally

**Prerequisites:** [only non-obvious tools, e.g. Python 3.11+, Node 20+, Docker]

```bash
# one-time setup
[setup commands]

# start
[run command]
```

The app runs at http://localhost:PORT.
```

Remove any steps that are redundant with the template (e.g. "clone the repo").

Do **not** add version badges, CI status, or unrelated content. Only update the local-dev section.

## Progress checklist

Copy and track as you go:

```
- [ ] Project type identified
- [ ] Dependencies installed cleanly
- [ ] Dependency conflicts resolved
- [ ] Start command found
- [ ] Project verified running
- [ ] README section written/confirmed correct
```
