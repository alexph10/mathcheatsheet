---
id: mcmc
title: Markov Chain Monte Carlo (MCMC)
domain: crossover/bayesian-inference
tags: [sampling, markov]
prerequisites: [bayes-theorem, common-distributions, markov-chains]
used_by: []
difficulty: 3
status: draft
notebook: mcmc.ipynb
---

# Markov Chain Monte Carlo (MCMC)

## TL;DR

Design a Markov chain whose stationary distribution is your target $\pi$; run it for a while; treat the samples as (correlated) draws from $\pi$. Lets you sample distributions known only up to a normalizing constant — exactly the situation in Bayesian posteriors.

## Definition

Given a target density $\pi(\theta)$ on $\Theta \subseteq \mathbb{R}^d$ — **known only up to a constant**, i.e. you can compute $\tilde\pi(\theta) = c \pi(\theta)$ — an **MCMC sampler** generates a sequence $\theta^{(0)}, \theta^{(1)}, \dots$ via a Markov transition kernel $K(\theta' \mid \theta)$ chosen so that

$$ \pi \text{ is invariant: } \quad \int \pi(\theta) K(\theta' \mid \theta) \, d\theta = \pi(\theta'). $$

Under mild conditions (irreducibility + aperiodicity), $\theta^{(t)} \xrightarrow{d} \pi$ and the ergodic average

$$ \frac{1}{T} \sum_{t=1}^T h(\theta^{(t)}) \xrightarrow{\text{a.s.}} \mathbb{E}_\pi[h(\theta)]. $$

## Intuition

You can't sample $\pi$ directly (no inverse CDF, possibly high-dimensional, unknown normalizer). But you *can* evaluate $\tilde\pi(\theta)$ at any point. Build a random walk whose long-run histogram matches $\pi$: at every step, propose a move and accept/reject based only on **ratios** $\tilde\pi(\theta') / \tilde\pi(\theta)$ — the normalizer cancels. After "burn-in" the walker forgets its start and visits each region of parameter space in proportion to $\pi$.

See [markov chains](../../core/stochastic-processes/markov-chains.md) for the underlying theory of stationary distributions and convergence.

## Key formulas

**Metropolis–Hastings.** Pick a proposal density $q(\theta' \mid \theta)$. At step $t$:

1. Draw $\theta' \sim q(\cdot \mid \theta^{(t)})$.
2. Compute the **acceptance ratio**

$$ \alpha(\theta^{(t)} \to \theta') = \min\!\left\{ 1,\ \frac{\tilde\pi(\theta') \, q(\theta^{(t)} \mid \theta')}{\tilde\pi(\theta^{(t)}) \, q(\theta' \mid \theta^{(t)})} \right\}. $$

3. With probability $\alpha$, set $\theta^{(t+1)} = \theta'$; otherwise $\theta^{(t+1)} = \theta^{(t)}$.

For symmetric proposals $q(\theta' \mid \theta) = q(\theta \mid \theta')$ (e.g. $\theta' = \theta + \mathcal{N}(0, \sigma^2 I)$ — "random-walk Metropolis"), the ratio collapses to $\min\{1, \tilde\pi(\theta') / \tilde\pi(\theta)\}$.

**Detailed balance** is the design principle:

