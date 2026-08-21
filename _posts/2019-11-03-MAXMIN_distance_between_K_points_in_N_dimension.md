---
title: "Maximin Point Separation on a High-Dimensional Sphere"
author_profile: true
permalink: 2019-11-03-MAXMIN_distance_between_K_points_in_N_dimension/
date: 2019-11-03
last_modified_at: 2026-08-21
last_modified_by: PIRA
tags: [geometry, optimization, spherical codes]
mathjax: true
header:
    image: "/imgs/spherical-code-hero-v2.jpg"
excerpt: "How far apart can K points be placed on a unit sphere in N-dimensional space?"
---

Suppose we place $K$ points on the unit sphere in $N$-dimensional Euclidean space. How should we arrange them so that even the closest pair is as far apart as possible? This is a **maximin** problem: maximize the minimum pairwise distance.

This question is a version of the **spherical-code problem**. It is easy to picture on a circle or an ordinary sphere, but higher dimensions reveal a particularly clean interaction between geometry and the number of points.

## Defining the problem

Each point $x_i$ lies on the unit sphere $S^{N-1}$, so $x_i \in \mathbb{R}^N$ and $\lVert x_i\rVert_2=1$. For one configuration, its separation is $d(x_1,\ldots,x_K)=\min_{i<j}\lVert x_i-x_j\rVert_2$. We want the largest attainable value, $d^*(N,K)=\max d(x_1,\ldots,x_K)$, over all choices of the $K$ points on the sphere.

Because the points have unit length, $\lVert x_i-x_j\rVert_2^2=2-2\langle x_i,x_j\rangle$. Maximizing the nearest-pair distance is therefore equivalent to making the largest pairwise inner product as small as possible. This form is convenient for numerical optimization: compute all pairwise inner products, focus on the largest one, and move the points to reduce it.

Two nearby questions originally motivated this post: point separation in a [hypercube](https://math.stackexchange.com/questions/1976250/what-is-the-maximum-distance-of-k-points-in-an-n-dimensional-hypercube) and maximum [average distance](https://mathoverflow.net/questions/279382/maximum-average-euclidean-distance-between-n-points-in-1-1n). They are related, but neither is the problem studied here: the domain here is the entire unit sphere, and the objective uses the closest pair rather than an average.

## Cases with exact answers

Before simulating anything, several regimes can be solved exactly using the classical bounds of [Rankin](https://doi.org/10.1017/S2040618500033219):

- When $N=2$, the sphere is a circle. A regular $K$-gon is optimal and gives $d^*(2,K)=2\sin(\pi/K)$.
- When $K\leq N+1$, the points can be the vertices of a regular simplex, giving $d^*(N,K)=\sqrt{2K/(K-1)}$.
- When $N+1<K\leq 2N$, points selected from the vertices $\{\pm e_1,\ldots,\pm e_N\}$ of a cross-polytope achieve the optimum $d^*(N,K)=\sqrt{2}$.

These formulas also explain some of the plateaus in the results below. For example, once $N\geq K-1$, a regular simplex already realizes the best possible separation, so adding more dimensions cannot improve it. [Henry Cohn's spherical-code overview](https://cohn.mit.edu/spherical-codes/) provides further background and tables for harder parameter choices.

## What must be approximated

The remaining cases in this experiment have $K>2N$. The accompanying program initializes several random configurations, then uses projected-gradient optimization: after every update, it normalizes each vector back onto the unit sphere. The loss is a smooth approximation to the largest pairwise inner product, and that approximation is sharpened gradually during the run.

Eight restarts reduce dependence on a single initialization. The best configuration found is a **constructive lower bound** on $d^*(N,K)$, not a proof of the optimum. Stars in the heatmap and triangles in the line chart identify these heuristic cases; unstarred cells and circles are exact.

<figure>
  <a href="{{ '/assets/files/spherical-code-results.png' | relative_url }}">
    <img src="{{ '/assets/files/spherical-code-results.png' | relative_url }}" alt="Heatmap and line chart of maximin separation for different dimensions and numbers of points, with heuristic cases marked by stars or triangles.">
  </a>
  <figcaption>Exact Rankin values are used where available. For $K>2N$, the plotted value is the best separation found across eight optimization restarts.</figcaption>
</figure>

Two monotonic facts explain the main patterns in the figure:

1. **For fixed $K$, separation cannot decrease as $N$ grows.** Any configuration in $\mathbb{R}^N$ can be embedded unchanged in $\mathbb{R}^{N+1}$ by appending a zero coordinate.
2. **For fixed $N$, separation cannot increase as $K$ grows.** Removing points from a configuration cannot make its closest remaining pair closer, so fitting more points can only maintain or reduce the optimum.

The computation is consistent with both statements. The simplex and cross-polytope regimes create exact plateaus; outside them, the numerical values change smoothly. As one concrete comparison, $200$ points have separation about $1.041$ in $N=10$ in the best run, whereas $N=100$ reaches the exact cross-polytope value $\sqrt{2}\approx1.414$ because $K=2N$.

## Reproduce the experiment

Download the [Python script]({{ '/assets/files/approximate_spherical_codes.py' | relative_url }}) and the [resulting CSV file]({{ '/assets/files/spherical-code-results.csv' | relative_url }}). Running the script with no arguments reproduces the grid and figure; `python approximate_spherical_codes.py --help` lists options for dimensions, point counts, restarts, optimization steps, seed, and compute device.

The published run used Python 3.11.6, NumPy 2.4.3, PyTorch 2.11.0, Matplotlib 3.10.8, eight restarts, $1{,}200$ steps, and seed `20260821` on a CUDA device. Across the heuristic cells, the largest gap between the best and worst restart was about $0.0181$. This small spread is a useful stability check, but it is not an optimality certificate.

## A correction to the original experiment

The [original 2019 notebook](https://colab.research.google.com/drive/12oBtJPT_FGbEe2iByhTBkHR2Js5CWB2P) sampled coordinates uniformly from $[0,1]$ and then normalized each vector. That procedure places every point in the positive orthant and does not sample the unit sphere uniformly. It also selected the best of random configurations rather than optimizing the point locations.

This revision fixes the domain, uses exact answers whenever the theory supplies them, and labels every remaining number as a heuristic lower bound. The broader qualitative lesson survives, but the revised formulation makes clear which claims are mathematical guarantees and which depend on computation.
