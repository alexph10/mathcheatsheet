---
id: expectation-variance
title: Expectation, Variance & Moments
domain: core/probability
tags: []
prerequisites: [random-variables, common-distributions]
used_by: []
difficulty: 1
status: draft
notebook: expectation-variance.ipynb
---

# Expectation, Variance & Moments

## TL;DR

Expectation is the probability-weighted mean of a random variable, variance is its mean squared deviation from the mean, and the moment-generating function packs every moment into a single transform.

## Definition

For a random variable $X$ with pmf $p$ (discrete) or pdf $f$ (continuous):

$$ \mathbb{E}[X] = \sum_x x\, p(x) \quad \text{or} \quad \int_{-\infty}^\infty x\, f(x)\, dx, $$

assuming the sum/integral converges absolutely. The **variance** is

$$ \text{Var}(X) = \mathbb{E}\!\left[(X - \mathbb{E}[X])^2\right] = \mathbb{E}[X^2] - (\mathbb{E}[X])^2 \geq 0, $$

and the **standard deviation** is $\sigma_X = \sqrt{\text{Var}(X)}$.

## Law of the unconscious statistician (LOTUS)

For any (measurable) $g$, you do **not** need the distribution of $g(X)$:

$$ \mathbb{E}[g(X)] = \sum_x g(x)\, p(x) \quad \text{or} \quad \int g(x)\, f(x)\, dx. $$

This is the workhorse identity: every other expectation formula below is a special case.

## Key formulas

**Linearity of expectation** (holds **without** any independence assumption):

$$ \mathbb{E}[aX + bY + c] = a\,\mathbb{E}[X] + b\,\mathbb{E}[Y] + c. $$

**Variance under affine transforms:**

$$ \text{Var}(aX + b) = a^2 \, \text{Var}(X). $$

**Variance of a sum:**

$$ \text{Var}(X + Y) = \text{Var}(X) + \text{Var}(Y) + 2\,\text{Cov}(X, Y). $$

If $X \perp Y$ (or merely uncorrelated), the cross term vanishes and variances simply add.

**Iterated expectation / tower property:**

$$ \mathbb{E}[X] = \mathbb{E}\!\left[ \mathbb{E}[X \mid Y] \right]. $$

**Law of total variance:**

$$ \text{Var}(X) = \mathbb{E}\!\left[\text{Var}(X \mid Y)\right] + \text{Var}\!\left(\mathbb{E}[X \mid Y]\right). $$

## Higher moments

The $k$-th **raw moment** is $\mu_k' = \mathbb{E}[X^k]$; the $k$-th **central moment** is $\mu_k = \mathbb{E}[(X - \mu)^k]$. Standardized shape descriptors:

| Moment | Formula | Tells you |
| ------ | ------- | --------- |
| Mean | $\mu = \mathbb{E}[X]$ | Location |
| Variance | $\sigma^2 = \mathbb{E}[(X-\mu)^2]$ | Spread |
| Skewness | $\gamma_1 = \mathbb{E}[(X-\mu)^3] / \sigma^3$ | Asymmetry (right-tail if $> 0$) |
| Excess kurtosis | $\gamma_2 = \mathbb{E}[(X-\mu)^4] / \sigma^4 - 3$ | Tail heaviness vs Normal |

Normal has skewness $0$ and excess kurtosis $0$. Financial returns typically show negative skew and positive excess kurtosis ("fat tails").

## Moment-generating and characteristic functions

The **moment-generating function** (MGF), when it exists in a neighborhood of $0$:

$$ M_X(t) = \mathbb{E}\!\left[e^{tX}\right], \qquad \mathbb{E}[X^k] = M_X^{(k)}(0). $$

Properties:

- **Independence $\Rightarrow$ MGFs multiply:** $M_{X+Y}(t) = M_X(t)\, M_Y(t)$ if $X \perp Y$.
- **Affine:** $M_{aX + b}(t) = e^{bt} M_X(at)$.
- **Uniqueness:** if two distributions share an MGF on a neighborhood of $0$, they are equal — handy for proving distributional results (e.g., Binomial $\to$ Normal).

The **characteristic function** $\varphi_X(t) = \mathbb{E}[e^{itX}]$ always exists (bounded by 1) and serves the same role when the MGF does not — required for Cauchy, stable laws, and rigorous CLT proofs.

