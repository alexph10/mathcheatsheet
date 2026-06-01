---
id: pca
title: Principal Component Analysis (PCA)
domain: ml/unsupervised
tags: [dimensionality-reduction, decomposition]
prerequisites: [svd, eigendecomposition, vectors]
used_by: []
difficulty: 2
status: draft
notebook: pca.ipynb
---

# Principal Component Analysis (PCA)

## TL;DR

Center the data, take the SVD of the centered matrix; the right singular vectors are orthonormal directions of maximum variance, and the squared singular values are the variances along them.

## Definition

Given data $X \in \mathbb{R}^{n \times d}$ (rows = observations), let $\tilde X = X - \mathbf{1}\bar{\mathbf{x}}^\top$ be the column-centered data. PCA seeks orthonormal directions $\mathbf{v}_1, \dots, \mathbf{v}_k \in \mathbb{R}^d$ that successively maximize the variance of projections:

$$ \mathbf{v}_1 = \arg\max_{\lVert\mathbf{v}\rVert=1} \operatorname{Var}(\tilde X \mathbf{v}), \qquad \mathbf{v}_j = \arg\max_{\lVert\mathbf{v}\rVert=1,\, \mathbf{v}\perp \mathbf{v}_{<j}} \operatorname{Var}(\tilde X \mathbf{v}). $$

Equivalently, $\mathbf{v}_j$ is the top-$j$ eigenvector of the sample covariance

$$ C = \frac{1}{n-1} \tilde X^\top \tilde X \in \mathbb{R}^{d \times d}. $$

## Intuition

Imagine an ellipsoidal point cloud in $\mathbb{R}^d$. PCA finds its principal axes — the longest direction first, then the longest perpendicular direction, and so on. Projecting onto the top $k$ axes throws away the thinnest directions, which carry the least variance and (under a Gaussian noise model) the most noise. PCA is a **lossy but optimal** linear compressor in mean-squared-error sense (Eckart–Young, via [SVD](../../core/linear-algebra/svd.md)).

## Key formulas

**Two equivalent routes.** With $\tilde X = U \Sigma V^\top$ (economy SVD), and $C = \tilde X^\top \tilde X / (n-1)$,

$$ C = V \left( \tfrac{1}{n-1}\Sigma^2 \right) V^\top, \qquad \text{eigenvalues } \lambda_j = \tfrac{\sigma_j^2}{n-1}. $$

The principal directions $\mathbf{v}_j$ are columns of $V$; the variance along the $j$-th axis is $\lambda_j$.

**Scores / projections** onto the first $k$ components:

$$ Z = \tilde X V_k = U_k \Sigma_k \in \mathbb{R}^{n \times k}. $$

**Rank-$k$ reconstruction** in the original space:

$$ \hat{\tilde X}_k = U_k \Sigma_k V_k^\top = \tilde X V_k V_k^\top. $$

**Explained variance ratio** for component $j$:

$$ \text{EVR}_j = \frac{\lambda_j}{\sum_{i=1}^{d} \lambda_i} = \frac{\sigma_j^2}{\sum_i \sigma_i^2}. $$

## Properties & identities

- $V$ is orthonormal: $V^\top V = I$. Components are uncorrelated.
- Total variance is preserved: $\sum_j \lambda_j = \operatorname{tr}(C) = \tfrac{1}{n-1}\lVert \tilde X \rVert_F^2$.
- Rank-$k$ reconstruction error in Frobenius norm is $\sum_{j>k} \sigma_j^2$ — **Eckart–Young** optimality.
- PCA on $\tilde X / \sqrt{n-1}$ via SVD ↔ eigendecomp of $C$ — same answer up to sign of columns, but SVD avoids forming $C$ (squaring the condition number).
- For $d \gg n$, decompose the smaller Gram matrix $\tilde X \tilde X^\top \in \mathbb{R}^{n \times n}$ and recover $V$ via $V = \tilde X^\top U \Sigma^{-1}$.
- Scaling matters: PCA on raw data is dominated by high-variance features. **Standardize** (z-score each column) when features have incommensurable units.

## Worked micro-example

Four points in $\mathbb{R}^2$: $(2,0), (0,1), (-2,0), (0,-1)$. Mean is $\mathbf{0}$, so $\tilde X = X$.

$$ C = \frac{1}{3} X^\top X = \frac{1}{3}\begin{bmatrix} 8 & 0 \\ 0 & 2 \end{bmatrix} = \begin{bmatrix} 8/3 & 0 \\ 0 & 2/3 \end{bmatrix}. $$

Eigenvalues $\lambda_1 = 8/3$, $\lambda_2 = 2/3$ with eigenvectors $\mathbf{e}_1, \mathbf{e}_2$. The first PC is along the $x$-axis (longest spread), explaining $8/10 = 80\%$ of the variance. Projecting to 1D drops the $y$-coordinate.

> See [companion notebook](./pca.ipynb) for a 2D point cloud with overlaid principal axes, a 3D Gaussian projected to 2D, and a scree plot.

## Common pitfalls

- **Forgetting to center.** Without centering, the first "PC" mostly tracks the mean direction.
- **Mixing scales.** Standardize when feature units differ (price in USD vs. age in years).
- **Building $X^\top X$ explicitly** when $X$ is ill-conditioned — squares condition number. Use SVD on $\tilde X$.
- **Sign ambiguity.** Each $\mathbf{v}_j$ is determined up to a sign; don't compare signs across implementations.
- **PCA is linear.** Curved manifolds need kernel PCA, t-SNE, UMAP, autoencoders, etc.
- **Components are not "features"** in any interpretable sense unless the loading vectors $\mathbf{v}_j$ have a domain meaning.

## Applications in ML

- **Preprocessing / compression** before clustering or regression on high-dimensional data.
- **Whitening:** transform to identity covariance via $Z = \tilde X V \Lambda^{-1/2}$.
- **Visualization** of high-dim data in 2D/3D scatter plots.
- **Anomaly detection:** points with large reconstruction error are outliers.

## Applications in quant

- **Yield-curve decomposition:** top 3 PCs of bond returns ≈ level, slope, curvature.
- **Statistical risk models / factor models:** PCs of return covariance form latent factors.
- **Denoising covariance matrices** by truncating noisy small eigenvalues (Marchenko–Pastur).

## See also

- [SVD](../../core/linear-algebra/svd.md) — numerical engine of PCA
- [Eigendecomposition](../../core/linear-algebra/eigendecomposition.md)
- [Vectors](../../core/linear-algebra/vectors.md)
- [Linear regression](../supervised/linear-regression.md) — PCA regression as a regularizer

## References

- Hastie, Tibshirani, Friedman, *The Elements of Statistical Learning*, §14.5.
- Jolliffe, *Principal Component Analysis*, Chs. 1–3.
