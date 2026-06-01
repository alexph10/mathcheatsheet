---
id: gradient-descent
title: Gradient Descent
domain: core/optimization
tags: [optimizer, convex]
prerequisites: [gradients, convexity]
used_by: []
difficulty: 2
status: draft
notebook: gradient-descent.ipynb
---

# Gradient Descent

## TL;DR

Iteratively take a step opposite the gradient: $\mathbf{x}_{k+1} = \mathbf{x}_k - \eta \nabla f(\mathbf{x}_k)$. With the right step size it converges to a minimum at rate $O(1/k)$ for convex $f$ and *geometrically* for strongly convex $f$.

## Definition

For a differentiable $f: \mathbb{R}^n \to \mathbb{R}$ and step size (a.k.a. learning rate) $\eta_k > 0$,

$$ \mathbf{x}_{k+1} = \mathbf{x}_k - \eta_k \nabla f(\mathbf{x}_k). $$

Variants differ in how $\eta_k$ is chosen and how $\nabla f$ is computed:

- **Full-batch gradient descent:** exact $\nabla f$.
- **Stochastic gradient descent (SGD):** $\nabla f$ replaced by an unbiased estimate $\hat{\mathbf{g}}_k$, e.g. the gradient of one minibatch.
- **Momentum / heavy ball:** $\mathbf{v}_{k+1} = \beta \mathbf{v}_k - \eta \nabla f(\mathbf{x}_k);\ \mathbf{x}_{k+1} = \mathbf{x}_k + \mathbf{v}_{k+1}$.
- **Nesterov accelerated gradient:** look-ahead gradient $\nabla f(\mathbf{x}_k + \beta \mathbf{v}_k)$; achieves the optimal $O(1/k^2)$ rate on smooth convex problems.

## Intuition

The gradient points uphill; subtracting it walks downhill. The step size controls how far you walk before re-measuring the slope. Too small → glacially slow. Too large → overshoot and possibly diverge. The geometry of the level sets matters: in narrow valleys (high condition number) plain GD zig-zags; momentum and preconditioning straighten the path.

## Key formulas

### Step-size selection

- **Fixed:** $\eta_k = \eta$ — simplest; needs $\eta \leq 1/L$ for guaranteed descent on $L$-smooth $f$ (gradient $L$-Lipschitz).
- **Backtracking line search (Armijo).** Start with $\eta = \eta_0$; while

$$ f(\mathbf{x}_k - \eta \nabla f(\mathbf{x}_k)) > f(\mathbf{x}_k) - c \eta \lVert \nabla f(\mathbf{x}_k) \rVert^2 $$

  shrink $\eta \leftarrow \rho \eta$ (typical $c = 10^{-4}$, $\rho = 0.5$).

- **Diminishing:** $\eta_k = \eta_0 / (1 + k)$ or $\eta_k = \eta_0 / \sqrt{k}$ — required for SGD convergence with noisy gradients.
- **Exact line search:** $\eta_k = \arg\min_{\eta \geq 0} f(\mathbf{x}_k - \eta \nabla f(\mathbf{x}_k))$ — cheap only for quadratics.

### Convergence rates ($f$ convex, $\nabla f$ $L$-Lipschitz)

| Setting | Rate |
| ------- | ---- |
| Convex, fixed $\eta = 1/L$ | $f(\mathbf{x}_k) - f^\star \leq \dfrac{L \lVert \mathbf{x}_0 - \mathbf{x}^\star \rVert^2}{2 k}$ |
| Convex + Nesterov | $f(\mathbf{x}_k) - f^\star \leq \dfrac{2 L \lVert \mathbf{x}_0 - \mathbf{x}^\star \rVert^2}{(k+1)^2}$ |
| $m$-strongly convex, $\eta = 1/L$ | $\lVert \mathbf{x}_k - \mathbf{x}^\star \rVert^2 \leq \left(1 - \tfrac{m}{L}\right)^k \lVert \mathbf{x}_0 - \mathbf{x}^\star \rVert^2$ |
| $m$-strongly convex + Nesterov | rate $(1 - \sqrt{m/L})^k$ |

The condition number $\kappa = L/m$ is the key constant; GD takes $O(\kappa \log(1/\epsilon))$ steps, Nesterov $O(\sqrt{\kappa} \log(1/\epsilon))$.

### SGD

With unbiased gradient and bounded variance $\mathbb{E}\lVert \hat{\mathbf{g}}_k - \nabla f(\mathbf{x}_k) \rVert^2 \leq \sigma^2$:

