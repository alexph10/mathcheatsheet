---
id: mean-variance
title: Mean–Variance Portfolio Optimization
domain: quant/portfolio-theory
tags: [factor-model, convex]
prerequisites: [vectors, common-distributions, convexity]
used_by: []
difficulty: 2
status: draft
notebook: mean-variance.ipynb
---

# Mean–Variance Portfolio Optimization

## TL;DR

Choose portfolio weights to minimize variance for a target expected return — a [convex](../../core/optimization/convexity.md) quadratic program whose closed-form solution traces the efficient frontier.

## Setup

$n$ risky assets with expected return vector $\boldsymbol{\mu} \in \mathbb{R}^n$ and positive-definite covariance matrix $\boldsymbol{\Sigma} \in \mathbb{R}^{n \times n}$. A portfolio is a [weight vector](../../core/linear-algebra/vectors.md) $\mathbf{w} \in \mathbb{R}^n$ with

$$ \text{return} = \mathbf{w}^\top \boldsymbol{\mu}, \qquad \text{variance} = \mathbf{w}^\top \boldsymbol{\Sigma} \mathbf{w}. $$

The fully-invested constraint is $\mathbf{w}^\top \mathbf{1} = 1$; short-selling is allowed unless explicitly excluded.

## Markowitz problem

For a target return $r$:

$$ \min_{\mathbf{w}} \; \tfrac{1}{2}\mathbf{w}^\top \boldsymbol{\Sigma} \mathbf{w} \quad \text{s.t.} \quad \mathbf{w}^\top \boldsymbol{\mu} = r, \; \mathbf{w}^\top \mathbf{1} = 1. $$

Convex (quadratic objective with $\boldsymbol{\Sigma} \succ 0$, linear constraints), so the KKT conditions give the unique global optimum.

## Closed-form solution

Lagrangian $\mathcal{L} = \tfrac{1}{2}\mathbf{w}^\top \boldsymbol{\Sigma} \mathbf{w} - \lambda(\mathbf{w}^\top \boldsymbol{\mu} - r) - \gamma(\mathbf{w}^\top \mathbf{1} - 1)$ gives

$$ \mathbf{w}^\star = \boldsymbol{\Sigma}^{-1}(\lambda \boldsymbol{\mu} + \gamma \mathbf{1}). $$

Define the scalars

$$ A = \mathbf{1}^\top \boldsymbol{\Sigma}^{-1} \mathbf{1}, \quad B = \mathbf{1}^\top \boldsymbol{\Sigma}^{-1} \boldsymbol{\mu}, \quad C = \boldsymbol{\mu}^\top \boldsymbol{\Sigma}^{-1} \boldsymbol{\mu}, \quad D = AC - B^2. $$

Solving the two linear equations for $\lambda, \gamma$ yields

$$ \lambda = \frac{Ar - B}{D}, \qquad \gamma = \frac{C - Br}{D}, $$

and the minimum-variance value is

$$ \sigma^2(r) = \frac{Ar^2 - 2Br + C}{D}. $$

A parabola in $r$ — the **efficient frontier**, drawn as $(\sigma, r)$ it is a hyperbola.

### Special portfolios

- **Global minimum-variance portfolio.** Drop the return constraint:
  $$ \mathbf{w}_{\text{mv}} = \frac{\boldsymbol{\Sigma}^{-1}\mathbf{1}}{\mathbf{1}^\top \boldsymbol{\Sigma}^{-1}\mathbf{1}}, \qquad r_{\text{mv}} = B/A, \qquad \sigma^2_{\text{mv}} = 1/A. $$
- **Tangency portfolio (with risk-free rate $r_f$).** Maximize the Sharpe ratio $(\mathbf{w}^\top \boldsymbol{\mu} - r_f)/\sqrt{\mathbf{w}^\top \boldsymbol{\Sigma} \mathbf{w}}$ subject to $\mathbf{w}^\top \mathbf{1} = 1$:
  $$ \mathbf{w}_{\text{tan}} \propto \boldsymbol{\Sigma}^{-1}(\boldsymbol{\mu} - r_f \mathbf{1}), $$
  normalized so weights sum to 1.

