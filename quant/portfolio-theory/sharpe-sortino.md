---
id: sharpe-sortino
title: Sharpe, Sortino, and Risk-Adjusted Performance Ratios
domain: quant/portfolio-theory
tags: [metric]
prerequisites: [random-variables, expectation-variance, mean-variance]
used_by: []
difficulty: 1
status: draft
notebook: sharpe-sortino.ipynb
---

# Sharpe, Sortino, and Risk-Adjusted Performance Ratios

## TL;DR

Performance ratios divide excess return by a measure of risk to make strategies comparable. Sharpe uses total volatility; Sortino punishes only downside deviation; Information Ratio measures alpha per unit of tracking error.

## Definitions

Let $R_t$ be a strategy's return, $R_f$ the risk-free rate, and $R_b$ a benchmark return.

| Ratio | Formula | Risk measure |
|---|---|---|
| **Sharpe** | $\dfrac{\mathbb{E}[R - R_f]}{\sigma(R - R_f)}$ | Total volatility |
| **Sortino** | $\dfrac{\mathbb{E}[R - \tau]}{\sigma_{\text{down}}(R - \tau)}$ | Downside deviation below threshold $\tau$ |
| **Information Ratio** | $\dfrac{\mathbb{E}[R - R_b]}{\sigma(R - R_b)}$ | Tracking-error volatility |
| **Treynor** | $\dfrac{\mathbb{E}[R - R_f]}{\beta_{R, R_b}}$ | Market beta |
| **Calmar** | $\dfrac{\text{annual return}}{\text{max drawdown}}$ | Worst peak-to-trough |
| **Omega** | $\dfrac{\mathbb{E}[(R - \tau)^+]}{\mathbb{E}[(\tau - R)^+]}$ | Gain/loss ratio above threshold |

**Downside deviation** below threshold $\tau$:

$$ \sigma_{\text{down}}(R) = \sqrt{\mathbb{E}\!\left[\min(R - \tau, 0)^2\right]}. $$

## Annualization

For non-overlapping returns with sampling period $\Delta t$ years (e.g., $\Delta t = 1/252$ for daily):

- **Annualized mean:** $\hat{\mu}_{\text{annual}} = \hat{\mu} / \Delta t$ (or $(1+\hat{\mu})^{1/\Delta t} - 1$ for compounded).
- **Annualized vol:** $\hat{\sigma}_{\text{annual}} = \hat{\sigma} / \sqrt{\Delta t}$.
- **Annualized Sharpe:** $\widehat{SR}_{\text{annual}} = \widehat{SR} \cdot \sqrt{1/\Delta t}$.

For daily returns: multiply Sharpe by $\sqrt{252}$.

## Sample-Sharpe is itself random

If you have $T$ i.i.d. observations of returns:

$$ \text{Var}(\widehat{SR}) \approx \frac{1 + \tfrac{1}{2} SR^2}{T}. $$

So even a "true" Sharpe of 1 measured on 1 year of daily data ($T = 252$) has SD $\approx \sqrt{1.5/252} \approx 0.077$ — meaningful uncertainty.

With non-Gaussian (skewed, kurtotic) returns, the asymptotic variance grows further; Lo (2002) gives the correction. For autocorrelated returns, Sharpe is **overstated** if not adjusted (Sharpe per period stays right but annualization needs an $\sqrt{T}$ instead of $T$ scaling).

## Sharpe vs Sortino: when do they disagree?

- For symmetric, near-Normal returns: nearly identical (rescaling).
- For **positively skewed** strategies: Sortino is much higher than Sharpe.
- For **negatively skewed** strategies (typical: short-vol, picking up nickels in front of a steamroller): Sortino flags the asymmetry; Sharpe may look fine until a tail event.

> See [companion notebook](./sharpe-sortino.ipynb) for a side-by-side on Normal vs left-skewed return series.

## Comparing strategies / hypothesis tests

- **Sharpe difference** (Jobson-Korkie / Memmel correction) — proper test that adjusts for the covariance between the two estimators.
- **Probabilistic Sharpe Ratio** (Bailey & López de Prado) — probability that the true Sharpe exceeds a benchmark, accounting for skew/kurtosis.
- **Deflated Sharpe Ratio** — corrects for multiple-testing inflation when you tried many strategies.

## Common pitfalls

- **In-sample optimism.** Backtest Sharpe is biased upward; out-of-sample is typically far worse.
- **Autocorrelated returns** inflate Sharpe (e.g., illiquid assets with stale prices). Use Newey-West or fix the smoothing.
- **Heavy tails.** Volatility is a poor risk proxy when kurtosis is large; consider [VaR/CVaR](../risk/var-cvar.md) or Sortino.
- **Ignoring leverage.** Sharpe is leverage-invariant in theory but tail-risk explodes. Combine with max-drawdown / VaR.
- **Comparing different sample windows** invalidates Sharpe ordering.

## Applications in quant

- **Strategy selection** in fund of funds, allocator decisions.
- **Manager compensation** sometimes contractually tied to Sharpe or IR thresholds.
- **Live monitoring** of strategies — rolling Sharpe is a leading indicator of decay.

## See also

- [Mean-variance](./mean-variance.md)
- [Expectation and variance](../../core/probability/expectation-variance.md)
- [Var/CVaR](../risk/var-cvar.md)

## References

- Sharpe (1966, 1994).
- Lo (2002), "The Statistics of Sharpe Ratios."
- Bailey & López de Prado (2014), Deflated Sharpe Ratio.