A few common MGFs (parameter conventions match [common-distributions](./common-distributions.md)):

| $X$ | $M_X(t)$ |
| --- | -------- |
| Bernoulli($p$) | $1 - p + p e^t$ |
| Binomial($n, p$) | $(1 - p + p e^t)^n$ |
| Poisson($\lambda$) | $\exp(\lambda(e^t - 1))$ |
| Normal($\mu, \sigma^2$) | $\exp(\mu t + \tfrac{1}{2}\sigma^2 t^2)$ |
| Exponential($\lambda$) | $\lambda / (\lambda - t)$ for $t < \lambda$ |

## Useful inequalities

- **Markov:** for $X \geq 0$, $a > 0$, $\;P(X \geq a) \leq \mathbb{E}[X]/a$.
- **Chebyshev:** $P(|X - \mu| \geq k\sigma) \leq 1/k^2$.
- **Jensen:** for convex $\varphi$, $\;\varphi(\mathbb{E}[X]) \leq \mathbb{E}[\varphi(X)]$.

Tighter exponential tail bounds derived from MGFs (Chernoff, Hoeffding) live in [concentration-inequalities](./concentration-inequalities.md).

## Worked micro-example

Let $X \sim \text{Binomial}(10, 0.3)$. Then $\mathbb{E}[X] = np = 3$ and $\text{Var}(X) = np(1-p) = 2.1$. Differentiating the MGF $M_X(t) = (0.7 + 0.3 e^t)^{10}$ at $t = 0$ gives the same mean; the second derivative at $0$ gives $\mathbb{E}[X^2] = 11.1$, recovering $\text{Var}(X) = 11.1 - 9 = 2.1$. ✓

> See [companion notebook](./expectation-variance.ipynb) for a Monte Carlo check of linearity (dependent case) and of $\text{Var}(X+Y)$ vs the analytic formula.

## Common pitfalls

- **Linearity does not need independence** — students often add a needless "if independent" caveat to $\mathbb{E}[X + Y] = \mathbb{E}[X] + \mathbb{E}[Y]$.
- **Variance is not linear** — $\text{Var}(aX) = a^2 \text{Var}(X)$, and variances of sums add only for uncorrelated variables.
- **$\mathbb{E}[1/X] \neq 1/\mathbb{E}[X]$** (Jensen's inequality goes the other way for convex $1/x$).
- **Undefined moments** — Cauchy has no mean; Student-$t_\nu$ has no variance when $\nu \leq 2$. Always check existence before invoking the LLN/CLT.
- **MGF need not exist** (e.g., log-normal, Cauchy) — fall back to characteristic functions.
- **Sample mean / variance vs population** — sample variance with denominator $n-1$ is unbiased; with $n$ it is the MLE but biased.

## Applications in ML

- **Loss functions** are expectations: MSE is $\mathbb{E}[(Y - \hat Y)^2]$, cross-entropy is $-\mathbb{E}[\log p(Y)]$.
- **Bias-variance decomposition** of expected prediction error uses linearity and the law of total variance. See [bias-variance](../../ml/evaluation/bias-variance.md).
- **Variance reduction** in Monte Carlo (control variates, antithetic sampling) targets $\text{Var}(\hat\theta)$ directly.
- **REINFORCE / score-function estimators** in RL rely on identities involving $\mathbb{E}[\nabla \log p_\theta \cdot R]$.

## Applications in quant

- **Risk metrics** — volatility (standard deviation), skew, and kurtosis describe return distributions.
- **Sharpe ratio** $= \mathbb{E}[R - r_f] / \sigma_R$. See [sharpe-sortino](../../quant/portfolio-theory/sharpe-sortino.md).
- **Risk-neutral pricing** computes derivative prices as expectations under an equivalent martingale measure.
- **Method of moments** in econometrics matches sample moments to theoretical moments to estimate parameters.

## See also

- [Random variables](./random-variables.md)
- [Common distributions](./common-distributions.md)
- [Conditional probability](./conditional-probability.md) (for the tower property)
- [Covariance and correlation](./covariance-correlation.md)
- [Concentration inequalities](./concentration-inequalities.md)

## References

- Wasserman, *All of Statistics*, Ch. 3–4.
- Grimmett & Stirzaker, *Probability and Random Processes*, Ch. 3–5.
