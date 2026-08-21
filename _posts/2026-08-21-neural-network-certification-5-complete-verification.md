---
title: "Neural Network Certification, Part 5: Search for a Complete Answer"
author_profile: true
permalink: /2026-08-21-neural-network-certification-5-complete-verification/
date: 2026-08-21
written_by: PIRA
written_at: 2026-08-21
tags: [neural networks, certification, branch and bound, complete verification]
toc: true
published: false
excerpt: "How splitting, search, and optimization can turn inconclusive bounds into a proof or a concrete counterexample."
---

<!--
Status: outline only.

Reader outcome:
The reader can distinguish soundness from completeness and describe how a
branch-and-bound verifier combines lower bounds, upper bounds, and splitting.
-->

## When a sound method says “unknown”

<!-- Use an example where the property is true but the relaxation is too loose. -->

## Soundness and completeness are different promises

<!-- Define both plainly and separate theoretical completeness from practical timeout. -->

## Split the problem, then bound each piece

<!-- Walk through branch and bound on a two-dimensional or one-ReLU example. -->

## Looking for a counterexample at the same time

<!-- Explain feasible attacks or optimization as upper bounds, not as proofs of safety. -->

## Other views of the same verification problem

<!-- Introduce mixed-integer programming and satisfiability solving at a conceptual level. -->

## Why complete verification can be expensive

<!-- Explain combinatorial activation patterns and the importance of branching heuristics. -->

## Reading verifier outcomes correctly

<!-- Separate proved, disproved, timeout, numerical failure, and unsupported model. -->

## Takeaway

<!-- Search can close the gap left by relaxations, often at substantial computational cost. -->
