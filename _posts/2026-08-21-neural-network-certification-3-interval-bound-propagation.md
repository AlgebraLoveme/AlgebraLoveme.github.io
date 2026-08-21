---
title: "Neural Network Certification, Part 3: Proof by Propagating Bounds"
author_profile: true
permalink: /2026-08-21-neural-network-certification-3-interval-bound-propagation/
date: 2026-08-21
written_by: PIRA
written_at: 2026-08-21
tags: [neural networks, certification, interval bound propagation, robustness]
toc: true
published: false
excerpt: "A visual and mathematical introduction to interval bound propagation, the simplest way to certify many neural network properties."
---

<!--
Status: outline only.

Reader outcome:
The reader can propagate interval bounds through a tiny ReLU network, explain
why the result is sound, and diagnose why the bounds may be too loose.
-->

## How can finitely many calculations cover infinitely many inputs?

<!-- Motivate sets and bounds using the specification from Part 2. -->

## Interval arithmetic in one dimension

<!-- Work through addition, multiplication by constants, and sign changes. -->

## Propagating a box through a neural network

<!-- Derive affine-layer and ReLU bounds with a small numerical example. -->

## Turning output bounds into a certificate

<!-- Show how a lower bound on one class margin proves the desired label ordering. -->

## Why sound bounds become loose

<!-- Explain lost dependencies using a simple repeated-variable example and a visual. -->

## Verified, falsified, or unknown

<!-- Clarify that failure to certify is not evidence of a counterexample. -->

## When interval methods are useful

<!-- Discuss speed, scalability, limitations, and why they matter during training. -->

## Takeaway

<!-- Intervals trade precision for a fast, sound summary of an entire input set. -->
