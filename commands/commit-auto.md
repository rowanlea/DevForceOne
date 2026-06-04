---
description: Generate a meaningful commit message from current changes, then add, commit, and push.
---

# Auto-Commit

Assumes the user has already reviewed all changes. Do not ask for confirmation — just commit and push.

## Workflow

Run these shell commands in order, collecting output as you go:

```
git diff HEAD
git status --short
```

Use the combined output to draft the commit message (see format below), then execute:

```
git add -A
git commit -m "<generated message>"
git push
```

If `git push` fails because no upstream is set, run:

```
git push --set-upstream origin HEAD
```

Report the final pushed commit hash and message to the user.

## Commit message format

```
<type>(<scope>): <short imperative summary>

<optional body — bullet points for non-obvious changes>
```

- **type**: `feat` | `fix` | `refactor` | `chore` | `docs` | `test` | `style` | `perf`
- **scope**: the primary module, file, or feature area affected (omit if changes span the whole repo)
- **summary**: ≤72 chars, imperative mood, no trailing period
- **body**: include only when the *why* or *what* is not obvious from the diff; use `-` bullet points

### Examples

```
feat(auth): add JWT refresh-token rotation
```

```
fix(api): correct null-pointer in user lookup

- Guard against missing profile records returned by legacy endpoint
- Add regression test for the empty-profile case
```

```
chore: upgrade dependencies to latest patch versions
```

## Edge cases

| Situation | Action |
|-----------|--------|
| Nothing to commit (`git status` is clean) | Tell the user there is nothing to commit |
| Merge conflict markers present | Stop, report the conflicts, do not commit |
| `git push` rejected (non-fast-forward) | Stop, report the rejection, do not force-push |
