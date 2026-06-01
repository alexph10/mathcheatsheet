---
id: optimizers
title: Stochastic Optimizers
domain: ml/deep-learning
tags: [optimizer]
prerequisites: [gradient-descent, gradients]
used_by: []
difficulty: 2
status: draft
notebook: optimizers.ipynb
---

# Stochastic Optimizers

## TL;DR

A reference card for the gradient-based optimizers used in deep learning — they differ in how they accumulate past gradients, adapt per-coordinate, and handle weight decay. Adam is the default; SGD-with-momentum often generalizes better.

## Notation

Let $\mathbf{g}_t = \nabla L_t(\boldsymbol{\theta}_t)$ be the (stochastic) gradient at step $t$. All optimizers below are written for parameters $\boldsymbol{\theta} \in \mathbb{R}^d$. Element-wise operations are applied coordinatewise.

## Reference table

| Optimizer | Update | Key hyperparameters | Comment |
|---|---|---|---|
| **SGD** | $\boldsymbol{\theta} \leftarrow \boldsymbol{\theta} - \alpha \mathbf{g}_t$ | $\alpha$ | Vanilla; needs careful lr schedule |
| **SGD + momentum** | $\mathbf{m}_t = \beta \mathbf{m}_{t-1} + \mathbf{g}_t; \quad \boldsymbol{\theta} \leftarrow \boldsymbol{\theta} - \alpha \mathbf{m}_t$ | $\alpha, \beta{\approx}0.9$ | Accelerates flat directions, dampens oscillation |
| **Nesterov** | Same but $\mathbf{g}_t$ evaluated at $\boldsymbol{\theta} - \alpha\beta\mathbf{m}_{t-1}$ | $\alpha, \beta$ | "Look-ahead" momentum |
| **AdaGrad** | $\mathbf{v}_t = \mathbf{v}_{t-1} + \mathbf{g}_t^2; \quad \boldsymbol{\theta} \leftarrow \boldsymbol{\theta} - \alpha \mathbf{g}_t / (\sqrt{\mathbf{v}_t} + \varepsilon)$ | $\alpha$ | Per-coord lr; lr decays monotonically (problem for non-convex) |
| **RMSProp** | $\mathbf{v}_t = \rho \mathbf{v}_{t-1} + (1-\rho) \mathbf{g}_t^2; \quad \boldsymbol{\theta} \leftarrow \boldsymbol{\theta} - \alpha \mathbf{g}_t / (\sqrt{\mathbf{v}_t} + \varepsilon)$ | $\alpha, \rho{\approx}0.99$ | EWMA fixes AdaGrad's decay |
| **Adam** | $\mathbf{m}_t = \beta_1 \mathbf{m}_{t-1} + (1-\beta_1)\mathbf{g}_t$; $\mathbf{v}_t = \beta_2 \mathbf{v}_{t-1} + (1-\beta_2) \mathbf{g}_t^2$; bias-correct $\hat{\mathbf{m}} = \mathbf{m}_t/(1-\beta_1^t)$, $\hat{\mathbf{v}} = \mathbf{v}_t/(1-\beta_2^t)$; $\boldsymbol{\theta} \leftarrow \boldsymbol{\theta} - \alpha \hat{\mathbf{m}}/(\sqrt{\hat{\mathbf{v}}} + \varepsilon)$ | $\alpha, \beta_1{=}0.9, \beta_2{=}0.999$ | RMSProp + momentum + bias correction — current default |
| **AdamW** | Adam, but weight decay decoupled: $\boldsymbol{\theta} \leftarrow (1 - \alpha \lambda)\boldsymbol{\theta} - \alpha \hat{\mathbf{m}}/(\sqrt{\hat{\mathbf{v}}}+\varepsilon)$ | + $\lambda$ | Fixes Adam's incorrect $\ell_2$; recommended for Transformers |
| **NAdam** | Adam + Nesterov-style momentum | similar | Marginally better than Adam on some tasks |
| **AdaBelief** | Adam but with $\mathbf{v}$ tracking $(\mathbf{g}_t - \mathbf{m}_t)^2$ | similar | Closer to "natural variance"; sometimes more stable |
| **Lion** | $\boldsymbol{\theta} \leftarrow \boldsymbol{\theta} - \alpha\, \text{sign}(\beta_1 \mathbf{m}_{t-1} + (1-\beta_1)\mathbf{g}_t)$ | smaller $\alpha$ | Sign-based; memory cheaper than Adam |
| **LARS / LAMB** | Adam-like with **layerwise** trust ratio $\|\boldsymbol{\theta}_\ell\|/\|\text{update}_\ell\|$ scaling | + layer scaling | Enables large-batch training (LARS for ResNet, LAMB for BERT) |
| **Shampoo / K-FAC** | Second-order / preconditioned with Kronecker-factored Fisher | many | Costly but powerful; gaining traction at scale |

## Choosing an optimizer (rough field guide)

| Setting | Reasonable default |
|---|---|
| Computer vision, ResNet-style | SGD + momentum + cosine schedule + warmup |
| Transformers / NLP | AdamW + linear warmup + cosine decay |
| Tabular MLPs | Adam, lr $\approx 10^{-3}$ |
| Small problems, deterministic | Full-batch L-BFGS (not in this table — second-order, not stochastic) |
| Reinforcement learning | Adam with low lr ($10^{-4}$) and gradient clipping |

## Learning-rate schedules (orthogonal to optimizer choice)

- **Step decay:** $\alpha \times \gamma$ at milestones.
- **Cosine annealing:** $\alpha(t) = \alpha_{\min} + \tfrac{1}{2}(\alpha_{\max} - \alpha_{\min})(1 + \cos(\pi t / T))$.
- **Warmup:** linearly ramp $\alpha$ from $0$ over the first few thousand steps — almost mandatory for Transformers.
- **OneCycle:** triangular warmup + cosine cool-down; works well for small/medium nets.

## Practical pitfalls

- **Adam can fail to converge** on some convex problems (Reddi et al., 2018) — AMSGrad fixes the proof; not always needed in practice.
- **Weight decay ≠ $\ell_2$ in Adam.** Use AdamW.
- **Gradient clipping** ($\|\mathbf{g}\| \leq c$) is often the cheapest way to stabilize RNNs / Transformers.
- **Hyperparameter coupling:** changing batch size by $k$ usually requires lr × $k$ (linear scaling rule) up to a limit.
- **EMA of weights** (different from EMA of gradients) at inference often gives a free $0.1$–$0.3$% improvement.

> See [companion notebook](./optimizers.ipynb) for trajectories of SGD / Momentum / RMSProp / Adam on a 2D quadratic and the Rosenbrock function.

## See also

- [Gradient descent](../../core/optimization/gradient-descent.md) — the underlying method
- [Gradients](../../core/calculus/gradients.md)
- [Backpropagation](./backpropagation.md)
