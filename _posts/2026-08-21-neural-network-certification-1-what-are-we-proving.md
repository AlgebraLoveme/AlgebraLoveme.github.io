---
title: "Testing Is Not Proof: A First Look at Neural Network Certification"
author_profile: true
permalink: /2026-08-21-neural-network-certification-1-what-are-we-proving/
date: 2026-08-21
written_by: PIRA
written_at: 2026-08-21
tags: [neural networks, certification, formal verification, robustness]
mathjax: true
toc: true
excerpt: "April the Siberian cat helps us follow one image from ordinary robustness to adversarial attacks, incomplete testing, and neural network certification."
---

Meet April. He is a Siberian cat.

<figure style="text-align: center;">
  <a href="{{ '/imgs/April_the_cat.jpg' | relative_url }}">
    <img src="{{ '/imgs/April_the_cat.jpg' | relative_url }}" width="520" style="display: block; margin: 0 auto;" alt="April, a cream-colored Siberian cat with gray ears, sitting beside a tree in sunlight.">
  </a>
  <figcaption>April, a Siberian cat, will be our running example. We will follow this one photo from ordinary testing to a mathematical guarantee.</figcaption>
</figure>

Imagine that we give this photo to an image classifier and it predicts **cat**.
That answer is correct, but one correct prediction tells us very little about
what happens next. Would the model still recognize a darker photo of April? What
about camera noise, image compression, or a few carefully chosen pixel changes?

These questions lead from accuracy to robustness, from robustness to adversarial
attacks, and finally from testing to certification.

## Why models need to be robust

Suppose our classifier labels 9,800 of 10,000 test images correctly. Its test
accuracy is 98%. This is useful evidence about performance on that sample. Under
appropriate sampling assumptions, it may also help us estimate performance on
similar data.

The accuracy number does not tell us whether the prediction for April is stable.
The same scene can reach the model through different cameras, lighting
conditions, compression settings, and preprocessing pipelines. To us, the image
still shows April. To the classifier, each version is a different array of
numbers.

A **robust** model preserves the required behavior under the changes we care
about. That definition contains two choices:

1. Which input changes should we consider?
2. Which model behavior should remain unchanged?

For April's photo, we may require the predicted class to remain **cat** under a
specified amount of image noise. A different application may care about
rotation, brightness, camera position, or an entirely different output property.
There is no useful claim that a model is simply “robust to everything.”

## From robustness to adversarial robustness

Ordinary noise follows some process, such as random sensor error. **Adversarial
robustness** asks a worst-case question instead:

> Can someone deliberately choose an **allowed** change to April's photo that
> makes the classifier stop predicting cat?

