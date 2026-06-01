---
id: multi-armed-bandits
title: Multi-Armed Bandits
domain: crossover/game-theory
tags: [bandit, sampling]
prerequisites: [random-variables, common-distributions, bayes-theorem]
used_by: []
difficulty: 2
status: draft
notebook: multi-armed-bandits.ipynb
---

# Multi-Armed Bandits

## TL;DR

You face $K$ slot machines with unknown reward distributions and a finite budget; the **bandit problem** is to sequentially pull arms so as to maximize cumulative reward — equivalently, to minimize *regret* against the (unknown) best arm. Optimal strategies (UCB, Thompson sampling) achieve regret $O(\log T)$.

## Definition

A **stochastic multi-armed bandit** is a tuple $(\mathcal{A}, \{\nu_a\}_{a \in \mathcal{A}})$ where $\mathcal{A} = \{1, \dots, K\}$ is the set of arms and each $\nu_a$ is a reward distribution on $\mathbb{R}$ with mean $\mu_a$. At each step $t = 1, 2, \dots, T$ the agent picks arm $A_t$ (possibly using all past observations) and receives reward $R_t \sim \nu_{A_t}$ independently.

Let $\mu^\star = \max_a \mu_a$, $a^\star \in \arg\max_a \mu_a$, and the per-arm **gap** $\Delta_a = \mu^\star - \mu_a$. **Pseudo-regret** after $T$ rounds:

$$ \mathcal{R}_T = T \mu^\star - \mathbb{E}\!\left[\sum_{t=1}^T R_t\right] = \sum_{a} \Delta_a \, \mathbb{E}[N_a(T)], $$

where $N_a(T) = \sum_{t \le T} \mathbb{1}[A_t = a]$ is the number of pulls of arm $a$.

## Intuition

The whole tension is **exploration vs. exploitation**: an arm with a poor running average might just be unlucky; one with a good running average might be lucky. Algorithms encode this as either

- **Optimism** (UCB): act as if every arm is as good as its data plausibly allows, then watch unlucky arms fall behind, or
- **Probability matching** (Thompson sampling): keep a posterior over each $\mu_a$, sample from it, act greedily on the sample — automatically explores arms whose posterior overlaps the optimum.

## Key formulas

**$\varepsilon$-greedy.** With probability $\varepsilon$ pull a uniformly random arm; otherwise pull $\arg\max_a \hat\mu_a$ where $\hat\mu_a$ is the empirical mean of arm $a$. Linear regret $\Theta(\varepsilon T)$ for fixed $\varepsilon$; the schedule $\varepsilon_t = \min(1, cK / t)$ achieves $O(\log T)$.

**UCB1** (Auer, Cesa-Bianchi, Fischer 2002) — rewards in $[0, 1]$. After every arm has been tried once, pull

$$ A_t = \arg\max_a \left[ \hat\mu_a(t-1) + \sqrt{\frac{2 \ln t}{N_a(t-1)}} \right]. $$

The bonus is a Hoeffding confidence radius; arms with few pulls get explored. **Regret bound:**

$$ \mathcal{R}_T \le \sum_{a: \Delta_a > 0} \left( \frac{8 \ln T}{\Delta_a} + \left(1 + \frac{\pi^2}{3}\right) \Delta_a \right) = O\!\left( \sum_a \frac{\log T}{\Delta_a} \right). $$

This matches the Lai–Robbins lower bound up to constants.

