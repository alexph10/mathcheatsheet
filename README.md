# Math Cheat Sheets for ML & Quant Finance

Practical, exhaustive, atomic cheat sheets for the math that actually shows up in machine learning and quantitative finance. Each topic is a single markdown file following a fixed template, with an optional companion Jupyter notebook for code, numerical examples, and plots.

## Design principles

1. **Atomic** — one concept per file. Easy to link, easy to update, easy to skim.
2. **Hierarchical** — every sheet declares its `prerequisites` and what it's `used_by`, forming a DAG.
3. **Layered** — `core/` holds canonical primitives; `ml/`, `quant/`, `crossover/` are thin applied sheets that link back. No formula is restated in two places.
4. **Template-driven** — every `.md` follows [template.md](./template.md). Every `.ipynb` follows [template.ipynb](./template.ipynb).
5. **Tooling-friendly** — YAML frontmatter on every sheet enables auto-generated indexes, prerequisite graphs, and link validation in CI.

## Repository layout

```
core/         domain-agnostic math primitives (linear algebra, probability, calculus, …)
ml/           machine learning applications (regression, PCA, backprop, …)
quant/        quant finance applications (Black-Scholes, GARCH, VaR, …)
crossover/    shared mid-level theory (game theory, Bayesian inference, convex opt)
_meta/        build scripts, shared styles, CI helpers
```

See [taxonomy.md](./taxonomy.md) for the controlled vocabulary of tags and difficulty levels, and [contributing.md](./contributing.md) for how to add a new sheet.

## Status

| Area                           | Sheets | Notebooks |
| ------------------------------ | -----: | --------: |
| core/calculus                  |      5 |         4 |
| core/information-theory        |      2 |         1 |
| core/linear-algebra            |      6 |         4 |
| core/optimization              |      3 |         1 |
| core/probability               |      8 |         6 |
| core/stochastic-processes      |      1 |         1 |
| crossover/bayesian-inference   |      1 |         1 |
| crossover/game-theory          |      1 |         1 |
| ml/deep-learning               |      4 |         2 |
| ml/evaluation                  |      1 |         1 |
| ml/supervised                  |      3 |         3 |
| ml/unsupervised                |      1 |         1 |
| quant/derivatives-pricing      |      2 |         2 |
| quant/market-microstructure    |      1 |         1 |
| quant/portfolio-theory         |      3 |         3 |
| quant/risk                     |      1 |         1 |
| quant/stochastic-calculus      |      1 |         0 |
| quant/time-series              |      1 |         1 |

_Counts populated by `python _meta/scripts/build_index.py`._

## Quickstart (for readers)

Browse any folder, open the `.md` for the reference, open the `.ipynb` for runnable code.

```bash
pip install -r requirements.txt
jupyter lab
```

## Quickstart (for contributors)

1. Pick a topic, copy `template.md` (and `template.ipynb` if code/plots help).
2. Fill in frontmatter — especially `prerequisites` and `used_by`.
3. Run `python _meta/scripts/validate.py` to check frontmatter and links.
4. Run `python _meta/scripts/build_index.py` to refresh the master index.

## License

MIT.
