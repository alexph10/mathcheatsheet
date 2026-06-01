---
id: clt-lln
title: Law of Large Numbers & Central Limit Theorem
domain: core/probability
tags: [inequality]
prerequisites: [random-variables, common-distributions]
used_by: []
difficulty: 2
status: draft
notebook: clt-lln.ipynb
---

# Law of Large Numbers & Central Limit Theorem

## TL;DR

LLN: the sample mean of iid draws converges to the true mean. CLT: it does so at rate $1/\sqrt{n}$, and the fluctuation, properly rescaled, is asymptotically Normal — regardless of the underlying distribution (given finite variance).

## Definition

Let $X_1, X_2, \ldots$ be iid with $\mathbb{E}[X_i] = \mu$ and (where required) $\operatorname{Var}(X_i) = \sigma^2 < \infty$. Let $\bar X_n = \tfrac{1}{n}\sum_{i=1}^n X_i$.

**Weak law of large numbers (WLLN).** Convergence in probability:

$$ \bar X_n \xrightarrow{P} \mu, \quad\text{i.e.}\quad \Pr\!\bigl(|\bar X_n - \mu| > \varepsilon\bigr) \to 0 \ \ \forall \varepsilon > 0. $$

Holds whenever $\mathbb{E}|X_1| < \infty$.

**Strong law of large numbers (SLLN).** Almost-sure convergence:

$$ \bar X_n \xrightarrow{\text{a.s.}} \mu, \quad\text{i.e.}\quad \Pr\!\bigl(\lim_n \bar X_n = \mu\bigr) = 1. $$

Also holds under $\mathbb{E}|X_1| < \infty$ (Kolmogorov).

**Central limit theorem (CLT).** With finite variance,

$$ \sqrt{n}\,\frac{\bar X_n - \mu}{\sigma} \xrightarrow{d} \mathcal{N}(0, 1), \qquad \text{equivalently} \qquad \bar X_n \approx \mathcal{N}\!\left(\mu, \tfrac{\sigma^2}{n}\right) \ \text{for large } n. $$

## Intuition

LLN says the *average* stabilizes — randomness averages out. CLT says the *scaled deviation* of that average looks Gaussian no matter what the input distribution was; that's why the Normal distribution shows up everywhere there are sums of many small independent influences.

Two distinct convergence statements:
- **Almost sure** (strong): individual sample paths $n \mapsto \bar X_n(\omega)$ settle to $\mu$.
- **In distribution** (CLT): the *distribution* of $\sqrt{n}(\bar X_n - \mu)$ stabilizes.

## Key formulas

- **Sample-mean variance:** $\operatorname{Var}(\bar X_n) = \sigma^2 / n$.
- **Standard error:** $\operatorname{SE}(\bar X_n) = \sigma / \sqrt{n}$.
- **Asymptotic CI (95%):** $\bar X_n \pm 1.96 \cdot \hat\sigma / \sqrt{n}$.
- **Berry–Esseen bound** (rate of CLT, $\mathbb{E}|X_1|^3 < \infty$):

$$ \sup_z \left| \Pr\!\Bigl( \tfrac{\sqrt n (\bar X_n - \mu)}{\sigma} \leq z \Bigr) - \Phi(z) \right| \leq \frac{C \, \mathbb{E}|X_1 - \mu|^3}{\sigma^3 \sqrt n}, \qquad C \approx 0.47. $$

## Properties & identities

- **Lindeberg–Lévy CLT** is the iid + finite-variance version above.
- **Lindeberg condition** generalizes to triangular arrays $\{X_{n,i}\}_{i=1}^{k_n}$ that are independent but not identically distributed: if $s_n^2 = \sum_i \operatorname{Var}(X_{n,i})$ and for every $\varepsilon > 0$

$$ \frac{1}{s_n^2} \sum_{i=1}^{k_n} \mathbb{E}\!\left[(X_{n,i} - \mu_{n,i})^2 \mathbf{1}\{|X_{n,i} - \mu_{n,i}| > \varepsilon s_n\}\right] \to 0, $$

  then $s_n^{-1} \sum_i (X_{n,i} - \mu_{n,i}) \xrightarrow{d} \mathcal{N}(0,1)$. The condition says no single term dominates the variance.
