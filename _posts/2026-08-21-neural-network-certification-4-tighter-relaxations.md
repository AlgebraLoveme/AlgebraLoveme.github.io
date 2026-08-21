---
title: "Why Do Simple Bounds Lose Information? Neural Network Certification, Part 4"
author_profile: true
permalink: /2026-08-21-neural-network-certification-4-tighter-relaxations/
date: 2026-08-21
written_by: PIRA
written_at: 2026-08-21
tags: [neural networks, certification, linear relaxation, abstract interpretation]
toc: true
published: false
excerpt: "April's classifier exposes what intervals forget, then linear bounds preserve enough relationships to prove more."
---

<!--
Status: outline only.

Reader outcome:
The reader can locate dependency loss in interval propagation, draw sound linear
bounds for an unstable ReLU, and use the retained relationships to tighten the
same output margin.

Continuity requirement:
Begin with the larger-region unknown case from Part 3. Reuse the exact network,
numbers, property, and diagram conventions; change the reasoning method only.
-->

## Why did April's margin cross zero?

<!--
Reproduce only the decisive lines of the Part 3 calculation. Track where two
values that depend on the same input are later treated as if they could vary
independently.
-->

## The missing information is a relationship

<!--
Introduce this post's one main formal object: an affine bound that remains a
function of the original input. Contrast it visually with a box, using the
existing April network rather than a detached algebra example.
-->

## Enclose an unstable ReLU with lines

<!--
Draw the ReLU graph on its known input interval. Derive intuitive lower and upper
lines that contain every possible ReLU output.
-->

## Carry the lines to April's output margin

<!--
Substitute the affine bounds through the remaining layer. Compare the resulting
margin bound with the interval result on the exact same region and state whether
the tighter calculation now certifies it.
-->

## One geometric viewpoint

<!--
Name abstract interpretation only after the worked result: boxes and affine
relationships are two sound ways to summarize a set of neuron values. Keep this
as a short unifying perspective, not a separate tutorial or taxonomy.
-->

## What remains unknown?

<!--
Increase to the prevalidated large radius. Show in one compact calculation that
even the tighter bound is inconclusive, and use this result to motivate splitting
in Part 5.
-->

## Takeaway

<!--
Preserving relationships can turn an interval unknown into a certificate. End
with the question: when one bound is still inconclusive, can smaller regions help?
-->
