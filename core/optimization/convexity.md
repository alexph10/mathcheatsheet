---
id: convexity
title: Convexity
domain: core/optimization
tags: [convex]
prerequisites: [gradients]
used_by: []
difficulty: 2
status: draft
---

# Convexity

## TL;DR

A function is convex when its graph lies below every chord. The point: every local minimum is a global minimum, first-order conditions are sufficient (not just necessary), and there is a rich algorithmic + duality theory that makes the problem actually solvable.

## Definition

**Convex set.** $C \subseteq \mathbb{R}^n$ is convex iff for all $\mathbf{x}, \mathbf{y} \in C$ and $\theta \in [0, 1]$,

$$ \theta \mathbf{x} + (1 - \theta) \mathbf{y} \in C. $$

**Convex function.** $f: C \to \mathbb{R}$ on a convex domain $C$ is convex iff

$$ f(\theta \mathbf{x} + (1 - \theta) \mathbf{y}) \leq \theta f(\mathbf{x}) + (1 - \theta) f(\mathbf{y}) \quad \forall \mathbf{x}, \mathbf{y} \in C,\ \theta \in [0,1]. $$

**Strictly convex** if the inequality is strict for $\mathbf{x} \neq \mathbf{y}$ and $\theta \in (0, 1)$. **Strongly convex with parameter $m > 0$** if $f(\mathbf{x}) - \tfrac{m}{2}\lVert \mathbf{x} \rVert^2$ is convex; equivalently

$$ f(\mathbf{y}) \geq f(\mathbf{x}) + \nabla f(\mathbf{x})^\top (\mathbf{y} - \mathbf{x}) + \tfrac{m}{2} \lVert \mathbf{y} - \mathbf{x} \rVert^2. $$

**Concave:** $-f$ convex.

## Intuition

Convex functions are bowl-shaped: any chord sits above the surface. There are no "false" local minima to get trapped in, no exotic saddle structure: gradient = 0 already implies you're at the global optimum. That single fact is why convex programs are tractable while general nonlinear optimization isn't.

Strong convexity adds curvature uniformly from below: the function grows at least as fast as a quadratic, which gives *linear* convergence rates for gradient methods.

## Key formulas

For differentiable $f$ on a convex domain:

**First-order characterization.** $f$ is convex iff for all $\mathbf{x}, \mathbf{y}$:

$$ f(\mathbf{y}) \geq f(\mathbf{x}) + \nabla f(\mathbf{x})^\top (\mathbf{y} - \mathbf{x}). $$

The tangent hyperplane is a global underestimator.

**Second-order characterization.** For twice-differentiable $f$ on an open convex set:

$$ f \text{ convex} \iff \nabla^2 f(\mathbf{x}) \succeq 0 \ \forall \mathbf{x}; \qquad f \text{ strictly convex} \Leftarrow \nabla^2 f \succ 0. $$

Strong convexity with parameter $m$: $\nabla^2 f(\mathbf{x}) \succeq m I$ everywhere.

**Jensen's inequality.** $f$ convex, $X$ a random variable in its domain:

$$ f(\mathbb{E}[X]) \leq \mathbb{E}[f(X)]. $$

(Reverse for concave.) Generalizes the chord inequality from two points to any distribution.

## Operations that preserve convexity

If $f, g$ are convex on $C$, then so are:

- **Nonneg combinations:** $\alpha f + \beta g$ for $\alpha, \beta \geq 0$.
- **Pointwise max:** $\max(f, g)$, and more generally $\sup_{i \in I} f_i$.
- **Affine composition:** $f(A \mathbf{x} + \mathbf{b})$.
- **Composition with nondecreasing convex outer:** $g \circ f$ if $g$ is convex and nondecreasing on the range of $f$.
- **Perspective:** $g(\mathbf{x}, t) = t f(\mathbf{x}/t)$ for $t > 0$.
- **Partial minimization:** $g(\mathbf{x}) = \inf_{\mathbf{y} \in C_y} f(\mathbf{x}, \mathbf{y})$ if $f$ is jointly convex in $(\mathbf{x}, \mathbf{y})$.

(Pointwise *min* does **not** preserve convexity in general.)

## Properties & identities