- **Continuous mapping theorem.** If $Y_n \xrightarrow{d} Y$ and $g$ is continuous (at the support of $Y$), then $g(Y_n) \xrightarrow{d} g(Y)$. Same for $\xrightarrow{P}$ and $\xrightarrow{\text{a.s.}}$.
- **Delta method.** If $\sqrt{n}(\hat\theta_n - \theta) \xrightarrow{d} \mathcal{N}(0, \sigma^2)$ and $g$ is differentiable with $g'(\theta) \neq 0$, then

$$ \sqrt{n}\,(g(\hat\theta_n) - g(\theta)) \xrightarrow{d} \mathcal{N}(0,\, g'(\theta)^2 \sigma^2). $$

- **Slutsky.** $X_n \xrightarrow{d} X$ and $Y_n \xrightarrow{P} c$ ⇒ $X_n + Y_n \xrightarrow{d} X + c$, $X_n Y_n \xrightarrow{d} c X$.
- **Multivariate CLT.** $\sqrt{n}(\bar{\mathbf{X}}_n - \boldsymbol\mu) \xrightarrow{d} \mathcal{N}(\mathbf{0}, \boldsymbol\Sigma)$ where $\boldsymbol\Sigma = \operatorname{Cov}(\mathbf{X}_1)$.

## Worked micro-example

Roll a fair six-sided die $n$ times. $\mu = 3.5$, $\sigma^2 = 35/12 \approx 2.917$. For $n = 100$:

$$ \operatorname{SE}(\bar X_{100}) = \sqrt{2.917/100} \approx 0.171. $$

A 95% interval around the true mean is $3.5 \pm 1.96 \cdot 0.171 = [3.165, 3.835]$. Observe an average outside this range with probability $\approx 5\%$, *even though the die outputs are discrete and decidedly non-Normal* — CLT only requires finite variance.

> See [companion notebook](./clt-lln.ipynb) for sample-mean convergence and CLT histograms across distributions.

## Common pitfalls

- **CLT requires finite variance.** For heavy-tailed $X$ (e.g. Cauchy, Pareto with tail index $\alpha \leq 2$), the sample mean does *not* concentrate at the usual $\sqrt{n}$ rate; instead a *stable* limit law applies.
- **iid is sufficient, not necessary** — CLT versions exist for weakly dependent and triangular-array data (Lindeberg, martingale CLT) but require extra conditions.
- **"Large $n$" is distribution-dependent.** Highly skewed distributions need much bigger $n$ before $\bar X_n$ looks Gaussian; the Berry–Esseen rate $1/\sqrt{n}$ is sharp but the constant depends on $\mathbb{E}|X|^3/\sigma^3$.
- **Don't confuse CLT with LLN.** LLN says $\bar X_n \to \mu$ (a point); CLT describes the *distribution* of its $\sqrt{n}$-rescaled deviation.
- **Plug-in variance** is fine asymptotically (Slutsky) but adds finite-sample error; for small $n$ use Student-$t$ for Normal data or bootstrap otherwise.

## Applications in ML

- **Confidence intervals on test-set metrics** (accuracy, AUC) use CLT-based standard errors.
- **Monte Carlo expectations** $\hat\mu = \tfrac{1}{n}\sum g(X_i)$ converge at rate $1/\sqrt{n}$ regardless of input dimension — the basis of MC integration.
- **SGD averaging (Polyak–Ruppert):** the time-averaged iterate is asymptotically Normal around the optimum.
- **Bootstrap** justification rests on CLT-like behavior of the empirical distribution.

## Applications in quant

- **Diversification:** portfolio of $n$ uncorrelated assets has variance scaling like $1/n$ — direct LLN.
- **VaR backtesting** uses CLT-based binomial-Normal approximations for exception counts.
- **Sharpe-ratio standard error** $\approx \sqrt{(1 + S^2/2)/n}$ comes from a delta-method CLT.
- **Brownian motion** as the scaling limit of random walks is a functional (Donsker) version of the CLT.

## See also

- [Random variables](./random-variables.md)
- [Common distributions](./common-distributions.md)
- [Bayes' theorem](./bayes-theorem.md)

## References

- Wasserman, *All of Statistics*, Ch. 5.
- Billingsley, *Probability and Measure*, Ch. 27 (CLT).
- Durrett, *Probability: Theory and Examples*, Ch. 3.
