---
name: code-coverage
description: Detects and runs code coverage tools for the current project. Checks if a coverage tool is already installed for the project's programming language; if one is found, runs it immediately. If none is found, installs the most popular free tool for that language first and then runs it. If the choice of tool is ambiguous, presents the user with a list of options. Use when the user wants to measure test coverage, generate a coverage report, or check which coverage tools are in use.
disable-model-invocation: true
---

# Code Coverage

## Workflow

1. **Detect the project language** — look for language-specific manifest/config files
2. **Check for an existing coverage tool** — scan manifests, config files, and installed CLIs
3. **If a tool is found** — run it immediately
4. **If no tool is found** — determine the best options (see below), install, then run

---

## Step 1: Language Detection

| Signal files | Language |
|---|---|
| `package.json` | JavaScript / TypeScript |
| `pyproject.toml`, `setup.py`, `requirements*.txt`, `Pipfile` | Python |
| `pom.xml`, `build.gradle`, `build.gradle.kts` | Java / Kotlin |
| `go.mod` | Go |
| `Cargo.toml` | Rust |
| `Gemfile` | Ruby |
| `composer.json` | PHP |
| `*.csproj`, `*.sln` | C# / .NET |
| `CMakeLists.txt` or `Makefile` with `.c`/`.cpp` files | C / C++ |

When multiple signals are present, use the predominant one or ask the user.

---

## Step 2: Detecting Existing Tools

Scan for evidence of an already-configured coverage tool:

- Package manifests (`package.json` devDependencies, `Gemfile`, `composer.json`, `Cargo.toml`, `pom.xml`, `build.gradle`, `*.csproj`)
- Config files (`.coveragerc`, `pyproject.toml [tool.coverage]`, `tox.ini`, `jest.config.*`, `.nycrc`, `codecov.yml`, etc.)
- Installed CLIs (`coverage --version`, `nyc --version`, `c8 --version`, `cargo tarpaulin --version`, etc.)
- CI configuration (`.github/workflows/`, `.gitlab-ci.yml`) — often references the tool by name

If a tool is found, run it. Do not proceed to Step 3.

---

## Step 3: Finding and Installing a Tool (nothing installed)

**Do not use a static lookup list.** Instead:

1. Use your own knowledge of the ecosystem for the detected language to identify the most popular, actively maintained, free-to-use coverage tools available today.
2. If you are uncertain about current recommendations or want to verify that a tool is still actively maintained, use the `WebSearch` tool to find up-to-date information (e.g. search `"best code coverage tools for <language> <current year>"`).
3. Prefer tools that integrate with any test runner already present in the project.

**If there is a clear single best option** — tell the user which tool you are installing and why, then install and run it.

**If the choice is ambiguous** — present the user with a shortlist (2–4 options) using the `AskQuestion` tool if available, otherwise list them conversationally. For each option include: name, one-line description, and why it fits this project. Wait for the user to choose before installing anything.
