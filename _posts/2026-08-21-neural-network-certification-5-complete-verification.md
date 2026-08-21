---
title: "How Do We Turn Unknown into an Answer? Neural Network Certification, Part 5"
author_profile: true
permalink: /2026-08-21-neural-network-certification-5-complete-verification/
date: 2026-08-21
written_by: PIRA
written_at: 2026-08-21
tags: [neural networks, certification, branch and bound, complete verification]
toc: true
published: false
excerpt: "Split April's input region, bound each piece, and search until every piece is safe or one contains a concrete failure."
---

<!--
Status: outline only.

Reader outcome:
The reader can simulate branch and bound on the running classifier, distinguish
soundness from completeness, and interpret a proof, counterexample, or timeout.

Continuity requirement:
Start from the exact unresolved region left by Part 4. Reuse the same network,
property, bounds, and visual coordinate system so that splitting is the only new
idea.
-->

## One region is too hard; can two be easier?

<!--
Open with the remaining unknown for April. Show geometrically how dividing the
allowed set can make each local bound tighter.
-->

## Bound, split, and repeat

<!--
Introduce this post's one main formal object as a search tree. Work through the
mechanism before naming it: bound a region, discard it if proved safe, split it
if inconclusive, and repeat on its children.
-->

## Work through April's search tree

<!--
Use the prevalidated numerical example from Parts 2–4. Show each split and each
margin bound until all leaves are safe, or pair this proof case with a nearby
radius where a concrete counterexample is found.
-->

## Search for a failing input at the same time

<!--
Explain why an attack supplies candidate points while bounding handles entire
regions. A valid failing point immediately falsifies the claim; a successful
proof must cover every remaining region.
-->

## Now give the method its name

<!--
Name branch and bound after the worked mechanism. Then map MILP, SMT, and
specialized neural-network verifiers onto the same prove-or-find-a-counterexample
goal in one concise conceptual section, linking papers through arXiv.
-->

## Soundness, completeness, and timeouts

<!--
Define soundness and completeness using the finished search tree. Distinguish a
theoretically complete procedure from a run stopped by a resource limit, because
this distinction is required to interpret the algorithm's outcome.
-->

## Read the three outcomes from the tree

<!--
Return to verified, falsified, and unknown. Show exactly what artifact supports
each outcome: covered leaves, a concrete input, or an unfinished tree.
-->

## Takeaway

<!--
Splitting converts one difficult whole-set problem into smaller ones that bounds
can settle. End by asking whether training can make these proofs easier from the
start.
-->
