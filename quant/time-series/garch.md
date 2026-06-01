---
id: garch
title: GARCH
domain: quant/time-series
tags: [stochastic-process]
prerequisites: [random-variables, common-distributions, expectation-variance]
used_by: []
difficulty: 2
status: draft
notebook: garch.ipynb
---

# GARCH

## TL;DR

A simple recursive model for **conditional volatility**: today's variance is a weighted combination of a long-run level, yesterday's squared shock, and yesterday's variance. It captures the empirical fact that big moves cluster.

## Setup

Daily returns:

$$ r_t = \mu + \sigma_t \varepsilon_t, \qquad \varepsilon_t \overset{\text{iid}}{\sim} \mathcal{N}(0, 1)\text{ (or Student-}t\text{)}. $$

The **GARCH(1,1)** model for the conditional variance is

$$ \boxed{\,\sigma_t^2 = \omega + \alpha\, r_{t-1}^2 + \beta\, \sigma_{t-1}^2\,} $$

with $\omega > 0$, $\alpha, \beta \geq 0$, and $\alpha + \beta < 1$ for covariance-stationarity. (The mean $\mu$ is often modeled separately or assumed zero.)

## Why these terms

- $\omega$: a positive baseline ensures $\sigma_t^2 > 0$.
- $\alpha$: weight on the most recent shock — captures the response to news.
- $\beta$: weight on yesterday's variance — captures persistence (the source of volatility clustering).

## Unconditional variance

If $\alpha + \beta < 1$, the long-run variance is

$$ \bar{\sigma}^2 = \frac{\omega}{1 - \alpha - \beta}. $$

Rewrite the recursion as a deviation from this:

$$ \sigma_t^2 - \bar{\sigma}^2 = \alpha (r_{t-1}^2 - \bar{\sigma}^2) + \beta (\sigma_{t-1}^2 - \bar{\sigma}^2). $$

## $h$-step ahead forecast

$$ \mathbb{E}[\sigma_{t+h}^2 \mid \mathcal{F}_t] = \bar{\sigma}^2 + (\alpha + \beta)^{h-1} (\sigma_{t+1}^2 - \bar{\sigma}^2). $$

Forecasts mean-revert to $\bar{\sigma}^2$ geometrically — slowly when $\alpha + \beta$ is close to 1.

## Estimation: MLE

Conditional log-likelihood for $T$ Gaussian-innovation observations:

$$ \ell(\omega, \alpha, \beta) = -\tfrac{1}{2}\sum_{t=1}^T \left( \log \sigma_t^2 + \frac{(r_t - \mu)^2}{\sigma_t^2} \right) + \text{const}. $$

Maximize numerically (`scipy.optimize.minimize` with constraints). Initialize $\sigma_1^2 = \bar{\sigma}^2$ from sample variance; iterate.

## Asymmetric extensions

| Model | Key idea |
|---|---|
| **GJR-GARCH** | Adds $\gamma\, r_{t-1}^2 \mathbf{1}[r_{t-1} < 0]$ — negative shocks raise vol more (leverage effect) |
| **EGARCH** | Log-volatility model: $\log \sigma_t^2 = \omega + \alpha (|z_{t-1}| - \mathbb{E}|z|) + \gamma z_{t-1} + \beta \log \sigma_{t-1}^2$ |
| **TGARCH** | Threshold-style; similar in spirit to GJR |
| **IGARCH** | $\alpha + \beta = 1$ (integrated; non-stationary) — like RiskMetrics |
| **FIGARCH** | Long memory via fractional differencing |
| **Multivariate** | DCC, BEKK for correlated assets |

## Worked micro-example

Pick $\omega = 0.00001$, $\alpha = 0.05$, $\beta = 0.94$ — typical for daily equity returns. Then $\bar{\sigma}^2 = 0.00001 / 0.01 = 10^{-3}$, so $\bar{\sigma} \approx 3.16\%$ per day, $\bar{\sigma}\sqrt{252} \approx 50\%$ annualized. Persistence $\alpha + \beta = 0.99$ means shocks decay slowly — half-life $\approx \log 2 / (-\log 0.99) \approx 69$ days.

> See [companion notebook](./garch.ipynb) for simulation, MLE estimation, and conditional-volatility tracking on a synthetic series.

## Common pitfalls

- **Stationarity constraint $\alpha + \beta < 1$** must be enforced in MLE (use bounds or reparameterize).
- **Initial variance** choice affects early forecasts; use sample variance or burn-in.
- **Gaussian innovations** under-estimate tail risk for real returns. Switch to Student-$t$ innovations (one extra parameter $\nu$) for fat tails.
- **Asymmetry matters** — symmetric GARCH misses leverage effect. GJR or EGARCH usually preferred for equities.
- **Misuse for forecasting horizons longer than weeks** — GARCH is best at short-horizon vol.

## Applications in quant

- **VaR / [CVaR](../risk/var-cvar.md)** computation with conditional variance instead of historical sample variance.
- **Option pricing** with stochastic vol approximations (GARCH option-pricing models).
- **Portfolio rebalancing triggers** based on realized vs forecasted vol.
- **RiskMetrics EWMA** is essentially GARCH(1,1) with $\omega = 0$, $\alpha + \beta = 1$.

## Applications in ML

- **Heteroscedastic regression** benchmarks (compare to learned variance heads).
- **Feature for downstream models** — the conditional-vol forecast is a useful input to direction-prediction models.

## See also

- [Common distributions](../../core/probability/common-distributions.md) — Normal vs Student-$t$ innovations
- [Expectation and variance](../../core/probability/expectation-variance.md)
- [Var/CVaR](../risk/var-cvar.md)

## References

- Bollerslev (1986), "Generalized Autoregressive Conditional Heteroskedasticity."
- Engle (1982), the original ARCH paper (Nobel-cited).
