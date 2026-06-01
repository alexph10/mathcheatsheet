---
id: bayes-theorem
title: Bayes' Theorem
domain: core/probability
tags: [identity]
prerequisites: [random-variables]
used_by: []
difficulty: 1
status: draft
notebook: bayes-theorem.ipynb
---

# Bayes' Theorem

## TL;DR

$P(H \mid E) = P(E \mid H) P(H) / P(E)$ — inverts a conditional probability, letting you update beliefs from evidence.

## Definition

For events $A, B$ with $P(B) > 0$:

$$ P(A \mid B) = \frac{P(B \mid A)\, P(A)}{P(B)} $$

The denominator expands via the **law of total probability**: if $\{A_i\}$ partition the sample space,

$$ P(B) = \sum_i P(B \mid A_i) P(A_i). $$

For random variables with densities:

$$ p(\theta \mid x) = \frac{p(x \mid \theta)\, p(\theta)}{p(x)} = \frac{p(x \mid \theta)\, p(\theta)}{\int p(x \mid \theta')\, p(\theta')\, d\theta'} $$

## Intuition

The "Bayesian update" reads:

$$ \underbrace{p(\theta \mid x)}_{\text{posterior}} \propto \underbrace{p(x \mid \theta)}_{\text{likelihood}} \cdot \underbrace{p(\theta)}_{\text{prior}} $$

You start with a prior belief over hypotheses, observe data, and re-weight each hypothesis by how well it predicted the data. The normalizing constant $p(x)$ (the **evidence** or **marginal likelihood**) is often the hard part — many methods (MCMC, variational inference) exist precisely to avoid computing it.

## Key formulas

- **Bayes' rule:** as above.
- **Odds form** (often cleaner — no normalizer):

$$ \frac{P(H_1 \mid E)}{P(H_2 \mid E)} = \underbrace{\frac{P(E \mid H_1)}{P(E \mid H_2)}}_{\text{Bayes factor}} \cdot \frac{P(H_1)}{P(H_2)} $$

- **Sequential updates** (data $x_1, x_2, \ldots$ conditionally independent given $\theta$):

$$ p(\theta \mid x_{1:n}) \propto p(\theta) \prod_{i=1}^n p(x_i \mid \theta) $$

So the posterior after $n$ data points = prior $\times$ joint likelihood.

## Properties & identities

- **Posterior is a probability distribution** — it must integrate/sum to one. The proportionality form omits the normalizer but it's there implicitly.
- **Conjugacy:** for certain prior–likelihood pairs the posterior has the same family as the prior — closed-form updates (see [common-distributions.md](./common-distributions.md) for the conjugate table).
- **As data grows**, the posterior concentrates on the true parameter (Bernstein–von Mises) — prior influence vanishes.
- **Posterior predictive:**

$$ p(x_{\text{new}} \mid x_{1:n}) = \int p(x_{\text{new}} \mid \theta) p(\theta \mid x_{1:n})\, d\theta $$

## Worked micro-example

A disease has 1% prevalence. A test is 99% sensitive (true positive rate) and 95% specific (true negative rate). Given a positive test, what is the probability the patient has the disease?

Let $D$ = disease, $+$ = positive test.

$$ P(D \mid +) = \frac{P(+ \mid D) P(D)}{P(+ \mid D) P(D) + P(+ \mid \neg D) P(\neg D)} = \frac{0.99 \cdot 0.01}{0.99 \cdot 0.01 + 0.05 \cdot 0.99} \approx 0.167. $$

Only ~17% — the **base rate fallacy** in action. Even an accurate test produces mostly false positives when the disease is rare.

> See [companion notebook](./bayes-theorem.ipynb) for this example numerically, sequential updating of a Beta prior, and a visualization of the base-rate effect across prevalences.

## Common pitfalls

- **Confusing $P(A \mid B)$ with $P(B \mid A)$** — the asymmetry is the whole point of Bayes. "Sensitivity is not predictive value."
- **Ignoring the prior** (base-rate neglect) — see the disease example.
- **Improper priors** can yield improper posteriors; check integrability.
- **Selection bias in evidence:** conditioning on $E$ is only valid if $E$ was observed without filtering.

## Applications in ML

- **Naive Bayes classifiers** assume conditional independence of features given class.
- **Bayesian inference** for all model parameters (MCMC, variational inference, Laplace approximation).
- **Bayesian optimization** uses a posterior over the objective function to pick the next query.
- **Belief networks / probabilistic graphical models** propagate beliefs via repeated application of Bayes' rule.

## Applications in quant

- **Bayesian portfolio construction** (Black–Litterman) blends prior market equilibrium views with investor views.
- **Updating signal beliefs** as new market data arrives.
- **Risk model parameter estimation** with informative priors to stabilize small-sample covariance estimates.

## See also

- [Random variables](./random-variables.md)
- [Common distributions](./common-distributions.md) — conjugate-prior table
- Bayesian inference (forthcoming, in `crossover/`)

## References

- Wasserman, *All of Statistics*, §2.3.
- Gelman et al., *Bayesian Data Analysis*, Ch. 1.
