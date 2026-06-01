---
id: markov-chains
title: Markov Chains
domain: core/stochastic-processes
tags: [markov, stochastic-process]
prerequisites: [random-variables]
used_by: []
difficulty: 2
status: draft
notebook: markov-chains.ipynb
---

# Markov Chains

## TL;DR

A discrete-time stochastic process $\{X_t\}$ where the future depends on the past only through the present: $\Pr(X_{t+1} \mid X_t, X_{t-1}, \ldots) = \Pr(X_{t+1} \mid X_t)$. Behavior is encoded in a transition matrix $P$; long-run behavior in its top eigenvector.

## Definition

**Markov property.** A sequence $\{X_t\}_{t \geq 0}$ on a countable state space $S$ is a (time-homogeneous, discrete-time) Markov chain if

$$ \Pr(X_{t+1} = j \mid X_t = i, X_{t-1}, \ldots, X_0) = \Pr(X_{t+1} = j \mid X_t = i) =: P_{ij}. $$

**Transition matrix** $P \in \mathbb{R}^{|S| \times |S|}$ is **stochastic**: $P_{ij} \geq 0$ and $\sum_j P_{ij} = 1$ (rows sum to one). The chain plus an initial distribution $\boldsymbol\pi_0$ specifies the joint distribution of the entire path.

**State distribution evolution.** Treat $\boldsymbol\pi_t$ as a row vector; then

$$ \boldsymbol\pi_{t+1} = \boldsymbol\pi_t P, \qquad \boldsymbol\pi_t = \boldsymbol\pi_0 P^t. $$

**$n$-step transition.** $\Pr(X_{t+n} = j \mid X_t = i) = (P^n)_{ij}$. Chapman–Kolmogorov:

$$ P^{m+n} = P^m P^n. $$

## Intuition

The state $X_t$ is a sufficient statistic for the future. The matrix $P^n$ summarizes "where you'd be in $n$ steps starting from each state". If the chain is "nice" (irreducible + aperiodic), $P^n$ converges to a matrix whose rows are all equal to the **stationary distribution** $\boldsymbol\pi$ — the long-run fraction of time in each state, independent of where you started.

## Key formulas

**Stationary distribution.** A row vector $\boldsymbol\pi$ with $\pi_i \geq 0$, $\sum_i \pi_i = 1$, satisfying

$$ \boldsymbol\pi P = \boldsymbol\pi. $$

Equivalently, $\boldsymbol\pi^\top$ is a left eigenvector of $P$ with eigenvalue $1$. By Perron–Frobenius, every finite stochastic matrix has at least one such $\boldsymbol\pi$.

**Detailed balance (reversibility).** If

$$ \pi_i P_{ij} = \pi_j P_{ji} \quad \forall i, j, $$

then $\boldsymbol\pi$ is stationary (sum over $i$ to verify). Chains satisfying detailed balance are called **reversible**; the Metropolis–Hastings algorithm constructs reversible chains targeting a desired $\boldsymbol\pi$.

**Convergence theorem.** If $P$ is finite, **irreducible** (every state reachable from every other), and **aperiodic** (period 1; equivalently, some power $P^n$ has all entries positive), then a *unique* stationary $\boldsymbol\pi$ exists and

$$ (P^n)_{ij} \xrightarrow{n \to \infty} \pi_j \qquad \forall i, j. $$

**Ergodic theorem (time average = space average).** For any bounded $f$,

$$ \frac{1}{n} \sum_{t=0}^{n-1} f(X_t) \xrightarrow{\text{a.s.}} \mathbb{E}_{\boldsymbol\pi}[f(X)] = \sum_i \pi_i f(i). $$

**Hitting / mean return time.** Expected return time to state $i$ from $i$:

$$ \mathbb{E}_i[T_i^+] = 1/\pi_i \qquad \text{(irreducible recurrent).} $$

## Classification of states

For an irreducible finite chain, every state is in exactly one class with the same labels:

- **Recurrent** vs **transient**. $i$ is recurrent if $\Pr(\text{return to } i) = 1$; transient otherwise. *All states of a finite irreducible chain are recurrent.*
- **Positive recurrent** ($\mathbb{E}_i[T_i^+] < \infty$) vs **null recurrent** ($= \infty$). Finite irreducible ⇒ positive recurrent.
- **Period** of $i$: $d(i) = \gcd\{n \geq 1 : (P^n)_{ii} > 0\}$. If $d(i) = 1$ the state is **aperiodic**. Period is a class property.

**Ergodic chain** = irreducible + aperiodic + positive recurrent (the first two suffice in the finite case).

## Properties & identities

