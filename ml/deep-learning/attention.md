---
id: attention
title: Attention
domain: ml/deep-learning
tags: []
prerequisites: [vectors, common-distributions]
used_by: []
difficulty: 2
status: draft
notebook: attention.ipynb
---

# Attention

## TL;DR

Attention is a differentiable lookup: given a query, compute similarity scores to a set of keys, softmax them into weights, and return a weighted average of values. The Transformer is "self-attention all the way down".

## Scaled dot-product attention

Given queries $Q \in \mathbb{R}^{n \times d_k}$, keys $K \in \mathbb{R}^{m \times d_k}$, values $V \in \mathbb{R}^{m \times d_v}$:

$$ \text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right) V \in \mathbb{R}^{n \times d_v}. $$

The softmax is taken **per row** (each query gets its own distribution over keys).

## Why the $\sqrt{d_k}$ scaling

If queries and keys are i.i.d. with zero mean and unit variance, $\mathbb{E}[(QK^\top)_{ij}] = 0$ and $\text{Var} = d_k$. So entries grow like $\sqrt{d_k}$, pushing softmax into saturated regions where gradients vanish. Dividing by $\sqrt{d_k}$ keeps the pre-softmax logits at unit scale.

## Self-attention vs cross-attention

- **Self-attention:** $Q, K, V$ are all linear projections of the **same** input $X \in \mathbb{R}^{n \times d}$:

$$ Q = XW_Q, \quad K = XW_K, \quad V = XW_V, $$

with $W_Q, W_K \in \mathbb{R}^{d \times d_k}$ and $W_V \in \mathbb{R}^{d \times d_v}$. Used in encoder layers and decoder self-attention.

- **Cross-attention:** $Q$ from one source (e.g., decoder), $K, V$ from another (e.g., encoder). Used in encoder-decoder Transformers and in models that condition on retrieved context.

## Multi-head attention

Run $h$ attention heads in parallel with separate projection matrices, then concatenate and project:

$$ \text{MHA}(X) = \text{Concat}(\text{head}_1, \ldots, \text{head}_h) W_O, \quad \text{head}_i = \text{Attention}(XW_Q^i, XW_K^i, XW_V^i). $$

Typically $d_k = d_v = d / h$, so total params/compute matches a single big head but the model learns multiple kinds of similarity simultaneously.

## Complexity

- **Time:** $O(n^2 d)$ (the $QK^\top$ matrix and the softmax-times-$V$ product).
- **Memory:** $O(n^2)$ for the attention matrix — this is the quadratic-context bottleneck driving research in sparse / linear / flash attention.

## Masking

For autoregressive (causal) modeling, mask the attention matrix so position $i$ cannot attend to positions $j > i$:

$$ M_{ij} = \begin{cases} 0 & j \leq i \\ -\infty & j > i \end{cases}, \quad A = \text{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}} + M\right). $$

The $-\infty$ entries become $0$ after softmax. Padding masks work the same way for variable-length batches.

## Positional information

Plain attention is **permutation-equivariant**: shuffling the input rows shuffles the output rows identically. To distinguish positions, add or multiply by position-dependent vectors:

- **Sinusoidal** (original Transformer): fixed $\sin/\cos$ at log-spaced frequencies.
- **Learned absolute:** parameter per position.
- **Rotary (RoPE):** rotation in 2D pairs of dimensions; preserves relative-position structure in dot products. Standard in modern LLMs.
- **ALiBi:** linear bias on attention logits proportional to relative distance.

## Worked micro-shape check

Input $X \in \mathbb{R}^{n \times d}$ with $n = 4$, $d = 8$, single head, $d_k = d_v = 8$:

- $Q, K, V \in \mathbb{R}^{4 \times 8}$
- $QK^\top \in \mathbb{R}^{4 \times 4}$ — divide by $\sqrt{8}$, softmax rowwise
- Multiply by $V \in \mathbb{R}^{4 \times 8}$ → output $\in \mathbb{R}^{4 \times 8}$.

> See [companion notebook](./attention.ipynb) for a worked numerical example with attention heatmaps and a causal mask demo.

## Common pitfalls

- **Forgetting the $\sqrt{d_k}$ scaling** silently causes gradients to vanish at the softmax.
- **Masking convention:** add $-\infty$ (or a very negative number) **before** softmax; multiplying after softmax breaks the probability simplex.
- **Variable-length batches:** padding tokens must be masked, otherwise they bleed into attention weights and corrupt training.
- **Quadratic memory** blows up past a few thousand tokens — use FlashAttention or windowed/sparse variants.

## Applications in ML

- **Transformers** (LLMs, ViTs, encoder-decoder architectures).
- **Sequence-to-sequence** without recurrence (translation, summarization).
- **Set / graph models** as a permutation-equivariant aggregator.

## Applications in quant

- **Sequence models for return prediction** where the relevant context window varies (regime-dependent dependency length).
- **Multi-asset signal combination** where each asset attends to a set of related-asset features.

## See also

- [Vectors](../../core/linear-algebra/vectors.md)
- [Common distributions](../../core/probability/common-distributions.md) — softmax is a categorical
- [Backpropagation](./backpropagation.md)
- [Common losses](./common-losses.md)
