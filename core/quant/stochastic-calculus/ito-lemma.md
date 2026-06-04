---
id: ito-lemma
title: Itô's Lemma
domain: quant/stochastic-calculus
tags: [stochastic-process, identity]
prerequisites: [random-variables, taylor-series, markov-chains]
used_by: []
difficulty: 3
status: draft
---

# Itô's Lemma

## TL;DR

The "chain rule for stochastic calculus" — when a process is driven by Brownian motion, ordinary calculus gains an extra $\tfrac{1}{2}\sigma^2 \partial^2 f/\partial x^2$ term because Brownian increments contribute non-negligible quadratic variation.

## Setup

Let $X_t$ be an Itô process satisfying the SDE

$$ dX_t = \mu(X_t, t)\, dt + \sigma(X_t, t)\, dW_t, $$

where $W_t$ is standard Brownian motion. For $f(x, t) \in C^{2,1}$ (twice continuously differentiable in $x$, once in $t$), define $Y_t = f(X_t, t)$.

## Itô's lemma (1D)

$$ \boxed{\, dY_t = \left( \frac{\partial f}{\partial t} + \mu \frac{\partial f}{\partial x} + \tfrac{1}{2} \sigma^2 \frac{\partial^2 f}{\partial x^2} \right) dt + \sigma \frac{\partial f}{\partial x}\, dW_t \,} $$

The drift term gains $\tfrac{1}{2}\sigma^2 f_{xx}$ — the **Itô correction** — beyond the naive chain rule.

## The intuition behind the correction

For ordinary calculus, $df = f_t\, dt + f_x\, dx$. Expanding $f(x + dx, t + dt)$ to second order:

$$ df \approx f_t\, dt + f_x\, dx + \tfrac{1}{2} f_{xx}\, (dx)^2 + \cdots $$

For deterministic $x$, $(dx)^2 = O(dt^2)$ and we drop it. For Itô processes, however, **$(dW_t)^2 = dt$** (formally — quadratic variation of BM grows linearly with time). So:

$$ (dX_t)^2 = (\mu\, dt + \sigma\, dW_t)^2 = \sigma^2\, dt + \text{higher-order}, $$

and the $\tfrac{1}{2} f_{xx} (dX)^2$ contributes a non-trivial $\tfrac{1}{2}\sigma^2 f_{xx}\, dt$ term.

## Itô's box rules

A useful mnemonic for multiplying differentials:

| × | $dt$ | $dW_t$ |
|---|---|---|
| **$dt$** | $0$ | $0$ |
| **$dW_t$** | $0$ | $dt$ |

For multidimensional BM, $dW_t^{(i)} dW_t^{(j)} = \rho_{ij}\, dt$.

## Multidimensional Itô

For $\mathbf{X}_t \in \mathbb{R}^n$ with $d\mathbf{X}_t = \boldsymbol{\mu}\, dt + \Sigma\, d\mathbf{W}_t$ and $f: \mathbb{R}^n \times [0, T] \to \mathbb{R}$:

$$ df = \left( f_t + \boldsymbol{\mu}^\top \nabla f + \tfrac{1}{2}\text{tr}(\Sigma \Sigma^\top H_f) \right) dt + (\nabla f)^\top \Sigma\, d\mathbf{W}_t. $$

## Canonical example: geometric Brownian motion

Suppose $dS_t = \mu S_t\, dt + \sigma S_t\, dW_t$ (Black–Scholes price dynamics). Apply Itô to $Y_t = \log S_t$ with $f(s) = \log s$, $f_s = 1/s$, $f_{ss} = -1/s^2$:

$$ d(\log S_t) = \left(\mu - \tfrac{1}{2}\sigma^2\right) dt + \sigma\, dW_t. $$

So $\log S_t$ is Brownian motion with drift, hence

$$ S_t = S_0 \exp\!\left( \left(\mu - \tfrac{1}{2}\sigma^2\right) t + \sigma W_t \right) \sim \text{Lognormal}. $$

The $-\tfrac{1}{2}\sigma^2$ term is exactly the Itô correction — without it, $\mathbb{E}[S_t]$ would be wrong by a factor of $e^{\sigma^2 t / 2}$.

## Connection to the Black-Scholes PDE

For a derivative $V(S, t)$ on $S_t = $ GBM, apply Itô to get $dV$, then construct a delta-hedged portfolio $\Pi = V - \Delta S$ with $\Delta = V_S$. The $dW$ terms cancel and arbitrage-free pricing forces:

$$ V_t + r S V_S + \tfrac{1}{2} \sigma^2 S^2 V_{SS} = r V. $$

This is the Black-Scholes PDE. Itô's lemma is the engine.

## Itô vs Stratonovich

Two stochastic integrals exist. They differ when $\sigma$ depends on $X$:

- **Itô** (non-anticipating, used in finance) — martingale property, $\mathbb{E}\!\left[\int \sigma\, dW\right] = 0$.
- **Stratonovich** (mid-point, used in physics) — obeys ordinary chain rule, no correction term.

Conversion: $\int \sigma\, dW^{\text{Strat}} = \int \sigma\, dW^{\text{Itô}} + \tfrac{1}{2} \int \sigma' \sigma\, dt$.

## Common pitfalls

- **"$(dW)^2 = dt$" is formal**, not a pointwise statement. It's shorthand for the quadratic variation accumulating linearly.
- **Forgetting the Itô correction** is the #1 mistake — it shows up in expectations of nonlinear functions of $S_t$.
- **Adapted vs anticipating integrands.** Itô's construction requires the integrand to be $\mathcal{F}_t$-measurable; using future information breaks the theory.
- **GBM ≠ Brownian motion.** GBM has multiplicative noise; its log is BM with drift.

## Applications in quant

- **Black-Scholes derivation** (above).
- **Hedging** — every Greek is an Itô-derived sensitivity.
- **Term-structure models** (Vasicek, Hull-White, HJM) all use Itô as the workhorse.

## Applications in ML

- **Diffusion models** apply Itô to derive the score-matching loss and the reverse SDE used for sampling.
- **Neural SDEs** (continuous-time generative models) rely on Itô calculus for backpropagation through stochastic dynamics.

## See also

- [Markov chains](../../core/stochastic-processes/markov-chains.md) — the discrete-state cousin
- [Taylor series](../../core/calculus/taylor-series.md) — Itô is a 2nd-order Taylor expansion with quadratic variation
- [Black-Scholes](../derivatives-pricing/black-scholes.md)

## References

- Shreve, *Stochastic Calculus for Finance II*, Ch. 4.
- Øksendal, *Stochastic Differential Equations*.
