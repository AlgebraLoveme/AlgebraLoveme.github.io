---
title: "Why Testing Is Not Proof: Neural Network Certification, Part 1"
series_nav_title: "Why Testing Is Not Proof"
author_profile: true
permalink: /2026-08-21-neural-network-certification-1-what-are-we-proving/
date: 2026-08-21
show_initial_release: false
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

Imagine that an image classifier receives this photo and predicts **cat**. The
prediction is correct for this input. Now darken the photo, compress it, add
camera noise, or change a few pixels. Will the prediction remain cat?

## Why models need to be robust

Suppose our classifier labels 9,800 of 10,000 test images correctly, giving 98%
test accuracy. That aggregate measure does not tell us whether a correct
prediction will survive nearby changes.

The same scene can reach the model through different cameras, lighting
conditions, compression settings, and preprocessing pipelines. We still see
April, but the classifier receives a different array of numbers each time.

A **robust** model preserves the required behavior when the input changes in
ways we have decided to allow. This raises two concrete questions:

1. Which input changes should we consider?
2. Which model behavior should remain unchanged?

For April's photo, we may require the predicted class to remain **cat** under a
specified amount of image noise. Another task might allow small rotations rather
than pixel noise. A regression task might instead require a numerical output to
remain within a safe range. The word *robust* is incomplete until we answer both
questions.

## From robustness to adversarial robustness

Random sensor noise is not chosen with the classifier in mind. An adversarial
perturbation is chosen specifically to make the classifier fail. **Adversarial
robustness** therefore asks a worst-case question:

> Can someone deliberately choose an **allowed** change to April's photo that
> makes the classifier stop predicting cat?

An allowed image that changes the prediction is an **adversarial example**.
Research on [adversarial examples](https://arxiv.org/abs/1312.6199) showed that
small, carefully chosen perturbations can change neural network predictions.
The [robust optimization viewpoint](https://arxiv.org/abs/1706.06083) frames
robustness through performance under the worst allowed perturbation. This
worst-case target motivates adversarial attacks, which search for an allowed
failure.

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
    <figcaption><strong>Conceptual perturbation.</strong> Visible noise illustrates a modified input. No classifier attack generated this image.</figcaption>
  </figure>
</div>

Restricting which changes are **allowed** prevents a trivial attack. Replacing
April's photo with a photo of a dog might change the prediction, but it tells us
nothing about whether the classifier is stable near the original photo. A
**threat model** draws this boundary by stating what may change, by how much, and
what counts as a successful attack.

Let $x_0$ represent April's photo, with pixel values normalized to $[0,1]$. We
measure a pixel perturbation with an $\ell_p$ norm, where
$1\leq p\leq\infty$, and limit its size with a radius $\epsilon$. The allowed
images therefore form the set

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

A standard gradient-based attack is [projected gradient descent
(PGD)](https://arxiv.org/abs/1706.06083). In the setting here, PGD takes steps
that *increase* the classification loss so that another class can outrank cat.
The word *projected* describes how every step is returned to the allowed set.
Starting from April's image or from a random point inside that set, PGD
repeatedly:

1. computes the gradient of the loss with respect to the pixels, which measures
   how the loss changes with each pixel.
2. changes the pixels in a direction that increases the loss.
3. projects the modified image back into $S_p(x_0,\epsilon)$.

For an $\ell_\infty$ threat model, the projection clips each pixel so that it
remains within $\epsilon$ of April's original pixel value and within the valid
range $[0,1]$. After several steps, PGD reports the highest-loss candidate it
found. Multiple random starting points, called **restarts**, let it search
different paths through the allowed set.

Two outcomes are possible:

- **The attack finds a failure.** An allowed input makes another class outrank
  cat. That counterexample disproves the robustness claim.
- **The attack finds no failure.** None of the candidate inputs evaluated by this
  particular search changed the prediction.

## Why attack-based testing is incomplete

Why does the second outcome fail to prove robustness? Within
$S_p(x_0,\epsilon)$,
each of the $d$ pixel values may vary, and those choices combine. A
$224\times224$ RGB input has three color values at every pixel, so
$d=224\cdot224\cdot3=150{,}528$. In the real-valued model, the set contains
infinitely many points. A digital system has only finitely many pixel values,
yet it still has far too many arrays to enumerate.

A stronger attack may find an adversarial input that an earlier attack missed.
If an attack finds no counterexample, none of the inputs it examined violated
the property, while every unexamined input in $S_p(x_0,\epsilon)$ remains
unresolved. Running more attacks can examine more inputs and strengthen the
empirical evidence. It still does not establish that no input in
$S_p(x_0,\epsilon)$ violates the property. The decisive difference is coverage:
**examined inputs** versus **all allowed inputs**.

## Certification covers every allowed input

A certificate must cover the inputs that attacks never visit. Let $y$ denote the
class **cat**. We want to prove

$$
\text{for every }x\in S_p(x_0,\epsilon),\qquad
f_y(x)>f_j(x)\quad\text{for every }j\neq y.
$$

The inequality requires cat to have a strictly higher score than every other
class for every allowed input. Proving it certifies
**local adversarial robustness** around $x_0$ at radius $\epsilon$.

Because enumeration is impossible, a certificate must reason about the network
and the input set without checking every point separately. In this series, a
**certificate** is a valid mathematical argument that proves the required
inequalities for every input in $S_p(x_0,\epsilon)$.

## Series map

This proof target determines the route through the series. Parts 2 through 6
follow one small April classifier from its first proof through certified
training. Parts 7 through 9 broaden the view to theoretical frontiers and
probabilistic certification:

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
  separate which functions certifiable networks can approximate, which models
  training can find, and which exact bounds a verifier can prove for a fixed
  network.
- **[Part 8 — How can random noise produce a certificate?]({{ '/2026-08-21-neural-network-certification-8-randomized-smoothing/' | relative_url }})** We will construct a
  randomized-smoothed classifier, derive its certified radius, then examine
  training objectives and why average certified radius can mislead.
- **[Part 9 — How can randomized smoothing adapt?]({{ '/2026-08-21-neural-network-certification-9-adaptive-randomized-smoothing/' | relative_url }})** We will use denoisers with
  pretrained classifiers, then certify input-dependent noise through Dual RS.

## Testing and certification answer different questions

The distinction drives the rest of the series. An attack asks, “Can I find an
allowed input that changes the prediction?” One counterexample disproves
robustness. A failed search leaves the claim unresolved. Certification supplies
the missing universal step by proving that **every input in the allowed set**
keeps the required prediction.
