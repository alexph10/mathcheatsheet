---
id: concentration-inequalities
title: Concentration Inequalities
domain: core/probability
tags: [inequality, concentration]
prerequisites: [random-variables, common-distributions, clt-lln]
used_by: []
difficulty: 2
status: draft
notebook: concentration-inequalities.ipynb
---

# Concentration Inequalities

## TL;DR

Non-asymptotic tail bounds — they tell you how rare it is for a random variable (often a sum or function of many independent RVs) to deviate far from its mean. Foundational for statistical learning theory and confidence-bound algorithms (UCB).

## Hierarchy from loose to tight

| Inequality | Statement | When to use |
|---|---|---|
| **Markov** | $P(X \geq t) \leq \mathbb{E}[X]/t$ for $X \geq 0$ | Crude bound; only needs the mean. |
| **Chebyshev** | $P(|X - \mu| \geq t) \leq \sigma^2 / t^2$ | Have variance; no other info. |
| **Chernoff** | $P(X \geq t) \leq \inf_{s>0} \mathbb{E}[e^{sX}] e^{-st}$ | Have an MGF; foundational technique. |
| **Hoeffding** | $P(\bar{X}_n - \mu \geq t) \leq \exp\!\left(-\dfrac{2nt^2}{(b-a)^2}\right)$ for bounded $X_i \in [a, b]$ | Sub-Gaussian bound for bounded RVs. |
| **Bernstein** | $P(\bar{X}_n - \mu \geq t) \leq \exp\!\left(-\dfrac{nt^2}{2\sigma^2 + 2bt/3}\right)$ for bounded $X_i$, var $\sigma^2$ | Tighter than Hoeffding when $\sigma^2 \ll (b-a)^2$. |
| **McDiarmid** | For $f(X_1,\ldots,X_n)$ with bounded differences $c_i$: $P(f - \mathbb{E}f \geq t) \leq \exp\!\left(-\dfrac{2t^2}{\sum c_i^2}\right)$ | Function of independent RVs. |
| **Matrix Chernoff / Bernstein** | Same shape for sums of random PSD matrices | Random-matrix theory. |

## Sub-Gaussian framework (unifies many bounds)

A random variable $X$ is **$\sigma$-sub-Gaussian** if $\mathbb{E}[e^{s(X - \mathbb{E}X)}] \leq e^{s^2 \sigma^2 / 2}$ for all $s \in \mathbb{R}$. Implications:

- $P(|X - \mathbb{E}X| \geq t) \leq 2 e^{-t^2/(2\sigma^2)}$.
- Sums: if $X_i$ are independent and $\sigma_i$-sub-Gaussian, $\sum X_i$ is $\sqrt{\sum \sigma_i^2}$-sub-Gaussian.
- Bounded $X \in [a, b]$ is $\tfrac{b-a}{2}$-sub-Gaussian (gives Hoeffding).
- Gaussian $\mathcal{N}(0, \sigma^2)$ is $\sigma$-sub-Gaussian.

**Sub-exponential** RVs (heavier tails) get Bernstein-type bounds.

## Intuition

The CLT tells you the asymptotic rate $1/\sqrt{n}$ but says nothing about how big $n$ must be. Concentration inequalities give explicit, finite-$n$ bounds — essential when you need a confidence radius for a specific sample size.

## Worked micro-example

Toss a fair coin $n$ times; $X_i \in \{0, 1\}$, $\bar{X}_n$ = sample mean. We want $P(|\bar{X}_n - 0.5| \geq 0.1)$.

- **Chebyshev** ($\sigma^2 = 0.25$): $\leq 0.25 / (n \cdot 0.01) = 25/n$.
- **Hoeffding** ($b - a = 1$): $\leq 2 \exp(-2n \cdot 0.01) = 2 e^{-0.02 n}$.
- For $n = 100$: Chebyshev $\leq 0.25$, Hoeffding $\leq 2 e^{-2} \approx 0.27$. Roughly comparable here.
- For $n = 500$: Chebyshev $\leq 0.05$, Hoeffding $\leq 2 e^{-10} \approx 9 \times 10^{-5}$. **Hoeffding crushes Chebyshev** at moderate $n$.

> See [companion notebook](./concentration-inequalities.ipynb) for a numerical comparison of Markov / Chebyshev / Hoeffding bounds against the true Binomial tail.

## Common pitfalls

- **Markov/Chebyshev are usually badly loose** — useful only as theoretical scaffolding or when you have very little distribution info.
- **Hoeffding requires bounded support;** unbounded RVs need sub-Gaussian / sub-exponential assumptions.
- **Independence is required** for most of these. Martingale-difference versions (Azuma, Freedman) cover dependent cases.
- **One-sided vs two-sided** factor of 2 matters when reporting confidence.

## Applications in ML

- **PAC learning bounds** use Hoeffding / McDiarmid to bound generalization error.
- **UCB algorithm** in [multi-armed bandits](../../crossover/game-theory/multi-armed-bandits.md) uses Hoeffding-style confidence radii: $\hat{\mu}_a + \sqrt{2 \log T / n_a}$.
- **Empirical Rademacher complexity** bounds rely on McDiarmid.

## Applications in quant

- **Sample Sharpe-ratio confidence intervals** (sub-Gaussian assumptions can be problematic for fat-tailed returns — heavier-tail inequalities apply).
- **Sample size requirements** for Monte-Carlo pricing: how many paths $n$ to bound MC error?

## See also

- [Central limit theorem and LLN](./clt-lln.md)
- [Common distributions](./common-distributions.md)
- [Multi-armed bandits](../../crossover/game-theory/multi-armed-bandits.md)
