---
id: matrix-calculus
title: Matrix Calculus
domain: core/linear-algebra
tags: [identity]
prerequisites: [vectors, gradients, jacobian]
used_by: []
difficulty: 2
status: draft
notebook: matrix-calculus.ipynb
---

# Matrix Calculus

## TL;DR

A bookkeeping discipline for derivatives whose inputs and/or outputs are vectors or matrices — pick a layout convention, learn a handful of identities, and the rest is the ordinary chain rule.

## Definition

For $f: \mathbb{R}^n \to \mathbb{R}^m$, the **Jacobian** $J \in \mathbb{R}^{m \times n}$ collects all partials:

$$ J_{ij} = \frac{\partial f_i}{\partial x_j}. $$

When $m = 1$, the **gradient** $\nabla f \in \mathbb{R}^n$ is the (transpose of the) Jacobian. For matrix-valued inputs $X \in \mathbb{R}^{p \times q}$ and a scalar $f(X)$, the derivative $\partial f / \partial X$ is the $p \times q$ matrix of partials $\partial f / \partial X_{ij}$.

## Layout conventions

Two competing conventions — pick one and stick with it:

| Convention | Shape of $\partial y / \partial x$ for $y \in \mathbb{R}^m$, $x \in \mathbb{R}^n$ |
| ---------- | --------------------------------------------------------------------------------- |
| **Numerator layout** (Jacobian) | $m \times n$ — rows index output, columns index input. |
| **Denominator layout** (gradient) | $n \times m$ — rows index input, columns index output. |

This sheet uses **numerator layout**: $\partial y / \partial x$ is the Jacobian. The gradient of a scalar is then a row vector $\partial f / \partial x \in \mathbb{R}^{1 \times n}$; we write $\nabla f \in \mathbb{R}^n$ for its column-vector transpose, which is what optimizers consume.

## Intuition

Think of every formula as a small linear-algebraic chain rule. The Jacobian of a composition is a product of Jacobians, so the only real skill is recognizing the "shape" of the answer (it must contract correctly with the input perturbation $dx$). The **differential trick** — write $df = \text{tr}(G^\top dX)$ and read off $\partial f / \partial X = G$ — sidesteps most index gymnastics.

## Key identities

Scalar-by-vector ($x, a \in \mathbb{R}^n$, $A \in \mathbb{R}^{n \times n}$):

$$ \frac{\partial (a^\top x)}{\partial x} = a^\top, \qquad \frac{\partial (x^\top A x)}{\partial x} = x^\top (A + A^\top). $$

Vector-by-vector ($A \in \mathbb{R}^{m \times n}$ constant):

$$ \frac{\partial (A x)}{\partial x} = A, \qquad \frac{\partial \lVert x \rVert_2^2}{\partial x} = 2 x^\top. $$

Scalar-by-matrix (with $X \in \mathbb{R}^{p \times q}$, $A$ conformable, $X$ square invertible where needed):

| $f(X)$ | $\partial f / \partial X$ |
| ------ | ------------------------- |
| $\text{tr}(AX)$ | $A^\top$ |
| $\text{tr}(X^\top A)$ | $A$ |
| $\text{tr}(X^\top A X)$ | $(A + A^\top) X$ |
| $\text{tr}(X A X^\top)$ | $X (A + A^\top)$ |
| $\log \lvert X \rvert$ (with $X$ SPD or invertible) | $X^{-\top}$ |
| $\lvert X \rvert$ | $\lvert X \rvert \, X^{-\top}$ |
| $\lVert X \rVert_F^2 = \text{tr}(X^\top X)$ | $2 X$ |

Inverse derivative (matrix-by-matrix; useful inside larger expressions):

$$ d(X^{-1}) = -X^{-1} (dX) X^{-1}. $$

## Chain rule in matrix form

If $z = g(y)$ and $y = f(x)$ with Jacobians $J_g, J_f$ in numerator layout, then

$$ \frac{\partial z}{\partial x} = J_g(y) \, J_f(x). $$

For a scalar loss $L$ flowing through an affine layer $y = Wx + b$:

$$ \frac{\partial L}{\partial W} = \frac{\partial L}{\partial y} \, x^\top, \qquad \frac{\partial L}{\partial b} = \frac{\partial L}{\partial y}, \qquad \frac{\partial L}{\partial x} = W^\top \frac{\partial L}{\partial y}. $$

