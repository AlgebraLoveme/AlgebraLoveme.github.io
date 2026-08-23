---
title: "Why Testing Is Not Proof: Neural Network Certification, Part 1"
series_nav_title: "Why Testing Is Not Proof"
author_profile: true
permalink: /2026-08-21-neural-network-certification-1-what-are-we-proving/
date: 2026-08-21
written_by: PIRA
written_at: 2026-08-21
tags: [neural networks, certification, formal verification, robustness, "Certification Series: 01"]
mathjax: true
toc: true
excerpt: "April the Siberian cat helps us see why an attack can disprove robustness, while only a certificate can prove it."
---

> **Reader background.** We assume undergraduate calculus, linear algebra,
> elementary probability, and basic neural networks. The series introduces
> program verification and neural network certification from first principles.

Meet April, my Siberian cat.

<figure style="text-align: center;">
  <a href="{{ '/imgs/April_the_cat.jpg' | relative_url }}">
    <img src="{{ '/imgs/April_the_cat.jpg' | relative_url }}" width="520" style="display: block; margin: 0 auto;" alt="April, a cream-colored Siberian cat with gray ears, sitting beside a tree in sunlight.">
  </a>
  <figcaption>We will use this photograph of April to move from one correct prediction to a mathematical guarantee.</figcaption>
</figure>

Imagine that an image classifier receives this photo and predicts **cat**. It is
right on this input. Now darken the photo, compress it, add camera noise, or
change a few pixels. Will the prediction remain cat?

## Why models need to be robust

Suppose our classifier labels 9,800 of 10,000 test images correctly, giving 98%
test accuracy. This aggregate does not tell us whether one correct prediction
will survive nearby changes.

The same scene can reach the model through different cameras, lighting
conditions, compression settings, and preprocessing pipelines. We still see
April, but the classifier receives a different array of numbers each time.

A **robust** model preserves the required behavior when the input changes in
ways we have decided to allow. This raises two concrete questions:

1. Which input changes should we consider?
2. Which model behavior should remain unchanged?

For April's photo, we may require the predicted class to remain **cat** under a
specified amount of image noise. Another task might allow small rotations rather
than pixel noise, or require a numerical output to remain within a safe range
rather than preserving a class label. The word *robust* is incomplete until we
answer both questions.

## From robustness to adversarial robustness

Random sensor noise is not chosen with the classifier in mind. An adversarial
perturbation is chosen specifically to make the classifier fail. **Adversarial
robustness** therefore asks a worst-case question:

> Can someone deliberately choose an **allowed** change to April's photo that
> makes the classifier stop predicting cat?

