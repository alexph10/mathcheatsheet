# Contributing

## Adding a new cheat sheet

1. **Pick a slug.** Lowercase, kebab-case, globally unique across the whole repo (e.g. `svd`, `mean-variance-portfolio`). Never rename a slug once published — other sheets link to it.
2. **Pick a domain.** Match an entry in [taxonomy.md](./taxonomy.md). The folder path == the `domain` field.
3. **Copy the template.**
   ```bash
   cp template.md core/linear-algebra/<slug>.md
   # if code/plots add value:
   cp template.ipynb core/linear-algebra/<slug>.ipynb
   ```
4. **Fill in frontmatter.** Especially `prerequisites` and `used_by` — these build the dependency graph.
5. **Write content** following the section order in template.md. Skip sections that genuinely don't apply rather than padding.
6. **Validate.**
   ```bash
   python _meta/scripts/validate.py
   ```
7. **Refresh the index.**
   ```bash
   python _meta/scripts/build_index.py
   ```

## When does a sheet need a notebook?

Add a `.ipynb` when **any** of these apply:
- A numerical example clarifies the concept (e.g. SVD of a small matrix).
- A plot conveys geometric intuition (e.g. eigenvectors, distribution shapes, gradient descent trajectories).
- A pitfall is easier to demonstrate than describe (e.g. numerical instability).
- The reader benefits from tweaking parameters.

Skip the notebook for purely definitional sheets (e.g. "what is a norm").

## Style rules

- **Math:** `$...$` inline, `$$...$$` display. GitHub renders both natively.
- **Don't duplicate.** If a primitive lives in `core/`, applied sheets link to it instead of restating the formula.
- **Link by relative path** — the validator checks for broken links.
- **Keep TL;DR to one sentence.**
- **Worked example must be the smallest non-trivial case.** Resist the urge to add a "realistic" example here; that goes in the notebook.

## Editing an existing sheet

- Bumping a sheet from `draft` → `reviewed` requires another contributor to spot-check formulas.
- Bumping `reviewed` → `stable` requires the sheet to have been used by at least one applied sheet (i.e. it appears in some other sheet's `prerequisites`).
- Breaking changes to formulas in a `stable` sheet require updating every sheet that lists it as a prerequisite.
