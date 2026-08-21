---
title: "Two Foundational Papers on Adversarial Examples"
author_profile: true
permalink: /2020-02-16-paper_summary1/
date: 2020-02-16
last_modified_at: 2026-08-21
last_modified_by: PIRA
tags: [adversarial examples, robustness, deep learning]
mathjax: true
toc: true
header:
    image: "/imgs/adversarial-papers-hero.jpg"
excerpt: "How early adversarial-example research moved from discovery to a fast attack and adversarial training."
---

Adversarial examples are inputs changed by a small, deliberately chosen perturbation that causes a model to make a wrong prediction. Two early papers established much of the modern vocabulary: Szegedy et al. showed that these examples exist and transfer between models, while Goodfellow et al. proposed a linear explanation, the fast gradient sign method, and practical adversarial training.

This post focuses on what each paper actually established and where its conclusions stop.

## Szegedy et al.: discovering transferable adversarial examples

[Intriguing Properties of Neural Networks](https://arxiv.org/abs/1312.6199) studies how small an input change can be while forcing a trained classifier toward a chosen target label.

For an input $x$, target label $\ell$, and perturbation $r$, the ideal attack seeks the smallest $\lVert r\rVert_2$ such that $f(x+r)=\ell$ and $x+r\in[0,1]^m$. Because the neural-network constraint is nonconvex, the authors approximate this problem with L-BFGS, a numerical optimization method, while constraining every pixel to the valid range. They minimize a weighted combination of perturbation size and classification loss, then search for a weight that produces the target label.

Their experiments support three important observations:

1. They found visually hard-to-distinguish adversarial examples for every tested sample across their studied MNIST, QuocNet, and AlexNet models.
2. Many examples transferred to networks trained with different architectures or hyperparameters.
3. Many also transferred to networks trained on disjoint training data.

The transfer results argue against a purely model-specific accident. The paper also reports that random perturbations are much less effective than deliberately optimized ones.

### What the Lipschitz analysis says

For a network composed of layers $\phi_1,\ldots,\phi_K$, suppose layer $k$ has Lipschitz constant $L_k$. Then the full network satisfies $\lVert\phi(x)-\phi(x+r)\rVert\leq L\lVert r\rVert$, where $L=\prod_{k=1}^K L_k$.

This bounds how much the output can change. Combined with a known margin between the correct output and its alternatives, a sufficiently small bound can certify that the predicted label is stable within a radius. A large upper bound, however, does **not** prove that an adversarial example exists. The paper's computed bounds were too conservative to explain transfer across models or training sets.

## Goodfellow et al.: linearity, FGSM, and adversarial training

[Explaining and Harnessing Adversarial Examples](https://arxiv.org/abs/1412.6572) proposes that locally linear behavior in high-dimensional models is sufficient to explain much of the phenomenon.

For a linear activation $w^\top x$, constrain a perturbation by $\lVert\eta\rVert_\infty\leq\epsilon$. Choosing $\eta=\epsilon\operatorname{sign}(w)$ changes the activation by $\epsilon\lVert w\rVert_1$. Each coordinate changes only slightly, but the contributions add across many dimensions.

The same idea applied to a model's loss $J$ yields the **fast gradient sign method (FGSM)**:

$$\eta=\epsilon\operatorname{sign}\!\left(\nabla_x J(\theta,x,y)\right).$$

FGSM needs one gradient computation, making adversarial examples far cheaper to generate than the earlier L-BFGS procedure. Goodfellow et al. use this efficiency to argue that approximate linearity, rather than extreme nonlinearity alone, can produce adversarial vulnerability.

### Adversarial training

The paper trains on both clean inputs and current FGSM adversarial inputs. Because the adversarial examples are regenerated as the model changes, training repeatedly exposes the model to inputs that increase its present loss rather than to arbitrary noise.

In the paper's MNIST maxout experiment, adversarial training reduced the error on FGSM adversarial examples from $89.4\%$ to $17.9\%$. The trained model was also more resistant to transferred examples, although it remained vulnerable and could still be highly confident when wrong. On the clean test set, the authors also reported a small improvement in their setting; that result should not be read as a general guarantee that robustness training always improves clean accuracy.

## What changed between the papers

Szegedy et al. established the phenomenon with an optimization-based attack and showed surprising transfer across models and datasets. Goodfellow et al. supplied a simpler mechanism: many small, aligned coordinate changes can accumulate into a large change in a locally linear model. That mechanism produced a one-step attack and made adversarial training much cheaper.

Neither paper proves robustness against every attack. The Lipschitz calculation is an upper-bound analysis rather than a tight certificate, and FGSM adversarial training targets a particular attack construction. Their lasting contribution is the shift in viewpoint: robustness depends not only on accuracy near observed data, but also on a model's behavior in carefully chosen nearby directions.
