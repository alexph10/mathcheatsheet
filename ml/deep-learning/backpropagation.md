---
id: backpropagation
title: Backpropagation
domain: ml/deep-learning
tags: [identity]
prerequisites: [chain-rule, gradients]
used_by: []
difficulty: 2
status: draft
---

# Backpropagation

## TL;DR

Backpropagation is the [chain rule](../../core/calculus/chain-rule.md) applied to a computational graph in reverse-mode: one forward pass caches activations, one backward pass propagates $\partial L / \partial \cdot$ through every node, yielding gradients of a scalar loss w.r.t. all parameters in $O(\text{forward cost})$.

## Definition

Let $f = f_L \circ f_{L-1} \circ \cdots \circ f_1$ be a composition of differentiable maps with parameters $\theta = (\theta_1, \dots, \theta_L)$, and let $L(\theta) = \ell(f(\mathbf{x}; \theta), \mathbf{y})$ be a scalar loss. **Reverse-mode automatic differentiation** computes $\nabla_\theta L$ by

1. **Forward pass:** compute and cache intermediate values $a_0 = \mathbf{x}, a_\ell = f_\ell(a_{\ell-1}; \theta_\ell)$.
2. **Backward pass:** initialize $\bar a_L = \partial L / \partial a_L$, then recursively

$$ \bar a_{\ell-1} = \left( \frac{\partial f_\ell}{\partial a_{\ell-1}} \right)^{\!\top} \bar a_\ell, \qquad \bar\theta_\ell = \left( \frac{\partial f_\ell}{\partial \theta_\ell} \right)^{\!\top} \bar a_\ell. $$

The overbar denotes the **adjoint** (cotangent / "upstream gradient") $\bar v = \partial L / \partial v$.

## Intuition

A neural network is a directed acyclic graph of elementary operations. Each node knows two recipes:

- **Forward:** given inputs, produce output (and stash anything the backward pass needs).
- **Backward:** given the gradient of the loss with respect to its output, produce gradients with respect to its inputs and parameters.

Backprop traverses the graph in reverse topological order, multiplying local Jacobian-vector products together. Because the loss is scalar, we always carry a vector (not a matrix) of size = activation dimension, so the cost is $O(\text{forward FLOPs})$ — the key reason deep networks are trainable at scale.

## Key formulas

For an **MLP** with layer $\ell$ doing $z_\ell = W_\ell a_{\ell-1} + b_\ell$, $a_\ell = \sigma(z_\ell)$, and a scalar loss $L$:

**Forward:**

$$ a_\ell = \sigma(W_\ell a_{\ell-1} + b_\ell), \quad \ell = 1, \dots, L. $$

**Backward** — define $\delta_\ell = \partial L / \partial z_\ell$ (per-sample column vector):

$$ \delta_L = \nabla_{a_L} L \,\odot\, \sigma'(z_L) $$

$$ \delta_\ell = \big( W_{\ell+1}^\top \delta_{\ell+1} \big) \odot \sigma'(z_\ell) $$

$$ \frac{\partial L}{\partial W_\ell} = \delta_\ell \, a_{\ell-1}^\top, \qquad \frac{\partial L}{\partial b_\ell} = \delta_\ell. $$

$\odot$ denotes the elementwise (Hadamard) product. For a **mini-batch** with $A_{\ell-1} \in \mathbb{R}^{d_{\ell-1} \times B}$ and $\Delta_\ell \in \mathbb{R}^{d_\ell \times B}$, the per-batch gradient becomes a sum:

$$ \frac{\partial L}{\partial W_\ell} = \Delta_\ell A_{\ell-1}^\top, \qquad \frac{\partial L}{\partial b_\ell} = \Delta_\ell \mathbf{1}_B. $$

**Reverse vs. forward mode cost.** For $f: \mathbb{R}^n \to \mathbb{R}^m$:
- Reverse mode: $O(m)$ passes for the full Jacobian; **one pass** when $m = 1$ (typical loss).
- Forward mode: $O(n)$ passes; better when $n \ll m$ (rare in ML — we usually have millions of parameters and a scalar loss).

## Properties & identities

