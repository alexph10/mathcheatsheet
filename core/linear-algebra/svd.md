---
id: svd
title: Singular Value Decomposition (SVD)
domain: core/linear-algebra
tags: [matrix-factorization, dimensionality-reduction]
prerequisites: [vectors, norms]
used_by: []
difficulty: 2
status: draft
notebook: svd.ipynb
---

# Singular Value Decomposition (SVD)

## TL;DR

Every real $m \times n$ matrix factors as $A = U \Sigma V^\top$ where $U, V$ are orthogonal and $\Sigma$ is non-negative diagonal — exposing the matrix's "axes of action" and their scales.

## Definition

For any $A \in \mathbb{R}^{m \times n}$ of rank $r$, there exist orthogonal $U \in \mathbb{R}^{m \times m}$, $V \in \mathbb{R}^{n \times n}$, and $\Sigma \in \mathbb{R}^{m \times n}$ with $\Sigma_{ii} = \sigma_i \geq 0$ (zero elsewhere) such that

$$ A = U \Sigma V^\top, \qquad \sigma_1 \geq \sigma_2 \geq \cdots \geq \sigma_r > 0 = \sigma_{r+1} = \cdots $$

- Columns of $V$: right singular vectors (orthonormal basis of $\mathbb{R}^n$).
- Columns of $U$: left singular vectors (orthonormal basis of $\mathbb{R}^m$).
- $\sigma_i$: singular values, the "stretch factors".

The **economy SVD** drops zero blocks: $A = U_r \Sigma_r V_r^\top$ with $U_r \in \mathbb{R}^{m \times r}$, $\Sigma_r \in \mathbb{R}^{r \times r}$, $V_r \in \mathbb{R}^{n \times r}$.

## Intuition

Any linear map $A: \mathbb{R}^n \to \mathbb{R}^m$ does exactly three things in sequence:

1. **Rotate** the input via $V^\top$ to a "canonical" coordinate frame.
2. **Stretch** each canonical axis by $\sigma_i$ via $\Sigma$.
3. **Rotate** into the output frame via $U$.

The singular values measure how much each independent direction is amplified. The unit sphere in $\mathbb{R}^n$ becomes an ellipsoid in $\mathbb{R}^m$ with semi-axis lengths $\sigma_i$.

## Key formulas

- **Rank:** $\text{rank}(A) = $ number of nonzero $\sigma_i$.
- **Frobenius norm:** $\lVert A \rVert_F = \sqrt{\sum_i \sigma_i^2}$.
- **Operator (spectral) norm:** $\lVert A \rVert_2 = \sigma_1$.
- **Condition number:** $\kappa_2(A) = \sigma_1 / \sigma_r$.
- **Pseudoinverse:** $A^+ = V \Sigma^+ U^\top$ with $\Sigma^+_{ii} = 1/\sigma_i$ for $\sigma_i > 0$, else $0$.
- **Best rank-$k$ approximation** (Eckart–Young):

$$ A_k = \sum_{i=1}^k \sigma_i \mathbf{u}_i \mathbf{v}_i^\top, \qquad \lVert A - A_k \rVert_F^2 = \sum_{i=k+1}^r \sigma_i^2 $$

minimizes Frobenius (and spectral) error over all rank-$k$ matrices.

## Properties & identities

- $A^\top A = V \Sigma^\top \Sigma V^\top$ — eigenvectors of $A^\top A$ are right singular vectors; eigenvalues are $\sigma_i^2$.
- $A A^\top = U \Sigma \Sigma^\top U^\top$ — same for left singular vectors.
- SVD exists for **every** real (or complex) matrix; eigendecomposition does not.
- $\det(A) = \prod_i \sigma_i$ when $A$ is square (up to sign from orientations).

## Worked micro-example

For

$$ A = \begin{bmatrix} 3 & 0 \\ 4 & 5 \end{bmatrix}, $$

compute $A^\top A = \begin{bmatrix} 25 & 20 \\ 20 & 25 \end{bmatrix}$, eigenvalues $\lambda = 45, 5$, so $\sigma_1 = \sqrt{45} \approx 6.708$, $\sigma_2 = \sqrt{5} \approx 2.236$. Hence $\lVert A \rVert_2 \approx 6.708$, $\lVert A \rVert_F = \sqrt{50} \approx 7.071$, $\kappa_2(A) = 3$.

> See [companion notebook](./svd.ipynb) for the full decomposition and a low-rank image approximation demo.

## Common pitfalls

- **Sign ambiguity:** singular vectors are unique only up to sign (and rotation within equal-singular-value subspaces). Don't compare $U, V$ entry-by-entry across implementations.
- **Full vs economy:** `np.linalg.svd(A)` returns full $U$; use `full_matrices=False` for the economy form to save memory when $m \gg n$ or vice versa.
- **Tiny singular values vs zero** — for rank determination use a tolerance like $\max(m,n) \cdot \sigma_1 \cdot \varepsilon_{\text{machine}}$.
- **SVD ≠ eigendecomposition** even when $A$ is square: they coincide only when $A$ is symmetric positive semidefinite.

## Applications in ML

- **PCA** is SVD of the centered data matrix; principal components = right singular vectors.
- **Low-rank approximation** for compression (e.g., embedding layers, image compression).
- **Latent semantic analysis** factors term-document matrices.
- **Pseudoinverse** gives the minimum-norm least-squares solution to $A\mathbf{x} = \mathbf{b}$.

## Applications in quant

- **Factor models** decompose return covariance into a few dominant factors via SVD/PCA.
- **Risk model dimensionality reduction:** keep top-$k$ singular components to denoise covariance estimates.
- **Regime detection** via SVD of rolling return matrices.

## See also

- [Vectors](./vectors.md)
- [Vector norms](./norms.md)
- Eigendecomposition (forthcoming)

## References

- Trefethen & Bau, *Numerical Linear Algebra*, Lectures 4–5.
- Strang, *Introduction to Linear Algebra*, Ch. 7.
