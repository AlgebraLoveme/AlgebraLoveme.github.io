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

We restrict the weights to integers written in binary. Thus each weight has a finite representation, and the number of bits used to write it contributes to the input size. Proving hardness under this restriction is enough: any broader version that permits integer weights contains these instances.

Consider the associated decision problem:

> Given $G$, $s$, $t$, and a nonnegative integer $B$, is there an $s\text{-}t$ path $P$ with $c(P)\leq B$?

This problem is in NP: a proposed simple path lists at most $\lvert V\rvert$ vertices, and we can sum its weights and check the bound in polynomial time. To prove NP-hardness, it is enough to consider the special case $B=0$.

## Reduction from Partition

An instance of **Partition** is a list of positive integers $a_1,\ldots,a_n$. It asks whether the numbers can be divided into two groups with equal sums. Partition is one of the classical NP-complete problems described by [Karp](https://doi.org/10.1007/978-1-4684-2001-2_9).

From this list, construct a layered graph with main vertices $v_0=s,v_1,\ldots,v_n=t$. Between $v_{i-1}$ and $v_i$, add two directed two-edge branches:

- the upper branch has weights $+a_i$ and $0$;
- the lower branch has weights $-a_i$ and $0$.

The intermediate branch vertices keep the graph simple—there are no parallel edges. Every edge points from one layer to the next, so the result is a directed acyclic graph.

<figure>
  <a href="{{ '/imgs/partition-path-reduction.svg' | relative_url }}">
    <img src="{{ '/imgs/partition-path-reduction.svg' | relative_url }}" alt="A chain of diamond-shaped graph gadgets. For each input number, a directed path chooses either a positive-weight branch or a negative-weight branch, followed by a zero-weight edge.">
  </a>
</figure>

The graph has $3n+1$ vertices and $4n$ edges, so the construction takes polynomial time. Every $s\text{-}t$ path chooses a sign $\sigma_i\in\{+1,-1\}$ for each input number, and its signed weight is $\sum_{i=1}^n\sigma_i a_i$.

## Why the reduction works

1. **A valid partition gives a zero-cost path.** Put the numbers in one group on upper branches and those in the other group on lower branches. Equal group sums imply $\sum_i\sigma_i a_i=0$, so the path cost is zero.
2. **A zero-cost path gives a valid partition.** Place every number whose path branch has sign $+1$ in one group and every number with sign $-1$ in the other. A path cost of zero means the two group sums are equal.

Therefore, the answer to Partition is yes exactly when the constructed graph contains an $s\text{-}t$ path of absolute weight zero. If we could solve the absolute-weight path optimization problem in polynomial time, we could run that algorithm and test whether its optimum is zero, thereby solving Partition in polynomial time.

Because the decision problem is also in NP, it is NP-complete. The optimization problem is therefore NP-hard. This hardness already holds on a directed acyclic graph, so it does not arise from negative cycles.

## A small example

Take the numbers $3,1,2$. Choosing $+3$, then $-1$, then $-2$ produces the path weight $3-1-2=0$. The signs encode the equal-sum groups $3$ and $1+2$.

This example also shows why an algorithm cannot safely keep only the prefix with the smallest absolute total at each vertex. Suppose two partial paths reach the same vertex with totals $0$ and $100$. The first looks better if we compare absolute values immediately, but a remaining edge of weight $-100$ makes the second prefix perfect. An exact algorithm may therefore need to retain many attainable prefix sums.

## Scope and limitations

- **Nonnegative weights are easy.** If every edge weight is nonnegative, taking an absolute value changes nothing, and the problem reduces to ordinary shortest path.
- **The reduction proves only weak NP-hardness.** Because it starts from Partition, the proof does not establish strong NP-hardness. On a DAG with integral weights and $A=\sum_{e\in E}\lvert w(e)\rvert$, a dynamic program can record the attainable sums at each vertex in time polynomial in the graph size and the numerical value of $A$. This dependence on a number's value rather than its bit length is called pseudo-polynomial. Since $A$ can be exponential in the number of bits used to write the weights, such a running time is not necessarily polynomial in the input length.
- **This post asks for simple paths.** In the constructed DAG, no directed walk can repeat a vertex, so allowing walks would not change the reduction.

*Acknowledgment: The central reduction idea came from Runze Wang.*