- **Correctness** follows from the multivariate chain rule: $\nabla_\theta L = J_\theta f^\top \, \nabla_f L$, applied composition-wise.
- **Memory cost** of vanilla backprop is $O(\text{sum of activation sizes})$ — must cache the forward pass. Gradient checkpointing trades compute for memory by recomputing selected activations during the backward pass.
- **Vector-Jacobian products** are what every framework implements per op; you never materialize the Jacobian.
- **Linearity of backprop:** sum / branch nodes route the upstream gradient unchanged or duplicate it; product / contraction nodes use the local Jacobian.
- **No parameter sharing assumed.** If a weight is reused (RNNs, conv layers, weight tying), its gradient is the **sum** over every usage site — backprop handles this automatically because every use contributes a term.

## Worked micro-example

Tiny network: one hidden unit with $\tanh$, scalar input $x$, scalar output, MSE loss.

$$ z_1 = w_1 x + b_1,\quad a_1 = \tanh(z_1),\quad \hat y = w_2 a_1 + b_2,\quad L = \tfrac12(\hat y - y)^2. $$

Backward:

$$ \delta_2 = \hat y - y \implies \frac{\partial L}{\partial w_2} = \delta_2 a_1,\ \frac{\partial L}{\partial b_2} = \delta_2. $$

$$ \delta_1 = w_2 \delta_2 \cdot (1 - a_1^2) \implies \frac{\partial L}{\partial w_1} = \delta_1 x,\ \frac{\partial L}{\partial b_1} = \delta_1. $$

With $x = 1, y = 0$, initial $w_1 = w_2 = 1$, $b_1 = b_2 = 0$: $z_1 = 1$, $a_1 = \tanh(1) \approx 0.7616$, $\hat y = 0.7616$, $\delta_2 = 0.7616$, $\delta_1 = 1 \cdot 0.7616 \cdot (1 - 0.7616^2) \approx 0.3197$. So $\partial L / \partial w_1 \approx 0.3197$ — the gradient *along* the forward path, reversed.

## Common pitfalls

- **Vanishing gradients.** Repeated multiplication by $\sigma'(z) \in (0, 1/4]$ for sigmoids/tanh shrinks $\delta_\ell$ exponentially in depth. ReLU, residual connections, and normalization (BatchNorm, LayerNorm) mitigate this.
- **Exploding gradients.** Repeated multiplication by large $W^\top$ in deep / recurrent models. Gradient clipping or careful initialization (Xavier/Glorot, He) helps.
- **In-place ops** corrupt cached activations needed for the backward pass — frameworks often warn or block.
- **Detaching too eagerly** (`.detach()`, `stop_gradient`) silently zeros out parts of the gradient.
- **Mismatched shapes** in custom layers — the adjoint must have the same shape as the primal.
- **Numerical gradient check.** Always finite-difference check a new layer: $\partial L / \partial \theta \approx (L(\theta + \varepsilon) - L(\theta - \varepsilon))/(2\varepsilon)$ with $\varepsilon \approx 10^{-5}$ in float64.

## Applications in ML

- The training algorithm for **every** parametric model trained by gradient methods: MLPs, CNNs, RNNs, transformers, GNNs, diffusion models, …
- **Differentiable programming:** any program whose ops have defined VJPs is trainable end-to-end (differentiable physics, renderers, optimizers).
- Backprop-through-time (BPTT) and backprop-through-solver (implicit differentiation) generalize the same machinery.

## Applications in quant

- **Calibrating neural surrogates** for option pricing or risk surfaces (loss = pricing error, gradients w.r.t. model weights).
- **Adjoint methods for Greeks:** the same reverse-mode trick gives all sensitivities of a derivative price in one extra pass — used in production XVA engines.

## See also

- [Chain rule](../../core/calculus/chain-rule.md)
- [Gradients](../../core/calculus/gradients.md)
- [Gradient descent](../../core/optimization/gradient-descent.md) — what consumes these gradients
- [Linear regression](../supervised/linear-regression.md) — the depth-1 special case

## References

- Goodfellow, Bengio, Courville, *Deep Learning*, Ch. 6.5.
- Griewank & Walther, *Evaluating Derivatives*, Ch. 3 (the AD bible).
- Baydin et al., "Automatic Differentiation in Machine Learning: a Survey," JMLR 2017.
