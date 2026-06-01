# Taxonomy

Controlled vocabulary for `tags`, `domain`, `difficulty`, and `status` in frontmatter. Keep this list curated — new tags should be added here first, with a one-line description, before being used in a sheet. This prevents tag sprawl.

## Domains

Top-level folders. A sheet's `domain` must match its folder path.

| Domain                          | Description                                                  |
| ------------------------------- | ------------------------------------------------------------ |
| `core/linear-algebra`           | Vectors, matrices, decompositions, matrix calculus.          |
| `core/probability`              | Sample spaces, RVs, distributions, limit theorems.           |
| `core/statistics`               | Estimation, inference, regression, hypothesis testing.       |
| `core/calculus`                 | Derivatives, integration, multivariable, vector calculus.    |
| `core/optimization`             | Gradient methods, convexity, duality, constrained opt.       |
| `core/information-theory`       | Entropy, divergence, mutual information.                     |
| `core/discrete-math`            | Combinatorics, graph theory, recurrences.                    |
| `core/numerical-methods`        | Floating point, stability, iterative solvers.                |
| `core/stochastic-processes`     | Markov chains, Brownian motion, martingales, Poisson process.|
| `core/functional-analysis`      | Hilbert/Banach spaces, RKHS, linear operators (planned).     |
| `core/measure-theory`           | Sigma-algebras, Lebesgue integration, Radon–Nikodym (planned).|
| `core/differential-equations`   | ODEs, PDEs, SDEs (planned; SDE specifics live in quant too). |
| `ml/supervised`                 | Regression, classification, kernel methods.                  |
| `ml/unsupervised`               | Clustering, dimensionality reduction, density estimation.    |
| `ml/deep-learning`              | Backprop, attention, normalization, optimizers.              |
| `ml/reinforcement-learning`     | MDPs, Bellman, policy gradient.                              |
| `ml/evaluation`                 | Metrics, cross-validation, calibration.                      |
| `quant/stochastic-calculus`     | Brownian motion, Ito calculus, SDEs.                         |
| `quant/derivatives-pricing`     | Black-Scholes, binomial trees, Greeks, exotic options.       |
| `quant/portfolio-theory`        | MPT, CAPM, factor models, performance metrics.               |
| `quant/time-series`             | ARMA, GARCH, cointegration, regime switching.                |
| `quant/risk`                    | VaR, CVaR, stress testing, copulas.                          |
| `quant/market-microstructure`   | Order books, market impact, execution.                       |
| `crossover/game-theory`         | Equilibria, bandits, mechanism design.                       |
| `crossover/bayesian-inference`  | Priors, posteriors, sampling, variational methods.           |
| `crossover/convex-optimization` | Convex sets/functions, duality, conic programs.              |

## Tags (cross-cutting themes)

| Tag                          | Description                                            |
| ---------------------------- | ------------------------------------------------------ |
| `matrix-factorization`       | Decomposing matrices into structured factors.          |
| `dimensionality-reduction`   | Reducing feature count while preserving information.   |
| `monte-carlo`                | Methods based on random sampling.                      |
| `convex`                     | Convex problems / functions / sets.                    |
| `distribution`               | A specific probability distribution.                   |
| `loss-function`              | Objective functions used in training.                  |
| `regularization`             | Penalties added to prevent overfitting.                |
| `kernel`                     | Kernel methods / RKHS.                                 |
| `stochastic-process`         | Random processes indexed by time.                      |
| `inequality`                 | A named inequality (Jensen, Cauchy-Schwarz, …).        |
| `identity`                   | A named identity or equality.                          |
| `decomposition`              | Matrix or operator decomposition (SVD, QR, Cholesky).  |
| `eigen`                      | Eigenvalues / eigenvectors / spectral content.         |
| `optimizer`                  | A specific optimization algorithm (Adam, SGD, BFGS…).  |
| `divergence`                 | Asymmetric "distance" between distributions (KL, JS…). |
| `concentration`              | Tail bounds on random variables (Hoeffding, Chernoff). |
| `markov`                     | Markov property / Markov chain content.                |
| `martingale`                 | Martingale-related identities or theorems.             |
| `bandit`                     | Multi-armed bandit / exploration–exploitation.         |
| `pricing`                    | Derivative pricing models / formulas.                  |
| `factor-model`               | Linear factor structure (CAPM, Fama-French, PCA risk). |
| `tail-risk`                  | VaR, CVaR, EVT, copula-based tail metrics.             |
| `metric`                     | Evaluation metric (accuracy, ROC-AUC, Sharpe…).        |
| `sampling`                   | Sampling algorithm (MCMC, importance, rejection…).     |

_Add new tags here with a one-line description before using them in a sheet._

## Difficulty

| Level | Meaning                                                                              |
| ----: | ------------------------------------------------------------------------------------ |
|   `1` | Introductory — assumes only high-school math + the listed prerequisites.             |
|   `2` | Working — undergraduate level; standard tool you should fluently use.                |
|   `3` | Advanced — graduate level; deeper theory, proofs, or specialized applications.       |

## Status

| Status     | Meaning                                                                       |
| ---------- | ----------------------------------------------------------------------------- |
| `draft`    | First pass, may have gaps or errors.                                          |
| `reviewed` | At least one other pair of eyes; formulas spot-checked.                       |
| `stable`   | Considered canonical; changes need justification.                             |
