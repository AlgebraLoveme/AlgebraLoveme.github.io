---
title: "Three Research Frontiers: Neural Network Certification, Part 7"
author_profile: true
permalink: /2026-08-21-neural-network-certification-7-frontiers/
date: 2026-08-21
written_by: PIRA
written_at: 2026-08-21
tags: [neural networks, certification, theory, abstract interpretation]
toc: true
published: false
excerpt: "Three surprising results separate what certifiable networks can represent, what training can find, and what a verifier can prove."
---

<!--
Status: outline only.

Reader outcome:
The reader can separate three questions that are often confused: whether a
certifiable network exists, whether training can find one, and whether a chosen
relaxation can prove its behavior. The reader will understand the interval
universal approximation theorem, the paradox of certified training, and the
expressiveness gap between single-neuron and multi-neuron relaxations.
-->

## April reaches the edge of our map

<!--
Open with April's classifier after Parts 1–6: we know how to state its property,
propagate bounds, refine an inconclusive result, and train it for certification.
Now ask a question that the algorithms alone cannot answer:

**What limits certified neural networks: what a model can represent, what
training can find, or what a verifier can prove?**

Preview three results that initially pull in different directions: even IBP has
a universal approximation theorem; tighter relaxations can train worse models;
and a relaxation that studies neurons jointly can prove facts that every
single-neuron relaxation misses.
-->

## Existence, training, and proof are different questions

<!--
Build the conceptual map for the post before introducing any theorem:

1. Representation: does a network with the desired certified behavior exist?
2. Optimization: can a practical training procedure find such a network?
3. Abstraction: can the verifier retain the relationships needed to prove it?

Use "exist, find, prove" as a recurring three-word guide. Keep the mathematics
to undergraduate calculus, linear algebra, and convex sets introduced visually.
-->

## Frontier 1: Can an IBP-certified network approximate any continuous function?

<!--
Briefly recall the ordinary universal approximation theorem: sufficiently large
neural networks can approximate continuous functions on compact domains. Then
explain why certification asks for more. We want the network's output and the
interval computed by IBP over each input box to approximate the true function
and its output range.

State the interval universal approximation result from Baader, Mirman, and
Vechev in reader-level language. Use a one-dimensional "April score" curve and
several input intervals: the constructed ReLU network follows the curve, while
its IBP bands follow the curve's actual range on each interval.

Primary source:
https://arxiv.org/abs/1909.13846

Generalization to squashable activation functions:
https://arxiv.org/abs/2007.06093
-->

## A network may exist before we know how to find it

<!--
Use the generalized interval-approximation result's construction complexity to
make the necessary transition from representation to optimization. An
existence theorem answers "can such a network exist?" Training must answer
"can we reach one with a useful architecture and a practical amount of work?"

Return to April: knowing that some large interval-friendly classifier exists
does not provide its weights. This prepares the certified-training paradox
without turning the theorem into a generic limitations discussion.
-->

## Frontier 2: Why can a tighter bound train a worse certifiable model?

<!--
Start from the intuition established in Parts 4 and 6: for fixed network
weights, a tighter sound relaxation gives a no-worse upper bound. Then change
one phrase—"fixed weights"—and follow what happens during training, when the
weights move after every gradient step.

Explain the paradox of certified training: loose interval-based objectives can
produce models with higher certified robustness than training with tighter
relaxations. Tightness describes the bound at one set of weights; optimization
also depends on how continuously and sensitively the bound changes as the
weights move.

Plan a figure with the same April classifier and two certified-loss landscapes.
Mark a few gradient steps so readers can see how the smoother training signal
can be easier to follow even when its value is looser.

Primary source:
https://arxiv.org/abs/2102.06700
-->

## Frontier 3: What can a relaxation express about several neurons?

<!--
Reconnect to Triangle and DeepPoly from Part 4. Each ReLU receives its own
convex constraints. Those constraints may be optimal for each neuron in
isolation while forgetting that two neurons came from the same input.

Use a tiny ReLU network encoding max(x_1, x_2). Draw the feasible pairs of two
hidden ReLU values. Individual convex envelopes admit combinations that no
single input can produce, so every single-neuron relaxation inherits a gap on
this example. Name this the single-neuron convex barrier only after the picture
has made the missing relationship concrete.
-->

## Multi-neuron relaxations remember joint geometry

<!--
Add one constraint over the pair of hidden neurons and show how it removes the
impossible combinations. Explain the expressiveness result: the max function
can be encoded by a ReLU network and bounded exactly by a multi-neuron
relaxation, while no single-neuron relaxation can do so.

Connect the theorem to scalable methods such as PRIMA, which approximate convex
hulls over small neuron groups. Group size creates the research decision:
preserve the relationships that matter while keeping the proof affordable.

Primary expressiveness source:
https://arxiv.org/abs/2410.06816

PRIMA:
https://arxiv.org/abs/2103.03638
-->

## Put the three frontiers on one map

<!--
Complete a compact table:

- Can the desired certifiable model exist? Interval universal approximation
  says yes for continuous targets under its assumptions.
- Can training find it? The certified-training paradox shows that bound
  tightness alone does not determine a useful optimization objective.
- Can the verifier prove it? Multi-neuron relaxations can express joint facts
  that single-neuron relaxations necessarily lose.

Derive one concrete research question from each row: constructive
interval-friendly architectures, certified objectives with favorable training
dynamics, and scalable selection of informative neuron groups.
-->

## Takeaway

<!--
Return to April and the three verbs. Existence belongs to the network class;
finding belongs to optimization; proving belongs to the verifier's abstraction.
Progress in neural network certification requires us to say which frontier a
new result moves.
-->
