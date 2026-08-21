---
title: "What Would Count as a Proof? Neural Network Certification, Part 2"
author_profile: true
permalink: /2026-08-21-neural-network-certification-2-writing-the-guarantee/
date: 2026-08-21
written_by: PIRA
written_at: 2026-08-21
tags: [neural networks, certification, specifications, robustness]
toc: true
published: false
excerpt: "April meets a tiny ReLU classifier as we turn an informal promise into a mathematical statement and prove it by hand."
---

<!--
Status: outline only.

Reader outcome:
The reader can state local robustness as a margin property over an input set,
follow a hand-built certificate, and interpret the outcomes of verification.

Shared example contract for Parts 2–5:
- Introduce one two-input ReLU "April classifier" here.
- Fix and record its exact weights, input point, and output margin; reuse them
  unchanged in Parts 3–5. Vary only the perturbation radius, and announce every
  change.
- Choose the numbers before drafting the prose and check them computationally:
  a small radius must admit the Part 2 hand proof and the Part 3 interval proof;
  a medium radius must be unknown to intervals but certified by the Part 4
  relaxation; a large radius must be unknown to that relaxation but resolved by
  the Part 5 search.
-->

## Can we prove that April remains a cat?

<!--
Return directly to April. Replace the full image network with a two-input ReLU
classifier small enough to draw and calculate by hand. State what each input
feature and each output score means.
-->

## Measure the decision with one margin

<!--
Introduce the post's one main formal object:
  m(x) = f_cat(x) - f_other(x).
Explain that m(x) > 0 means the classifier chooses cat, turning two output scores
into one quantity whose sign answers the question.
-->

## State the claim for every allowed input

<!--
Reuse S_p(x_0, epsilon) from Part 1 and state:
  m(x) > 0 for every x in S_p(x_0, epsilon).
Draw the two-dimensional allowed region and connect "for every" to the testing
gap from Part 1. Do not re-teach norm notation.
-->

## Build our first certificate by hand

<!--
Evaluate sound lower bounds through the tiny network one operation at a time.
End with a positive lower bound on m(x), and say explicitly why that proves the
whole-set claim rather than merely checking sample points.
-->

## Name the pieces of the proof

<!--
Only after the worked proof, extract the program-verification vocabulary:
- precondition or input set;
- fixed neural network;
- postcondition or output property;
- certificate.
Present P(x) => Q(f(x)) as a compact restatement of the proof just completed.
Briefly introduce bound-based and solver-based verification as the two method
families that later posts will develop; use arXiv links for papers.
-->

## What can a verifier report?

<!--
Use the April claim to define verified, falsified with a counterexample, and
unknown. Introduce soundness as the rule that a verified answer cannot be false.
Keep completeness conceptual and defer its fuller treatment to Part 5.
-->

## April's specification, in one box

<!--
Summarize the concrete model, x_0, allowed set, margin, and universal property in
one compact visual or callout. This becomes the stable reference for Parts 3–5.
-->

## Takeaway

<!--
A certificate proves that the margin stays positive over the entire allowed set.
End with the next question: how can we compute such a bound in a larger network?
-->
