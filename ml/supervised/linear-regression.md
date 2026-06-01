---
id: linear-regression
title: Linear Regression
domain: ml/supervised
tags: [regression]
prerequisites: [vectors, norms, gradients, svd]
used_by: []
difficulty: 1
status: draft
notebook: linear-regression.ipynb
---

# Linear Regression

## TL;DR

Fit $\mathbf{y} \approx X\boldsymbol\beta$ by minimizing $\lVert \mathbf{y} - X\boldsymbol\beta \rVert_2^2$; the closed form $\hat{\boldsymbol\beta} = (X^\top X)^{-1} X^\top \mathbf{y}$ is just the orthogonal projection of $\mathbf{y}$ onto the column space of $X$.

## Definition

Given a design matrix $X \in \mathbb{R}^{n \times p}$ (rows = observations, columns = features, including a column of ones for the intercept) and targets $\mathbf{y} \in \mathbb{R}^n$, the **ordinary least squares (OLS)** model assumes

$$ \mathbf{y} = X\boldsymbol\beta + \boldsymbol\varepsilon, \qquad \mathbb{E}[\boldsymbol\varepsilon] = 0,\ \operatorname{Cov}(\boldsymbol\varepsilon) = \sigma^2 I_n, $$

and estimates $\boldsymbol\beta \in \mathbb{R}^p$ by

$$ \hat{\boldsymbol\beta} = \arg\min_{\boldsymbol\beta} \lVert \mathbf{y} - X\boldsymbol\beta \rVert_2^2. $$

## Intuition

The fitted values $\hat{\mathbf{y}} = X\hat{\boldsymbol\beta}$ are the orthogonal projection of $\mathbf{y}$ onto $\operatorname{col}(X)$. The residual $\mathbf{r} = \mathbf{y} - \hat{\mathbf{y}}$ is perpendicular to every column of $X$ — that is the **normal equation** $X^\top \mathbf{r} = 0$. Among all linear combinations of features, OLS picks the one closest to $\mathbf{y}$ in Euclidean distance.

## Key formulas

**Normal equations** (set $\nabla_{\boldsymbol\beta} \lVert \mathbf{y} - X\boldsymbol\beta \rVert_2^2 = 0$):

$$ X^\top X \, \hat{\boldsymbol\beta} = X^\top \mathbf{y} \quad\Longrightarrow\quad \hat{\boldsymbol\beta} = (X^\top X)^{-1} X^\top \mathbf{y} \quad \text{(if $X$ has full column rank)}. $$

**Hat matrix** (projection onto $\operatorname{col}(X)$):

$$ H = X(X^\top X)^{-1} X^\top, \qquad \hat{\mathbf{y}} = H \mathbf{y}, \qquad H^2 = H = H^\top. $$

**Ridge regression** (Tikhonov $\ell_2$ regularization, $\lambda > 0$):

$$ \hat{\boldsymbol\beta}_{\text{ridge}} = (X^\top X + \lambda I_p)^{-1} X^\top \mathbf{y}. $$

Always invertible — $\lambda I$ stabilizes ill-conditioned $X^\top X$.

**SVD form** (works for rank-deficient $X$). With economy SVD $X = U\Sigma V^\top$,

$$ \hat{\boldsymbol\beta} = X^+ \mathbf{y} = V \Sigma^+ U^\top \mathbf{y}, \qquad \hat{\boldsymbol\beta}_{\text{ridge}} = V \,\operatorname{diag}\!\left(\tfrac{\sigma_i}{\sigma_i^2 + \lambda}\right) U^\top \mathbf{y}. $$

The SVD route is the numerically stable choice (see [SVD](../../core/linear-algebra/svd.md)).

**Gradient descent.** With $L(\boldsymbol\beta) = \tfrac{1}{2n}\lVert \mathbf{y} - X\boldsymbol\beta \rVert_2^2$,

$$ \nabla_{\boldsymbol\beta} L = \tfrac{1}{n} X^\top (X\boldsymbol\beta - \mathbf{y}), \qquad \boldsymbol\beta_{t+1} = \boldsymbol\beta_t - \eta \nabla_{\boldsymbol\beta} L. $$

