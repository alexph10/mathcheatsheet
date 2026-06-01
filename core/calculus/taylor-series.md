---
id: taylor-series
title: Taylor Series
domain: core/calculus
tags: [identity]
prerequisites: [gradients, hessian]
used_by: []
difficulty: 1
status: draft
notebook: taylor-series.ipynb
---

# Taylor Series

## TL;DR

Approximate a smooth function near a point by a polynomial in derivatives — the foundation of perturbation analysis, Newton's method, Laplace approximation, and almost every "linearize and solve" technique.

## Definition

**Single variable.** For $f$ infinitely differentiable at $a$:

$$ f(x) = \sum_{k=0}^\infty \frac{f^{(k)}(a)}{k!} (x - a)^k. $$

A truncation of order $N$ leaves the **remainder** (Lagrange form):

$$ R_N(x) = \frac{f^{(N+1)}(\xi)}{(N+1)!} (x - a)^{N+1}, \quad \xi \in (a, x). $$

**Multivariable.** For $f: \mathbb{R}^n \to \mathbb{R}$ near $\mathbf{a}$:

$$ f(\mathbf{a} + \mathbf{h}) = f(\mathbf{a}) + \nabla f(\mathbf{a})^\top \mathbf{h} + \tfrac{1}{2} \mathbf{h}^\top H_f(\mathbf{a}) \mathbf{h} + O(\|\mathbf{h}\|^3). $$

## Intuition

A Taylor polynomial matches $f$ in value, slope, curvature, and higher-order derivatives at one point. The further you move from $a$, the worse the approximation — controlled by the size of the next derivative.

## Key formulas

Common Maclaurin expansions ($a = 0$):

| $f(x)$ | Expansion | Convergence |
|---|---|---|
| $e^x$ | $\sum_{k\geq 0} x^k / k!$ | all $x$ |
| $\sin x$ | $\sum_{k\geq 0} (-1)^k x^{2k+1}/(2k+1)!$ | all $x$ |
| $\cos x$ | $\sum_{k\geq 0} (-1)^k x^{2k}/(2k)!$ | all $x$ |
| $\ln(1+x)$ | $\sum_{k\geq 1} (-1)^{k+1} x^k/k$ | $-1 < x \leq 1$ |
| $(1+x)^\alpha$ | $\sum_{k\geq 0} \binom{\alpha}{k} x^k$ | $|x|<1$ |
| $1/(1-x)$ | $\sum_{k\geq 0} x^k$ | $|x|<1$ |

## Properties & identities

- **Big-O of remainder** for $C^{N+1}$ functions: $R_N(\mathbf{x}) = O(\|\mathbf{x} - \mathbf{a}\|^{N+1})$.
- **Taylor's theorem with integral remainder** gives a sharper bound when smoothness is finite.
- **Analytic functions** equal their Taylor series on the radius of convergence; non-analytic smooth functions exist (e.g. $e^{-1/x^2}$ at $0$).

## Worked micro-example

For $f(x) = \cos x$ at $a = 0$, second-order approximation: $\cos x \approx 1 - x^2/2$. Truncation error at $x = 0.5$: exact $\cos 0.5 = 0.8776$, approx $0.8750$, error $0.0026 \approx (0.5)^4/24 = 0.0026$, matching the next-order term as expected.

> See [companion notebook](./taylor-series.ipynb) for visualizing truncations of $\sin x$ at various orders and the growing truncation error.

## Common pitfalls

- **Divergence outside the radius of convergence** (e.g. $\ln(1+x)$ for $x > 1$). The series may sum to nonsense.
- **Smooth $\neq$ analytic.** $f(x) = e^{-1/x^2}$ has all derivatives zero at $0$, so its Taylor series is identically zero, but $f \neq 0$.
- **Mismatched expansion point.** Always state $a$ explicitly; expansions around different points give different polynomials.
- **Catastrophic cancellation** in numerical implementations (e.g., $\cos x - 1$ near $0$) — use $-2\sin^2(x/2)$ instead.

## Applications in ML

- **Newton's method** uses the second-order Taylor approximation of the loss.
- **Laplace approximation** of a posterior is a Gaussian fit via a second-order expansion of $\log p$.
- **Influence functions** linearize the parameter response to data via first-order expansion.
- **Reparameterization gradients** use first-order expansions of the deterministic transform.

## Applications in quant

- **Duration & convexity** of bonds: first- and second-order Taylor expansion of price in yield.
- **Greeks via Taylor:** option P&L $\approx \Delta\cdot dS + \tfrac{1}{2}\Gamma\cdot(dS)^2 + \Theta\cdot dt + \mathcal{V}\cdot d\sigma$.
- **Itô's lemma** is essentially a second-order Taylor expansion of $f(X_t, t)$ where $(dW)^2 = dt$ creates the extra $\tfrac{1}{2}\sigma^2 \partial^2 f/\partial x^2$ term.

## See also

- [Gradients](./gradients.md)
- [Hessian](./hessian.md)
- [Itô's lemma](../../quant/stochastic-calculus/ito-lemma.md)
