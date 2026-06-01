---
id: conditional-probability
title: Conditional Probability & Independence
domain: core/probability
tags: []
prerequisites: [random-variables]
used_by: []
difficulty: 1
status: draft
---

# Conditional Probability & Independence

## TL;DR

$P(A \mid B)$ is the probability of $A$ once you restrict the sample space to outcomes consistent with $B$ — it is the engine behind every Bayesian update, chain-rule factorization, and graphical model.

## Definition

For events $A, B$ in a probability space with $P(B) > 0$,

$$ P(A \mid B) = \frac{P(A \cap B)}{P(B)}. $$

The map $A \mapsto P(A \mid B)$ is itself a probability measure (it sums to 1 over a partition of the restricted sample space).

For random variables $X, Y$, the **conditional pmf/pdf** is

$$ p_{X \mid Y}(x \mid y) = \frac{p_{X,Y}(x, y)}{p_Y(y)} \quad (\text{whenever } p_Y(y) > 0). $$

## Intuition

Conditioning is a zoom-in: you discard everything inconsistent with the conditioning event, then renormalize so the remaining mass sums to 1. It is **not** counterfactual ("what if $B$ had happened") — it just reads off the proportions inside the slice of the sample space where $B$ does happen.

## Key formulas

**Multiplication / chain rule** (no independence required):

$$ P(A \cap B) = P(A \mid B)\, P(B) = P(B \mid A)\, P(A). $$

Generalized:

$$ P(A_1 \cap \cdots \cap A_n) = P(A_1) \prod_{i=2}^n P(A_i \mid A_1, \ldots, A_{i-1}). $$

**Law of total probability** (LTP). If $\{B_i\}$ partitions the sample space and each $P(B_i) > 0$:

$$ P(A) = \sum_i P(A \mid B_i)\, P(B_i). $$

For random variables this becomes the **marginalization** identity $p_X(x) = \sum_y p_{X \mid Y}(x \mid y)\, p_Y(y)$ (integral in the continuous case).

**Bayes' rule** (one line from the chain rule):

$$ P(B \mid A) = \frac{P(A \mid B)\, P(B)}{P(A)}. $$

See [Bayes' theorem](./bayes-theorem.md) for the full treatment.

## Independence

Events $A$ and $B$ are **independent** ($A \perp B$) iff

$$ P(A \cap B) = P(A) P(B) \iff P(A \mid B) = P(A) \quad (\text{when } P(B) > 0). $$

Random variables: $X \perp Y$ iff $p_{X,Y}(x, y) = p_X(x) p_Y(y)$ for all $x, y$.

**Mutual independence** of $A_1, \ldots, A_n$ requires the product rule to hold for **every** subset, not just pairs (pairwise independence does **not** imply mutual independence).

## Conditional independence

$X$ and $Y$ are conditionally independent given $Z$, written $X \perp Y \mid Z$, iff

$$ p_{X, Y \mid Z}(x, y \mid z) = p_{X \mid Z}(x \mid z) \, p_{Y \mid Z}(y \mid z) \quad \forall x, y, z. $$

Equivalently, $p_{X \mid Y, Z}(x \mid y, z) = p_{X \mid Z}(x \mid z)$ — given $Z$, knowing $Y$ adds no information about $X$. This is the **building block of graphical models** (Bayesian networks, HMMs).

Crucial subtleties:

- Marginal independence does **not** imply conditional independence (and vice versa).
- $X \perp Y$ and $X \perp Y \mid Z$ are logically independent statements.

## Worked micro-example

A test for a disease prevalent in 1% of a population has 95% sensitivity ($P(+ \mid D) = 0.95$) and 90% specificity ($P(- \mid \neg D) = 0.90$). What is $P(D \mid +)$?

By LTP: $P(+) = 0.95 \cdot 0.01 + 0.10 \cdot 0.99 = 0.0095 + 0.099 = 0.1085$.

By Bayes: $P(D \mid +) = (0.95 \cdot 0.01) / 0.1085 \approx 0.0876$ — about **8.8%**, not 95%. The low base rate dominates the high accuracy. This is the classic **base-rate fallacy**.

## Simpson's paradox (brief)

A trend that appears in each subgroup can **reverse** when the groups are pooled. Example: a drug might have a higher recovery rate than placebo for both men and women separately, yet a lower recovery rate overall, if treatment assignment was correlated with sex and sex itself affects recovery. Lesson: conditioning on confounders matters; aggregated probabilities are not summaries of conditional ones.

## Common pitfalls

- **$P(A \mid B) \neq P(B \mid A)$** (the **inverse fallacy**) — the prosecutor's fallacy and base-rate fallacy are both this confusion in disguise.
- **Conditioning on a zero-probability event** — undefined classically; needs measure-theoretic regular conditional probability (or a density argument).
- **Pairwise vs mutual independence** — three events can be pairwise independent yet not mutually independent (classic example: $A, B, A \triangle B$ on a uniform 4-element sample space).
- **"Independent" vs "disjoint"** — disjoint nontrivial events are **dependent**: if $A \cap B = \emptyset$, then $P(A \mid B) = 0$, not $P(A)$.
- **Ignoring the conditioning set** — Simpson-style reversals show why $P(A \mid B)$ alone is rarely a sufficient summary; you also need the conditioning structure.
- **Selection / survivorship bias** — implicitly conditioning on "observed" can flip apparent correlations (Berkson's paradox).

## Applications in ML

- **Naive Bayes** assumes feature conditional independence given the class label.
- **Probabilistic graphical models** (Bayesian networks, MRFs) factorize joint distributions through (conditional) independence structure.
- **Causal inference** relies on conditioning on the right covariates (back-door criterion); ignorability is a conditional-independence assumption.

## Applications in quant

- **Filtration-based pricing** — every conditional expectation $\mathbb{E}[X \mid \mathcal{F}_t]$ in martingale theory is a conditional probability in disguise.
- **Credit modeling** — joint default probabilities are built from marginals plus a (conditional) dependence structure (copulas).
- **Regime-switching models** condition observable dynamics on a latent regime.

## See also

- [Random variables](./random-variables.md)
- [Bayes' theorem](./bayes-theorem.md)
- [Expectation and variance](./expectation-variance.md) — the conditional expectation $\mathbb{E}[X \mid Y]$ is the analogue for random variables.
- [Covariance and correlation](./covariance-correlation.md) — uncorrelated $\neq$ independent.

## References

- Wasserman, *All of Statistics*, Ch. 1.
- Pearl, *Causality*, Ch. 1 (for the conditioning/causation distinction).
