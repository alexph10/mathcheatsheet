---
id: random-variables
title: Random Variables
domain: core/probability
tags: []
prerequisites: []
used_by: []
difficulty: 1
status: draft
---

# Random Variables

## TL;DR

A random variable is a function $X: \Omega \to \mathbb{R}$ assigning a number to each outcome of a random experiment; its distribution describes the probabilities of $X$ falling in various sets.

## Definition

Given a probability space $(\Omega, \mathcal{F}, P)$, a **random variable** is a measurable function $X: \Omega \to \mathbb{R}$ — meaning $\{ \omega : X(\omega) \leq x \} \in \mathcal{F}$ for every $x \in \mathbb{R}$.

Two flavors that cover almost all practice:

- **Discrete** — $X$ takes values in a countable set; characterized by the **probability mass function** $p_X(x) = P(X = x)$.
- **Continuous** — $X$ admits a **probability density function** $f_X$ with $P(X \in B) = \int_B f_X(x)\, dx$.

The **cumulative distribution function** (CDF) $F_X(x) = P(X \leq x)$ exists for both and is the unifying object.

## Intuition

Forget the measure-theoretic machinery on first pass: a random variable is "a number whose value is uncertain", and its distribution is "how the probability is spread across possible values".

- Discrete: think of a histogram with spikes.
- Continuous: think of a smooth curve where area = probability.

## Key formulas

- **CDF:** $F_X(x) = P(X \leq x)$, non-decreasing, right-continuous, with $\lim_{x \to -\infty} F = 0$, $\lim_{x \to \infty} F = 1$.
- **PMF / PDF relation to CDF:** $p_X(x) = F_X(x) - F_X(x^-)$ (discrete); $f_X(x) = F_X'(x)$ (continuous).
- **Expectation:**

$$ \mathbb{E}[X] = \sum_x x\, p_X(x) \quad \text{or} \quad \mathbb{E}[X] = \int_{-\infty}^\infty x\, f_X(x)\, dx $$

- **Variance:** $\text{Var}(X) = \mathbb{E}[(X - \mathbb{E}[X])^2] = \mathbb{E}[X^2] - \mathbb{E}[X]^2$.
- **Law of the unconscious statistician** (LOTUS): $\mathbb{E}[g(X)] = \int g(x) f_X(x)\, dx$ — no need to first derive the distribution of $g(X)$.
- **Change of variables** (continuous, $g$ monotone): if $Y = g(X)$, then $f_Y(y) = f_X(g^{-1}(y)) \left| \frac{d g^{-1}}{dy} \right|$.

## Properties & identities

- **Linearity of expectation:** $\mathbb{E}[aX + bY] = a \mathbb{E}[X] + b \mathbb{E}[Y]$ — **no independence required**.
- **Variance of a sum:** $\text{Var}(X + Y) = \text{Var}(X) + \text{Var}(Y) + 2 \text{Cov}(X, Y)$.
- **Scale:** $\text{Var}(aX) = a^2 \text{Var}(X)$.
- **Independence** $\Rightarrow$ $\mathbb{E}[XY] = \mathbb{E}[X]\mathbb{E}[Y]$ and $\text{Cov}(X, Y) = 0$. The converse fails in general.

## Worked micro-example

Roll a fair six-sided die; let $X$ be the result.

- $p_X(k) = 1/6$ for $k = 1, \ldots, 6$.
- $\mathbb{E}[X] = (1+2+\cdots+6)/6 = 3.5$.
- $\mathbb{E}[X^2] = (1+4+9+16+25+36)/6 = 91/6$.
- $\text{Var}(X) = 91/6 - 3.5^2 = 35/12 \approx 2.917$.

## Common pitfalls

- **$f_X(x)$ is not a probability** — it's a density. $f_X(x) > 1$ is allowed (e.g. Uniform on $[0, 0.5]$ has density $2$).
- **$P(X = x) = 0$ for continuous $X$** at any single point; only intervals carry probability.
- **Confusing independence with uncorrelation:** independence is strictly stronger.
- **Expectation can fail to exist** (e.g. Cauchy distribution) — always check integrability before quoting LLN/CLT.

## Applications in ML

- Every model output, every weight initialization, every dropout mask is a random variable.
- Loss = expectation of a per-sample loss under the data distribution; training minimizes an empirical estimate of this.

## Applications in quant

- Asset returns are modeled as random variables; expected return = $\mathbb{E}[R]$, risk = $\text{Var}(R)$ or higher moments.
- Option payoff is a random variable; price is a (risk-neutral) expectation.

## See also

- Common distributions (forthcoming)
- Expectation and variance — deeper (forthcoming)
- Bayes' theorem (forthcoming)
