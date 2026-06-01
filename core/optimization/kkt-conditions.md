---
id: kkt-conditions
title: KKT Conditions
domain: core/optimization
tags: [convex]
prerequisites: [convexity, gradients]
used_by: []
difficulty: 2
status: draft
---

# Karush–Kuhn–Tucker (KKT) Conditions

## TL;DR

The KKT conditions are the first-order necessary conditions for optimality in constrained optimization — and, under convexity + a constraint qualification, also sufficient.

## Definition

Consider the general (smooth) constrained problem:

$$ \min_{\mathbf{x}} f(\mathbf{x}) \quad \text{s.t.} \quad g_i(\mathbf{x}) \leq 0,\ i=1,\ldots,m; \quad h_j(\mathbf{x}) = 0,\ j=1,\ldots,p. $$

Form the **Lagrangian**

$$ L(\mathbf{x}, \boldsymbol{\lambda}, \boldsymbol{\mu}) = f(\mathbf{x}) + \sum_i \lambda_i g_i(\mathbf{x}) + \sum_j \mu_j h_j(\mathbf{x}). $$

A point $\mathbf{x}^*$ (with multipliers $\boldsymbol{\lambda}^*, \boldsymbol{\mu}^*$) satisfies the **KKT conditions** iff:

1. **Stationarity:** $\nabla_{\mathbf{x}} L(\mathbf{x}^*, \boldsymbol{\lambda}^*, \boldsymbol{\mu}^*) = \mathbf{0}$.
2. **Primal feasibility:** $g_i(\mathbf{x}^*) \leq 0$ and $h_j(\mathbf{x}^*) = 0$.
3. **Dual feasibility:** $\lambda_i^* \geq 0$.
4. **Complementary slackness:** $\lambda_i^* g_i(\mathbf{x}^*) = 0$ for all $i$.

## Intuition

At an optimum, the gradient of $f$ must be a non-negative combination of the active-constraint gradients (pointing into the feasible region) plus any combination of equality-constraint gradients:

$$ -\nabla f(\mathbf{x}^*) = \sum_{i \in \mathcal{A}} \lambda_i^* \nabla g_i(\mathbf{x}^*) + \sum_j \mu_j^* \nabla h_j(\mathbf{x}^*). $$

Complementary slackness says: a constraint either is **active** ($g_i = 0$, possibly $\lambda_i > 0$) or has **slack** ($g_i < 0$, forcing $\lambda_i = 0$).

## When KKT is necessary / sufficient

- **Necessary** (with a constraint qualification like LICQ, Slater, MFCQ) for any local optimum.
- **Sufficient** when the problem is **convex** and a constraint qualification holds (e.g., **Slater's**: there exists strictly feasible $\mathbf{x}$ with $g_i(\mathbf{x}) < 0$). Then KKT ⇔ globally optimal.
- For equality-only problems, KKT collapses to the classical **Lagrange multipliers** ($\nabla f = \sum_j \mu_j \nabla h_j$).

## Strong duality and the dual

Define the **dual function** $g(\boldsymbol{\lambda}, \boldsymbol{\mu}) = \inf_{\mathbf{x}} L(\mathbf{x}, \boldsymbol{\lambda}, \boldsymbol{\mu})$. The **dual problem** is $\max_{\boldsymbol{\lambda} \geq 0, \boldsymbol{\mu}} g(\boldsymbol{\lambda}, \boldsymbol{\mu})$.

- **Weak duality** always: dual optimum $\leq$ primal optimum.
- **Strong duality** (no gap) holds for convex problems satisfying Slater. KKT then witnesses both optimums simultaneously.

## Worked micro-example

Minimize $f(x, y) = x^2 + y^2$ subject to $x + y \geq 1$ (rewrite $g(x, y) = 1 - x - y \leq 0$).

Lagrangian: $L = x^2 + y^2 + \lambda(1 - x - y)$. Stationarity gives $2x = \lambda$, $2y = \lambda$, so $x = y$. Plug into the constraint $x + y = 1$ (active because $\lambda > 0$ by stationarity): $x = y = 1/2$, $\lambda = 1$. Complementary slackness, dual feasibility, primal feasibility all satisfied. Optimum: $f^* = 1/2$.

## Common pitfalls

- **Sign convention:** $g_i \leq 0$ matched with $\lambda_i \geq 0$. Flip signs and the dual feasibility flips too.
- **Missing constraint qualification.** Without LICQ/Slater/etc., KKT may fail to hold at a true optimum (e.g., cusp constraints).
- **Equality constraints have unsigned multipliers $\mu_j$** — they can be negative.
- **Inactive constraints don't influence the solution** but appear in the KKT system with $\lambda_i = 0$ — don't drop them prematurely.

## Applications in ML

- **SVM** dual derivation: KKT gives support vectors as those points with $\lambda_i > 0$.
- **Constrained probability simplex problems** (sum-to-one) use equality multipliers.
- **Sparse coding / Lasso** subdifferential conditions are the convex analogue when $\ell_1$ is non-smooth.

## Applications in quant

- **Mean-variance with constraints** (no-shorting $w_i \geq 0$, sector caps): KKT identifies which constraints bind at the optimal portfolio.
- **Constrained execution** problems (Almgren-Chriss with limits) use KKT for closed-form schedules.

## See also

- [Convexity](./convexity.md)
- [Gradients](../calculus/gradients.md)
- [Mean-variance](../../quant/portfolio-theory/mean-variance.md)
- [SVM](../../ml/supervised/svm.md)
