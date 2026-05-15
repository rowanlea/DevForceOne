---
name: html-doc
description: Creates a polished, self-contained HTML presentation document from a given prompt. Use when the user asks to generate an HTML doc, write a presentation, create a tech explainer page, or produce a visual summary of work for colleagues.
disable-model-invocation: true
---

# HTML Doc

Produce a single, self-contained `.html` file — no external dependencies, all CSS and any JS inline — that looks like a professional presentation.

## Audience & purpose

This HTML is intended to show colleagues the work being done and help them understand how it works. Prioritise clarity and visual appeal over density of information.

## Design principles

- **Light mode** colour scheme throughout.
- Use the Codurance brand palette (see below) for accents, headings, highlights, and interactive elements.
- Leverage modern HTML/CSS fully: CSS variables, flexbox/grid layouts, smooth transitions, hover effects, subtle shadows, clean typography.
- Structure content like a mini slide-deck or well-sectioned article — clear hierarchy, generous whitespace, scannable at a glance.
- Use icons (inline SVG or Unicode) and visual dividers to break up sections.
- Avoid walls of text; prefer bullet lists, callout boxes, code blocks, and short paragraphs.

## Codurance colour palette

```css
:root {
  --tango:          #ef7726;
  --crimson:        #d60d47;
  --gold:           #ffd000;
  --persimmon:      #ff5851;
  --persimmon-dark: #ff4f33;

  /* Recommended neutrals for light mode */
  --bg:             #ffffff;
  --surface:        #f8f8f8;
  --border:         #e5e5e5;
  --text-primary:   #1a1a1a;
  --text-secondary: #555555;
}
```

Use `--tango` as the primary accent (headings underlines, links, key highlights).  
Use `--crimson` for badges, warnings, or call-to-action elements.  
Use `--gold` sparingly for highlights or "star" callouts.  
Use `--persimmon` / `--persimmon-dark` for gradients or hover states.

## HTML structure template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>[Title]</title>
  <style>
    /* All styles here — no external stylesheets */
  </style>
</head>
<body>
  <!-- Hero / title banner -->
  <header> ... </header>

  <!-- One <section> per major topic -->
  <main>
    <section> ... </section>
  </main>

  <!-- Optional: footer with date / author -->
  <footer> ... </footer>
</body>
</html>
```

## Output

- Write the file to the project root (or a location the user specifies) with a descriptive kebab-case filename, e.g. `ci-pipeline-overview.html`.
- After writing, tell the user the filename and that they can open it in any browser.
