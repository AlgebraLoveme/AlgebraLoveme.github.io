---
title: "Neural Network Certification, Part 2: Writing the Guarantee"
author_profile: true
permalink: /2026-08-21-neural-network-certification-2-writing-the-guarantee/
date: 2026-08-21
written_by: PIRA
written_at: 2026-08-21
tags: [neural networks, certification, specifications, robustness]
toc: true
published: false
excerpt: "How to turn an informal reliability goal into the inputs, outputs, assumptions, and mathematical property that a verifier can check."
---

<!--
Status: outline only.

Reader outcome:
The reader can translate a small informal robustness claim into a precise
verification specification and identify what that specification omits.
-->

## From “robust” to a statement we can check

<!-- Start with ambiguous uses of robust. Show why the verifier needs a bounded claim. -->

## The anatomy of a specification

<!-- Introduce the model, input set or precondition, and output property or postcondition. -->

## Our running example in symbols

<!--
Formalize local classification robustness gradually. Define logits, the predicted
class, a perturbation set, norms, and the radius. Put plain language before each
equation and use a two-dimensional picture.
-->

## Choosing the input set

<!--
Compare box constraints and common norm balls. Explain that mathematical distance
does not automatically equal perceptual similarity or real-world plausibility.
-->

## Properties beyond an unchanged label

<!-- Brief examples: output bounds, monotonicity, fairness constraints, and control safety. -->

## When the specification proves the wrong thing

<!-- Cover omitted preprocessing, unrealistic perturbations, and weak proxies for safety. -->

## A specification checklist

<!-- Give a reusable template that prepares the reader for the algorithmic posts. -->

## Takeaway

<!-- A useful certificate begins with a precise and meaningful specification. -->