These three lines underpin every fully-connected layer in [backprop](../../ml/deep-learning/backpropagation.md).

## Differential trick — derivation pattern

To find $\partial f / \partial X$ for a scalar $f(X)$:

1. Compute the differential $df$ as a linear function of $dX$, using $d(AB) = (dA)B + A(dB)$, $d(X^{-1}) = -X^{-1} dX X^{-1}$, $d \log \lvert X \rvert = \text{tr}(X^{-1} dX)$, etc.
2. Cyclically rearrange under the trace so $df = \text{tr}(G^\top \, dX)$.
3. Read off $\partial f / \partial X = G$.

Example: $f(X) = \log \lvert X \rvert$. Then $df = \text{tr}(X^{-1} dX) = \text{tr}((X^{-\top})^\top dX)$, so $\partial f / \partial X = X^{-\top}$.

## Worked micro-example

Let $f(x) = x^\top A x$ with $A = \begin{bmatrix} 2 & 1 \\ 1 & 3 \end{bmatrix}$ and $x = (1, 2)^\top$.

$$ \nabla f(x) = (A + A^\top) x = \begin{bmatrix} 4 & 2 \\ 2 & 6 \end{bmatrix} \begin{bmatrix} 1 \\ 2 \end{bmatrix} = \begin{bmatrix} 8 \\ 14 \end{bmatrix}. $$

Check: $f(x) = 2(1)^2 + 2(1)(2)(1) + 3(2)^2 = 2 + 4 + 12 = 18$, and a tiny perturbation $x + \varepsilon e_1$ gives $\Delta f \approx 8\varepsilon$, matching the first gradient entry.

> See [companion notebook](./matrix-calculus.ipynb) for SymPy-verified identities and a finite-difference sanity check.

## Common pitfalls

- **Layout drift** — mixing numerator and denominator layouts mid-derivation flips transposes. Pick one at the top and label every Jacobian's shape.
- **Quadratic forms with non-symmetric $A$** — many references silently assume $A = A^\top$. The general answer is $(A + A^\top)x$, not $2Ax$.
- **Treating $X$ and $X^\top$ as independent** when computing $\partial / \partial X$ of expressions like $\text{tr}(X^\top A X)$ — they're not; both occurrences must be differentiated.
- **Forgetting the trace trick's conjugate** — if you derive $df = \text{tr}(G \, dX)$ (no transpose), then $\partial f / \partial X = G^\top$, not $G$.
- **Sign on inverse derivative** — the minus in $d(X^{-1}) = -X^{-1}(dX)X^{-1}$ is responsible for most sign bugs in Gaussian MLEs.

## Applications in ML

- **Backprop** through every layer reduces to applying these identities to compositions of affine maps and elementwise nonlinearities. See [backpropagation](../../ml/deep-learning/backpropagation.md).
- **Gaussian MLE / EM** — derivatives w.r.t. covariance use $\partial \log \lvert \Sigma \rvert / \partial \Sigma = \Sigma^{-1}$ and $\partial \text{tr}(\Sigma^{-1} S)/\partial \Sigma = -\Sigma^{-1} S \Sigma^{-1}$.
- **Natural gradient / Fisher information** — derivations rely on matrix-by-matrix differentials.

## Applications in quant

- **Mean-variance optimization** — KKT conditions and analytical portfolio weights come from $\partial (w^\top \Sigma w) / \partial w = 2\Sigma w$. See [mean-variance](../../quant/portfolio-theory/mean-variance.md).
- **Kalman filter gain** — derivation uses $d(X^{-1})$ identities.
- **Greeks** — sensitivities of pricing functions to vector parameters (rates, vols) are matrix derivatives. See [greeks](../../quant/derivatives-pricing/greeks.md).

## See also

- [Gradients](../calculus/gradients.md)
- [Jacobian](../calculus/jacobian.md)
- [Chain rule](../calculus/chain-rule.md)
- [Hessian](../calculus/hessian.md)

## References

- Petersen & Pedersen, *The Matrix Cookbook* — exhaustive identity reference.
- Magnus & Neudecker, *Matrix Differential Calculus*, Ch. 5–6.
- Minka, "Old and New Matrix Algebra Useful for Statistics" (tech note).
