---
title: "Why Minimizing the Absolute Weight of a Path Is NP-Hard"
author_profile: true
permalink: /MY_INSIGHTS/2019-11-21-Hardness_of_a_variant_of_Shortest_Path/
date: 2019-11-21
last_modified_at: 2026-08-21
last_modified_by: PIRA
tags: [complexity theory, graph algorithms, NP-completeness]
mathjax: true
header:
    image: "/imgs/absolute-weight-path-hero.jpg"
excerpt: "A small change to the shortest-path objective turns it into a disguised Partition problem."
---

Ordinary shortest path minimizes the sum of the edge weights along a route. Consider one small-looking change: instead, minimize the **absolute value** of that sum. Positive and negative edges may now cancel, so a path with a large positive prefix can ultimately be better than one whose prefix is already near zero.

That loss of a reliable “best prefix” is not merely inconvenient. The resulting optimization problem is NP-hard, even on a directed acyclic graph.

## The problem

Let $G=(V,E)$ be a directed graph with designated vertices $s$ and $t$. Every edge $e$ has an integer weight $w(e)$, which may be positive, zero, or negative. For a simple $s\text{-}t$ path $P$, define its cost as $c(P)=\left\lvert\sum_{e\in P}w(e)\right\rvert$. The goal is to find a path of minimum cost.

Using integers is deliberate. Standard complexity analysis assumes that an algorithm receives a finite sequence of bits. Binary notation gives every integer a finite representation, and the number of bits becomes part of the input size. Rational weights can be converted to integers by multiplying every weight by a common denominator. This scales every path total by the same positive factor, so the optimal path does not change. Arbitrary real numbers, however, may not have finite representations and require a different computational model.

It is helpful to state the associated decision problem:

> Given $G$, $s$, $t$, and a nonnegative integer $B$, is there an $s\text{-}t$ path $P$ with $c(P)\leq B$?

This problem is in NP: a path is a polynomial-size certificate, and its weight can be summed and checked in polynomial time. We will prove NP-hardness by considering only the special case $B=0$.

## Reduction from Partition

An instance of **Partition** is a list of positive integers $a_1,\ldots,a_n$. It asks whether the numbers can be divided into two groups with equal sums. Partition is one of the classical NP-complete problems described by [Karp](https://doi.org/10.1007/978-1-4684-2001-2_9).

From this list, construct a layered graph with main vertices $v_0=s,v_1,\ldots,v_n=t$. Between $v_{i-1}$ and $v_i$, add two directed two-edge branches:

- the upper branch has weights $+a_i$ and $0$;
- the lower branch has weights $-a_i$ and $0$.

The intermediate branch vertices keep the graph simple—there are no parallel edges. Every edge points from one layer to the next, so the result is a directed acyclic graph.

<figure>
  <a href="{{ '/imgs/partition-path-reduction.svg' | relative_url }}">
    <img src="{{ '/imgs/partition-path-reduction.svg' | relative_url }}" alt="A chain of diamond-shaped graph gadgets. At item i, a directed path chooses either a branch weighted plus a sub i or a branch weighted minus a sub i, followed by a zero-weight edge.">
  </a>
  <figcaption>The reduction uses one choice gadget per input number. Every $s\text{-}t$ path selects exactly one sign for each $a_i$.</figcaption>
</figure>

The graph has only $3n+1$ vertices and $4n$ edges, so it can be built in polynomial time. More importantly, every $s\text{-}t$ path corresponds to a sign choice $\sigma_i\in\{+1,-1\}$ for each input number, and its signed weight is $\sum_{i=1}^n\sigma_i a_i$.

## Why the reduction works

The two directions are direct:

1. **A valid partition gives a zero-cost path.** Put the numbers in one group on upper branches and those in the other group on lower branches. Equal group sums imply $\sum_i\sigma_i a_i=0$, so the path cost is zero.
2. **A zero-cost path gives a valid partition.** Place every number whose path branch has sign $+1$ in one group and every number with sign $-1$ in the other. A path cost of zero means the two group sums are equal.

Therefore, the Partition instance is a yes-instance exactly when the constructed graph contains an $s\text{-}t$ path of absolute weight zero. If we could solve the absolute-weight path optimization problem in polynomial time, we could run that algorithm and test whether its optimum is zero, thereby solving Partition in polynomial time.

The decision problem is thus NP-complete, and the optimization problem is NP-hard. The proof is stronger than a generic negative-edge argument: the constructed graph is acyclic, so negative cycles and repeated walks play no role. If we remove the edge directions, each $v_i$ still separates the earlier gadgets from the later ones; consequently, the same construction also proves hardness for undirected simple paths.

## A small example

Take the numbers $3,1,2$. The path can choose $+3$, then $-1$, then $-2$, producing total weight $3-1-2=0$. Reading the signs recovers the partition $\{3\}$ and $\{1,2\}$.

This example also shows why a conventional shortest-path recurrence loses the information it needs. Suppose two partial paths reach the same vertex with totals $0$ and $100$. The first looks better if we compare absolute values immediately, but a remaining edge of weight $-100$ makes the second prefix perfect. An algorithm may need to retain many attainable prefix sums rather than one “best” value per vertex.

## What the proof does—and does not—say

- **Nonnegative weights are easy.** If every edge weight is nonnegative, taking an absolute value changes nothing, and the problem reduces to ordinary shortest path.
- **The hardness shown here is weak NP-hardness.** The reduction comes from Partition, which admits pseudo-polynomial algorithms. On a DAG with integral weights and $A=\sum_{e\in E}\lvert w(e)\rvert$, dynamic programming over vertices and attainable sums can run in time polynomial in $A$, but $A$ may be exponential in the binary input length.
- **The route must be defined precisely.** This post uses simple paths. The acyclic reduction makes the distinction between paths and walks irrelevant for the constructed instances, but it can matter in other graphs.

The motivating application was bicycle redistribution: visiting a station can contribute a signed pickup or delivery amount, and one may want the final load imbalance to be close to zero. Real routing systems also impose vehicle capacities, travel costs, time windows, and possibly station revisits. The proof above establishes hardness for the abstract cancellation objective; it should not be mistaken for a complete model of the operational problem.

The central reduction idea came from my roommate, Runze Wang. The polished version makes the graph construction and both directions of the proof explicit.