An allowed image that changes the prediction is an **adversarial example**.
Research on [adversarial examples](https://arxiv.org/abs/1312.6199) showed that
small, carefully chosen perturbations could change neural network predictions.
The [robust optimization viewpoint](https://arxiv.org/abs/1706.06083) frames
robustness as performance under the worst allowed perturbation rather than under
average noise.

The right panel below is a conceptual illustration with visible noise, making a
pixel perturbation easy to see while April remains recognizable.

<div style="display: flex; flex-wrap: wrap; gap: 1rem; justify-content: center; align-items: flex-start;">
  <figure style="flex: 1 1 260px; max-width: 360px; margin: 0; text-align: center;">
    <a href="{{ '/imgs/April_the_cat.jpg' | relative_url }}">
      <img src="{{ '/imgs/April_the_cat.jpg' | relative_url }}" alt="Original photograph of April the Siberian cat beside a tree.">
    </a>
    <figcaption><strong>Original.</strong> The classifier receives April's photograph.</figcaption>
  </figure>
  <figure style="flex: 1 1 260px; max-width: 360px; margin: 0; text-align: center;">
    <a href="{{ '/imgs/April_the_cat_conceptual_perturbation.jpg' | relative_url }}">
      <img src="{{ '/imgs/April_the_cat_conceptual_perturbation.jpg' | relative_url }}" alt="Conceptual illustration of April's photograph with fine multicolored pixel noise.">
    </a>
    <figcaption><strong>Conceptual perturbation.</strong> Visible noise illustrates a modified input rather than the output of a classifier attack.</figcaption>
  </figure>
</div>

Restricting which changes are **allowed** prevents a trivial attack. Replacing
April's photo with a photo of a dog might change the prediction, but it tells us
nothing about whether the classifier is stable near the original photo. A
**threat model** draws the boundary: it states what may change, by how much, and
what counts as a successful attack.

Let $x_0$ represent April's photo, with pixel values normalized to $[0,1]$. We
measure a pixel perturbation with an $\ell_p$ norm, where
$1\leq p\leq\infty$, and limit its size with a radius $\epsilon$. The allowed
images form the set

$$
S_p(x_0,\epsilon)
=\left\{x\in[0,1]^d:\lVert x-x_0\rVert_p\leq\epsilon\right\}.
$$

Here, $d$ counts all pixel values across all color channels, and $p$ determines
how their changes are combined. When $p=\infty$, the norm measures the largest
absolute change to any pixel value. Thus, $x\in S_p(x_0,\epsilon)$ means that $x$
is a valid pixel array and its distance from April's original photo is at most
$\epsilon$. The norm and radius are part of the robustness claim: changing either
one changes the set of inputs that a certificate must cover.

## An attack searches for an allowed input that fails

Let $f_j(x)$ be the score that the classifier assigns to class $j$ for image $x$.
The predicted class is the one with the highest score. An attack starts from
$x_0$ and searches inside $S_p(x_0,\epsilon)$ for an input on which some other
class outranks **cat**.

A gradient-based attack, for example, uses information about how the model's
loss changes with the pixels. At each step, it uses this information to change
the pixels in a direction expected to cause a mistake.

Two outcomes are possible:

- **The attack finds a failure.** An allowed input makes another class outrank
  cat. That counterexample disproves the robustness claim.
- **The attack finds no failure.** None of the candidate inputs evaluated by this
  particular search changed the prediction.

## Why attack-based testing is incomplete

Why can the second outcome not prove robustness? Within $S_p(x_0,\epsilon)$,
each of the $d$ pixel values may vary, and those choices combine. For example, a
$224\times224$ RGB input has $d=150{,}528$ pixel values. In the real-valued
model, the set contains infinitely many points. A digital system has only
finitely many pixel values, but still far too many arrays to enumerate.

A stronger attack may find an adversarial input that an earlier attack missed.
If an attack finds no counterexample, none of the inputs it examined violated
the property, but every unexamined input in $S_p(x_0,\epsilon)$ remains
unresolved. Running more attacks may examine more inputs and strengthen the
empirical evidence. It does not establish the desired claim that no input in
$S_p(x_0,\epsilon)$ violates the property. The difference is coverage:
**examined inputs** versus **all allowed inputs**.

## Certification covers every allowed input

A certificate must cover the inputs that attacks never visit. Let $y$ denote the
class **cat**. We want to prove

$$
\text{for every }x\in S_p(x_0,\epsilon),\qquad
f_y(x)>f_j(x)\quad\text{for every }j\neq y.
$$

The inequality says that cat has a strictly higher score than every other class
for every allowed input. Proving it certifies
**local adversarial robustness** around $x_0$ at radius $\epsilon$.

Because enumeration is impossible, a certificate must reason about the network
and the input set without checking every point separately. In this series, a
**certificate** is a valid mathematical argument that proves the required
inequalities for every input in $S_p(x_0,\epsilon)$.

## Series map

Our target is now precise: prove the score inequality over the allowed set. The
rest of the series follows one small April classifier from its first proof to
the field's current research frontiers:

- **[Part 2 — What would count as a proof?]({{ '/2026-08-21-neural-network-certification-2-writing-the-guarantee/' | relative_url }})** We will build a tiny ReLU classifier
  and certify it by hand.
- **[Part 3 — How can bounds travel through a network?]({{ '/2026-08-21-neural-network-certification-3-interval-bound-propagation/' | relative_url }})** We will propagate ranges
  through the same classifier.
- **[Part 4 — Why do simple bounds lose information?]({{ '/2026-08-21-neural-network-certification-4-tighter-relaxations/' | relative_url }})** We will preserve useful
  relationships with linear bounds.
- **[Part 5 — What should we do if the bound is inconclusive?]({{ '/2026-08-21-neural-network-certification-5-complete-verification/' | relative_url }})** We will repeatedly
  split and bound the input region until every piece is certified or a
  counterexample is found.
- **[Part 6 — How can training make robustness easier to prove?]({{ '/2026-08-21-neural-network-certification-6-certified-training/' | relative_url }})** We will bracket
  the worst-case loss between attacks and certificates, then distinguish sound
  bound-based objectives from unsound training surrogates.
- **[Part 7 — What are the frontiers of neural network certification?]({{ '/2026-08-21-neural-network-certification-7-frontiers/' | relative_url }})** We will
  separate what certifiable networks can represent, what training can find,
  and what single- and multi-neuron relaxations can prove.
- **[Part 8 — How can random noise produce a certificate?]({{ '/2026-08-21-neural-network-certification-8-randomized-smoothing/' | relative_url }})** We will construct a
  randomized-smoothed classifier, derive its certified radius, then examine
  training objectives and why average certified radius can mislead.
- **[Part 9 — How can randomized smoothing adapt?]({{ '/2026-08-21-neural-network-certification-9-adaptive-randomized-smoothing/' | relative_url }})** We will use denoisers with
  pretrained classifiers, then certify input-dependent noise through Dual RS.

## Takeaway

An attack asks, “Can I find an allowed input that changes the prediction?” One
counterexample disproves robustness. If the attack finds none, the question
remains open. Certification closes it by proving that **every input in the
allowed set** keeps the required prediction.
