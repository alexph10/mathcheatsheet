---
id: common-distributions
title: Common Probability Distributions
domain: core/probability
tags: [distribution]
prerequisites: [random-variables]
used_by: []
difficulty: 1
status: draft
notebook: common-distributions.ipynb
---

# Common Probability Distributions

## TL;DR

A reference card for the dozen distributions you'll meet 95% of the time in ML and quant — what they look like, when to reach for them, and their moments.

## Discrete distributions

| Distribution | Support | PMF $p(k)$ | $\mathbb{E}[X]$ | $\text{Var}(X)$ | Use when |
| ------------ | ------- | ---------- | --------------- | --------------- | -------- |
| **Bernoulli($p$)** | $\{0, 1\}$ | $p^k(1-p)^{1-k}$ | $p$ | $p(1-p)$ | Single binary outcome (coin flip). |
| **Binomial($n, p$)** | $\{0, \ldots, n\}$ | $\binom{n}{k} p^k (1-p)^{n-k}$ | $np$ | $np(1-p)$ | Number of successes in $n$ independent Bernoulli trials. |
| **Geometric($p$)** | $\{1, 2, \ldots\}$ | $(1-p)^{k-1} p$ | $1/p$ | $(1-p)/p^2$ | Number of trials until the first success. |
| **Poisson($\lambda$)** | $\{0, 1, 2, \ldots\}$ | $\dfrac{\lambda^k e^{-\lambda}}{k!}$ | $\lambda$ | $\lambda$ | Count of rare events in a fixed interval. |
| **Categorical($\boldsymbol{\pi}$)** | $\{1, \ldots, K\}$ | $\pi_k$ | — | — | One draw from $K$ classes (classification labels). |
| **Multinomial($n, \boldsymbol{\pi}$)** | $\{ \mathbf{k} : \sum k_i = n\}$ | $\frac{n!}{\prod k_i!} \prod \pi_i^{k_i}$ | $n\boldsymbol{\pi}$ | $n(\text{diag}(\boldsymbol{\pi}) - \boldsymbol{\pi}\boldsymbol{\pi}^\top)$ | Counts across $K$ categories in $n$ trials. |

## Continuous distributions

| Distribution | Support | PDF $f(x)$ | $\mathbb{E}[X]$ | $\text{Var}(X)$ | Use when |
| ------------ | ------- | ---------- | --------------- | --------------- | -------- |
| **Uniform($a, b$)** | $[a, b]$ | $1/(b-a)$ | $(a+b)/2$ | $(b-a)^2/12$ | No prior preference within an interval. |
| **Normal($\mu, \sigma^2$)** | $\mathbb{R}$ | $\frac{1}{\sigma\sqrt{2\pi}} e^{-(x-\mu)^2/(2\sigma^2)}$ | $\mu$ | $\sigma^2$ | Default for sums of small effects (CLT). |
| **Exponential($\lambda$)** | $[0, \infty)$ | $\lambda e^{-\lambda x}$ | $1/\lambda$ | $1/\lambda^2$ | Waiting time for a Poisson event; memoryless. |
| **Gamma($\alpha, \beta$)** | $[0, \infty)$ | $\frac{\beta^\alpha}{\Gamma(\alpha)} x^{\alpha-1} e^{-\beta x}$ | $\alpha/\beta$ | $\alpha/\beta^2$ | Sum of $\alpha$ iid Exponentials (when $\alpha$ integer). |
| **Beta($\alpha, \beta$)** | $[0, 1]$ | $\frac{x^{\alpha-1}(1-x)^{\beta-1}}{B(\alpha,\beta)}$ | $\alpha/(\alpha+\beta)$ | $\frac{\alpha\beta}{(\alpha+\beta)^2(\alpha+\beta+1)}$ | Distribution over a probability (Bayesian prior). |
| **Log-normal** | $(0, \infty)$ | $\frac{1}{x\sigma\sqrt{2\pi}} e^{-(\ln x - \mu)^2/(2\sigma^2)}$ | $e^{\mu + \sigma^2/2}$ | $(e^{\sigma^2}-1)e^{2\mu+\sigma^2}$ | Multiplicative noise; asset prices in GBM. |
| **Student-$t_\nu$** | $\mathbb{R}$ | $\propto (1 + x^2/\nu)^{-(\nu+1)/2}$ | $0$ (if $\nu > 1$) | $\nu/(\nu-2)$ (if $\nu > 2$) | Heavy-tailed returns; small-sample inference. |

