---
title: "Neural Network Certification, Part 6: Training Models to Be Certifiable"
author_profile: true
permalink: /2026-08-21-neural-network-certification-6-certified-training/
date: 2026-08-21
written_by: PIRA
written_at: 2026-08-21
tags: [neural networks, certification, certified training, robustness]
toc: true
published: false
excerpt: "Why post-hoc verification may fail, and how training can encourage both robust behavior and stronger certificates."
---

<!--
Status: outline only.

Reader outcome:
The reader understands why certifiability depends on the trained network and how
a differentiable certificate can become part of the training objective.
-->

## Verification cannot rescue every trained model

<!-- Separate a false property from a true property that current bounds cannot prove. -->

## From ordinary loss to a robust objective

<!-- Review empirical risk, adversarial examples, and worst-case loss conceptually. -->

## Training against a sound upper bound

<!-- Show how interval or relaxation bounds provide a differentiable surrogate. -->

## A simple certified-training loop

<!-- Present pseudocode and explain radius schedules and bound propagation. -->

## The trade-offs

<!-- Discuss clean accuracy, certified accuracy, training cost, and certificate tightness. -->

## What to measure

<!-- Define certified accuracy carefully and require matched radius, norm, data, and model. -->

## Takeaway

<!-- Certification can shape training, not merely audit the finished network. -->
