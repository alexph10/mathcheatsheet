---
id: entropy
title: Entropy
domain: core/information-theory
tags: [inequality, divergence]
prerequisites: [random-variables, common-distributions]
used_by: []
difficulty: 2
status: draft
---

# Entropy

## TL;DR

Entropy measures the average uncertainty (or expected information content) of a random variable. Discrete: $H(X) = -\sum p(x) \log p(x)$. Continuous: $h(X) = -\int f(x) \log f(x)\, dx$. Maximized by the "most spread out" distribution allowed by the constraints.

## Definition

**Shannon entropy (discrete).** For $X$ with pmf $p$ on a countable support,

$$ H(X) = -\sum_{x} p(x) \log p(x) = \mathbb{E}[-\log p(X)]. $$

Convention $0 \log 0 = 0$. Base of the logarithm sets the unit: $\log_2 \to$ bits, $\ln \to$ nats.

**Differential entropy (continuous).** For $X$ with pdf $f$,

$$ h(X) = -\int f(x) \log f(x)\, dx. $$

**Joint, conditional, cross-entropy.** For discrete $X, Y$ and a second pmf $q$:

$$ H(X, Y) = -\sum_{x, y} p(x, y) \log p(x, y), $$

$$ H(Y \mid X) = -\sum_{x, y} p(x, y) \log p(y \mid x) = \mathbb{E}_X[H(Y \mid X = x)], $$

$$ H(p, q) = -\sum_x p(x) \log q(x). $$

## Intuition

Two readings of $H(X)$:

1. **Average surprise.** $-\log p(x)$ is the "surprise" of outcome $x$ (rare = surprising); $H$ averages it under the true distribution.
2. **Optimal code length.** $H(X)$ in bits is the expected number of bits per symbol of the best lossless code for iid draws of $X$ (Shannon's source coding theorem).

Conditional entropy $H(Y \mid X)$: residual uncertainty in $Y$ after observing $X$. It can only shrink with more information: $H(Y \mid X) \leq H(Y)$.

## Key formulas

**Chain rule.**

$$ H(X, Y) = H(X) + H(Y \mid X) = H(Y) + H(X \mid Y). $$

Generalizes: $H(X_1, \ldots, X_n) = \sum_i H(X_i \mid X_1, \ldots, X_{i-1})$.

**Mutual information.**

$$ I(X; Y) = H(X) + H(Y) - H(X, Y) = H(X) - H(X \mid Y) = D(p_{XY} \,\Vert\, p_X p_Y) \geq 0. $$

(See [KL divergence](./kl-divergence.md).)

**Cross-entropy ↔ KL.**

$$ H(p, q) = H(p) + D(p \,\Vert\, q), $$

so minimizing cross-entropy in $q$ at fixed $p$ is equivalent to minimizing KL — the basis of MLE for parametric models.

**Independence ⇔ additivity.** If $X \perp Y$: $H(X, Y) = H(X) + H(Y)$, $I(X; Y) = 0$.

## Properties & identities

- **Non-negativity (discrete).** $0 \leq H(X) \leq \log |\mathcal{X}|$, with the upper bound attained iff $p$ is uniform.
- **Differential entropy can be negative.** E.g. $h(\mathcal{N}(0, \sigma^2)) = \tfrac{1}{2} \log(2 \pi e \sigma^2)$ is negative for $\sigma^2 < 1/(2\pi e)$. Differences (KL, MI) remain well-behaved.
- **Concavity in $p$.** $p \mapsto H(p)$ is concave; Jensen's inequality (see [convexity](../optimization/convexity.md)) underlies most entropy inequalities.
- **Data processing.** For Markov $X \to Y \to Z$: $I(X; Z) \leq I(X; Y)$. Processing cannot create information.
- **Fano's inequality.** Bounds the error probability of predicting $X$ from $Y$ in terms of $H(X \mid Y)$.
- **Translation invariance (continuous).** $h(X + c) = h(X)$. Scaling: $h(aX) = h(X) + \log |a|$.

## Maximum-entropy distributions

Given a set of moment constraints, the distribution maximizing $H$ (or $h$) is the "most non-committal" one. Useful canonical results:

| Constraint | Maximum-entropy distribution |
| ---------- | ---------------------------- |
| Support on finite $\{1, \ldots, K\}$ | **Uniform** on $\{1, \ldots, K\}$; $H = \log K$ |
| Support on $[a, b]$, $f$ pdf | **Uniform**$(a, b)$; $h = \log(b - a)$ |
| Support $[0, \infty)$, mean $\mu$ | **Exponential**$(\lambda = 1/\mu)$; $h = 1 + \log \mu$ |
| Support $\mathbb{R}$, variance $\sigma^2$ | **Normal**$(\mu, \sigma^2)$; $h = \tfrac{1}{2}\log(2\pi e \sigma^2)$ |
| Support $\mathbb{R}^d$, covariance $\boldsymbol{\Sigma}$ | **Multivariate Normal** with covariance $\boldsymbol{\Sigma}$; $h = \tfrac{1}{2} \log\!\bigl((2\pi e)^d \det \boldsymbol{\Sigma}\bigr)$ |
| Support $\{0, 1, \ldots\}$, mean $\mu$ | **Geometric** with mean $\mu$ |

Proved by Lagrange multipliers on $-\int f \log f$ subject to the constraints; the result is always an exponential-family distribution.

## Worked micro-example

Bernoulli($p$) entropy (binary, base-2):

$$ H(p) = -p \log_2 p - (1-p) \log_2 (1 - p). $$

Maximum at $p = 1/2$ with $H = 1$ bit; goes to $0$ as $p \to 0$ or $1$. The function $H(p)$ is concave and symmetric around $1/2$ — the canonical "binary entropy" curve.

Numeric: $H(0.1) \approx 0.469$ bits, $H(0.5) = 1$ bit.

## Common pitfalls

- **Units matter.** $\log_2$ for bits, $\ln$ for nats. Cross-entropy losses in ML usually use natural log.
- **Differential entropy is not a limit of discrete entropy.** It can be negative and isn't reparameterization-invariant. KL and MI are; prefer them when comparing distributions.
- **Empirical entropy is biased.** Plug-in $\hat H = -\sum \hat p(x) \log \hat p(x)$ systematically underestimates $H$ when the support is large relative to sample size; corrections (Miller–Madow, NSB) help.
- **Joint entropy is not the sum** unless variables are independent — common error in deriving information identities.
- **Conditional entropy convention.** $H(Y \mid X) = \mathbb{E}_X[H(Y \mid X = x)]$, *not* $H(Y \mid X = x)$ for a specific $x$.

## Applications in ML

- **Cross-entropy loss** for classification = $H(p_{\text{data}}, q_\theta)$; minimizing it is MLE.
- **Maximum-entropy modelling** (MaxEnt, logistic regression as a special case) picks the least-committal model consistent with given moments.
- **Information bottleneck** trades $I(X; T)$ vs $I(T; Y)$ for a representation $T$.
- **Decision trees** split on features that maximize information gain $H(Y) - H(Y \mid X_{\text{split}})$.
- **Policy entropy regularization** in RL encourages exploration.

## Applications in quant

- **Entropic risk measure** $\rho(X) = \tfrac{1}{\gamma} \log \mathbb{E}[e^{-\gamma X}]$ comes from a dual formulation involving relative entropy.
- **Maximum-entropy calibration** of risk-neutral densities from option prices fills in unobserved strikes minimally.
- **Diversification index** based on portfolio-weight entropy $H(\mathbf{w}) = -\sum w_i \log w_i$ measures concentration.

## See also

- [Random variables](../probability/random-variables.md)
- [Common distributions](../probability/common-distributions.md)
- [KL divergence](./kl-divergence.md)

## References

- Cover & Thomas, *Elements of Information Theory*, Ch. 2, 8, 12.
- MacKay, *Information Theory, Inference, and Learning Algorithms*, Ch. 2, 4.
