---
id: vectors
title: Vectors
domain: core/linear-algebra
tags: []
prerequisites: []
used_by: []
difficulty: 1
status: draft
---

# Vectors

## TL;DR

A vector is an ordered tuple of $n$ real numbers; equivalently, an arrow with magnitude and direction in $\mathbb{R}^n$.

## Definition

A vector $\mathbf{x} \in \mathbb{R}^n$ is an element of the $n$-dimensional real vector space:

$$ \mathbf{x} = \begin{bmatrix} x_1 \\ x_2 \\ \vdots \\ x_n \end{bmatrix}, \quad x_i \in \mathbb{R}. $$

Vectors support two operations satisfying the eight vector-space axioms:

- **Addition:** $(\mathbf{x} + \mathbf{y})_i = x_i + y_i$
- **Scalar multiplication:** $(\alpha \mathbf{x})_i = \alpha x_i$

## Intuition

Two complementary mental models — use whichever helps:

1. **Geometric** — an arrow from the origin to a point. Addition is tip-to-tail; scaling stretches/flips.
2. **Algebraic** — a list of coordinates. Addition is componentwise; scaling multiplies each component.

In ML, a single data point is usually a vector of feature values. In quant, a portfolio's weights across $n$ assets is a vector in $\mathbb{R}^n$.

## Key formulas

- **Dot product:** $\mathbf{x} \cdot \mathbf{y} = \sum_{i=1}^n x_i y_i = \mathbf{x}^\top \mathbf{y}$
- **Magnitude (Euclidean):** $\lVert \mathbf{x} \rVert_2 = \sqrt{\mathbf{x}^\top \mathbf{x}}$
- **Angle:** $\cos\theta = \dfrac{\mathbf{x}^\top \mathbf{y}}{\lVert \mathbf{x} \rVert_2 \lVert \mathbf{y} \rVert_2}$
- **Unit vector:** $\hat{\mathbf{x}} = \mathbf{x} / \lVert \mathbf{x} \rVert_2$

## Properties & identities

- Addition is commutative and associative.
- The zero vector $\mathbf{0}$ is the additive identity.
- $\mathbf{x} \cdot \mathbf{y} = \mathbf{y} \cdot \mathbf{x}$ (symmetry).
- $\mathbf{x} \cdot \mathbf{y} = 0 \iff \mathbf{x} \perp \mathbf{y}$ (orthogonality).

## Worked micro-example

Let $\mathbf{x} = (3, 4)^\top$ and $\mathbf{y} = (1, 2)^\top$.

- $\mathbf{x} + \mathbf{y} = (4, 6)^\top$
- $\mathbf{x}^\top \mathbf{y} = 3\cdot 1 + 4\cdot 2 = 11$
- $\lVert \mathbf{x} \rVert_2 = \sqrt{9 + 16} = 5$

## Common pitfalls

- **Row vs column:** by default a vector is a column. $\mathbf{x}^\top \mathbf{y}$ is a scalar; $\mathbf{x} \mathbf{y}^\top$ is an $n \times n$ matrix (outer product).
- **Element-wise vs dot product:** $\mathbf{x} \odot \mathbf{y}$ (Hadamard) is componentwise multiplication — a vector — not a scalar.
- **Dimension mismatch** silently breaks broadcasting in NumPy; check shapes.

## Applications in ML

Feature vectors, embeddings, weight vectors, gradients — essentially every ML object is a vector or a collection of vectors.

## Applications in quant

Portfolio weight vectors, asset return vectors, factor loadings.

## See also

- Norms (forthcoming)
- Inner products and orthogonality (forthcoming)
- Matrix operations (forthcoming)
