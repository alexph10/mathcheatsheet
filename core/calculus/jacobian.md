---
id: jacobian
title: Jacobian
domain: core/calculus
tags: [identity]
prerequisites: [gradients, vectors]
used_by: []
difficulty: 2
status: draft
notebook: jacobian.ipynb
---

# Jacobian

## TL;DR

For a vector-valued $\mathbf{f}: \mathbb{R}^n \to \mathbb{R}^m$, the Jacobian is the $m \times n$ matrix of all partial derivatives — the best linear approximation of $\mathbf{f}$ at a point.

## Definition

$$ J_{\mathbf{f}}(\mathbf{x}) = \begin{bmatrix}
\dfrac{\partial f_1}{\partial x_1} & \cdots & \dfrac{\partial f_1}{\partial x_n} \\
\vdots & \ddots & \vdots \\
\dfrac{\partial f_m}{\partial x_1} & \cdots & \dfrac{\partial f_m}{\partial x_n}
\end{bmatrix} \in \mathbb{R}^{m \times n}. $$

The first-order Taylor expansion is $\mathbf{f}(\mathbf{x} + \mathbf{h}) \approx \mathbf{f}(\mathbf{x}) + J_{\mathbf{f}}(\mathbf{x})\mathbf{h}$.

## Intuition

Near $\mathbf{x}$, the nonlinear map $\mathbf{f}$ looks like the linear map $\mathbf{h} \mapsto J_{\mathbf{f}}(\mathbf{x})\mathbf{h}$. The Jacobian is "the derivative" in higher dimensions; the gradient is just its transpose when $m = 1$.

## Key formulas

- **Scalar output ($m=1$):** $J_f = (\nabla f)^\top$ — a row vector.
- **Chain rule:** $J_{\mathbf{f} \circ \mathbf{g}}(\mathbf{x}) = J_{\mathbf{f}}(\mathbf{g}(\mathbf{x})) \cdot J_{\mathbf{g}}(\mathbf{x})$.
- **Jacobian of a linear map** $\mathbf{f}(\mathbf{x}) = A\mathbf{x}$: $J_{\mathbf{f}} = A$.
- **Jacobian determinant** ($m = n$) measures local volume scaling: integral change-of-variables uses $|\det J|$.

| Map | Jacobian |
|---|---|
| $\mathbf{f}(\mathbf{x}) = A\mathbf{x}$ | $A$ |
| $\mathbf{f}(\mathbf{x}) = \mathbf{x} \odot \mathbf{x}$ (elementwise square) | $\text{diag}(2\mathbf{x})$ |
| Softmax $\sigma(\mathbf{z})_i = e^{z_i}/\sum_j e^{z_j}$ | $\text{diag}(\sigma) - \sigma\sigma^\top$ |
| Polar→Cartesian $(r,\theta)\mapsto(r\cos\theta, r\sin\theta)$ | $\begin{bmatrix}\cos\theta & -r\sin\theta \\ \sin\theta & r\cos\theta\end{bmatrix}$, $|\det|=r$ |

## Properties & identities

- **Inverse-function theorem:** if $J_{\mathbf{f}}(\mathbf{x}_0)$ is invertible, $\mathbf{f}$ is locally invertible with $J_{\mathbf{f}^{-1}}(\mathbf{f}(\mathbf{x}_0)) = J_{\mathbf{f}}(\mathbf{x}_0)^{-1}$.
- **Change of variables in integration:** $\int_{\mathbf{f}(D)} g\, dV = \int_D g(\mathbf{f}(\mathbf{x})) |\det J_{\mathbf{f}}|\, dV$.
- **Rank of $J$** = local dimensionality of $\mathbf{f}$'s image; rank drop signals singularity.

## Worked micro-example

$\mathbf{f}(x, y) = (x^2 - y^2,\, 2xy)^\top$. Partials give

$$ J_{\mathbf{f}}(x, y) = \begin{bmatrix} 2x & -2y \\ 2y & 2x \end{bmatrix}, \quad \det J = 4(x^2 + y^2). $$

At $(1, 1)^\top$, $J = \begin{bmatrix}2 & -2 \\ 2 & 2\end{bmatrix}$, $\det J = 8$.

> See [companion notebook](./jacobian.ipynb) for vector-field visualization and a chain-rule check.

## Common pitfalls

- **Shape convention:** $J$ has output dimension first ($m \times n$). The "denominator-layout" gradient $\nabla f$ for scalar $f$ is $J^\top$ (column vector).
- **Jacobian ≠ Hessian.** Jacobian is first derivative of vector function; Hessian is second derivative of scalar function (equivalently, Jacobian of the gradient).
- **`np.gradient`** estimates gradients on a grid; it does not compute Jacobians. Use `jax.jacobian` / `torch.autograd.functional.jacobian` for autodiff Jacobians.

## Applications in ML

- **Backprop with vector outputs** (autodiff frameworks build vector-Jacobian products `vjp` and Jacobian-vector products `jvp`).
- **Normalizing flows** require $|\det J|$ of an invertible transform.
- **Sensitivity analysis** of neural-network outputs to inputs.

## Applications in quant

- **Multi-asset Greeks:** the Jacobian of the price vector w.r.t. the underlier vector.
- **Coordinate transforms** in stochastic models (e.g., $r \to \log r$).

## See also

- [Gradients](./gradients.md)
- [Chain rule](./chain-rule.md)
- [Hessian](./hessian.md)
- [Matrix calculus](../linear-algebra/matrix-calculus.md)
