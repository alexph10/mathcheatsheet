---
id: gradients
title: Gradients
domain: core/calculus
tags: []
prerequisites: [vectors]
used_by: []
difficulty: 1
status: draft
notebook: gradients.ipynb
---

# Gradients

## TL;DR

The gradient $\nabla f(\mathbf{x})$ of a scalar function is the vector of its partial derivatives — pointing in the direction of steepest ascent, with magnitude equal to the maximum rate of change.

## Definition

For $f: \mathbb{R}^n \to \mathbb{R}$ differentiable at $\mathbf{x}$,

$$ \nabla f(\mathbf{x}) = \begin{bmatrix} \dfrac{\partial f}{\partial x_1} \\[4pt] \vdots \\[2pt] \dfrac{\partial f}{\partial x_n} \end{bmatrix} \in \mathbb{R}^n. $$

The **directional derivative** along unit vector $\mathbf{u}$ is

$$ D_{\mathbf{u}} f(\mathbf{x}) = \nabla f(\mathbf{x})^\top \mathbf{u}. $$

## Intuition

Two equivalent ways to read $\nabla f$:

1. **Best linear approximation:** near $\mathbf{x}_0$, $f(\mathbf{x}) \approx f(\mathbf{x}_0) + \nabla f(\mathbf{x}_0)^\top (\mathbf{x} - \mathbf{x}_0)$. The gradient is the slope vector of that tangent plane.
2. **Steepest ascent:** of all unit directions, $\mathbf{u} = \nabla f / \lVert \nabla f \rVert$ maximizes $D_{\mathbf{u}} f$. So $-\nabla f$ is steepest *descent* — the foundation of gradient-based optimization.

The gradient is always **orthogonal to level sets** $\{ \mathbf{x} : f(\mathbf{x}) = c \}$.

## Key formulas

Common gradient identities for $\mathbf{x}, \mathbf{a} \in \mathbb{R}^n$, $A \in \mathbb{R}^{n \times n}$:

| $f(\mathbf{x})$              | $\nabla f$                              |
| ---------------------------- | --------------------------------------- |
| $\mathbf{a}^\top \mathbf{x}$ | $\mathbf{a}$                            |
| $\mathbf{x}^\top \mathbf{x}$ | $2\mathbf{x}$                           |
| $\mathbf{x}^\top A \mathbf{x}$ (general $A$) | $(A + A^\top)\mathbf{x}$  |
| $\mathbf{x}^\top A \mathbf{x}$ (symmetric $A$) | $2 A \mathbf{x}$        |
| $\lVert \mathbf{x} \rVert_2$ | $\mathbf{x} / \lVert \mathbf{x} \rVert_2$ (for $\mathbf{x} \neq 0$) |
| $\lVert \mathbf{x} - \mathbf{a} \rVert_2^2$ | $2(\mathbf{x} - \mathbf{a})$ |
| $\log \mathbf{a}^\top \mathbf{x}$ | $\mathbf{a} / (\mathbf{a}^\top \mathbf{x})$ |

**Chain rule** (scalar-valued composition): if $f(\mathbf{x}) = g(h(\mathbf{x}))$ with $g: \mathbb{R} \to \mathbb{R}$ and $h: \mathbb{R}^n \to \mathbb{R}$, then

$$ \nabla f(\mathbf{x}) = g'(h(\mathbf{x})) \, \nabla h(\mathbf{x}). $$

For vector-to-vector composition, use the Jacobian (forthcoming sheet).

## Properties & identities

- **Linearity:** $\nabla (\alpha f + \beta g) = \alpha \nabla f + \beta \nabla g$.
- **Product rule:** $\nabla (fg) = g \nabla f + f \nabla g$.
- **First-order optimality:** at an interior local extremum of a differentiable $f$, $\nabla f(\mathbf{x}^*) = \mathbf{0}$.
- **Convex $f$:** $\nabla f(\mathbf{x}^*) = \mathbf{0}$ is both necessary and sufficient for a global minimum.

## Worked micro-example

Let $f(\mathbf{x}) = x_1^2 + 3 x_1 x_2 + 2 x_2^2$. Then

$$ \frac{\partial f}{\partial x_1} = 2 x_1 + 3 x_2, \qquad \frac{\partial f}{\partial x_2} = 3 x_1 + 4 x_2. $$

So $\nabla f(\mathbf{x}) = (2 x_1 + 3 x_2,\, 3 x_1 + 4 x_2)^\top$. At $\mathbf{x} = (1, 1)^\top$: $\nabla f = (5, 7)^\top$. The steepest ascent direction at that point is $(5, 7)/\sqrt{74}$.

In matrix form, $f(\mathbf{x}) = \mathbf{x}^\top A \mathbf{x}$ with $A = \begin{bmatrix}1 & 1.5 \\ 1.5 & 2\end{bmatrix}$, giving $\nabla f = 2 A \mathbf{x} = (5, 7)^\top$. ✓

> See [companion notebook](./gradients.ipynb) for gradient-field visualization and a hand-rolled gradient descent.

## Common pitfalls

- **Shape conventions:** treat $\nabla f$ as a column vector by default. The "denominator layout" used in some ML textbooks puts it as a row — be consistent within a derivation.
- **Non-differentiable points:** $f(x) = |x|$ has no gradient at $0$. Use subgradients for $\ell_1$-style objectives.
- **Numerical gradients** via finite differences are useful for checking but use **central differences** $(f(x+h) - f(x-h))/(2h)$, not forward differences, and pick $h$ near $\sqrt{\varepsilon_{\text{machine}}}$.
- **Gradient $\neq$ descent direction in ill-conditioned problems** — the steepest-descent step can zig-zag badly; preconditioned / second-order methods (Newton) fix this.

## Applications in ML

- **Gradient descent and all its variants** (SGD, Adam, etc.) drive nearly all model training.
- **Backpropagation** is the chain rule applied to a computational graph of vector-to-vector composites.
- **Adversarial examples** use $\nabla_{\mathbf{x}}$ (input gradient) rather than the usual $\nabla_{\boldsymbol{\theta}}$ (parameter gradient).

## Applications in quant

- **Greeks** (Delta, Gamma, Vega, ...) are partial derivatives of option price with respect to inputs — gradients in the parameter space.
- **Sensitivity analysis** of portfolio P&L to factor exposures uses the gradient $\nabla_{\boldsymbol{\beta}} \text{PnL}$.

## See also

- [Vectors](../linear-algebra/vectors.md)
- [Chain rule](./chain-rule.md)
- Jacobian (forthcoming)
- Hessian (forthcoming)

## References

- Boyd & Vandenberghe, *Convex Optimization*, §A.4.
- Petersen & Pedersen, *The Matrix Cookbook*, §2.4 — exhaustive gradient identity table.
