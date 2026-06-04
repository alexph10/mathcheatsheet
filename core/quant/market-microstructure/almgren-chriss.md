---
id: almgren-chriss
title: Almgren–Chriss Optimal Execution
domain: quant/market-microstructure
tags: [convex]
prerequisites: [convexity, mean-variance]
used_by: []
difficulty: 3
status: draft
notebook: almgren-chriss.ipynb
---

# Almgren–Chriss Optimal Execution

## TL;DR

You need to liquidate $X$ shares over a horizon $T$. Trade fast and you move the market against yourself (impact cost); trade slow and you bear price uncertainty (variance). Almgren–Chriss is the closed-form mean-variance optimal schedule.

## Setup

- Initial inventory: $X$ shares to sell over $[0, T]$, divided into $N$ steps of length $\tau = T/N$.
- Inventory at step $k$: $x_k$ (with $x_0 = X$, $x_N = 0$).
- Shares traded between steps: $n_k = x_{k-1} - x_k$ (so $\sum n_k = X$).

**Price dynamics with impact:**

- **Permanent impact** (changes the equilibrium price): each trade $n_k$ shifts price by $-\gamma n_k$.
- **Temporary impact** (only at execution): trading $n_k$ in $\tau$ time hits the trader at price $S_k - \eta (n_k / \tau)$.
- **Random walk** in the absence of trading: $S_k = S_{k-1} + \sigma \sqrt{\tau} \varepsilon_k$, $\varepsilon_k \sim \mathcal{N}(0,1)$.

## Cost decomposition

Total **implementation shortfall** is the difference between the value at the arrival price $S_0 X$ and the realized proceeds. Splitting:

$$ \mathbb{E}[\text{cost}] = \tfrac{1}{2}\gamma X^2 + \eta \sum_k \frac{n_k^2}{\tau}, \qquad \text{Var}(\text{cost}) = \sigma^2 \sum_k \tau\, x_k^2. $$

The permanent-impact term $\tfrac{1}{2}\gamma X^2$ is **constant** (depends only on total order, not schedule) — so we drop it from optimization.

## The optimization

Minimize expected cost plus a risk-aversion penalty $\lambda$ on variance:

$$ \min_{x_0, \ldots, x_N} \quad \eta \sum_{k=1}^N \frac{(x_{k-1} - x_k)^2}{\tau} + \lambda \sigma^2 \sum_{k=1}^N \tau\, x_k^2 \quad \text{s.t. } x_0 = X,\ x_N = 0. $$

This is a strictly [convex](../../core/optimization/convexity.md) quadratic program with linear endpoint constraints — closed-form solution exists.

## Closed-form trajectory

Define the **urgency parameter**

$$ \kappa^2 = \frac{\lambda \sigma^2}{\eta}\quad \text{(per-time-unit cost-of-variance to cost-of-impact ratio)}. $$

In the continuous-time limit ($\tau \to 0$), the optimal inventory path is

$$ \boxed{\, x(t) = X \cdot \frac{\sinh(\kappa (T - t))}{\sinh(\kappa T)} \,} $$

with trading rate

$$ v(t) = -\frac{dx}{dt} = X \kappa \cdot \frac{\cosh(\kappa(T - t))}{\sinh(\kappa T)}. $$

## Two limits

| Limit | Behavior | Schedule |
|---|---|---|
| $\lambda \to 0$ (risk-neutral) | $\kappa \to 0$, $\sinh / \sinh \to (T-t)/T$ | **Linear** (TWAP-like): uniform trading |
| $\lambda \to \infty$ (risk-averse) | $\kappa \to \infty$ | **Front-loaded**: dump quickly to avoid variance |

So $\lambda$ smoothly interpolates between minimum-cost (slow) and minimum-variance (fast).

## Efficient frontier of execution

Vary $\lambda$ and trace $(\mathbb{E}[\text{cost}], \text{Var}(\text{cost}))$. The locus is the **execution efficient frontier** — directly analogous to the [mean-variance](../portfolio-theory/mean-variance.md) frontier in portfolio theory, with cost playing the role of negative return.

> See [companion notebook](./almgren-chriss.ipynb) for inventory trajectories at several $\lambda$ and the execution efficient frontier plot.

## Extensions

- **Adaptive strategies** (Lo & Almgren): respond to realized price moves, not just fixed schedule.
- **Multi-asset / portfolio execution:** correlated $\Sigma$ replaces scalar $\sigma^2$; off-diagonal hedging trades naturally appear.
- **Nonlinear / sublinear impact:** $\eta v^\alpha$ with $\alpha \in (0.5, 1]$ — empirically $\alpha \approx 0.6$.
- **Dark pools, hidden orders** and execution algorithms (VWAP, POV, Implementation Shortfall).
- **Order-book models** (Obizhaeva-Wang, Cont): explicit liquidity replenishment dynamics.

## Common pitfalls

- **Calibrating $\eta$ and $\gamma$** requires intraday trade data; rough estimates use square-root law $\Delta p \propto \sigma \sqrt{Q / V}$.
- **Linear permanent impact** is an idealization; in practice impact has memory / decay.
- **Risk aversion $\lambda$** has no natural scale — express it in units of "$ per $^2$ of variance" relative to your book's tolerance.
- **Schedule is open-loop:** doesn't react to news mid-execution. Closed-loop / dynamic-programming versions exist (Bertsimas-Lo).
- **Short horizons (~minutes)** are dominated by order-book dynamics; AC is best for hours-to-days execution.

## Applications in quant

- **Execution algos** at sell-side desks (broker algos: VWAP, IS, POV, AC).
- **Buy-side trading cost analysis** (TCA) benchmarks fills against AC-style optimal cost.
- **Transaction cost models** for backtesting: realistic strategies must include execution cost, not just slippage estimates.

## See also

- [Convexity](../../core/optimization/convexity.md)
- [Mean-variance](../portfolio-theory/mean-variance.md) — same trade-off structure

## References

- Almgren & Chriss (2000), "Optimal Execution of Portfolio Transactions."
- Gatheral & Schied (2013), *Optimal Trade Execution* (survey).
