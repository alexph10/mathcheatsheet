---
id: svm
title: Support Vector Machines (SVM)
domain: ml/supervised
tags: [kernel, convex]
prerequisites: [convexity, vectors, inner-products, kkt-conditions]
used_by: []
difficulty: 2
status: draft
notebook: svm.ipynb
---

# Support Vector Machines (SVM)

## TL;DR

Find the hyperplane that maximizes the margin between two classes. The dual problem depends on the data only through inner products $\langle \mathbf{x}_i, \mathbf{x}_j \rangle$ — replace with a kernel $k(\cdot, \cdot)$ and you get nonlinear decision boundaries for free.

## Hard-margin (linearly separable) SVM

Find $(\mathbf{w}, b)$ that correctly classifies all points $y_i \in \{-1, +1\}$ and maximizes the geometric margin $1/\|\mathbf{w}\|$:

$$ \min_{\mathbf{w}, b} \tfrac{1}{2}\|\mathbf{w}\|^2 \quad \text{s.t.} \quad y_i (\mathbf{w}^\top \mathbf{x}_i + b) \geq 1, \ \forall i. $$

Convex QP. The optimal $\mathbf{w}$ is a sparse linear combination of **support vectors** (training points on the margin).

## Soft-margin SVM

Real data isn't separable; introduce slack $\xi_i \geq 0$ and a penalty $C$:

$$ \min_{\mathbf{w}, b, \boldsymbol{\xi}} \tfrac{1}{2}\|\mathbf{w}\|^2 + C \sum_i \xi_i \quad \text{s.t.} \quad y_i(\mathbf{w}^\top \mathbf{x}_i + b) \geq 1 - \xi_i, \ \xi_i \geq 0. $$

$C$ is a hyperparameter: large $C$ ⇒ less slack (closer to hard margin); small $C$ ⇒ wider margin, more misclassification.

Equivalent unconstrained form using **hinge loss** $\ell(z) = \max(0, 1 - z)$:

$$ \min_{\mathbf{w}, b} \tfrac{1}{2}\|\mathbf{w}\|^2 + C \sum_i \ell\!\left(y_i (\mathbf{w}^\top \mathbf{x}_i + b)\right). $$

## Dual problem and the kernel trick

Applying [KKT](../../core/optimization/kkt-conditions.md), the dual is

$$ \max_{\boldsymbol{\alpha}} \sum_i \alpha_i - \tfrac{1}{2} \sum_{i,j} \alpha_i \alpha_j y_i y_j \langle \mathbf{x}_i, \mathbf{x}_j \rangle \quad \text{s.t.} \quad 0 \leq \alpha_i \leq C, \ \sum_i \alpha_i y_i = 0. $$

Then $\mathbf{w}^* = \sum_i \alpha_i^* y_i \mathbf{x}_i$ and prediction is $\hat{y}(\mathbf{x}) = \text{sign}\!\left(\sum_i \alpha_i^* y_i \langle \mathbf{x}_i, \mathbf{x} \rangle + b^*\right)$.

**Kernel trick:** replace $\langle \mathbf{x}_i, \mathbf{x}_j \rangle$ with a positive-definite kernel $k(\mathbf{x}_i, \mathbf{x}_j) = \langle \phi(\mathbf{x}_i), \phi(\mathbf{x}_j) \rangle_{\mathcal{H}}$. The feature map $\phi$ can be infinite-dimensional and you never compute it explicitly.

## Common kernels

| Name | $k(\mathbf{x}, \mathbf{z})$ | Feature space |
|---|---|---|
| Linear | $\mathbf{x}^\top \mathbf{z}$ | $\mathbb{R}^d$ |
| Polynomial (degree $d$) | $(\mathbf{x}^\top \mathbf{z} + c)^d$ | polynomials of degree $\leq d$ |
| RBF / Gaussian | $\exp\!\left(-\gamma \|\mathbf{x} - \mathbf{z}\|^2\right)$ | infinite-dimensional |
| Sigmoid | $\tanh(\kappa \mathbf{x}^\top \mathbf{z} + c)$ | not always PD |

## Support vectors via KKT

Three cases for each $i$ at the optimum:

1. $\alpha_i = 0$: point is correctly classified outside the margin (no influence).
2. $0 < \alpha_i < C$: point lies exactly on the margin ($y_i(\mathbf{w}^\top \mathbf{x}_i + b) = 1$) — used to compute $b^*$.
3. $\alpha_i = C$: point violates the margin (either inside or misclassified).

The solution is fully determined by support vectors — typically a small fraction of training data.

> See [companion notebook](./svm.ipynb) for linear and RBF SVMs on 2D data with support vectors highlighted.

## Common pitfalls

- **Feature scaling** is critical, especially for RBF — distances dominate.
- **$C$ and $\gamma$ require cross-validation** (often log-scale grid).
- **Soft-margin classifier scores ≠ probabilities.** Use Platt scaling or `CalibratedClassifierCV`.
- **Quadratic in $n$:** training scales as $O(n^2)$ to $O(n^3)$; impractical past ~$10^5$ samples. Use linear SVM (`LinearSVC`, primal) or stochastic methods (SGD with hinge loss) at scale.

## Applications in ML

- Strong baseline on small-to-medium tabular and text data; RBF-SVM is hard to beat on $n < 10^4$ datasets with informative features.
- The kernel framework generalizes to **kernel ridge regression**, **Gaussian processes**, **kernel PCA**.

## Applications in quant

- Classifying regime states from limited engineered features (small sample, kernel benefits).
- Credit scoring as a non-linear alternative to logistic regression where interpretability isn't required.

## See also

- [Convexity](../../core/optimization/convexity.md)
- [KKT conditions](../../core/optimization/kkt-conditions.md)
- [Inner products](../../core/linear-algebra/inner-products.md)
- [Logistic regression](./logistic-regression.md) — the other linear classifier