Convex quadratic — gradient descent converges to the OLS solution for any $\eta < 2/\sigma_{\max}(X^\top X / n)$.

## Properties & identities

- **Unbiased:** $\mathbb{E}[\hat{\boldsymbol\beta}] = \boldsymbol\beta$ under the model assumptions.
- **Variance:** $\operatorname{Cov}(\hat{\boldsymbol\beta}) = \sigma^2 (X^\top X)^{-1}$.
- **Gauss–Markov:** OLS is the **B**est **L**inear **U**nbiased **E**stimator (lowest variance among linear unbiased estimators) when errors are uncorrelated and homoscedastic.
- $\operatorname{tr}(H) = p$ — degrees of freedom equal the number of parameters.
- Ridge **shrinks** components along small singular directions much more than large ones — see SVD form above.
- Adding the intercept by augmenting $X$ with a column of ones is equivalent to centering $\mathbf{y}$ and the columns of $X$.

## Worked micro-example

Three data points: $(1, 2), (2, 2), (3, 4)$ — fit $y = \beta_0 + \beta_1 x$.

$$ X = \begin{bmatrix} 1 & 1 \\ 1 & 2 \\ 1 & 3 \end{bmatrix}, \quad \mathbf{y} = \begin{bmatrix} 2 \\ 2 \\ 4 \end{bmatrix}, \quad X^\top X = \begin{bmatrix} 3 & 6 \\ 6 & 14 \end{bmatrix}, \quad X^\top \mathbf{y} = \begin{bmatrix} 8 \\ 18 \end{bmatrix}. $$

Solving $X^\top X \hat{\boldsymbol\beta} = X^\top \mathbf{y}$: $\hat\beta_1 = 1$, $\hat\beta_0 = 2/3$. Fit: $\hat y = 0.667 + 1\cdot x$.

> See [companion notebook](./linear-regression.ipynb) for normal equations vs. sklearn vs. gradient descent, and a collinear-features pitfall where SVD/pseudoinverse rescues the rank-deficient case.

## Common pitfalls

- **Multicollinearity.** Highly correlated columns make $X^\top X$ near-singular; $(X^\top X)^{-1}$ blows up coefficients. Use ridge or the SVD pseudoinverse.
- **Forgetting to center / scale** before ridge — the $\ell_2$ penalty is not scale invariant.
- **Heteroscedasticity / correlated errors.** OLS is still unbiased but standard errors are wrong; use weighted/generalized least squares.
- **Outliers** have leverage proportional to the diagonal of $H$; a single high-leverage point can dominate the fit.
- **Extrapolation.** The model is only trustworthy inside the convex hull of training features.
- **Don't form $(X^\top X)^{-1}$ explicitly.** Solve the linear system (`np.linalg.lstsq`, QR, or SVD) — squaring $X$ squares its condition number.

## Applications in ML

- Baseline for any regression task; the linear part of generalized linear models.
- Ridge ([regularization](../../core/linear-algebra/norms.md)) and lasso ($\ell_1$) are the building blocks of regularized linear estimators.
- Featureized linear regression underlies kernel ridge regression and Gaussian process means.
- Polynomial regression is OLS on a polynomial feature expansion (see [bias-variance](../evaluation/bias-variance.md)).

## Applications in quant

- **Factor models** (Fama–French, Barra): regress returns on factor exposures.
- **Hedging ratios**: $\hat\beta$ from regressing portfolio returns on a hedging instrument.
- **Cointegration tests** rely on residuals of a regression between non-stationary series.

## See also

- [Vectors](../../core/linear-algebra/vectors.md)
- [Vector norms](../../core/linear-algebra/norms.md)
- [SVD](../../core/linear-algebra/svd.md) — for rank-deficient and ridge formulations
- [Gradients](../../core/calculus/gradients.md)
- [Bias–variance tradeoff](../evaluation/bias-variance.md)

## References

- Hastie, Tibshirani, Friedman, *The Elements of Statistical Learning*, Ch. 3.
- Strang, *Introduction to Linear Algebra*, Ch. 4 (projections and least squares).
