---
id: bias-variance
title: Bias–Variance Tradeoff
domain: ml/evaluation
tags: [metric]
prerequisites: [random-variables, common-distributions]
used_by: []
difficulty: 2
status: draft
notebook: bias-variance.ipynb
---

# Bias–Variance Tradeoff

## TL;DR

Expected squared prediction error decomposes as $\text{Bias}^2 + \text{Variance} + \text{Irreducible noise}$ — making the model more flexible drives bias down but pumps variance up, so the test error is U-shaped in model complexity (until you cross into the modern overparameterized regime).

## Definition

Fix a test input $\mathbf{x}_0$. Suppose $y = f(\mathbf{x}_0) + \varepsilon$ with $\mathbb{E}[\varepsilon] = 0$ and $\operatorname{Var}(\varepsilon) = \sigma^2$. Let $\hat f$ be an estimator trained on a random dataset $\mathcal{D}$. The **expected squared error at $\mathbf{x}_0$**, taken over both the training set $\mathcal{D}$ and the noise $\varepsilon$, decomposes as

$$ \mathbb{E}\big[(y - \hat f(\mathbf{x}_0))^2\big] = \underbrace{\big(\mathbb{E}_\mathcal{D}[\hat f(\mathbf{x}_0)] - f(\mathbf{x}_0)\big)^2}_{\text{Bias}^2} + \underbrace{\operatorname{Var}_\mathcal{D}(\hat f(\mathbf{x}_0))}_{\text{Variance}} + \underbrace{\sigma^2}_{\text{Irreducible}}. $$

**Derivation sketch.** Let $\bar f = \mathbb{E}_\mathcal{D}[\hat f(\mathbf{x}_0)]$. Then

$$ \mathbb{E}\big[(y - \hat f)^2\big] = \mathbb{E}\big[(y - \bar f + \bar f - \hat f)^2\big] $$

and the cross terms vanish: $\mathbb{E}[\varepsilon] = 0$ kills $(y - f)$ correlations, and $\mathbb{E}_\mathcal{D}[\bar f - \hat f] = 0$ kills the other. The three squared terms remain.

## Intuition

- **Bias** measures *systematic error*: how far off the *average* prediction is from truth. A linear model fitting a sine wave will always underfit — high bias.
- **Variance** measures *training-set sensitivity*: how much $\hat f$ jitters as $\mathcal{D}$ is resampled. A degree-20 polynomial on 30 points wiggles wildly — high variance.
- **Irreducible noise** is the floor; no model can beat $\sigma^2$.

Adding flexibility (more parameters, less regularization, deeper trees) generally ↓ bias and ↑ variance. The sweet spot minimizes the sum.

## Key formulas

For a fixed $\mathbf{x}_0$:

$$ \text{Bias}(\hat f) = \mathbb{E}_\mathcal{D}[\hat f(\mathbf{x}_0)] - f(\mathbf{x}_0), \qquad \text{Var}(\hat f) = \mathbb{E}_\mathcal{D}\!\left[(\hat f(\mathbf{x}_0) - \mathbb{E}_\mathcal{D}[\hat f(\mathbf{x}_0)])^2\right]. $$

**Levers that shift the tradeoff:**

| Increase                            | Bias | Variance |
| ----------------------------------- | :--: | :------: |
| Model capacity (depth, basis size)  |  ↓   |    ↑     |
| Regularization strength $\lambda$   |  ↑   |    ↓     |
| Training-set size $n$               |  →   |    ↓     |
| Feature noise / mislabeling         |  ↑   |    ↑     |

**Asymptotics for linear regression** under fixed design: variance scales as $\sigma^2 p / n$, so adding features inflates variance linearly in $p$.

## Properties & identities

- Decomposition holds for any squared-loss estimator; for classification, analogues exist (0-1 loss has additive bias/variance components in Domingos's formulation).
- **Bagging** averages over bootstrap-resampled models — reduces variance with (approximately) no effect on bias.
- **Boosting** chains weak learners — reduces bias while controlling variance via small step sizes.
- **Regularization** (ridge, lasso, weight decay) intentionally introduces bias in exchange for a larger variance reduction.
- **Double descent (modern).** In heavily overparameterized models the classical U-curve gives way to a second descent: test error first rises near the interpolation threshold ($p \approx n$), then *falls again* as $p \gg n$. Implicit bias of the optimizer (e.g., SGD picks minimum-norm interpolators) is the standard explanation.

## Worked micro-example

True function $f(x) = x$ on $[0, 1]$; training set is a single point $(x_1, y_1)$ with $y_1 = x_1 + \varepsilon$, $\varepsilon \sim \mathcal{N}(0, \sigma^2)$. Two estimators at the test point $x_0 = 0.5$:

- $\hat f_{\text{const}}(x_0) = y_1$ (fit a constant) — $\mathbb{E}[\hat f] = x_1$, so bias $ = x_1 - 0.5$ and variance $ = \sigma^2$.
- $\hat f_0(x_0) = 0.5$ (ignore data) — bias $ = 0$ but variance $ = 0$ as well.

If $x_1$ is itself random uniform on $[0,1]$, the constant fit has zero bias *on average over training sets* but variance $\sigma^2 + 1/12$. The "do nothing" model wins on MSE when $\sigma^2$ is large — overfitting to a single noisy point can be worse than a confident prior.

> See [companion notebook](./bias-variance.ipynb) for a Monte Carlo bias/variance decomposition of polynomial regression at varying degrees — the classic U-curve.

## Common pitfalls

- **Comparing training error to test error and calling the gap "variance".** It's a related diagnostic, but bias and variance are defined w.r.t. the *true* $f$, not the training labels.
- **Tuning hyperparameters on the test set.** That leaks information; report the final number on a held-out fold you never touched during selection.
- **Assuming "more data always reduces error".** It reduces variance, but not bias — a misspecified model has a noise floor above $\sigma^2$.
- **Forgetting irreducible noise.** No amount of cleverness gets below $\sigma^2$. Stop tuning when test loss plateaus near that floor.
- **The U-curve isn't universal.** In overparameterized regimes (modern deep nets, kernel ridgeless regression) you may see double descent or monotonically decreasing error.

## Applications in ML

- **Model selection / cross-validation:** the goal is to pick the complexity that minimizes total error.
- **Ensembling** (bagging, random forests, deep ensembles) explicitly attacks the variance component.
- **Regularization** ([ridge](../supervised/linear-regression.md), dropout, early stopping, weight decay) trades variance for bias.
- **Learning curves** plot train/test error vs. $n$ to diagnose whether more data (variance-limited) or a better model class (bias-limited) is needed.

## Applications in quant

- **Covariance shrinkage** (Ledoit–Wolf) is bias–variance applied to portfolio inputs: the shrinkage target adds bias but slashes variance, improving out-of-sample Sharpe.
- **Signal averaging across factors / horizons** as a bias–variance balanced ensemble.

## See also

- [Random variables](../../core/probability/random-variables.md)
- [Common distributions](../../core/probability/common-distributions.md)
- [Linear regression](../supervised/linear-regression.md) — ridge is the canonical bias-injecting regularizer
- [PCA](../unsupervised/pca.md) — variance reduction by dimensionality reduction

## References

- Hastie, Tibshirani, Friedman, *The Elements of Statistical Learning*, §2.9, §7.3.
- Belkin et al., "Reconciling Modern Machine-Learning Practice and the Classical Bias–Variance Trade-off," PNAS 2019 (double descent).
