# Chain Rule

## TL;DR

The derivative of a composition is the product of the derivatives: $(f \circ g)'(x) = f'(g(x)) \cdot g'(x)$. In higher dimensions, replace "product" with "matrix product of Jacobians" — this is what backpropagation computes.

## Definition

**Scalar case** ($f, g: \mathbb{R} \to \mathbb{R}$, both differentiable):

$$ \frac{d}{dx} f(g(x)) = f'(g(x)) \cdot g'(x). $$

**Multivariable scalar output** ($f: \mathbb{R}^n \to \mathbb{R}$, $\mathbf{g}: \mathbb{R}^m \to \mathbb{R}^n$):

$$ \nabla_{\mathbf{x}} f(\mathbf{g}(\mathbf{x})) = J_{\mathbf{g}}(\mathbf{x})^\top \nabla_{\mathbf{y}} f(\mathbf{y})\Big|_{\mathbf{y} = \mathbf{g}(\mathbf{x})}, $$

where $J_{\mathbf{g}}$ is the Jacobian $(\partial g_i / \partial x_j)$ of size $n \times m$.

**General vector composition** ($\mathbf{h} = \mathbf{f} \circ \mathbf{g}$):

$$ J_{\mathbf{h}}(\mathbf{x}) = J_{\mathbf{f}}(\mathbf{g}(\mathbf{x})) \cdot J_{\mathbf{g}}(\mathbf{x}). $$

Jacobians multiply in the order the functions are applied (outermost on the left). This is the matrix generalization of the scalar product.

## Intuition

If $g$ stretches its input by a factor of $g'(x)$ near $x$, and then $f$ stretches its input by $f'(g(x))$ near $g(x)$, the composition stretches by the product. The same logic in higher dimensions becomes "compose two linear maps", which is matrix multiplication of Jacobians.

For a deep network $L(\boldsymbol{\theta}) = \ell(f_K(f_{K-1}(\cdots f_1(\mathbf{x}; \boldsymbol{\theta}_1) \cdots ; \boldsymbol{\theta}_K)))$, the gradient with respect to any earlier $\boldsymbol{\theta}_i$ is a product of all the downstream Jacobians — the chain rule applied recursively. **That is backpropagation**.

## Key formulas

- **Two-function scalar:** $\dfrac{dy}{dx} = \dfrac{dy}{du} \cdot \dfrac{du}{dx}$.
- **Three-function scalar:** $\dfrac{dy}{dx} = \dfrac{dy}{du} \cdot \dfrac{du}{dv} \cdot \dfrac{dv}{dx}$.
- **Total derivative for $f(x, y)$ with $y = y(x)$:**

$$ \frac{df}{dx} = \frac{\partial f}{\partial x} + \frac{\partial f}{\partial y} \cdot \frac{dy}{dx}. $$

- **Backprop core equation** (loss $L$, intermediate activations $\mathbf{z}^{(\ell)}$):

$$ \frac{\partial L}{\partial \boldsymbol{\theta}^{(\ell)}} = \left(\prod_{k=\ell+1}^{K} J^{(k)}\right)^\top \nabla_{\mathbf{z}^{(K)}} L \, \cdot \, \frac{\partial \mathbf{z}^{(\ell)}}{\partial \boldsymbol{\theta}^{(\ell)}}. $$

## Properties & identities

- **Associativity** of the Jacobian product mirrors associativity of matrix multiplication — but the *order of multiplication* determines compute cost (forward-mode vs reverse-mode autodiff).
- **Reverse-mode** (backprop): right-to-left, cheap when output is a scalar and parameters are many.
- **Forward-mode**: left-to-right, cheap when input is low-dimensional.

## Worked micro-example

Let $y = (3x^2 + 1)^4$. Set $u = 3x^2 + 1$.

$$ \frac{dy}{dx} = \frac{dy}{du} \cdot \frac{du}{dx} = 4 u^3 \cdot 6x = 24 x (3x^2 + 1)^3. $$

**Vector case.** Let $f(\mathbf{y}) = \tfrac{1}{2}\lVert \mathbf{y} \rVert^2$ and $\mathbf{y} = A\mathbf{x}$, with $A \in \mathbb{R}^{m \times n}$. Then

$$ \nabla_{\mathbf{y}} f = \mathbf{y}, \quad J_{\mathbf{y}}(\mathbf{x}) = A, $$

so by the chain rule

$$ \nabla_{\mathbf{x}} f(A\mathbf{x}) = A^\top (A\mathbf{x}) = A^\top A \mathbf{x}. $$

This is the gradient at the heart of least-squares regression.

## Common pitfalls

- **Forgetting an intermediate variable** that depends on $x$ — use the total-derivative form when in doubt.
- **Confusing $\partial / \partial x$ with $d / dx$** when $f$ depends on $x$ both directly and through other variables.
- **Jacobian multiplication order** — outermost function's Jacobian is on the left.
- **Numerical stability:** long chain-rule products can underflow / overflow (vanishing / exploding gradients). LayerNorm, residual connections, and gradient clipping exist to combat this.

## Applications in ML

- **Backpropagation** is the chain rule, period. Every autodiff framework (PyTorch, JAX, TensorFlow) is essentially a chain-rule machine over a computational graph.
- **Reparameterization trick** in VAEs uses the chain rule to push gradients through a sampling step.

## Applications in quant

- **Greeks of structured products** — pricing a complex derivative requires chaining derivatives through intermediate model variables.
- **Sensitivity of portfolio metrics** to underlying factors, when the relationship is layered (factor → asset return → portfolio return).

## See also

- [Gradients](./gradients.md)
- Jacobian (forthcoming sheet)
- Backprop (forthcoming, `ml/deep-learning`)
