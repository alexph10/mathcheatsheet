---
id: logistic-regression
title: Logistic Regression
domain: ml/supervised
tags: [regression, loss-function]
prerequisites: [linear-regression, gradients, gradient-descent]
used_by: []
difficulty: 1
status: draft
notebook: logistic-regression.ipynb
---

# Logistic Regression

## TL;DR

A linear model for binary classification: pass a linear score through the sigmoid to get a probability, then maximize the Bernoulli log-likelihood. Convex loss, no closed form, solved by gradient descent / Newton (IRLS).

## Definition

Given features $\mathbf{x} \in \mathbb{R}^d$ and label $y \in \{0, 1\}$:

$$ p(y = 1 \mid \mathbf{x}; \mathbf{w}, b) = \sigma(\mathbf{w}^\top \mathbf{x} + b), \quad \sigma(z) = \frac{1}{1 + e^{-z}}. $$

The decision boundary $\sigma(z) = 0.5 \iff z = 0$ is the **hyperplane** $\mathbf{w}^\top \mathbf{x} + b = 0$ — same shape as in linear regression, but interpreted as a classifier.

## Loss: binary cross-entropy (≡ negative log-likelihood)

For $n$ i.i.d. samples, the NLL is

$$ L(\mathbf{w}, b) = -\sum_{i=1}^n \left[ y_i \log \hat{p}_i + (1 - y_i) \log(1 - \hat{p}_i) \right], \quad \hat{p}_i = \sigma(\mathbf{w}^\top \mathbf{x}_i + b). $$

This loss is **convex** in $(\mathbf{w}, b)$ (Hessian is PSD: $\sum_i \hat{p}_i(1-\hat{p}_i) \mathbf{x}_i \mathbf{x}_i^\top$) — so any local optimum is global.

## Key formulas

- **Gradient:** $\nabla_{\mathbf{w}} L = \sum_i (\hat{p}_i - y_i)\, \mathbf{x}_i = X^\top (\hat{\mathbf{p}} - \mathbf{y})$. Identical in form to OLS gradient, but $\hat{\mathbf{p}}$ is the sigmoid output, not $X\mathbf{w}$.
- **Hessian:** $H = X^\top D X$ where $D = \text{diag}(\hat{p}_i (1 - \hat{p}_i))$. Always PSD.
- **L2-regularized (ridge) logistic:** add $\tfrac{\lambda}{2} \|\mathbf{w}\|^2$ — Hessian becomes $X^\top D X + \lambda I$ (strictly PD when $\lambda > 0$).
- **Newton update / IRLS:** $\mathbf{w} \leftarrow \mathbf{w} - H^{-1} \nabla L$. Equivalent to solving a weighted-least-squares problem each iteration.
- **Softmax / multinomial logistic** ($K$ classes): $p(y = k \mid \mathbf{x}) = e^{\mathbf{w}_k^\top \mathbf{x}}/\sum_j e^{\mathbf{w}_j^\top \mathbf{x}}$, with categorical cross-entropy loss.

## Geometric & probabilistic view

- **Geometric:** the boundary is a hyperplane; $\sigma$ smooths the 0/1 indicator into a probability.
- **GLM:** logistic regression is the canonical GLM for Bernoulli with log-odds link $\log \frac{p}{1-p} = \mathbf{w}^\top \mathbf{x}$. The coefficients have a clean interpretation as log-odds ratios.

## Worked micro-example

One feature, $\mathbf{x}_i = x_i \in \mathbb{R}$. Data $(x, y) = \{(-1, 0), (0, 0), (1, 1), (2, 1)\}$. The MLE fit gives roughly $\hat{w} \approx 1.7$, $\hat{b} \approx -0.85$, so $P(y=1 \mid x = 0.5) = \sigma(0) = 0.5$ — the decision boundary lands at $x = 0.5$.

> See [companion notebook](./logistic-regression.ipynb) for a 2D synthetic dataset fit via your own GD loop and sklearn, with decision-boundary visualization.

## Common pitfalls

- **Perfectly separable data** → $\|\mathbf{w}\| \to \infty$, MLE diverges. Use L2 regularization or early stopping.
- **Class imbalance** distorts thresholds; either reweight the loss or pick the decision threshold from the validation ROC.
- **"Predicted probabilities" are calibrated only when the model is well-specified.** Otherwise post-hoc calibration (Platt, isotonic) is needed.
- **Don't apply linear regression to {0,1} targets** — it predicts outside $[0,1]$, has non-Gaussian residuals, and the boundary becomes data-dependent in pathological ways. See the notebook for a side-by-side.

## Applications in ML

- Baseline classifier — often shockingly hard to beat.
- Final layer of many deep classifiers (softmax over class logits).
- Calibration baseline before more complex models.

## Applications in quant

- **Default-probability models** (credit scoring) historically use logistic regression for its interpretability (regulators audit it).
- **Direction-of-move classifiers** for short-horizon trading signals.

## See also

- [Linear regression](./linear-regression.md)
- [Gradient descent](../../core/optimization/gradient-descent.md)
- [Common losses](../deep-learning/common-losses.md)
- [Convexity](../../core/optimization/convexity.md)