**Thompson sampling (Bernoulli-Beta).** Rewards $R_t \in \{0,1\}$, prior $\mu_a \sim \text{Beta}(\alpha_0, \beta_0)$. After $s_a$ successes and $f_a$ failures, the posterior is $\text{Beta}(\alpha_0 + s_a, \beta_0 + f_a)$ (conjugacy — see [Bayes' theorem](../../core/probability/bayes-theorem.md)). At each step:

1. Sample $\tilde\mu_a \sim \text{Beta}(\alpha_0 + s_a, \beta_0 + f_a)$ for every arm.
2. Pull $A_t = \arg\max_a \tilde\mu_a$, observe $R_t$, update $(s_a, f_a)$.

Thompson sampling is also $O(\log T)$ and is asymptotically optimal in the Lai–Robbins sense. In finite samples it usually edges UCB.

## Properties & identities

- **Lai–Robbins lower bound:** every consistent policy satisfies $\liminf_{T\to\infty} \mathcal{R}_T / \log T \ge \sum_{a:\Delta_a>0} \Delta_a / \mathrm{KL}(\nu_a \,\|\, \nu_{a^\star})$.
- **Gap-free regret:** $\mathcal{R}_T = O(\sqrt{KT \log T})$ for UCB — better when the gaps are tiny.
- **Adversarial bandits** drop the i.i.d. assumption — algorithms like EXP3 achieve $O(\sqrt{KT \log K})$ regret.
- **Contextual bandits** observe a feature vector $x_t$ before choosing; LinUCB and Thompson with linear models reduce to bandit-flavored regression.

## Worked micro-example

Two Bernoulli arms with means $\mu_1 = 0.5, \mu_2 = 0.6$ — gap $\Delta = 0.1$. After $t = 100$ steps, suppose arm 1 has been pulled $80$ times with $\hat\mu_1 = 0.48$ and arm 2 has been pulled $20$ times with $\hat\mu_2 = 0.55$.

UCB1 indices:

$$ \text{UCB}_1 = 0.48 + \sqrt{2 \ln 100 / 80} \approx 0.48 + 0.339 = 0.819, $$

$$ \text{UCB}_2 = 0.55 + \sqrt{2 \ln 100 / 20} \approx 0.55 + 0.679 = 1.229. $$

UCB picks arm 2 — even though arm 1 is exploited far more, the wide confidence interval on the under-explored (and currently better-looking) arm dominates. Optimism does its job.

> See [companion notebook](./multi-armed-bandits.ipynb) for a Bernoulli bandit simulation comparing cumulative regret of $\varepsilon$-greedy, UCB1, and Thompson sampling averaged over many seeds.

## Common pitfalls

- **Initializing UCB with zero pulls** makes the bonus undefined; standard fix is to pull each arm once first.
- **Tuning $\varepsilon$ on the test distribution.** $\varepsilon$-greedy with constant $\varepsilon$ has linear regret no matter how cleverly you set it.
- **Ignoring non-stationarity.** All bounds above assume i.i.d. rewards. Use sliding-window or discounted UCB / Thompson for drifting environments.
- **Off-policy evaluation pitfalls.** Naïvely averaging rewards across arms ignores selection bias — use importance weighting.
- **Reward scale.** UCB1's confidence width is calibrated for $[0,1]$; rescale or use sub-Gaussian variants (UCB-V) for other ranges.

## Applications in ML

- **A/B testing** — bandits adaptively allocate traffic, faster than fixed-split A/B with the same statistical power.
- **Hyperparameter search / Bayesian optimization** — successive halving and Hyperband are bandit algorithms over configurations.
- **Recommender systems** (LinUCB, neural Thompson) for cold-start exploration.
- **Reinforcement learning** — bandits are the depth-one special case; UCB and Thompson generalize to UCT (MCTS) and posterior sampling for RL.

## Applications in quant

- **Smart-order routing:** treat each venue / dark pool as an arm with unknown fill quality.
- **Online execution algorithms:** explore vs. exploit different child-order sizes.
- **Strategy allocation:** sequentially shift capital among trading strategies with unknown Sharpe ratios.

## See also

- [Random variables](../../core/probability/random-variables.md)
- [Common distributions](../../core/probability/common-distributions.md) — Beta-Bernoulli conjugacy
- [Bayes' theorem](../../core/probability/bayes-theorem.md) — the engine behind Thompson sampling
- [MCMC](../bayesian-inference/mcmc.md) — when posteriors aren't conjugate, sample them

## References

- Lattimore & Szepesvári, *Bandit Algorithms* (the modern reference).
- Auer, Cesa-Bianchi, Fischer, "Finite-time Analysis of the Multiarmed Bandit Problem," *Machine Learning* 47 (2002).
- Russo et al., "A Tutorial on Thompson Sampling," *FnT in ML* 11 (2018).
