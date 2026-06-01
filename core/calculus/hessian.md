---
id: hessian
title: Hessian
domain: core/calculus
tags: [identity]
prerequisites: [gradients, jacobian]
used_by: []
difficulty: 2
status: draft
notebook: hessian.ipynb
---

# Hessian

## TL;DR

The Hessian $H_f$ is the square matrix of second partial derivatives of a scalar function — it tells you the local curvature and powers second-order optimization (Newton's method).

## Definition

For $f: \mathbb{R}^n \to \mathbb{R}$ with continuous second partials,

$$ H_f(\mathbf{x}) = \begin{bmatrix}
\dfrac{\partial^2 f}{\partial x_1^2} & \cdots & \dfrac{\partial^2 f}{\partial x_1 \partial x_n} \\
\vdots & \ddots & \vdots \\
\dfrac{\partial^2 f}{\partial x_n \partial x_1} & \cdots & \dfrac{\partial^2 f}{\partial x_n^2}
\end{bmatrix} = J(\nabla f)(\mathbf{x}). $$

By **Clairaut's theorem**, $H_f$ is symmetric: $\partial^2 f / \partial x_i \partial x_j = \partial^2 f / \partial x_j \partial x_i$.

## Intuition

$H_f$ encodes the second-order Taylor expansion:

$$ f(\mathbf{x} + \mathbf{h}) \approx f(\mathbf{x}) + \nabla f(\mathbf{x})^\top \mathbf{h} + \tfrac{1}{2} \mathbf{h}^\top H_f(\mathbf{x}) \mathbf{h}. $$

Eigenvalues of $H$ are curvatures along its eigenvector directions. Large positive eigenvalue ⇒ steep bowl in that direction; large negative ⇒ steep hill; mixed signs ⇒ saddle.

## Key formulas

- **Newton's update:** $\mathbf{x}_{k+1} = \mathbf{x}_k - H_f(\mathbf{x}_k)^{-1} \nabla f(\mathbf{x}_k)$ — quadratic convergence near a non-degenerate minimum.
- **Gauss-Newton approximation:** for least-squares $f = \tfrac{1}{2} \|\mathbf{r}(\mathbf{x})\|^2$, $H \approx J_{\mathbf{r}}^\top J_{\mathbf{r}}$.
- **Condition number** $\kappa(H) = \lambda_{\max}/\lambda_{\min}$ governs gradient-descent convergence rate; ill-conditioned $H$ (large $\kappa$) makes GD zig-zag.

## Properties & identities

- **Symmetric** under standard smoothness assumptions.
- **Second-order optimality** (sufficient): $\nabla f(\mathbf{x}^*) = 0$ and $H_f(\mathbf{x}^*) \succ 0$ ⇒ strict local minimum.
- **Classification of critical points by $H$ at the point:**
  - $H \succ 0$ (all eigenvalues > 0): local min
  - $H \prec 0$: local max
  - indefinite: saddle
  - singular: inconclusive (needs higher-order test)
- **Convexity of $f$** on a convex set $\iff H_f \succeq 0$ everywhere.

## Worked micro-example

$f(x, y) = x^2 + 3y^2 + 2xy$. Then $\nabla f = (2x+2y,\, 6y+2x)^\top$, and

$$ H_f = \begin{bmatrix} 2 & 2 \\ 2 & 6 \end{bmatrix}. $$

Eigenvalues are $4 \pm 2\sqrt{2} \approx \{1.17, 6.83\}$ — both positive, so $f$ is strictly convex, and the unique critical point at the origin is the global minimum. $\kappa(H) \approx 5.83$.

> See [companion notebook](./hessian.ipynb) for Newton vs GD on the Rosenbrock function.

## Common pitfalls

- **Storage / inversion cost.** $H$ has $\Theta(n^2)$ entries and $\Theta(n^3)$ inversion — infeasible for large neural nets. Use quasi-Newton (L-BFGS), Gauss-Newton, or Hessian-free methods.
- **Indefinite Hessian** breaks Newton's step (can move uphill). Damped/trust-region variants or modify eigenvalues to enforce positivity.
- **Symmetric in theory, asymmetric in finite-difference estimates** — symmetrize via $(H + H^\top)/2$.
- **Numerical second derivatives** amplify noise: use central differences with $h \approx \varepsilon_{\text{mach}}^{1/3}$ (not $\sqrt{\varepsilon}$ as for first derivatives).

## Applications in ML

- **Second-order optimizers** (Newton, BFGS, Hessian-free CG).
- **Curvature for generalization:** flat minima (small Hessian eigenvalues) often generalize better.
- **Laplace approximation:** posterior $\approx \mathcal{N}(\hat{\boldsymbol{\theta}}, H_{\text{loss}}^{-1})$ at MAP.
- **Influence functions** use $H^{-1}$ to estimate the effect of removing a training point.

## Applications in quant

- **Convex risk minimization** in portfolio construction uses Newton-style solvers.
- **Bond convexity** = second derivative of price w.r.t. yield — a 1D Hessian by another name.
- **Gamma** (option Greek) is the 1D Hessian of price w.r.t. underlier.

## See also

- [Gradients](./gradients.md)
- [Jacobian](./jacobian.md)
- [Taylor series](./taylor-series.md)
- [Convexity](../optimization/convexity.md)
