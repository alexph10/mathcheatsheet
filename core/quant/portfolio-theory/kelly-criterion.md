---
id: kelly-criterion
title: Kelly Criterion
domain: quant/portfolio-theory
tags: []
prerequisites: [random-variables, expectation-variance]
used_by: []
difficulty: 2
status: draft
notebook: kelly-criterion.ipynb
---

# Kelly Criterion

## TL;DR

The Kelly fraction $f^*$ is the bet size that maximizes the long-run geometric growth rate of wealth: $f^* = (bp - q)/b$ for a discrete bet, $f^* = (\mu - r)/\sigma^2$ for a continuous return. Bet more and you grow faster on average but go broke faster; bet less and you under-compound.

## Discrete-bet setup

You're offered repeated bets: win $b$ units per unit staked with probability $p$, lose 1 unit per unit staked with probability $q = 1 - p$. Pick fraction $f$ of current wealth to bet.

After one bet, wealth $W$ becomes either $W(1 + fb)$ or $W(1 - f)$. The **long-run growth rate** $g(f)$ satisfies

$$ g(f) = \mathbb{E}[\log(1 + R(f))] = p \log(1 + fb) + q \log(1 - f). $$

Setting $g'(f) = 0$:

$$ \boxed{\, f^* = \dfrac{bp - q}{b} = p - \dfrac{q}{b} \,} $$

Required edge: $bp > q$ (positive expected value) — otherwise $f^* \leq 0$.

## Continuous (log-normal asset) setup

Asset with arithmetic return $\mu$, volatility $\sigma$, risk-free rate $r$. Hold fraction $f$ in the risky asset; the log-return of wealth is

$$ d(\log W_t) = \left[ r + f(\mu - r) - \tfrac{1}{2} f^2 \sigma^2 \right] dt + f \sigma\, dW_t. $$

Maximizing the drift:

$$ \boxed{\, f^* = \dfrac{\mu - r}{\sigma^2} \,} $$

This is the **continuous Kelly fraction** — the famous result. The maximum growth rate is $r + \tfrac{1}{2}(\mu - r)^2/\sigma^2$.

## Multi-asset Kelly

With excess return vector $\boldsymbol{\mu} - r\mathbf{1}$ and covariance $\Sigma$:

$$ \mathbf{f}^* = \Sigma^{-1} (\boldsymbol{\mu} - r\mathbf{1}). $$

This is **proportional to the tangency portfolio** in [mean-variance](./mean-variance.md). Kelly gives the scale; mean-variance gives the direction.

## Properties

- **Maximizes median terminal wealth** (and any percentile under broad conditions).
- **Asymptotically dominates** any other constant-rebalanced strategy — for sufficiently long horizons, $W_T^{\text{Kelly}}/W_T^{\text{other}} \to \infty$ in probability.
- **Time-additive log utility** — Kelly is the unique strategy that maximizes $\mathbb{E}[\log W_T]$.
- **Half-Kelly** (or fractional Kelly) is overwhelmingly preferred in practice: same growth ≈ 75% of full Kelly with ~50% the volatility.

## Why fractional Kelly?

1. **Estimation error.** $\hat{\mu}$ is much noisier than $\hat{\sigma}$; full Kelly with overestimated $\mu$ leads to ruinous over-leverage.
2. **Volatility drag.** Drawdowns at full Kelly are gigantic — peak-to-trough losses of 50%+ are routine. Most investors can't endure them.
3. **Discrete-time approximation.** Continuous Kelly assumes continuous rebalancing; in reality you can't react instantly.

A useful rule: **f = ½ Kelly trades 25% of the growth rate for 75% less variance**.

## Worked micro-example

Bet on a biased coin: $p = 0.55$, $b = 1$ (even money). Then

$$ f^* = \frac{1 \cdot 0.55 - 0.45}{1} = 0.10, \quad g(f^*) = 0.55 \log(1.10) + 0.45 \log(0.90) \approx 0.005. $$

So you bet 10% of wealth each round and grow $\approx 0.5\%$ per round geometrically. After 1000 rounds, $W \approx W_0 \cdot e^{5} \approx 148 W_0$ on average — but variance of $\log W$ is also large.

> See [companion notebook](./kelly-criterion.ipynb) for terminal-wealth distributions at $f \in \{0.5 f^*, f^*, 1.5 f^*, 2 f^*\}$ showing the growth/ruin trade-off.

## Common pitfalls

- **$\mu$ is estimated, not given.** Plug-in $\hat{\mu}$ wildly overestimates $f^*$ when $\mu$ is small relative to $\sigma$.
- **Bet sizes can exceed 100%** when $\mu - r > \sigma^2$ — implies leverage. Cap by available leverage and counterparty limits.
- **Negative-edge case** ($bp < q$): Kelly says bet $0$ (don't play). Beware optimization software returning negative fractions you can't actually short.
- **Non-iid returns.** Real returns have time-varying $\mu, \sigma$, autocorrelation, regime shifts — classical Kelly assumes stationarity.
- **Drawdown vs growth.** Maximizing growth is not the same as minimizing risk of ruin under finite horizon / utility constraints.

## Applications in quant

- **Position-sizing** for systematic strategies: each signal has an edge and risk; Kelly suggests the natural scale.
- **Sportsbook & options market-making** classically use Kelly variants.
- **Hedge-fund capital allocation** across strategies often modeled as multi-asset Kelly.

## Applications in ML

- **Bandit problems**: Thompson-sampling allocation can be viewed as a Kelly-like log-growth criterion.
- **Reinforcement-learning bet sizing** when the reward is log of wealth.

## See also

- [Expectation and variance](../../core/probability/expectation-variance.md)
- [Mean-variance](./mean-variance.md)
- [Sharpe/Sortino](./sharpe-sortino.md)

## References

- Kelly (1956), "A New Interpretation of Information Rate."
- Thorp (2006), "The Kelly Criterion in Blackjack, Sports Betting, and the Stock Market."
- MacLean, Thorp & Ziemba (2010), *The Kelly Capital Growth Investment Criterion*.
