---
title: "How Can Bounds Travel Through a Network? Neural Network Certification, Part 3"
author_profile: true
permalink: /2026-08-21-neural-network-certification-3-interval-bound-propagation/
date: 2026-08-21
written_by: PIRA
written_at: 2026-08-21
tags: [neural networks, certification, interval bound propagation, robustness]
toc: true
published: false
excerpt: "Follow ranges through April's tiny classifier and turn a lower bound on its output margin into a certificate."
---

<!--
Status: outline only.

Reader outcome:
The reader can propagate interval bounds through a tiny ReLU network, explain
why a positive margin bound is a certificate, and recognize an inconclusive
bound without treating it as a counterexample.

Continuity requirement:
Reuse the exact two-input April classifier, weights, x_0, perturbation region,
and margin defined in Part 2. Do not introduce a second toy network.
-->

## How can we follow every allowed version of April at once?

<!--
Open with the Part 2 property and its hand proof. The obstacle is scale: tracing
each input separately is impossible, so each neuron will carry a range.
-->

## Give each input a lower and upper bound

<!--
Introduce this post's one main formal object: an interval [l, u]. Use the two
coordinates of the existing April input region. Explain addition, multiplication
by positive and negative weights, and sign changes only as they occur in the
worked network.
-->

## Carry the bounds through an affine layer

<!-- Derive every numerical lower and upper bound for the fixed network. -->

## Carry the bounds through ReLU

<!--
Show the three cases: always inactive, always active, and uncertain, while
keeping the calculation tied to the neurons in the April classifier.
-->

## Turn the output bound into a certificate

<!--
Propagate to the output margin. For the smaller region, obtain a positive lower
bound and connect it directly to the universal property from Part 2.
-->

## Increase the radius: the bound becomes inconclusive

<!--
Run the same calculation on the preselected larger region. The interval margin
should cross zero even though no counterexample has been produced. Label the
result unknown, not unsafe. This is the single obstacle that motivates Part 4.
-->

## The propagation rule in one pass

<!--
Condense the worked calculation into short pseudocode from input bounds to the
margin test. Keep the emphasis on the mechanism, not a survey of use cases.
-->

## Takeaway

<!--
Intervals can certify a whole region with one forward pass. End by asking what
information was lost in the larger-region calculation.
-->
