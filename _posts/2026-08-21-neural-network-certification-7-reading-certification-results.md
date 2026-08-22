---
title: "How Should We Read Certification Results? Neural Network Certification, Part 7"
author_profile: true
permalink: /2026-08-21-neural-network-certification-7-reading-certification-results/
date: 2026-08-21
written_by: PIRA
written_at: 2026-08-21
tags: [neural networks, certification, evaluation, robustness]
toc: true
published: false
excerpt: "Reconstruct the guarantees behind a table of April classifiers and compare clean, attacked, and certified results fairly."
---

<!--
Status: outline only.

Reader outcome:
The reader can reconstruct the exact claim behind each reported number, compare
models under matched conditions, and distinguish certification from attack-based
testing and unresolved verification runs. The reader also keeps the soundness of
the training objective separate from the soundness of post-training evaluation.
-->

## Which April classifier should we trust?

<!--
Open with one hypothetical table containing several April classifiers. Include
separate columns for the training objective and evaluation verifier, along with
enough result columns to tell the full story. Let the concrete comparison create
the need for each definition.
-->

## Reconstruct the claim behind one row

<!--
Introduce this post's main formal object: a result tuple containing the model,
training objective and its soundness, input set (norm and radius), property,
evaluation verifier, clean accuracy, attacked accuracy, certified accuracy,
unresolved fraction, and runtime. Fill it from the first row.
-->

## Read clean, attacked, certified, and unresolved together

<!--
Use the definitions from Part 6 and the three verifier outcomes from Parts 2 and
5. Show how an unsound training objective can still lead to sound certified
accuracy when the evaluation verifier is sound. Interpret each number through
the concrete rows rather than a detached checklist.
-->

## Make the comparison fair

<!--
Compare only matched models and claims: architecture, data and preprocessing,
property, norm, radius, verifier budget, and hardware where runtime matters.
Revise or annotate the table so that mismatches become visually obvious.
-->

## Tell the story of the whole table

<!--
Walk row by row from ordinary training through adversarial and certified training,
and from fast incomplete bounds to complete search. State the decision each
comparison supports; do not crown a winner from one isolated number.
-->

## Reconstruct the evidence behind the numbers

<!--
Name the minimum artifacts needed to understand or reproduce the table: precise
specification, model, preprocessing, verifier and numerical settings, timeout,
hardware, and code. Tie each item to a column already interpreted.
-->

## The path April took through the series

<!--
Retell the complete chain in one compact visual:
robustness question -> threat model -> attack -> testing gap -> universal property
-> bound -> tighter bound -> split search -> certified training -> reported result.
Mention other certifiable properties only as a brief epilogue after this chain.
-->

## Series conclusion

<!--
Return to April and the core distinction: an attack can disprove the claim with
one allowed input; a certificate proves the claim for every allowed input.
-->
