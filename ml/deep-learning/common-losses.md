---
id: common-losses
title: Common Loss Functions
domain: ml/deep-learning
tags: [loss-function]
prerequisites: [random-variables, kl-divergence, entropy]
used_by: []
difficulty: 1
status: draft
---

# Common Loss Functions

## TL;DR

The loss function is the bridge between the model and a probabilistic assumption about the data. Most "standard" losses are negative log-likelihoods of well-known distributions; the rest are designed for specific geometric or ranking properties.

## Regression losses

| Loss | Formula (per example) | Equivalent NLL | When to use | Pitfalls |
|---|---|---|---|---|
| **MSE / L2** | $(y - \hat{y})^2$ | Gaussian | Default; smooth, differentiable | Sensitive to outliers |
| **MAE / L1** | $\|y - \hat{y}\|$ | Laplace | Robust to outliers | Non-smooth at 0 |
| **Huber** | $\begin{cases}\tfrac{1}{2}(y-\hat{y})^2 & \|y-\hat{y}\| \leq \delta \\ \delta(\|y-\hat{y}\| - \tfrac{\delta}{2}) & \text{else}\end{cases}$ | Pseudo-Gaussian | MSE near zero, MAE in tails | Hyperparameter $\delta$ |
| **Quantile (pinball)** | $\max(\tau(y - \hat{y}), (\tau-1)(y - \hat{y}))$ | Asymmetric Laplace | Quantile regression; VaR estimation | Asymmetric; $\tau \in (0,1)$ |
| **Log-cosh** | $\log(\cosh(y - \hat{y}))$ | smooth ≈ MAE | Smooth Huber-like alternative | Same flavor as Huber |

## Classification losses

| Loss | Formula | Equivalent NLL | Notes |
|---|---|---|---|
| **0–1** | $\mathbf{1}[y \neq \hat{y}]$ | — | Target metric; non-differentiable |
| **Binary cross-entropy** | $-y \log \hat{p} - (1-y) \log(1-\hat{p})$ | Bernoulli | Default for binary classification |
| **Categorical CE** | $-\sum_k y_k \log \hat{p}_k$ | Categorical | Multi-class; pair with softmax |
| **Hinge** | $\max(0, 1 - y \cdot s)$, $y \in \{\pm 1\}$ | — | SVMs; encourages margin |
| **Squared hinge** | $\max(0, 1 - y \cdot s)^2$ | — | Smoother, more penalty on big errors |
| **Focal** | $-(1 - \hat{p}_t)^\gamma \log \hat{p}_t$ | weighted CE | Class imbalance; down-weights easy examples |
| **Label-smoothed CE** | CE against $(1-\varepsilon)\mathbf{e}_y + \varepsilon/K$ | — | Regularizes confidence |

## Probabilistic / divergence losses

| Loss | Formula | Notes |
|---|---|---|
| **NLL** | $-\log p_{\boldsymbol{\theta}}(y \mid x)$ | Generic; instantiates to all the above |
| **KL divergence** | $\sum_x p(x) \log \frac{p(x)}{q(x)}$ | Match a target distribution; see [kl-divergence](../../core/information-theory/kl-divergence.md) |
| **Reverse KL** | $D(q \| p)$ | Mode-seeking; used in VI |
| **Wasserstein-1** | $\sup_{\|f\|_L \leq 1} \mathbb{E}_p[f] - \mathbb{E}_q[f]$ | WGAN; robust when supports are disjoint |
| **JS divergence** | $\tfrac{1}{2}(D(p\|m) + D(q\|m)), m = \tfrac{p+q}{2}$ | Symmetric; saturates when supports disjoint |

## Ranking / metric losses

| Loss | Formula | Notes |
|---|---|---|
| **Pairwise hinge** | $\max(0, m - (s_+ - s_-))$ | Used in learning-to-rank |
| **Triplet** | $\max(0, \|a - p\|^2 - \|a - n\|^2 + \alpha)$ | Anchor / positive / negative |
| **Contrastive (NT-Xent)** | $-\log \frac{\exp(s_+/\tau)}{\sum \exp(s_*/\tau)}$ | SimCLR, CLIP — softmax over similarities |

## Structured / specialized

| Loss | Use |
|---|---|
| **Dice / IoU** | Segmentation; handles class imbalance better than CE |
| **CTC** | Sequence-to-sequence without alignment (speech) |
| **CRF NLL** | Structured prediction over label sequences |
| **Negative ELBO** | VAEs: reconstruction + KL to prior |

## Bridges to information theory

- **Cross-entropy = entropy of target + KL to predicted**: $H(p, q) = H(p) + D_{\text{KL}}(p \| q)$. When the target is one-hot, $H(p) = 0$, so CE equals KL.
- **MLE = minimizing KL** to the data distribution.
- **Logistic regression NLL = cross-entropy with Bernoulli target**.

## Common pitfalls

- **MSE on classification** predicts off-target probabilities and has vanishing gradients near the wrong end of the sigmoid.
- **Sum vs mean reductions** matter for learning-rate scaling; pick one and be consistent.
- **Numerical stability:** compute $\log\text{softmax}$ in one step (`log_softmax`), never $\log(\text{softmax}(z))$.
- **Class imbalance + CE** can lock predictions on the majority class — use focal, reweighting, or threshold tuning.

## Applications in ML

Direct (every supervised model picks one). Loss choice often dominates architecture choice on tabular / smaller datasets.

## Applications in quant

- **Quantile pinball loss** is the natural objective for **VaR** estimation.
- **Asymmetric losses** for direction-aware error budgets (e.g., penalize underestimating downside more than upside).
- **MSE on log-returns** vs **MAE on raw returns** changes optimal models dramatically.

## See also

- [Logistic regression](../supervised/logistic-regression.md)
- [SVM](../supervised/svm.md)
- [Entropy](../../core/information-theory/entropy.md)
- [KL divergence](../../core/information-theory/kl-divergence.md)
