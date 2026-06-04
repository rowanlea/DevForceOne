Audit and enhance the documentation for this project. Follow these steps exactly.

---

## Step 1 — Survey what exists

Read the top-level documentation file (README.md or equivalent) in full.

Then read whatever project and configuration files are present to understand:
- Language(s), runtimes, and their versions
- How the project is built and run
- What test frameworks are in use
- Any existing architecture or contribution documentation

Only record what you can read directly from files on disk — do not guess.

---

## Step 2 — Identify the actual layout

Walk the project and build a real directory tree (2–3 levels deep), skipping build artifacts, dependency caches, and version-control internals.

For each top-level directory, infer its purpose from its contents. Note where source code, tests, and configuration live, and record any layout rules found in existing documentation.

---

## Step 3 — Evaluate the documentation against these five requirements

For each, note: **present**, **partial**, or **missing**.

1. **Prerequisites and setup** — Everything a developer must install before they can open, build, or run the project, with versions pinned where the project files specify them.
2. **Architecture** — How the project is structured, what each major folder or module is for, and the key design rules or conventions.
3. **Developer onboarding** — How to navigate the codebase, where to add a new feature, and the conventions for where things belong.
4. **How to run the project** — How to start the application in development mode and, if applicable, how to build or run it headlessly.
5. **Tests** — Whether tests exist, what frameworks are used, where test files live, and how to run them.

---

## Step 4 — Patch the documentation with the minimum necessary changes

**Do not rewrite the README.** Preserve every word, heading, and structure that already exists. Only make the smallest edits that bring it up to the five requirements — add missing sections, expand stubs, fill empty content. If a section already covers a requirement well, leave it alone.

1. For each gap, add only what is needed to close it — no restructuring or reformatting of existing content.
2. If a required section is entirely absent, append it at the end of the file rather than inserting it mid-document.
3. Never delete or reword existing content unless it is factually wrong based on what you read from disk.

Derive all new content from what you found in Steps 1 and 2 — do not invent versions, commands, or folder names.

---

## Step 5 — Report what changed

Print a brief summary:
- Which sections were added or updated
- Any gaps you could not fill from the information available on disk, so the developer knows what to fill in manually
