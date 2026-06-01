---
id: inner-products
title: Inner Products
domain: core/linear-algebra
tags: []
prerequisites: [vectors, norms]
used_by: []
difficulty: 1
status: draft
---

# Inner Products

## TL;DR

An inner product is a bilinear, symmetric, positive-definite "dot product" that gives a vector space the geometric notions of length, angle, and orthogonality.

## Definition

An **inner product** on a real vector space $V$ is a map $\langle \cdot, \cdot \rangle : V \times V \to \mathbb{R}$ satisfying, for all $x, y, z \in V$ and $\alpha \in \mathbb{R}$:

1. **Symmetry:** $\langle x, y \rangle = \langle y, x \rangle$.
2. **Bilinearity:** $\langle \alpha x + z, y \rangle = \alpha \langle x, y \rangle + \langle z, y \rangle$ (and similarly in the second slot).
3. **Positive definiteness:** $\langle x, x \rangle \geq 0$, with equality iff $x = 0$.

A vector space with an inner product is an **inner-product space**; when complete in the induced norm, a **Hilbert space**.

(Complex case: replace symmetry by conjugate symmetry $\langle x, y \rangle = \overline{\langle y, x \rangle}$, and bilinearity becomes sesquilinearity.)

## Intuition

The dot product on $\mathbb{R}^n$ measures how much two vectors "agree" in direction. A general inner product just lets you decide which directions are special (down-weighted, up-weighted, correlated) by inserting a positive-definite matrix $M$ in the middle. The geometry (lengths, angles) bends accordingly, but the algebra stays the same.

## Key formulas

**Standard dot product** on $\mathbb{R}^n$:

$$ \langle x, y \rangle = x^\top y = \sum_{i=1}^n x_i y_i. $$

**Weighted (Mahalanobis-like) inner product** with $M \in \mathbb{R}^{n \times n}$ symmetric positive definite:

$$ \langle x, y \rangle_M = x^\top M y. $$

Any inner product on $\mathbb{R}^n$ has this form for some SPD $M$ (its **Gram matrix** in the standard basis).

**Induced norm** and distance:

$$ \lVert x \rVert = \sqrt{\langle x, x \rangle}, \qquad d(x, y) = \lVert x - y \rVert. $$

**Cauchy–Schwarz inequality:**

$$ \lvert \langle x, y \rangle \rvert \leq \lVert x \rVert \, \lVert y \rVert, $$

with equality iff $x, y$ are linearly dependent.

**Angle** between nonzero vectors:

$$ \cos \theta = \frac{\langle x, y \rangle}{\lVert x \rVert \, \lVert y \rVert} \in [-1, 1]. $$

Vectors are **orthogonal** when $\langle x, y \rangle = 0$.

## Properties & identities

- **Parallelogram law** (characterizes inner-product norms):
  $$ \lVert x + y \rVert^2 + \lVert x - y \rVert^2 = 2\lVert x \rVert^2 + 2\lVert y \rVert^2. $$
- **Polarization identity** (recover the inner product from the norm):
  $$ \langle x, y \rangle = \tfrac{1}{4}\left( \lVert x + y \rVert^2 - \lVert x - y \rVert^2 \right). $$
- **Pythagoras:** if $\langle x, y \rangle = 0$, then $\lVert x + y \rVert^2 = \lVert x \rVert^2 + \lVert y \rVert^2$.
- **Orthogonal projection** of $y$ onto $\text{span}\{x\}$: $\dfrac{\langle x, y \rangle}{\langle x, x \rangle} x$.
- **Triangle inequality** follows from Cauchy–Schwarz.

## Gram–Schmidt (briefly)

Given linearly independent $v_1, \ldots, v_k$, construct an orthonormal basis $\{u_1, \ldots, u_k\}$:

$$ w_i = v_i - \sum_{j=1}^{i-1} \langle v_i, u_j \rangle \, u_j, \qquad u_i = \frac{w_i}{\lVert w_i \rVert}. $$

Numerically prefer **modified Gram–Schmidt** or a QR factorization; classical Gram–Schmidt loses orthogonality with finite precision.

## Worked micro-example

Take $x = (1, 2)^\top$, $y = (3, 1)^\top$ in $\mathbb{R}^2$ with the standard inner product:

$$ \langle x, y \rangle = 1\cdot 3 + 2 \cdot 1 = 5, \qquad \lVert x \rVert = \sqrt{5}, \quad \lVert y \rVert = \sqrt{10}. $$

So $\cos \theta = 5 / \sqrt{50} = 1/\sqrt{2}$, giving $\theta = 45°$.

Now switch to $M = \text{diag}(1, 4)$. Then $\langle x, y \rangle_M = 1\cdot 3 + 4 \cdot 2 \cdot 1 = 11$, $\lVert x \rVert_M = \sqrt{17}$, $\lVert y \rVert_M = \sqrt{13}$. The vectors are no longer at 45° — the weighting stretched the $y$-axis, changing the geometry.

## Common pitfalls

- **An arbitrary symmetric matrix is not an inner product** — $M$ must be **positive definite** (not just PSD), otherwise positive definiteness of $\langle \cdot, \cdot \rangle$ fails for vectors in the null space.
- **Not every norm comes from an inner product** — only those satisfying the parallelogram law. The $\ell^1$ and $\ell^\infty$ norms do not.
- **Confusing $\langle x, y \rangle$ with $\langle x, y \rangle_M$** — formulas for projection, angle, orthogonality must use the inner product you actually chose.
- **Complex case sign** — $\langle x, x \rangle$ is real because of conjugate symmetry; forgetting the conjugate gives complex "norms".

## Applications in ML

- **Kernel methods / SVMs / Gaussian processes** replace explicit inner products with a kernel $k(x, y) = \langle \varphi(x), \varphi(y) \rangle_{\mathcal{H}}$ in a (possibly infinite-dimensional) **reproducing kernel Hilbert space** (RKHS). See [SVM](../../ml/supervised/svm.md).
- **Mahalanobis distance** $d_M(x, y) = \sqrt{(x-y)^\top M (x-y)}$ is the metric induced by an inner product weighted by $M = \Sigma^{-1}$.
- **Embedding similarity** (cosine similarity) is the angle from an inner product on the embedding space.

## Applications in quant

- **Risk-weighted distances** use $M = \Sigma^{-1}$ where $\Sigma$ is the return covariance — the natural inner product on excess-return space.
- **Function-space methods** for PDE-based option pricing live in Hilbert spaces of square-integrable functions.

## See also

- [Vectors](./vectors.md)
- [Vector norms](./norms.md)
- [Covariance and correlation](../probability/covariance-correlation.md) — the angle interpretation of correlation comes from the inner product $\langle X, Y \rangle = \mathbb{E}[XY]$ on centered random variables.

## References

- Axler, *Linear Algebra Done Right*, Ch. 6.
- Trefethen & Bau, *Numerical Linear Algebra*, Lecture 2 (and Lectures 7–8 for QR).