## Multivariate

| Distribution | Support | Density | Mean | Covariance |
| ------------ | ------- | ------- | ---- | ---------- |
| **Multivariate Normal $\mathcal{N}(\boldsymbol{\mu}, \boldsymbol{\Sigma})$** | $\mathbb{R}^d$ | $(2\pi)^{-d/2} \lvert\boldsymbol{\Sigma}\rvert^{-1/2} \exp(-\tfrac{1}{2}(\mathbf{x}-\boldsymbol{\mu})^\top \boldsymbol{\Sigma}^{-1} (\mathbf{x}-\boldsymbol{\mu}))$ | $\boldsymbol{\mu}$ | $\boldsymbol{\Sigma}$ |
| **Dirichlet($\boldsymbol{\alpha}$)** | simplex | $\propto \prod x_i^{\alpha_i - 1}$ | $\alpha_i/\sum_j \alpha_j$ | — | conjugate prior for Categorical/Multinomial. |

## Key relationships

- **Bernoulli $\to$ Binomial:** sum of $n$ iid Bernoullis is Binomial$(n, p)$.
- **Binomial $\to$ Poisson:** Binomial$(n, p) \to$ Poisson$(np)$ as $n \to \infty$, $p \to 0$, $np$ fixed.
- **Binomial $\to$ Normal:** Binomial$(n, p) \approx \mathcal{N}(np, np(1-p))$ for large $n$ (CLT).
- **Exponential $\to$ Gamma:** sum of $k$ iid Exponential$(\lambda)$ is Gamma$(k, \lambda)$.
- **Normal $\to$ Log-normal:** $\ln X \sim \mathcal{N}(\mu, \sigma^2) \iff X \sim \text{Lognormal}(\mu, \sigma^2)$.

## Conjugate prior pairs (Bayesian)

| Likelihood | Conjugate prior | Posterior |
| ---------- | --------------- | --------- |
| Bernoulli / Binomial | Beta | Beta (update $\alpha \mathrel{+}{=} k$, $\beta \mathrel{+}{=} n - k$) |
| Categorical / Multinomial | Dirichlet | Dirichlet (update $\alpha_i \mathrel{+}{=} k_i$) |
| Poisson | Gamma | Gamma |
| Normal (known $\sigma^2$) | Normal | Normal |
| Normal (unknown $\mu, \sigma^2$) | Normal-Inverse-Gamma | Normal-Inverse-Gamma |

## Worked micro-example

You observe 7 heads in 10 coin flips. Under a Beta$(1,1)$ (uniform) prior, the posterior over the head probability is Beta$(1 + 7, 1 + 3) = $ Beta$(8, 4)$, with posterior mean $8/12 = 2/3$.

> See [companion notebook](./common-distributions.ipynb) for PDF/PMF plots of every distribution above and an interactive look at how parameters shape each one.

## Common pitfalls

- **Parameterization conventions vary** — `scipy.stats.gamma` uses shape and *scale* ($\theta = 1/\beta$), not rate. Always check.
- **"Normal" assumptions** often fail for financial returns — they have heavier tails (use Student-$t$).
- **Geometric** has two conventions: number of trials until first success ($\{1, 2, \ldots\}$) vs. number of failures before first success ($\{0, 1, \ldots\}$).
- **Multivariate Normal degenerate case:** if $\boldsymbol{\Sigma}$ is singular, density doesn't exist; the distribution lives on a lower-dimensional subspace.

## Applications in ML

- **Bernoulli / Categorical** for classification labels; their likelihoods become cross-entropy losses.
- **Normal** as noise model in regression (gives MSE loss) and as weight initialization.
- **Dirichlet / Categorical** in topic models (LDA).
- **Beta** as the principled prior over a click-through-rate.

## Applications in quant

- **Log-normal** for asset prices under geometric Brownian motion (Black-Scholes).
- **Student-$t$** as a fat-tailed return model.
- **Poisson** for trade arrival counts in market microstructure.
- **Multivariate Normal** for joint asset returns in portfolio theory.

## See also

- [Random variables](./random-variables.md)
- Bayes' theorem (forthcoming) for conjugate-update mechanics
- Central limit theorem (forthcoming) for why Normal is everywhere

## References

- Wasserman, *All of Statistics*, Ch. 2–3.
- Murphy, *Probabilistic Machine Learning*, Ch. 2.