- **Local = global.** Any local minimum of a convex $f$ is a global minimum; the set of minimizers is convex.
- **First-order optimality.** Differentiable convex $f$: $\nabla f(\mathbf{x}^\star) = 0$ iff $\mathbf{x}^\star$ is a global minimizer.
- **Strict convexity ⇒ unique minimizer** (if one exists).
- **Strong convexity ⇒** unique minimizer + quadratic lower bound + linear convergence of gradient descent (see [gradient descent](./gradient-descent.md)).
- **Convex hull** $\operatorname{conv}(S)$ = smallest convex set containing $S$ = all finite convex combinations of points in $S$.
- **Epigraph** $\operatorname{epi}(f) = \{(\mathbf{x}, t) : f(\mathbf{x}) \leq t\}$ is a convex set iff $f$ is convex.
- **Separating hyperplane theorem:** two disjoint convex sets can be separated by a hyperplane — the foundation of duality and SVMs.

## Common convex examples

| Function | Domain | Convex? |
| -------- | ------ | ------- |
| $\mathbf{a}^\top \mathbf{x} + b$ | $\mathbb{R}^n$ | convex *and* concave (affine) |
| $\lVert \mathbf{x} \rVert$ (any norm) | $\mathbb{R}^n$ | convex |
| $e^{ax}$ | $\mathbb{R}$ | convex for all $a$ |
| $-\log x$ | $(0, \infty)$ | convex |
| $x \log x$ | $(0, \infty)$ | convex |
| $\mathbf{x}^\top A \mathbf{x}$ | $\mathbb{R}^n$ | convex iff $A \succeq 0$ |
| $\log \sum_i e^{x_i}$ (log-sum-exp) | $\mathbb{R}^n$ | convex |
| $\max_i x_i$ | $\mathbb{R}^n$ | convex |
| $-\log \det X$ | $\{X \succ 0\}$ | convex |

## Worked micro-example

Show $f(\mathbf{x}) = \tfrac{1}{2} \mathbf{x}^\top A \mathbf{x} - \mathbf{b}^\top \mathbf{x}$ with symmetric $A \succeq 0$ is convex and find its minimum.

Hessian: $\nabla^2 f = A \succeq 0$, so $f$ is convex (strongly convex with parameter $\lambda_{\min}(A)$ if $A \succ 0$). First-order optimality:

$$ \nabla f(\mathbf{x}^\star) = A \mathbf{x}^\star - \mathbf{b} = 0 \quad \Rightarrow \quad \mathbf{x}^\star = A^{-1} \mathbf{b} \quad (\text{when } A \succ 0). $$

By convexity, this critical point is the global minimum — no need to check second-order or compare with other points.

## Common pitfalls

- **"Convex on each coordinate" ≠ jointly convex.** $f(x, y) = xy$ is linear (and thus convex) in each variable separately but not jointly convex.
- **$\nabla^2 f \succeq 0$ only proves convexity on a *convex* domain.** Check the domain too.
- **Composition rules are directional.** $g(f(x))$ with $g$ convex requires monotonicity of $g$ matched to the convexity of $f$. E.g. $\log(\text{convex})$ is generally not concave.
- **Convexity is not preserved by minimization in general** — only by joint minimization over a single block of variables in a jointly convex objective.
- **Strict ≠ strong.** $f(x) = x^4$ is strictly convex but not strongly convex (Hessian vanishes at 0). This matters for convergence rates.
- **Empirical risk minimization** is convex when both the loss and the model are convex (e.g. logistic regression). Neural-network training is *not* convex; convex-optimization intuition is a rough guide, not a proof.

## Applications in ML

- **Convex losses:** squared error, hinge, logistic, cross-entropy (in the linear-model parameters).
- **Regularization:** $\ell_1$, $\ell_2$, nuclear norm — all convex penalties, preserving convexity of the objective.
- **SVMs** are quadratic programs (convex).
- **Maximum-entropy / logistic models** have convex negative log-likelihoods.
- Many **relaxations** of NP-hard problems (LASSO for sparse selection, SDP for clustering) are convex surrogates.

## Applications in quant

- **Mean-variance portfolio optimization** is a convex QP (subject to convex constraints).
- **Risk-parity** and **CVaR minimization** are convex programs.
- **Calibration of arbitrage-free vol surfaces** uses convexity constraints on prices.
- **Convex risk measures** (e.g. coherent risk measures) have duality reps that yield tractable stress tests.

## See also

- [Gradients](../calculus/gradients.md)
- [Gradient descent](./gradient-descent.md)

## References

- Boyd & Vandenberghe, *Convex Optimization*, Ch. 2–3.
- Rockafellar, *Convex Analysis* (the canonical reference).
- Nesterov, *Lectures on Convex Optimization*, Ch. 1–2.