$$ \mathbb{E}\bigl[f(\bar{\mathbf{x}}_k) - f^\star\bigr] = O\!\left(\frac{1}{\sqrt{k}}\right) \quad (\text{convex}), \qquad O\!\left(\frac{1}{k}\right) \quad (m\text{-strongly convex, diminishing } \eta_k). $$

## Properties & identities

- **Descent lemma** ($L$-smooth $f$): $f(\mathbf{y}) \leq f(\mathbf{x}) + \nabla f(\mathbf{x})^\top (\mathbf{y} - \mathbf{x}) + \tfrac{L}{2} \lVert \mathbf{y} - \mathbf{x} \rVert^2$. Plugging $\mathbf{y} = \mathbf{x} - \eta \nabla f(\mathbf{x})$ gives the per-step decrease and the safe step size $\eta \leq 1/L$.
- **Polyak–Łojasiewicz (PL) condition** $\tfrac{1}{2} \lVert \nabla f \rVert^2 \geq m (f - f^\star)$ implies linear convergence of GD even without convexity.
- **GD on quadratic** $f(\mathbf{x}) = \tfrac{1}{2} \mathbf{x}^\top A \mathbf{x}$: iteration matrix is $I - \eta A$; converges iff $\eta < 2/\lambda_{\max}(A)$; optimal $\eta = 2/(\lambda_{\max} + \lambda_{\min})$.
- **Saddle points:** GD escapes strict saddles almost surely from random initialization (Lee et al. 2016).

## Worked micro-example

Minimize $f(x) = \tfrac{1}{2} x^2$, $\nabla f(x) = x$, $L = 1$, $m = 1$. With $\eta = 1$ and $x_0 = 4$:

$$ x_{k+1} = x_k - x_k = 0. $$

One step to the optimum — the "Newton" step. With $\eta = 0.5$:

$$ x_k = 4 \cdot 0.5^k, $$

linear convergence with ratio $1 - m/L \cdot \eta = 0.5$. With $\eta = 2$:

$$ x_k = 4 \cdot (-1)^k, $$

it oscillates without decreasing — exactly at the divergence threshold $\eta = 2/L$.

> See [companion notebook](./gradient-descent.ipynb) for a 2D ill-conditioned quadratic, backtracking line search vs. fixed step, divergence with too-large $\eta$, and a momentum trajectory.

## Common pitfalls

- **Too large $\eta$ diverges.** Always sanity-check by plotting $f(\mathbf{x}_k)$ — it should monotonically decrease for full-batch GD on convex $f$.
- **Too small $\eta$ wastes compute.** Iterations are cheap; doubling $\eta$ until you see oscillation, then halving, is a quick tune.
- **Ill-conditioning** ($L \gg m$): plain GD zig-zags. Use momentum/Nesterov, preconditioning (diagonal/Hessian), or change of variables.
- **Local minima / saddles for non-convex $f$.** GD finds a stationary point, not a global optimum. For deep nets this happens to be okay empirically; in general it isn't guaranteed.
- **SGD with fixed large $\eta$** does not converge to the optimum — it bounces around it. You need decreasing $\eta_k$ for convergence, or accept a noise ball of radius $\propto \sqrt{\eta \sigma^2}$.
- **Gradient direction $\neq$ optimal direction.** Steepest descent is *coordinate-system dependent*. Different norms (preconditioned, natural gradient) give better directions; Newton is the limit.
- **Numerical:** very large/small gradients cause float over-/underflow. Gradient clipping and float32→float64 in critical regions help.

## Applications in ML

- Backbone of nearly all model training: SGD, Adam, RMSProp, LAMB are all variants.
- **Logistic / linear regression** with $\ell_2$ regularization is strongly convex — gradient methods have provable linear convergence.
- **Deep learning** uses SGD + momentum + adaptive step sizes despite non-convexity.
- **Adversarial training** alternates gradient steps on $\mathbf{x}$ (attack) and $\boldsymbol{\theta}$ (defense).

## Applications in quant

- **Calibration of pricing models** (local-vol, SABR, Heston) often reduces to a nonlinear least-squares solved by GD / Levenberg–Marquardt.
- **Portfolio optimization with smooth penalties** (e.g. transaction-cost terms) uses gradient methods when QP solvers don't apply.
- **Online learning of trading signals** uses SGD-style updates on streaming data.

## See also

- [Gradients](../calculus/gradients.md)
- [Convexity](./convexity.md)
- [Chain rule](../calculus/chain-rule.md)

## References

- Boyd & Vandenberghe, *Convex Optimization*, Ch. 9.
- Nesterov, *Lectures on Convex Optimization*, Ch. 2.
- Bubeck, *Convex Optimization: Algorithms and Complexity*, §3.
