---
id: kl-divergence
title: Kullback–Leibler Divergence
domain: core/information-theory
tags: [inequality, divergence]
prerequisites: [entropy, common-distributions]
used_by: []
difficulty: 2
status: draft
notebook: kl-divergence.ipynb
---

# Kullback–Leibler Divergence

## TL;DR

$D(P \,\Vert\, Q) = \mathbb{E}_P[\log (p/q)]$ measures how much $Q$ misrepresents $P$. Always $\geq 0$, zero iff $P = Q$, but asymmetric and not a metric. It's the gap between the cross-entropy of using code $Q$ for source $P$ and the optimal entropy.

## Definition

For probability measures $P, Q$ on the same space with $P \ll Q$ (absolute continuity):

$$ D(P \,\Vert\, Q) = \mathbb{E}_P\!\left[\log \frac{dP}{dQ}\right]. $$

**Discrete:**

$$ D(P \,\Vert\, Q) = \sum_x p(x) \log \frac{p(x)}{q(x)}. $$

**Continuous:**

$$ D(P \,\Vert\, Q) = \int p(x) \log \frac{p(x)}{q(x)}\, dx. $$

Conventions: $0 \log (0/q) = 0$; $p \log(p/0) = \infty$ for $p > 0$. So $D = \infty$ whenever $P$ puts mass where $Q$ does not.

## Intuition

Three equivalent readings:

