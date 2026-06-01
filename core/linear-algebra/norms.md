---
id: norms
title: Vector Norms
domain: core/linear-algebra
tags: [inequality]
prerequisites: [vectors]
used_by: []
difficulty: 1
status: draft
notebook: norms.ipynb
---

# Vector Norms

## TL;DR

A norm $\lVert \cdot \rVert$ measures the "size" of a vector; different norms emphasize different notions of size (Euclidean length, absolute sum, max coordinate).

## Definition

A function $\lVert \cdot \rVert : \mathbb{R}^n \to \mathbb{R}_{\geq 0}$ is a **norm** iff for all $\mathbf{x}, \mathbf{y}$ and $\alpha \in \mathbb{R}$:

1. **Non-negativity:** $\lVert \mathbf{x} \rVert \geq 0$, with equality $\iff \mathbf{x} = \mathbf{0}$.
2. **Absolute homogeneity:** $\lVert \alpha \mathbf{x} \rVert = |\alpha| \lVert \mathbf{x} \rVert$.
3. **Triangle inequality:** $\lVert \mathbf{x} + \mathbf{y} \rVert \leq \lVert \mathbf{x} \rVert + \lVert \mathbf{y} \rVert$.

## Intuition

A norm assigns each vector a single non-negative number representing its magnitude. The **unit ball** $\{\mathbf{x} : \lVert \mathbf{x} \rVert \leq 1\}$ visualizes the geometry — see the companion notebook.

## Key formulas

The **$\ell_p$ norm** family for $p \geq 1$:

$$ \lVert \mathbf{x} \rVert_p = \left( \sum_{i=1}^n |x_i|^p \right)^{1/p} $$

Special cases:

| Norm        | Formula                                       | Shape of unit ball in $\mathbb{R}^2$ |
| ----------- | --------------------------------------------- | ------------------------------------ |
| $\ell_1$    | $\sum_i |x_i|$                                | diamond / rotated square             |
| $\ell_2$    | $\sqrt{\sum_i x_i^2}$                         | circle                               |
| $\ell_\infty$ | $\max_i |x_i|$                              | square                               |

The **$\ell_0$ "norm"** $\lVert \mathbf{x} \rVert_0 = |\{i : x_i \neq 0\}|$ counts nonzeros — not actually a norm (fails homogeneity), but ubiquitous in sparsity literature.

## Properties & identities

- **Equivalence of norms** in finite dimensions: for any two norms there exist $c_1, c_2 > 0$ with $c_1 \lVert \mathbf{x} \rVert_a \leq \lVert \mathbf{x} \rVert_b \leq c_2 \lVert \mathbf{x} \rVert_a$. So convergence in one $\equiv$ convergence in another.
- **Cauchy-Schwarz:** $|\mathbf{x}^\top \mathbf{y}| \leq \lVert \mathbf{x} \rVert_2 \lVert \mathbf{y} \rVert_2$.
- **Hölder's inequality:** $|\mathbf{x}^\top \mathbf{y}| \leq \lVert \mathbf{x} \rVert_p \lVert \mathbf{y} \rVert_q$ where $1/p + 1/q = 1$.
- **Norm ordering** (for fixed $\mathbf{x}$): $\lVert \mathbf{x} \rVert_\infty \leq \lVert \mathbf{x} \rVert_2 \leq \lVert \mathbf{x} \rVert_1 \leq \sqrt{n}\, \lVert \mathbf{x} \rVert_2 \leq n \lVert \mathbf{x} \rVert_\infty$.

## Worked micro-example

For $\mathbf{x} = (3, -4)^\top$:

- $\lVert \mathbf{x} \rVert_1 = 3 + 4 = 7$
- $\lVert \mathbf{x} \rVert_2 = \sqrt{9 + 16} = 5$
- $\lVert \mathbf{x} \rVert_\infty = 4$

Notice $\lVert \mathbf{x} \rVert_\infty < \lVert \mathbf{x} \rVert_2 < \lVert \mathbf{x} \rVert_1$, consistent with the ordering above.

## Common pitfalls

- **$\ell_0$ is not a norm.** Optimization with it is NP-hard; $\ell_1$ is its convex relaxation.
- **NumPy default:** `np.linalg.norm(x)` returns the $\ell_2$ norm. For others pass `ord=1`, `ord=np.inf`, etc.
- **Don't confuse vector and matrix norms** — `np.linalg.norm` on a 2D array defaults to the Frobenius norm, not $\ell_2$.

## Applications in ML

- **Regularization:** $\ell_2$ (ridge) shrinks; $\ell_1$ (lasso) induces sparsity. The unit-ball geometry (see notebook) explains *why* $\ell_1$ produces zeros.
- **Distance metrics:** $\ell_2$ for k-NN with continuous features; $\ell_1$ (Manhattan) is more robust to outliers.
- **Gradient clipping:** typically by $\ell_2$ norm to stabilize training.

## Applications in quant

- **Risk constraints:** $\lVert \mathbf{w} \rVert_1 \leq L$ caps total leverage; $\lVert \mathbf{w} \rVert_\infty \leq c$ caps single-position concentration.
- **Tracking error** is an $\ell_2$ deviation from a benchmark weight vector.

## See also

- [Vectors](./vectors.md)
- SVD (forthcoming) — uses the $\ell_2$ norm to define matrix rank approximation.

## References

- Boyd & Vandenberghe, *Convex Optimization*, §A.1.
