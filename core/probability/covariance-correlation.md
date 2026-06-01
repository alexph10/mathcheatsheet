---
id: covariance-correlation
title: Covariance & Correlation
domain: core/probability
tags: []
prerequisites: [random-variables, expectation-variance]
used_by: []
difficulty: 1
status: draft
notebook: covariance-correlation.ipynb
---

# Covariance & Correlation

## TL;DR

Covariance measures how two random variables co-vary in raw units; correlation is its dimensionless cousin in $[-1, 1]$; both detect only **linear** association.

## Definition

For random variables $X, Y$ with finite second moments,

$$ \text{Cov}(X, Y) = \mathbb{E}\!\left[(X - \mu_X)(Y - \mu_Y)\right] = \mathbb{E}[XY] - \mu_X \mu_Y, $$

with $\mu_X = \mathbb{E}[X]$, $\mu_Y = \mathbb{E}[Y]$. The **Pearson correlation** is

$$ \rho(X, Y) = \frac{\text{Cov}(X, Y)}{\sigma_X \sigma_Y} \in [-1, 1], $$

defined whenever $\sigma_X, \sigma_Y > 0$. The bounds follow from Cauchy–Schwarz applied to the inner product $\langle X, Y \rangle = \mathbb{E}[XY]$ on centered variables.

## Intuition

Covariance is the inner product of centered random variables; correlation is the cosine of the angle between them. $\rho = \pm 1$ means $Y$ is an exact affine function of $X$ (positive or negative slope); $\rho = 0$ means **linearly** unrelated — the variables can still be strongly dependent in nonlinear ways.

## Key formulas

**Bilinearity** (for constants $a, b, c, d$):

$$ \text{Cov}(aX + b,\; cY + d) = ac\, \text{Cov}(X, Y). $$

$$ \text{Cov}\!\left(\sum_i a_i X_i,\; \sum_j b_j Y_j\right) = \sum_{i,j} a_i b_j\, \text{Cov}(X_i, Y_j). $$

**Variance of a sum** (already in [expectation and variance](./expectation-variance.md)):

$$ \text{Var}(X + Y) = \text{Var}(X) + \text{Var}(Y) + 2\,\text{Cov}(X, Y). $$

**Affine invariance of correlation:** for $a, c > 0$, $\rho(aX + b, cY + d) = \rho(X, Y)$.

**Covariance matrix.** For $\mathbf{X} = (X_1, \ldots, X_d)^\top$,

$$ \Sigma = \mathbb{E}\!\left[(\mathbf{X} - \boldsymbol\mu)(\mathbf{X} - \boldsymbol\mu)^\top\right], \qquad \Sigma_{ij} = \text{Cov}(X_i, X_j). $$

Properties: **symmetric** and **positive semidefinite** ($a^\top \Sigma a = \text{Var}(a^\top \mathbf{X}) \geq 0$ for all $a$); positive **definite** iff no nontrivial linear combination of the $X_i$ is a.s. constant. Linear transform:

$$ \text{Cov}(A\mathbf{X} + b) = A\, \Sigma\, A^\top. $$

The **correlation matrix** $\mathbf{R}$ is $\Sigma$ rescaled so $\mathbf{R}_{ii} = 1$:

$$ \mathbf{R} = D^{-1/2}\, \Sigma\, D^{-1/2}, \qquad D = \text{diag}(\Sigma). $$

## Sample estimators

Given iid samples $(x^{(i)}, y^{(i)})_{i=1}^n$ with sample means $\bar x, \bar y$:

$$ \widehat{\text{Cov}}(X, Y) = \frac{1}{n - 1} \sum_{i=1}^n (x^{(i)} - \bar x)(y^{(i)} - \bar y). $$