If such a modified image exists, it is an **adversarial example**. The change is
chosen for its effect on the model rather than sampled at random. Research on
[adversarial examples](https://arxiv.org/abs/1312.6199) showed that carefully
chosen small perturbations could change neural network predictions. The
[robust optimization viewpoint](https://arxiv.org/abs/1706.06083) asks us
to evaluate the worst allowed perturbation rather than an average one.

The comparison below makes the idea of a perturbation visible. The right image
adds a fine noise pattern while preserving the scene that we recognize as April.

<div style="display: flex; flex-wrap: wrap; gap: 1rem; justify-content: center; align-items: flex-start;">
  <figure style="flex: 1 1 260px; max-width: 360px; margin: 0; text-align: center;">
    <a href="{{ '/imgs/April_the_cat.jpg' | relative_url }}">
      <img src="{{ '/imgs/April_the_cat.jpg' | relative_url }}" alt="Original photograph of April the Siberian cat beside a tree.">
    </a>
    <figcaption><strong>Original.</strong> The classifier receives April's photograph.</figcaption>
  </figure>
  <figure style="flex: 1 1 260px; max-width: 360px; margin: 0; text-align: center;">
    <a href="{{ '/imgs/April_the_cat_conceptual_perturbation.jpg' | relative_url }}">
      <img src="{{ '/imgs/April_the_cat_conceptual_perturbation.jpg' | relative_url }}" alt="Conceptual AI-generated variation of April's photograph with fine multicolored pixel noise; it is not a verified adversarial example.">
    </a>
    <figcaption><strong>Conceptual perturbation.</strong> Visible noise illustrates a modified input; no classifier attack was run.</figcaption>
  </figure>
</div>

The word *allowed* is essential. We need a **threat model** that states what may
change and by how much. It may also specify what the attacker knows and what
counts as success. Different threat models describe different questions.

Let $x_0$ represent April's photo. Assume that its pixel values lie between 0 and
1. Choose an $\ell_p$ norm, with $1\leq p\leq\infty$, to measure the size of a
change and a radius $\epsilon$ to limit it. The allowed images form the set

$$
S_p(x_0,\epsilon)
=\left\{x\in[0,1]^d:\lVert x-x_0\rVert_p\leq\epsilon\right\}.
$$

Here, $d$ counts all pixels and color channels. The value of $p$ determines how
their changes are combined. When $p=\infty$, the norm measures the largest
absolute pixel change, so every pixel may change by at most $\epsilon$. Every
point in $S_p(x_0,\epsilon)$ is one numerical version of April's photo permitted
by our threat model.

This threat model is mathematically convenient, but it is not a perfect model of
visual similarity. Its pixel-wise limits do not directly describe rotation,
camera motion, or every lighting change. We will examine such modeling choices
in the next post.

## An attack searches for a version that fails

Let $f_j(x)$ be the score that the classifier assigns to class $j$ for image $x$.
The predicted class is the one with the highest score. An attack starts from
$x_0$ and searches inside $S_p(x_0,\epsilon)$ for a version on which some other
class outranks **cat**.

A gradient-based attack, for example, uses information about how the model's
loss changes with the pixels. It adjusts them in directions that appear more
likely to cause a mistake. The result is a targeted test of the model rather
than a random collection of image changes.

Two outcomes are possible:

- **The attack finds a failure.** We now have a modified version of April's photo
  that the model does not label cat. This one image disproves the robustness
  claim.
- **The attack finds no failure.** The images visited by this search did not
  break the model.

The first conclusion is decisive. The second is not.

## Why attack-based testing is incomplete

Why is a failed attack inconclusive? The allowed set changes every pixel, and
all those choices combine. In the real-valued model, $S_p(x_0,\epsilon)$ contains
infinitely many numerical images. A digital system uses finite precision, but
the number of possible images is still far too large for ordinary enumeration.

An attack navigates this space intelligently, but it still examines only part of
it unless its search comes with a completeness guarantee. A stronger attack may
find a version of April's photo that an earlier attack missed. More attacks give
us better empirical evidence, but they do not automatically cover every allowed
image.

The logical distinction is:

- **No attack found a failure.** This is a report about the searches we ran.
- **No allowed failure exists.** This is a statement about the entire set.

This is the gap between **not finding a failure** and **proving that no failure
exists**.

## Certification asks about every allowed version

Neural network certification addresses this gap with a universal claim. Let
$y$ denote the class **cat**. Instead of checking selected versions of April's
photo, we want to prove

$$
\text{for every }x\in S_p(x_0,\epsilon),\qquad
f_y(x)>f_j(x)\quad\text{for every }j\neq y.
$$

In words, cat must have a strictly higher score than every other class for every
allowed version of the photo. If we prove this statement, we have certified
**local adversarial robustness** around $x_0$ at radius $\epsilon$.

Certification does not run the network separately on every image. It reasons
about sets of possible values, using mathematical bounds, logical solving, or a
combination of both.

This task connects naturally to program verification. During inference, a fixed
neural network is a numerical program. It applies a known sequence of operations
to its input. Program verification describes the allowed inputs with a
**precondition** and the required outputs with a **postcondition**:

- The precondition $P(x)$ describes the allowed inputs.
- The postcondition $Q(f(x))$ describes the required outputs.

The verification claim is

$$
\text{for every }x,\qquad P(x)\Longrightarrow Q(f(x)).
$$

For April's photo, the precondition is $x\in S_p(x_0,\epsilon)$. The postcondition
requires cat to outrank every competing class.

The property holds exactly when no allowed input violates the postcondition.
Solver-based methods such as
[Reluplex](https://arxiv.org/abs/1702.01135) use this perspective to prove
supported properties or produce counterexamples. Bound-based methods enclose
all possible outputs and prove that none violate the requirement. For example,
[Fast-Lin and Fast-Lip](https://arxiv.org/abs/1804.09699) compute
certified lower bounds on the perturbation needed to change a ReLU network's
decision.

In this series, a **certificate** means that a sound mathematical procedure has
established the scoped claim.

## Three possible outcomes

A verification attempt for April's photo can have three practically important
outcomes:

- **Verified:** the method proves that every allowed version remains classified
  as cat.
- **Falsified:** the method finds an allowed version with a different predicted
  class.
- **Unknown:** the method establishes neither result. Its approximation may be
  too loose, it may run out of resources, or it may not support part of the
  model.

A trustworthy verified result requires **soundness**. A sound method does not
certify a false claim when its mathematical and numerical assumptions hold.
Soundness does not mean that the method can prove every true claim. Some sound
methods return unknown whenever their approximation is inconclusive.

Unknown is not the same as unsafe. The property may be false, or it may be true
but difficult for this method to prove. Later posts will show how tighter bounds
and search can resolve some unknown cases.

## Where the series goes next

April's photo has taken us from one correct prediction to robustness,
adversarial attacks, incomplete testing, and certification. The rest of the
series will build the technical ideas in small steps:

1. **Writing the guarantee:** turn an informal goal into input and output
   specifications.
2. **Proof by propagating bounds:** use interval arithmetic to reason about a
   whole input region.
3. **Tighter bounds with relaxations:** preserve more information with linear
   bounds and abstract domains.
4. **Search for a complete answer:** combine bounds with splitting,
   branch-and-bound, and solver-based reasoning.
5. **Training models to be certifiable:** make provable robustness part of the
   learning objective.
6. **Reading results critically:** compare certified models and verifiers under
   matched assumptions.

## Takeaway

An attack may find one allowed version of April's photo that fools the
classifier. If it does, the robustness claim is false. If it does not, other
versions remain untested. Certification makes the stronger claim: **every image
in the defined set** keeps the required prediction.
