---
id: eigendecomposition
title: Eigendecomposition
domain: core/linear-algebra
tags: [eigen, decomposition]
prerequisites: [vectors]
used_by: []
difficulty: 2
status: draft
notebook: eigendecomposition.ipynb
---

# Eigendecomposition

## TL;DR

A square matrix $A$ acts on its eigenvectors by pure scaling: $A\mathbf{v} = \lambda \mathbf{v}$. When $A$ has a full set of independent eigenvectors, it diagonalizes as $A = P D P^{-1}$, turning matrix powers and exponentials into scalar arithmetic on the eigenvalues.

## Definition

Let $A \in \mathbb{R}^{n \times n}$. A nonzero $\mathbf{v} \in \mathbb{C}^n$ is an **eigenvector** with **eigenvalue** $\lambda \in \mathbb{C}$ iff

$$ A \mathbf{v} = \lambda \mathbf{v}, \qquad \mathbf{v} \neq \mathbf{0}. $$

Equivalently $\det(A - \lambda I) = 0$ — the roots of the **characteristic polynomial** $p_A(\lambda)$ are the eigenvalues (counted with algebraic multiplicity).

$A$ is **diagonalizable** iff it has $n$ linearly independent eigenvectors. Stacking them as columns of $P$ gives

$$ A = P D P^{-1}, \qquad D = \operatorname{diag}(\lambda_1, \ldots, \lambda_n). $$

**Spectral theorem (real symmetric case).** If $A = A^\top$, then $A$ is *orthogonally* diagonalizable: there exist an orthogonal $Q$ ($Q^\top Q = I$) and real diagonal $\Lambda$ with

$$ A = Q \Lambda Q^\top. $$

## Intuition

Eigenvectors are the directions $A$ leaves invariant — apply $A$ and you stay on the same line, only rescaled by $\lambda$. In the eigenbasis the action of $A$ is independent scaling along each axis. Repeated application becomes trivial:

$$ A^k = P D^k P^{-1}, \qquad e^{A} = P e^{D} P^{-1}, $$

with $D^k$ and $e^D$ just elementwise on the diagonal. This is why eigendecomposition controls long-run behavior of iterated linear systems and linear ODEs.

## Key formulas

- **Trace = sum of eigenvalues:** $\operatorname{tr}(A) = \sum_i \lambda_i$.
- **Determinant = product:** $\det(A) = \prod_i \lambda_i$.
- **Inverse:** if $A = P D P^{-1}$ and all $\lambda_i \neq 0$, then $A^{-1} = P D^{-1} P^{-1}$.
- **Spectral radius:** $\rho(A) = \max_i |\lambda_i|$; controls whether $A^k \to 0$.
- **Rayleigh quotient (symmetric $A$):** $\dfrac{\mathbf{x}^\top A \mathbf{x}}{\mathbf{x}^\top \mathbf{x}} \in [\lambda_{\min}, \lambda_{\max}]$, with extremes attained at the corresponding eigenvectors.
- **Symmetric $A$ is PSD** $\iff$ all $\lambda_i \geq 0$; **PD** $\iff$ all $\lambda_i > 0$.

## Properties & identities

- Eigenvalues of $A^\top$ equal those of $A$; eigenvalues of $A^{-1}$ are $1/\lambda_i$; eigenvalues of $A + cI$ are $\lambda_i + c$.
- Distinct eigenvalues $\Rightarrow$ linearly independent eigenvectors $\Rightarrow$ diagonalizable.
- For symmetric $A$, eigenvectors of distinct eigenvalues are orthogonal.
- **Relation to SVD:** for symmetric PSD $A$, eigendecomposition = SVD. In general, the singular values of $A$ are $\sqrt{\lambda_i(A^\top A)}$ and the right singular vectors are eigenvectors of $A^\top A$. See [SVD](./svd.md).
- **Similar matrices share eigenvalues:** $A$ and $S^{-1} A S$ have the same spectrum.

## Worked micro-example

For

$$ A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}, $$

$\det(A - \lambda I) = (2-\lambda)^2 - 1 = (\lambda - 1)(\lambda - 3)$, so $\lambda_1 = 3, \lambda_2 = 1$. Eigenvectors: $\mathbf{v}_1 = (1, 1)^\top/\sqrt{2}$, $\mathbf{v}_2 = (1, -1)^\top/\sqrt{2}$. Then with $Q = [\mathbf{v}_1\ \mathbf{v}_2]$ and $\Lambda = \operatorname{diag}(3, 1)$,

$$ A = Q \Lambda Q^\top, \quad \operatorname{tr}(A) = 4 = 3 + 1, \quad \det(A) = 3 = 3 \cdot 1. $$

> See [companion notebook](./eigendecomposition.ipynb) for invariant-direction visualizations and a power-iteration demo.

## Common pitfalls

- **Defective matrices** lack a full eigenbasis (e.g. $\begin{bmatrix}1 & 1 \\ 0 & 1\end{bmatrix}$ has $\lambda = 1$ with algebraic multiplicity 2 but only one eigenvector). They are *not* diagonalizable; use the Jordan form or SVD instead.
- **Complex eigenvalues** appear for real non-symmetric matrices (e.g. rotations). They come in conjugate pairs.
- **Numerical sensitivity:** eigenvalues of non-symmetric matrices can be wildly unstable under tiny perturbations (the *condition number of the eigenproblem* is large when $P$ is near-singular). Prefer SVD or Schur decomposition for numerics.
- **Eigendecomposition $\neq$ SVD** in general — only for symmetric PSD matrices. Don't substitute one for the other when computing norms or pseudoinverses of non-symmetric data.
- **Order of eigenvalues** returned by `np.linalg.eig` is *not* sorted; use `np.linalg.eigh` for symmetric matrices (returns sorted ascending, real eigenvalues).

## Applications in ML

- **PCA:** eigendecomposition of the sample covariance $\Sigma$; principal components = top eigenvectors.
- **Spectral clustering / graph Laplacian methods** use eigenvectors of $L = D - W$.
- **Hessian analysis** of loss landscapes — eigenvalues describe curvature (positive = local minimum, negative = saddle direction).
- **Markov chain stationary distributions** are left eigenvectors with eigenvalue 1 (see [Markov chains](../stochastic-processes/markov-chains.md)).

## Applications in quant

- **Factor models / PCA of returns** decompose covariance into eigen-portfolios.
- **Risk decomposition:** eigenvalues of the covariance matrix give variances of uncorrelated risk modes.
- **Mean-reverting linear dynamics:** eigenvalues of the dynamics matrix determine speeds of mean reversion and stability.

## See also

- [Vectors](./vectors.md)
- [SVD](./svd.md)
- [Markov chains](../stochastic-processes/markov-chains.md)

## References

- Trefethen & Bau, *Numerical Linear Algebra*, Lectures 24–28.
- Strang, *Introduction to Linear Algebra*, Ch. 6.
- Horn & Johnson, *Matrix Analysis*, Ch. 1.