## Two-fund / capital-market line

**Two-fund theorem.** Every frontier portfolio is a linear combination of any two distinct frontier portfolios (e.g. min-variance and tangency).

With a risk-free asset, the efficient frontier becomes a straight line in $(\sigma, r)$ — the **capital market line** — tangent to the risky-only frontier at $\mathbf{w}_{\text{tan}}$:

$$ r = r_f + \frac{\mathbf{w}_{\text{tan}}^\top \boldsymbol{\mu} - r_f}{\sigma_{\text{tan}}} \, \sigma. $$

The slope is the maximum achievable Sharpe ratio.

## Worked micro-example

Two assets, $\boldsymbol{\mu} = (0.10, 0.20)^\top$, volatilities $(0.15, 0.30)$, correlation $\rho = 0.0$. Then $\boldsymbol{\Sigma} = \text{diag}(0.0225, 0.09)$, and

$$ \mathbf{w}_{\text{mv}} \propto (1/0.0225, 1/0.09)^\top = (44.4, 11.1)^\top \Rightarrow \mathbf{w}_{\text{mv}} = (0.8, 0.2)^\top, $$

with return $0.10 \cdot 0.8 + 0.20 \cdot 0.2 = 0.12$ and variance $0.8^2 \cdot 0.0225 + 0.2^2 \cdot 0.09 = 0.018$, i.e. $\sigma \approx 13.4\%$ — lower than either asset alone, thanks to imperfect correlation.

> See [companion notebook](./mean-variance.ipynb) for the efficient frontier of 5 synthetic assets, the tangency portfolio, and a sensitivity demo.

## Estimation-error sensitivity (the classic critique)

The solution depends on $\boldsymbol{\Sigma}^{-1}\boldsymbol{\mu}$. Small perturbations to $\boldsymbol{\mu}$ produce **huge** swings in $\mathbf{w}^\star$, especially when $\boldsymbol{\Sigma}$ has small eigenvalues (highly correlated assets). In practice:

- **Shrinkage / regularization** of $\boldsymbol{\Sigma}$ (Ledoit–Wolf) and of $\boldsymbol{\mu}$ (James–Stein, Black–Litterman).
- **Constraints** like $\mathbf{w} \geq 0$ (no shorts) act as implicit regularization.
- **Resampling / robust optimization** to penalize parameter uncertainty.
- Use **factor models** to give $\boldsymbol{\Sigma}$ low-rank-plus-diagonal structure.

## Common pitfalls

- **Variance ≠ downside risk.** Penalizes upside surprises equally. Drives interest in CVaR-based portfolios.
- **Single-period model.** Ignores rebalancing and transaction costs.
- **In-sample frontier overstates achievable Sharpe** — a backtest using out-of-sample $\boldsymbol{\mu}, \boldsymbol{\Sigma}$ is essential.
- **$\boldsymbol{\Sigma}$ must be positive-definite.** With more assets than observations, the sample covariance is singular; use shrinkage or factor structure.

## Applications in quant

- Foundation of CAPM and modern factor-investing pipelines.
- Risk-parity, minimum-variance, and Black–Litterman are direct descendants/refinements.
- Asset-allocation defaults in pension funds, robo-advisors.

## See also

- [Vectors](../../core/linear-algebra/vectors.md)
- [Common distributions](../../core/probability/common-distributions.md) — joint-Normal returns.
- [Convexity](../../core/optimization/convexity.md) — why the QP is solvable.

## References

- Markowitz, *Portfolio Selection*, J. of Finance, 1952.
- Luenberger, *Investment Science*, Ch. 6.
- Ledoit & Wolf, *Honey, I shrunk the sample covariance matrix*, 2003.
