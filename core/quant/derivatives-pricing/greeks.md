---
id: greeks
title: The Greeks
domain: quant/derivatives-pricing
tags: [pricing]
prerequisites: [black-scholes, gradients]
used_by: []
difficulty: 2
status: draft
notebook: greeks.ipynb
---

# The Greeks

## TL;DR

Sensitivities of an option's price $V$ to its inputs (spot $S$, time $t$, volatility $\sigma$, rate $r$, strike $K$). They're how traders measure risk and how desks hedge it.

## First-order Greeks

| Greek | Definition | Black-Scholes call | Black-Scholes put | Intuition |
|---|---|---|---|---|
| **Delta** ($\Delta$) | $\partial V / \partial S$ | $N(d_1)$ | $N(d_1) - 1$ | Equivalent stock position |
| **Vega** ($\mathcal{V}$) | $\partial V / \partial \sigma$ | $S\, n(d_1)\sqrt{T-t}$ | same | Profit if vol rises 1.0 (often quoted per 1%) |
| **Theta** ($\Theta$) | $\partial V / \partial t$ | $-\tfrac{S n(d_1) \sigma}{2\sqrt{T-t}} - rK e^{-r(T-t)} N(d_2)$ | $-\tfrac{S n(d_1) \sigma}{2\sqrt{T-t}} + rK e^{-r(T-t)} N(-d_2)$ | Time decay |
| **Rho** ($\rho$) | $\partial V / \partial r$ | $K(T-t) e^{-r(T-t)} N(d_2)$ | $-K(T-t) e^{-r(T-t)} N(-d_2)$ | Rate sensitivity |

where $n(\cdot)$ is the standard normal PDF, $N(\cdot)$ the CDF, $d_1$ and $d_2$ are the Black-Scholes auxiliary quantities (see [Black-Scholes](./black-scholes.md)).

## Second-order Greeks

| Greek | Definition | BSM call/put | Intuition |
|---|---|---|---|
| **Gamma** ($\Gamma$) | $\partial^2 V / \partial S^2$ | $n(d_1) / (S \sigma \sqrt{T-t})$ | Convexity in spot; peaks ATM, near expiry |
| **Vanna** | $\partial^2 V / \partial S \partial \sigma$ | $-n(d_1)\, d_2 / \sigma$ | Δ-vega cross-sensitivity |
| **Volga (Vomma)** | $\partial^2 V / \partial \sigma^2$ | $\mathcal{V} \cdot d_1 d_2 / \sigma$ | Vega convexity |
| **Charm** | $\partial \Delta / \partial t$ | (formula longer) | Delta decay over time |
| **Speed** | $\partial^3 V / \partial S^3$ | (longer) | Gamma rate of change |

## P&L decomposition via Taylor + Itô

For small moves $dS$, $dt$, $d\sigma$:

$$ dV \approx \Delta\, dS + \tfrac{1}{2}\Gamma\, (dS)^2 + \Theta\, dt + \mathcal{V}\, d\sigma + \rho\, dr + \cdots $$

Under [Itô](../stochastic-calculus/ito-lemma.md) for a delta-hedged portfolio ($\Pi = V - \Delta S$), $dS$ terms cancel; $\Gamma$ and $\Theta$ govern the P&L of the residual:

$$ d\Pi \approx \tfrac{1}{2}\Gamma\, (dS)^2 + \Theta\, dt = \tfrac{1}{2}\Gamma S^2 (\sigma_{\text{realized}}^2 - \sigma_{\text{implied}}^2)\, dt. $$

So a long-gamma, delta-hedged trader profits if realized vol exceeds implied vol (and vice versa). This is the **gamma-vega P&L** mechanic.

## Sign conventions (long position)

| Greek | Long call | Long put |
|---|---|---|
| $\Delta$ | $+$ | $-$ |
| $\Gamma$ | $+$ | $+$ |
| $\mathcal{V}$ | $+$ | $+$ |
| $\Theta$ | $-$ (usually) | $-$ (usually) |
| $\rho$ | $+$ | $-$ |

(Short positions flip every sign.)

## Hedging

- **Delta hedging:** continuously hold $-\Delta$ shares against an option to neutralize first-order spot risk.
- **Gamma hedging:** add another option to neutralize the residual second-order curvature.
- **Vega hedging:** use options at different maturities/strikes to neutralize vol exposure.
- **In practice:** hedge discretely (transaction costs) and across a vol surface (skew + term-structure).

> See [companion notebook](./greeks.ipynb) for Delta, Gamma, and Vega plotted against spot at multiple maturities.

## Common pitfalls

- **Vega units.** "Vega = 0.15" usually means P&L per 1% vol change, not per unit. Scale carefully.
- **Theta units.** Usually quoted per calendar day (or per year). Per-day theta = annual theta / 365.
- **Greeks are model-dependent.** Black-Scholes Greeks differ from local-vol or stochastic-vol Greeks — use the model that priced the book.
- **At expiry $\Gamma$ explodes** for ATM options (formula singular); use barrier-adjusted or jump-corrected models near the strike.
- **Higher-order Greeks** matter for exotics and risk; second-order ignored = nonlinear positions misrisked.

## Applications in quant

- **Delta-hedging desks** trade gamma against realized-vs-implied vol.
- **Greek risk reports** summarize a book's exposure dimension-by-dimension.
- **Margin / capital** for derivatives is often computed via Greek stress scenarios (SIMM, FRTB).

## See also

- [Black-Scholes](./black-scholes.md)
- [Itô's lemma](../stochastic-calculus/ito-lemma.md)
- [Gradients](../../core/calculus/gradients.md)
