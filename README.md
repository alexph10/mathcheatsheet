#### Repository layout

```
core/         domain-agnostic math primitives (linear algebra, probability, calculus, …)
ml/           machine learning applications (regression, PCA, backprop, …)
quant/        quant finance applications (Black-Scholes, GARCH, VaR, …)
crossover/    shared mid-level theory (game theory, Bayesian inference, convex opt)
_meta/        build scripts, shared styles, CI helpers
```

#### Quickstart (for readers)

Browse any folder, open the `.md` for the reference, open the `.ipynb` for runnable code.

```bash
pip install -r requirements.txt
jupyter lab
```