$$ \pi(\theta) \, K(\theta' \mid \theta) = \pi(\theta') \, K(\theta \mid \theta') \quad \implies \quad \pi \text{ is invariant}. $$

Metropolis–Hastings is *constructed* to satisfy detailed balance — that is why it works.

**Gibbs sampling.** When all full conditionals $p(\theta_i \mid \theta_{-i})$ are tractable, cycle through them:

$$ \theta_i^{(t+1)} \sim p\big(\theta_i \,\big|\, \theta_1^{(t+1)}, \dots, \theta_{i-1}^{(t+1)}, \theta_{i+1}^{(t)}, \dots, \theta_d^{(t)}\big). $$

Each update is a Metropolis–Hastings step with acceptance probability 1.

## Properties & identities

- **Bias of the ergodic average is $O(1/T)$;** Monte Carlo error is $O(1/\sqrt{\text{ESS}})$ where the **effective sample size** is

$$ \text{ESS} = \frac{T}{1 + 2 \sum_{k=1}^\infty \rho_k}, $$

with $\rho_k$ the lag-$k$ autocorrelation of $\{h(\theta^{(t)})\}$. Strong autocorrelation $\Rightarrow$ low ESS.

- **Optimal acceptance rates** for random-walk Metropolis: ≈ 0.234 in high dimension (Roberts–Gelman–Gilks), ≈ 0.44 in 1D. Adapt step size to hit this band.
- **Diagnostics.** Trace plots should look like "fuzzy caterpillars," not slow drifts. $\hat R$ (Gelman–Rubin) compares within- to between-chain variance across multiple chains; target $\hat R < 1.01$.
- **HMC / NUTS** uses gradient information to make long, low-rejection moves — drastically improves ESS in high dimensions.
- **MCMC is not approximate** in the sense of variational inference — given enough compute, samples are *exactly* from $\pi$. Variance, not bias, is the concern.

## Worked micro-example

Sample $\pi(\theta) \propto \exp(-\theta^2 / 2)$ on $\mathbb{R}$ (i.e. $\mathcal{N}(0,1)$, normalizer ignored). Random-walk Metropolis with proposal $\theta' = \theta + \varepsilon$, $\varepsilon \sim \mathcal{N}(0, \sigma^2)$. Acceptance:

$$ \alpha = \min\{1, \exp(-(\theta'^2 - \theta^2)/2)\}. $$

If $\theta^{(t)} = 1$, propose $\theta' = 1.5$: $\alpha = \exp(-(2.25 - 1)/2) = e^{-0.625} \approx 0.535$ — accept with prob 0.535. Propose $\theta' = 0.5$: $\alpha = \exp(-(0.25 - 1)/2) = e^{0.375} > 1$ — always accept (moves toward higher density).

> See [companion notebook](./mcmc.ipynb) for Metropolis sampling from a 2D mixture of Gaussians, the trace-plot diagnostic, and the effect of step size on acceptance rate.

## Common pitfalls

- **No burn-in.** Early samples reflect the initialization; discard the first 10–50% (or use multiple chains and check $\hat R$).
- **Step size too small** $\to$ acceptance near 1 but the chain barely moves $\to$ high autocorrelation, low ESS.
- **Step size too large** $\to$ acceptance near 0; the chain freezes at the current state.
- **Multi-modal targets.** Random-walk MCMC can fail to cross low-probability valleys. Use parallel tempering, HMC with rich gradients, or mode-jumping proposals.
- **Adapting the proposal during sampling** breaks the Markov property unless you stop adapting (or use a proven adaptive scheme — e.g. Roberts–Rosenthal).
- **Treating samples as i.i.d.** when computing standard errors — they aren't; use batch means or ESS-based estimators.

## Applications in ML

- **Bayesian neural networks / hierarchical models** — posteriors are intractable; HMC and NUTS (Stan, PyMC, NumPyro) sample them.
- **Topic models** (LDA) and many graphical models use Gibbs sampling.
- **Reinforcement learning / inverse RL** with Bayesian posterior over reward functions.
- **Simulation-based inference** combines MCMC with surrogate likelihoods.

## Applications in quant

- **Bayesian factor models** sample posterior factor loadings and covariances.
- **Stochastic volatility models** (Heston, SABR) calibrated via MCMC when likelihoods are intractable.
- **Credit risk / default correlation** — sample latent factors driving joint defaults.

## See also

- [Bayes' theorem](../../core/probability/bayes-theorem.md) — the posterior MCMC samples from
- [Markov chains](../../core/stochastic-processes/markov-chains.md) — invariant distributions, ergodicity, mixing
- [Common distributions](../../core/probability/common-distributions.md)
- [Multi-armed bandits](../game-theory/multi-armed-bandits.md) — Thompson sampling does posterior sampling, no MCMC needed in the conjugate case

## References

- Robert & Casella, *Monte Carlo Statistical Methods*, Chs. 6–10.
- Gelman et al., *Bayesian Data Analysis*, Ch. 11.
- Brooks et al. (eds.), *Handbook of Markov Chain Monte Carlo* (2011).
