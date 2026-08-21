---
title: "Can We Train a Network to Be Certifiable? Neural Network Certification, Part 6"
author_profile: true
permalink: /2026-08-21-neural-network-certification-6-certified-training/
date: 2026-08-21
written_by: PIRA
written_at: 2026-08-21
tags: [neural networks, certification, certified training, robustness]
toc: true
published: false
excerpt: "Move from ordinary training to adversarial and certified objectives, then read what each one teaches April's classifier."
---

<!--
Status: outline only.

Reader outcome:
The reader can distinguish ordinary, adversarial, and certified training losses,
follow a minimal certified-training loop, and interpret clean, attacked, and
certified accuracy.
-->

## Can training make April's prediction easier to prove?

<!--
Return to the proof effort in Part 5. Ask whether the network can learn parameters
that keep the April margin positive and make its lower bound easier to establish.
-->

## Ordinary training learns from the examples it sees

<!--
Introduce an ordinary classification loss on sampled images. Use April and a few
neighboring examples to show what the objective directly rewards.
-->

## Adversarial training adds hard searched examples

<!--
Connect to Part 1 attacks: approximately maximize the loss inside the allowed set,
then train on the found input. Keep the distinction between search and proof crisp.
-->

## Certified training optimizes a bound on every allowed input

<!--
Introduce this post's one main formal object: a certified robust loss obtained
from a sound bound on worst-case loss or margin. Connect its calculation to the
bound propagation already learned in Parts 3–4.
-->

## Put the three objectives side by side

<!--
Use one compact equation or diagram to compare ordinary, adversarial, and
certified objectives by what each optimizes. Avoid a broad literature survey.
-->

## A minimal certified-training loop

<!--
Give short pseudocode: sample a batch, construct allowed sets, propagate bounds,
compute the certified loss, update parameters. Explain any radius schedule only
where it appears in the loop.
-->

## Read the three accuracy numbers

<!--
Define clean accuracy, attacked accuracy, and certified accuracy near their first
joint use. Show a small hypothetical April-classifier result and ensure every
number uses the same model, norm, and radius.
-->

## Takeaway

<!--
Certification can shape the learned network rather than only auditing it later.
End by asking how to judge a larger table of such results fairly.
-->