The $n - 1$ denominator (**Bessel's correction**) makes the estimator unbiased. Dividing by $n$ gives the MLE under a Gaussian assumption but is biased. NumPy: `np.cov(..., ddof=1)` (default) vs `ddof=0`.

The **sample correlation** plugs into the same formula as the population version.

## Uncorrelated $\neq$ independent

Independence implies $\text{Cov}(X, Y) = 0$, but not conversely. A clean counterexample: $X \sim \mathcal{N}(0, 1)$ and $Y = X^2$. Then

$$ \mathbb{E}[XY] = \mathbb{E}[X^3] = 0, \quad \mathbb{E}[X] = 0 \;\;\Longrightarrow\;\; \text{Cov}(X, Y) = 0, $$

yet $Y$ is a **deterministic function** of $X$. (Special case where the implication does reverse: jointly Gaussian variables — uncorrelated jointly Gaussian variables **are** independent.)

## Rank correlations (brief)

When the relationship is monotone but not linear, Pearson can understate it. Two robust alternatives:

- **Spearman's $\rho_S$** — Pearson correlation of the **ranks** of $X$ and $Y$. Captures any monotone association, robust to outliers.
- **Kendall's $\tau$** — probability of concordance minus discordance among random pairs. More interpretable, slower to compute.

## Shrinkage (brief)

Sample covariance is noisy when $d$ is comparable to $n$ (and singular when $d > n$). **Ledoit–Wolf** and similar **shrinkage estimators** form a convex combination

$$ \hat\Sigma_{\text{shrunk}} = (1 - \lambda)\, \hat\Sigma + \lambda\, F, $$

where $F$ is a low-variance target (e.g., $\sigma^2 I$ or constant-correlation matrix) and $\lambda$ is chosen to minimize expected Frobenius error. Standard practice for portfolio optimization and high-dim Gaussian models.

## Worked micro-example

Roll two fair dice with outcomes $X, Y$ iid Uniform$\{1, \ldots, 6\}$. Let $S = X + Y$. Then

$$ \text{Cov}(X, S) = \text{Cov}(X, X) + \text{Cov}(X, Y) = \text{Var}(X) + 0 = \tfrac{35}{12}. $$

$\text{Var}(S) = 2 \cdot \tfrac{35}{12} = \tfrac{35}{6}$, so $\rho(X, S) = (35/12) / \sqrt{(35/12) \cdot (35/6)} = 1/\sqrt{2} \approx 0.707$.

> See [companion notebook](./covariance-correlation.ipynb) for joint-Gaussian visualizations, a sample-vs-true convergence plot, and the $Y = X^2$ uncorrelated-but-dependent counterexample.

## Common pitfalls

- **Correlation is not causation.** A confounder $Z$ can drive both $X$ and $Y$, producing any $\rho$ without a direct effect either way.
- **Zero correlation does not mean independent** unless the joint distribution is Gaussian.
- **Outliers** can dominate Pearson's $\rho$ (it's an inner product of *values*) — use Spearman or robust covariance estimators.
- **Sample size matters** — with small $n$, sample correlation has high variance; a "large" $|\hat\rho|$ may be noise. Test via Fisher's $z$-transform or bootstrap.
- **Sample covariance matrix is singular when $d > n$** — you cannot invert it for Mahalanobis / portfolio weights without shrinkage or regularization.
- **Mixing $n$ vs $n - 1$ conventions** between covariance and variance — NumPy and pandas default to `ddof=1`, but some libraries (and TensorFlow / scikit-learn `np.cov` with `bias=True`) use $n$.
- **Correlation of returns vs prices** — stock prices are non-stationary; correlate returns, not levels, unless you intend a cointegration analysis.

## Applications in ML

- **PCA** diagonalizes the (sample) covariance matrix to find directions of maximum variance. See [PCA](../../ml/unsupervised/pca.md).
- **Linear regression**: the slope is $\hat\beta = \widehat{\text{Cov}}(X, Y) / \widehat{\text{Var}}(X)$. See [linear-regression](../../ml/supervised/linear-regression.md).
- **Feature selection / multicollinearity diagnostics** — high pairwise correlations inflate parameter variance.
- **Whitening / Mahalanobis distance** — preprocessing uses $\Sigma^{-1/2}$.

## Applications in quant

- **Mean-variance portfolio optimization** trades off $w^\top \boldsymbol\mu$ against $w^\top \Sigma w$. See [mean-variance](../../quant/portfolio-theory/mean-variance.md).
- **Risk decomposition / factor models** — covariance structure separates systematic and idiosyncratic risk.
- **Pairs trading** uses cointegration / correlation of related instruments.
- **Copulas** model dependence beyond what correlation can capture (especially tail dependence).

## See also

- [Expectation and variance](./expectation-variance.md)
- [Random variables](./random-variables.md)
- [Inner products](../linear-algebra/inner-products.md) — covariance is an inner product on centered random variables.
- [PCA](../../ml/unsupervised/pca.md)
- [Mean-variance portfolio](../../quant/portfolio-theory/mean-variance.md)

## References

- Wasserman, *All of Statistics*, Ch. 3.
- Ledoit & Wolf, "A well-conditioned estimator for large-dimensional covariance matrices" (2004).
