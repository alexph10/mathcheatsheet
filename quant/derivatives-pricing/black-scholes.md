---
id: black-scholes
title: Black–Scholes Model
domain: quant/derivatives-pricing
tags: [pricing, distribution]
prerequisites: [common-distributions, random-variables]
used_by: []
difficulty: 2
status: draft
notebook: black-scholes.ipynb
---

#### Black–Scholes Model

#### TL;DR

Under geometric Brownian motion plus a few idealized market assumptions, the no-arbitrage price of a European option has a closed form involving the standard normal CDF — and its sensitivities (Greeks) likewise.

#### Setup

The underlying asset price $S_t$ follows a **geometric Brownian motion** (GBM)

$$ dS_t = \mu S_t \, dt + \sigma S_t \, dW_t, $$

so $S_T = S_0 \exp\!\left((\mu - \tfrac{1}{2}\sigma^2) T + \sigma W_T\right)$ is [log-normal](../../core/probability/common-distributions.md). Constant risk-free rate $r$, no dividends, no transaction costs, continuous trading, and frictionless short-selling.

**Risk-neutral pricing.** A self-financing replicating portfolio in $(S, \text{cash})$ implies a unique no-arbitrage price equal to the discounted expectation under the risk-neutral measure $\mathbb{Q}$, where $\mu$ is replaced by $r$:

$$ V_0 = e^{-rT}\, \mathbb{E}^{\mathbb{Q}}[\text{payoff}(S_T)]. $$

#### Black–Scholes PDE

Any sufficiently smooth derivative price $V(S, t)$ satisfies

$$ \frac{\partial V}{\partial t} + \tfrac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} + rS \frac{\partial V}{\partial S} - rV = 0, $$

with the terminal condition $V(S, T) = \text{payoff}(S)$. The European call/put formulas below solve this PDE.

## Closed-form European call and put

Define

$$ d_1 = \frac{\ln(S_0/K) + (r + \tfrac{1}{2}\sigma^2)T}{\sigma\sqrt{T}}, \qquad d_2 = d_1 - \sigma\sqrt{T}, $$

where $K$ is the strike, $T$ the time to maturity, and $\Phi$ the standard normal CDF. Then

$$ C = S_0 \Phi(d_1) - K e^{-rT} \Phi(d_2), \qquad P = K e^{-rT} \Phi(-d_2) - S_0 \Phi(-d_1). $$

**Put–call parity** (model-free, follows from replication):

$$ C - P = S_0 - K e^{-rT}. $$

## The Greeks

Sensitivities of $V$ to model inputs. Let $\phi$ be the standard normal PDF.

| Greek | Symbol | Call | Put |
| ----- | ------ | ---- | --- |
| Delta | $\partial V/\partial S$ | $\Phi(d_1)$ | $\Phi(d_1) - 1$ |
| Gamma | $\partial^2 V/\partial S^2$ | $\dfrac{\phi(d_1)}{S_0 \sigma \sqrt{T}}$ | same as call |
| Vega  | $\partial V/\partial \sigma$ | $S_0 \phi(d_1) \sqrt{T}$ | same as call |
| Theta | $\partial V/\partial t$ | $-\dfrac{S_0 \phi(d_1) \sigma}{2\sqrt{T}} - r K e^{-rT} \Phi(d_2)$ | $-\dfrac{S_0 \phi(d_1) \sigma}{2\sqrt{T}} + r K e^{-rT} \Phi(-d_2)$ |
| Rho   | $\partial V/\partial r$ | $K T e^{-rT} \Phi(d_2)$ | $-K T e^{-rT} \Phi(-d_2)$ |

Gamma and Vega are identical for call and put because they only differ by a forward-style linear term in $S$ and $K e^{-rT}$.

## Worked micro-example

$S_0 = 100$, $K = 100$, $r = 0.05$, $\sigma = 0.20$, $T = 1$. Then

$$ d_1 = \frac{0 + 0.07}{0.20} = 0.35, \quad d_2 = 0.15, $$

$$ C = 100 \cdot \Phi(0.35) - 100 e^{-0.05} \cdot \Phi(0.15) \approx 100(0.6368) - 95.123(0.5596) \approx 10.45. $$

Put–call parity gives $P = C - S_0 + K e^{-rT} \approx 10.45 - 4.88 \approx 5.57$.

> See [companion notebook](./black-scholes.ipynb) for the closed-form vs Monte-Carlo check, parity verification, and Delta/price curves.

## Key assumptions and what breaks them

- **Constant $\sigma$.** Reality shows a **volatility smile/skew**: implied vol depends on strike and maturity. Cured by local/stochastic vol models (Dupire, Heston, SABR).
- **Log-normal returns.** Empirical returns have heavier tails and negative skew. Drives jump-diffusion (Merton) and Lévy models.
- **Continuous trading, no costs.** Hedging is discrete, with bid–ask spreads and impact.
- **Constant $r$ and no dividends.** Easily patched: replace $S_0$ by $S_0 e^{-qT}$ for continuous dividend yield $q$; use stochastic-rate models for long-dated products.
- **No early exercise.** American options need numerical methods (binomial trees, LSM Monte Carlo).

## Common pitfalls

- **$d_1$ uses $r + \tfrac{1}{2}\sigma^2$**, not $r - \tfrac{1}{2}\sigma^2$. The drift correction flips sign between the measure ($\mathbb{Q}$ drift is $r - \tfrac{1}{2}\sigma^2$ for $\ln S_T$) and the $d_1$ formula because of an extra term from differentiating the expectation.
- **Units of $\sigma$ and $T$ must match** (annualized vol with $T$ in years).
- **Vega is per unit of $\sigma$** (e.g. 1.0 = 100 vol points), not per "1 vol point" — divide by 100 if you quote it that way.
- **Implied volatility is not realized volatility** — it is the $\sigma$ that makes the BS formula match the market price.

## Applications in quant

- Benchmark for European vanilla pricing and risk; the lingua franca of options trading via implied vol.
- Greeks drive delta/gamma/vega hedging strategies.
- Forms the baseline against which smile models (Heston, SABR, local vol) are calibrated.

## See also

- [Common distributions](../../core/probability/common-distributions.md) — log-normal of $S_T$.
- [Random variables](../../core/probability/random-variables.md)

## References

- Hull, *Options, Futures, and Other Derivatives*, Ch. 15.
- Shreve, *Stochastic Calculus for Finance II*, Ch. 4.
