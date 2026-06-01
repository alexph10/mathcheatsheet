---
id: var-cvar
title: Value-at-Risk and Conditional Value-at-Risk
domain: quant/risk
tags: [tail-risk, metric]
prerequisites: [random-variables, common-distributions]
used_by: []
difficulty: 2
status: draft
notebook: var-cvar.ipynb
---

# Value-at-Risk and Conditional Value-at-Risk

## TL;DR

**VaR** is the loss quantile at confidence level $\alpha$; **CVaR** is the expected loss beyond it. CVaR is the more honest tail metric — VaR is silent about *how* bad the bad days are.

## Definitions

Let $L$ be a loss random variable (positive = loss; $L = -\text{P\&L}$) over a fixed horizon (1 day, 10 days, …) at confidence level $\alpha \in (0, 1)$ (typically $0.95$ or $0.99$).

$$ \text{VaR}_\alpha(L) = \inf\{ x \in \mathbb{R} : \mathbb{P}(L \leq x) \geq \alpha \}, $$

i.e. the $\alpha$-quantile of the loss distribution.

$$ \text{CVaR}_\alpha(L) = \mathbb{E}[L \mid L \geq \text{VaR}_\alpha(L)] $$

(also called **Expected Shortfall**). For continuous $L$, equivalently

$$ \text{CVaR}_\alpha(L) = \frac{1}{1-\alpha} \int_{\alpha}^{1} \text{VaR}_u(L) \, du. $$

## Coherence

A risk measure $\rho$ is **coherent** if it is monotone, translation invariant, positively homogeneous, and **subadditive**: $\rho(L_1 + L_2) \leq \rho(L_1) + \rho(L_2)$.

- **VaR is not subadditive in general** — diversification can *increase* it. Hence VaR is not coherent.
- **CVaR is coherent** (Rockafellar & Uryasev, 2000) and convex in portfolio weights, so it plays nicely with optimization.

## Parametric (Normal) closed forms

If $L \sim \mathcal{N}(\mu_L, \sigma_L^2)$ (so P&L is Normal with mean $-\mu_L$), then with $z_\alpha = \Phi^{-1}(\alpha)$ and $\phi$ the standard normal PDF,

$$ \text{VaR}_\alpha = \mu_L + \sigma_L \, z_\alpha, \qquad \text{CVaR}_\alpha = \mu_L + \sigma_L \, \frac{\phi(z_\alpha)}{1-\alpha}. $$

For Student-$t_\nu$ losses with mean $\mu_L$ and scale $s$ (variance $s^2 \nu/(\nu-2)$),

$$ \text{VaR}_\alpha = \mu_L + s\, t_{\nu,\alpha}^{-1}, \qquad \text{CVaR}_\alpha = \mu_L + s\, \frac{\nu + (t_{\nu,\alpha}^{-1})^2}{\nu - 1} \cdot \frac{f_\nu(t_{\nu,\alpha}^{-1})}{1-\alpha}, $$

where $f_\nu, t_{\nu,\alpha}^{-1}$ are the standard Student-$t$ PDF and quantile.

## Estimation methods

| Method | How | Pros | Cons |
| ------ | --- | ---- | ---- |
| **Parametric** | Fit a [distribution](../../core/probability/common-distributions.md) (Normal, Student-$t$), use closed-form quantile. | Fast, smooth, low data needs. | Wrong distribution → systematic tail miss. |
| **Historical** | Empirical $\alpha$-quantile of past returns. | Assumption-free, captures realized non-normality. | Backward-looking; ignores regime change. |
| **Monte Carlo** | Simulate $L$ under a risk model, take sample quantile / tail average. | Flexible (any model, derivatives). | Slow; only as good as the model. |

CVaR estimate from samples: average the losses *above* the empirical VaR.

## Backtesting (Kupiec POF)

If true coverage is $\alpha$, the number of exceedances $X$ over $n$ days is $\text{Binomial}(n, 1-\alpha)$. The Kupiec proportion-of-failures test compares observed exceedance rate $\hat p = X/n$ to $1-\alpha$ via the LR statistic

$$ LR = -2 \ln \frac{(1-\alpha)^X \alpha^{n-X}}{\hat p^X (1-\hat p)^{n-X}} \;\overset{H_0}{\sim}\; \chi^2_1. $$

Reject the model if $LR$ exceeds the $\chi^2_1$ critical value.

## Worked micro-example

Daily P&L $\sim \mathcal{N}(0, 1\%)$. Then losses $L \sim \mathcal{N}(0, 0.01^2)$.

- $\text{VaR}_{0.95} = 0 + 0.01 \cdot 1.645 = 1.645\%$.
- $\text{CVaR}_{0.95} = 0 + 0.01 \cdot \phi(1.645)/0.05 = 0.01 \cdot 0.1031/0.05 \approx 2.063\%$.

So the average loss on the worst 5% of days is ~25% larger than the VaR threshold itself.

> See [companion notebook](./var-cvar.ipynb) for parametric vs historical vs Student-$t$ VaR/CVaR on simulated heavy-tailed returns.

## Common pitfalls

- **Sign convention.** Some texts define $L$ as gains; double-check whether you want the upper or lower tail.
- **Horizon scaling.** $\text{VaR}^{T\text{-day}} \approx \sqrt{T} \cdot \text{VaR}^{1\text{-day}}$ holds *only* for iid Normal returns with zero mean.
- **VaR cliff effect.** A 99% VaR ignores the worst 1% entirely — a $-1\text{M}$\$ loss and a $-1\text{B}$\$ loss look identical. Use CVaR.
- **Confidence ≠ probability of ruin.** A 99% 1-day VaR is exceeded once every 100 trading days on average — about 2.5×/year.
- **Stale or peaceful history** drastically under-estimates risk before regime breaks (2008, 2020).

## Limitations

- **Model risk.** Normal grossly under-states equity tail risk (true kurtosis $\gg 3$).
- **Tail dependence.** Linear correlation under-states co-crashes; copula models help.
- **Parameter uncertainty.** Quantile estimates have wide CIs in the tail where data is by definition scarce.
- **Liquidity & gap risk** are not captured by marginal-distribution metrics at all.

## Applications in quant

- **Basel III** uses 10-day 99% VaR (and increasingly Expected Shortfall) for market-risk capital.
- **Risk budgeting** across desks; CVaR-optimal portfolio construction (a tractable LP under historical scenarios).
- **Stress testing** as the deterministic complement.

## See also

- [Random variables](../../core/probability/random-variables.md)
- [Common distributions](../../core/probability/common-distributions.md) — Normal vs Student-$t$ tails.

## References

- Rockafellar & Uryasev, *Optimization of Conditional Value-at-Risk*, J. of Risk, 2000.
- McNeil, Frey & Embrechts, *Quantitative Risk Management*, Ch. 2 & 8.
- Jorion, *Value at Risk*, 3rd ed.