- **Spectrum of $P$.** All eigenvalues satisfy $|\lambda| \leq 1$. $\lambda_1 = 1$ always. For an ergodic chain, $\lambda_1 = 1$ is simple and all other $|\lambda_k| < 1$.
- **Mixing time.** $t_{\text{mix}}(\epsilon) = \min\{ t : \max_i \tfrac{1}{2} \lVert (P^t)_{i, \cdot} - \boldsymbol\pi \rVert_1 \leq \epsilon \}$. For reversible chains, $t_{\text{mix}} \asymp \tfrac{1}{1 - |\lambda_2|} \log(1/\epsilon)$ — the spectral gap controls mixing speed.
- **Random walk on a graph.** $P_{ij} = 1/\deg(i)$ for $(i,j)$ edge; stationary distribution $\pi_i \propto \deg(i)$; satisfies detailed balance.
- **Two-state chain.** $P = \begin{bmatrix} 1 - a & a \\ b & 1 - b \end{bmatrix}$, $a, b \in (0, 1)$. Stationary: $\boldsymbol\pi = \bigl( \tfrac{b}{a+b}, \tfrac{a}{a+b} \bigr)$; second eigenvalue $1 - a - b$.
- **Continuous-time chains** ($Q$-matrix) and **MCMC samplers** (Metropolis, Gibbs) inherit this whole framework.

## Worked micro-example

Two-state weather chain: sunny → rainy with probability $0.1$, rainy → sunny with probability $0.5$:

$$ P = \begin{bmatrix} 0.9 & 0.1 \\ 0.5 & 0.5 \end{bmatrix}. $$

Solve $\boldsymbol\pi P = \boldsymbol\pi$ with $\pi_S + \pi_R = 1$: $\pi_R = 0.1 \pi_S / 0.5 \cdot$ — straight from $\pi_S \cdot 0.1 = \pi_R \cdot 0.5$ (detailed balance). So $\pi_R / \pi_S = 1/5$, giving $\boldsymbol\pi = (5/6, 1/6) \approx (0.833, 0.167)$.

Check: in the long run sunny days are five times more frequent than rainy ones. Mean return time to a rainy day is $1/\pi_R = 6$.

> See [companion notebook](./markov-chains.ipynb) for a 3-state chain: simulate trajectories, watch $P^n$ converge, and visualize the stationary distribution.

## Common pitfalls

- **Row vs column conventions.** This sheet uses *row* stochastic matrices and *row* distributions ($\boldsymbol\pi P = \boldsymbol\pi$). Some references use column stochastic ($P\boldsymbol\pi = \boldsymbol\pi$); always check.
- **Periodicity blocks convergence.** A periodic chain (e.g. bipartite random walk) has $P^n$ that does not converge — the marginal oscillates. Average over a period or add a small "lazy" self-loop ($P' = \tfrac{1}{2}(I + P)$).
- **Reducible chains have non-unique $\boldsymbol\pi$** — one per closed communicating class.
- **Infinite state spaces** introduce null recurrence and transience for "boring" reasons (simple random walk on $\mathbb{Z}$ is null recurrent in 1D and 2D, transient in $\geq 3$D).
- **MCMC pitfall:** detailed balance is sufficient but *not necessary* for stationarity. Non-reversible chains can mix faster but are harder to verify.
- **Time-inhomogeneity.** If transition probabilities change with $t$, all the spectral theory above fails. Need to track $P_t \cdot P_{t-1} \cdots P_0$ explicitly.

## Applications in ML

- **MCMC sampling** (Metropolis–Hastings, Gibbs, HMC) constructs a chain whose stationary distribution is the posterior.
- **Hidden Markov models** for sequence data (speech, biological sequences) — observation model on top of a latent Markov chain.
- **Reinforcement learning:** Markov decision processes generalize Markov chains with rewards and actions.
- **PageRank** is the stationary distribution of a random surfer on the web graph (with teleport).
- **Diffusion models** are non-stationary Markov chains in the noise-to-data direction.

## Applications in quant

- **Credit-rating migration matrices** (AAA → AA → ... → default) are estimated as Markov chains.
- **Regime-switching models** for returns, volatility, and macro variables (Hamilton 1989).
- **Order-book dynamics** modeled as Markov chains on inventory / state of the book.
- **Bermudan / American option pricing** uses backward induction on Markov state lattices.

## See also

- [Random variables](../probability/random-variables.md)
- [Eigendecomposition](../linear-algebra/eigendecomposition.md) — the stationary distribution is a left eigenvector at $\lambda = 1$.
- [Bayes' theorem](../probability/bayes-theorem.md) — backbone of MCMC posterior inference.

## References

- Norris, *Markov Chains*, Ch. 1.
- Levin, Peres & Wilmer, *Markov Chains and Mixing Times*, Ch. 1–4.
- Durrett, *Essentials of Stochastic Processes*, Ch. 1.
