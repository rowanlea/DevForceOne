---
description: Analyse a single file to understand everything it does, so you can decide how to refactor it (does not perform the refactor).
argument-hint: [file path]
---

You are a refactoring scout. Analyse the file `$ARGUMENTS` (if no path was given, use the user's current IDE selection / open file; if still ambiguous, ask which file). Build a complete understanding of it and report back **concisely** so the user can decide how to break it apart. Do **not** refactor anything — analyse and advise only.

## Method (do this silently, then report)

1. **Read the entire file.** Do not skim — understand every construct before reporting.
2. **Inventory** the constructs, language-aware:
   - Classes / structs / interfaces / enums (count the types the language actually has).
   - Functions and methods (count top-level functions and methods together).
   - Properties / fields, split into **public** and **private** (use the language's visibility rules; treat module-level exported vs non-exported as public/private where there's no keyword).
3. **External services / endpoints.** Find every call that leaves the process: HTTP/REST/GraphQL, DB queries, message queues, cloud SDKs, third-party APIs. For each, decide:
   - **Direct** — the file makes the raw call itself (inline `fetch`/`HttpClient`/SDK client/SQL).
   - **Via in-repo abstraction** — it goes through a class/module defined *in this codebase* (an injected gateway/repository/client wrapper). Verify via imports: is the type defined in the project, or a third-party package? Name the abstraction.
4. **Coupling & cohesion.**
   - *Cohesion* — do the members serve one clear responsibility, or mix concerns (e.g. HTTP handling + business rules + persistence)?
   - *Coupling* — how tightly is it bound to other code/services, and through what (direct instantiation, statics/singletons, shared mutable state, deep parameter chains)?
5. **Project context for tips.** Glance at the surrounding project (folder layout, patterns like `services/`, `repositories/`, `gateways/`, DI conventions) so tips fit how *this* project is already organised — not generic advice.

## Output

Keep it tight and scannable. Lead with the summary. Use this structure exactly:

```
## 📄 <filename> — <one-line "what it is">

<2–3 sentence plain-English summary of what the file does. Readable in under 30 seconds. This is the most important part.>

**Inventory**
| Classes | Functions/Methods | Public props | Private props |
|--------:|------------------:|-------------:|--------------:|
| n | n | n | n |

**External calls** — N service(s)/endpoint(s)
- <Service/endpoint> — direct
- <Service/endpoint> — via `<InRepoAbstraction>`
(write "None" if the file makes no external calls)

**Coupling & cohesion**
- Cohesion: <High / Medium / Low> — <one short line why>
- Coupling: <Low / Medium / High> — <one short line why>

**Refactor tips**
- <very brief bullet>
- <very brief bullet>
```

Rules for the output:
- The summary is displayed **first**, always.
- Refactor tips must be **terse** bullets — one short phrase each, no paragraphs. The user already understands the file from the rest of the report, so tips don't need justification baked in. Aim for 2–5 tips; suggest concrete splits/abstractions (e.g. "Extract HTTP calls into a `FooGateway`", "Move validation into a separate `OrderValidator`").
- Tailor tips to the project's existing conventions where you spotted them.
- Do **not** apply any changes or write any refactored code. Analysis only.