1. **Coding overhead.** Bits wasted per symbol when you compress samples of $P$ with a code optimal for $Q$.
2. **Likelihood-ratio expectation.** $D(P \,\Vert\, Q) = \mathbb{E}_P[\log L]$ where $L = p/q$; concentrates as samples accumulate and rules out the wrong model (Stein's lemma).
3. **Statistical distance** (in spirit). $D$ is non-negative, vanishes iff $P = Q$, but is asymmetric and violates the triangle inequality. Square-root of (twice) KL bounds total variation: $\text{TV}(P, Q) \leq \sqrt{\tfrac{1}{2} D(P \,\Vert\, Q)}$ (Pinsker).

## Key formulas

**Gibbs' inequality (non-negativity).**

$$ D(P \,\Vert\, Q) \geq 0, \qquad \text{with equality iff } P = Q \text{ (a.e.)}. $$

Proof: $-\log$ is convex; apply Jensen to $\mathbb{E}_P[-\log(q/p)]$.

**Relation to entropy and cross-entropy.**

$$ D(P \,\Vert\, Q) = H(P, Q) - H(P), \qquad H(P, Q) = -\mathbb{E}_P[\log q]. $$

So minimizing $H(P, Q)$ in $Q$ (cross-entropy loss) ≡ minimizing $D(P \,\Vert\, Q)$ ≡ MLE under $Q_\theta$.

**Chain rule.** For joint distributions $P_{XY}, Q_{XY}$:

$$ D(P_{XY} \,\Vert\, Q_{XY}) = D(P_X \,\Vert\, Q_X) + \mathbb{E}_{P_X}\!\bigl[D(P_{Y|X} \,\Vert\, Q_{Y|X})\bigr]. $$

**Mutual information as KL.** $I(X; Y) = D(P_{XY} \,\Vert\, P_X P_Y)$.

**KL between two Gaussians (univariate).** $P = \mathcal{N}(\mu_1, \sigma_1^2)$, $Q = \mathcal{N}(\mu_2, \sigma_2^2)$:

$$ D(P \,\Vert\, Q) = \log \frac{\sigma_2}{\sigma_1} + \frac{\sigma_1^2 + (\mu_1 - \mu_2)^2}{2 \sigma_2^2} - \frac{1}{2}. $$

**KL between two multivariate Gaussians.** $P = \mathcal{N}(\boldsymbol\mu_1, \boldsymbol\Sigma_1)$, $Q = \mathcal{N}(\boldsymbol\mu_2, \boldsymbol\Sigma_2)$ in $\mathbb{R}^d$:

$$ D(P \,\Vert\, Q) = \tfrac{1}{2}\!\left[ \operatorname{tr}(\boldsymbol\Sigma_2^{-1} \boldsymbol\Sigma_1) + (\boldsymbol\mu_2 - \boldsymbol\mu_1)^\top \boldsymbol\Sigma_2^{-1} (\boldsymbol\mu_2 - \boldsymbol\mu_1) - d + \log \frac{\det \boldsymbol\Sigma_2}{\det \boldsymbol\Sigma_1} \right]. $$

**Pinsker's inequality.** $\text{TV}(P, Q) \leq \sqrt{\tfrac{1}{2} D(P \,\Vert\, Q)}$ — converts KL into a metric bound.

## Properties & identities

- **Asymmetry.** $D(P \,\Vert\, Q) \neq D(Q \,\Vert\, P)$ in general. Symmetrized variants: $D_{\text{sym}} = D(P\Vert Q) + D(Q \Vert P)$, **Jensen–Shannon**: $\text{JS}(P, Q) = \tfrac{1}{2} D(P \,\Vert\, M) + \tfrac{1}{2} D(Q \,\Vert\, M)$ with $M = \tfrac{1}{2}(P + Q)$. JS is symmetric, bounded by $\log 2$, and $\sqrt{\text{JS}}$ is a metric.
- **Joint convexity.** $(P, Q) \mapsto D(P \,\Vert\, Q)$ is jointly convex.
- **Data processing inequality.** For any (possibly stochastic) map $T$: $D(T_\# P \,\Vert\, T_\# Q) \leq D(P \,\Vert\, Q)$.
- **Forward vs reverse KL behaviour** (when used as an objective in $Q$ for fixed $P$):
  - **Forward $D(P \,\Vert\, Q)$ ("M-projection")** is *mean-seeking* / *zero-avoiding* — $Q$ spreads mass to cover all of $P$'s support; otherwise $\log(p/q) \to \infty$.
  - **Reverse $D(Q \,\Vert\, P)$ ("I-projection")** is *mode-seeking* / *zero-forcing* — $Q$ shrinks onto one mode of $P$; if $q > 0$ where $p = 0$, KL blows up.
  - Variational inference (e.g. VAE ELBO) minimizes the reverse KL.

## Worked micro-example

Two Bernoullis: $P = \text{Ber}(0.9)$, $Q = \text{Ber}(0.5)$.

$$ D(P \,\Vert\, Q) = 0.9 \log \tfrac{0.9}{0.5} + 0.1 \log \tfrac{0.1}{0.5} \approx 0.9 (0.588) + 0.1 (-1.609) \approx 0.368 \text{ nats}. $$

The reverse:

$$ D(Q \,\Vert\, P) = 0.5 \log \tfrac{0.5}{0.9} + 0.5 \log \tfrac{0.5}{0.1} \approx 0.5 (-0.588) + 0.5 (1.609) \approx 0.511 \text{ nats}. $$

Different — confirming asymmetry.

> See [companion notebook](./kl-divergence.ipynb) for numeric demos of asymmetry, Gaussian/Beta closed forms, and forward-vs-reverse projection onto a Gaussian mixture.

## Common pitfalls

- **Not a metric.** Don't symmetrize blindly or use $D$ as a "distance" in clustering — use JS or a metric like Wasserstein when symmetry/triangle inequality matter.
- **Support mismatch.** If $Q(x) = 0$ for some $x$ with $P(x) > 0$, $D = \infty$. Always smooth empirical distributions (Laplace / Dirichlet prior) before computing.
- **Direction matters in objectives.** Forward and reverse KL give qualitatively different fits — be deliberate.
- **Estimating KL from samples is hard** in high dimensions; plug-in / kNN estimators have heavy bias. Variational lower bounds (MINE, NWJ) are common workarounds for $I(X; Y) = D(P_{XY} \,\Vert\, P_X P_Y)$.
- **Units.** Nats (natural log) vs bits ($\log_2$). KL in nats × $\log_2 e \approx 1.4427$ = KL in bits.
- **Numerics.** $p \log(p/q)$ near $p \to 0$ should evaluate to $0$, not NaN. Use `scipy.special.xlogy(p, p/q)` or guard with `np.where`.

## Applications in ML

- **MLE = minimizing forward KL** from data distribution to model.
- **Variational inference / VAEs:** ELBO = $\mathbb{E}_q[\log p_\theta(x \mid z)] - D(q(z|x) \,\Vert\, p(z))$; the KL term regularizes the encoder toward the prior.
- **Distillation:** student minimizes $D(P_{\text{teacher}} \,\Vert\, P_{\text{student}})$ on the softmax outputs.
- **Policy gradients / TRPO / PPO:** trust region defined by $D(\pi_{\text{new}} \,\Vert\, \pi_{\text{old}}) \leq \delta$.
- **Mutual information estimators** for representation learning (InfoNCE, MINE) all reduce to KL bounds.

## Applications in quant

- **Model risk / scenario weighting:** the entropic constraint $D(Q \,\Vert\, P) \leq \epsilon$ defines a robust set of alternative measures around the reference $P$.
- **Entropic / KL-based risk measures** are coherent and have closed-form duals.
- **Calibration of risk-neutral densities** under entropic priors (max-entropy under price constraints = min relative entropy to a benchmark prior).
- **Density-ratio estimation** (regime detection, importance sampling) is governed by KL.

## See also

- [Entropy](./entropy.md)
- [Common distributions](../probability/common-distributions.md)
- [Convexity](../optimization/convexity.md)

## References

- Cover & Thomas, *Elements of Information Theory*, Ch. 2.3, 11.
- Murphy, *Probabilistic Machine Learning*, Ch. 6 & 21 (variational inference).
- Csiszár & Shields, *Information Theory and Statistics: A Tutorial*.
