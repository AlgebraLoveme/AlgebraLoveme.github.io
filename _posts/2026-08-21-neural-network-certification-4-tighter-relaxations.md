---
title: "Why Do Simple Bounds Lose Information? Neural Network Certification, Part 4"
author_profile: true
permalink: /2026-08-21-neural-network-certification-4-tighter-relaxations/
date: 2026-08-21
written_by: PIRA
written_at: 2026-08-22
tags: [neural networks, certification, linear relaxation, abstract interpretation]
mathjax: true
toc: true
excerpt: "April's classifier shows how linear ReLU bounds preserve relationships that intervals forget."
---

## Why did April's margin cross zero?

In [Part 3]({{ '/2026-08-21-neural-network-certification-3-interval-bound-propagation/' | relative_url }}),
interval bound propagation followed April's entire input square through the
network. At radius $0.2$, each feature lies in

$$
x_1,x_2\in[0.3,0.7].
$$

The two hidden neurons received the bounds

$$
h_1\in[0.1,0.9],\qquad h_2\in[0,0.4].
$$

After last-layer elision, April's margin is

$$
m=0.2+h_1-h_2.
$$

Using the two hidden intervals independently gives

$$
m\geq0.2+0.1-0.4=-0.1.
$$

The bound crosses zero, so IBP returns **unknown**. Yet the two values that
produce $-0.1$ cannot occur together. The lower endpoint $h_1=0.1$ comes from
$x_1=x_2=0.3$, while the upper endpoint $h_2=0.4$ comes from
$x_1=0.7,\ x_2=0.3$.

The problem is not that either interval is wrong. The problem is that the
calculation has forgotten how both neurons depend on the same input.

## The missing information is a relationship

An interval remembers two numbers: a lower endpoint and an upper endpoint. For
the second hidden neuron, it remembers only

$$
0\leq h_2\leq0.4.
$$

But this neuron is not free to take any value in that interval. It is connected
to the input through

$$
z_2=x_1-x_2,\qquad h_2=\operatorname{ReLU}(z_2).
$$

Instead of replacing that connection with two constants, we can enclose it
with **linear bounds**: lines that remain functions of $z_2$, and therefore of
$x_1$ and $x_2$.

## Enclose an unstable ReLU with lines

For April's radius-$0.2$ square,

$$
z_2=x_1-x_2\in[-0.4,0.4].
$$

This interval crosses zero, so the ReLU is unstable. Its graph bends at zero:

$$
h_2=\max(0,z_2).
$$

Three lines enclose every point on that graph over $[-0.4,0.4]$:

$$
h_2\geq0,\qquad
h_2\geq z_2,\qquad
h_2\leq \frac{1}{2}z_2+0.2.
$$

<figure style="text-align: center;">
  <img src="{{ '/imgs/relu-linear-relaxation.svg' | relative_url }}" width="640" style="display: block; margin: 0 auto;" alt="The ReLU graph between minus 0.4 and 0.4 enclosed by two lower lines and an upper line, forming a shaded triangular region.">
  <figcaption>Together, the blue upper line and the black ReLU branches form the shaded enclosure.</figcaption>
</figure>

The upper line joins the ReLU endpoints $(-0.4,0)$ and $(0.4,0.4)$. ReLU is
convex, so the straight segment between those endpoints stays above its graph.
The two lower inequalities describe the two branches of ReLU itself. More
generally, if $z\in[\ell,u]$ with $\ell<0<u$, the upper line is

$$
\operatorname{ReLU}(z)\leq\frac{u}{u-\ell}(z-\ell).
$$

Replacing the exact equality with this larger, line-bounded region is called a
**linear relaxation**. The shaded triangle includes the exact graph, so using
it cannot exclude a possible network behavior. It also keeps a useful fact that
the interval $h_2\in[0,0.4]$ discarded: the allowed upper value of $h_2$
changes with $z_2$.

## Carry the lines to April's output margin

The first hidden neuron is easier. Its pre-activation stays positive:

$$
z_1=x_1+x_2-0.5\in[0.1,0.9].
$$

ReLU therefore acts as the identity, giving the exact relationship

$$
h_1=x_1+x_2-0.5.
$$

To prove a lower bound on $m=0.2+h_1-h_2$, we need an upper bound on the term
being subtracted. Substitute the ReLU upper line and then replace
$z_2$ with $x_1-x_2$:

$$
\begin{aligned}
m
&=0.2+h_1-h_2\\
&\geq0.2+(x_1+x_2-0.5)
       -\left(\frac{1}{2}(x_1-x_2)+0.2\right)\\
&=\frac{1}{2}x_1+\frac{3}{2}x_2-0.5.
\end{aligned}
$$

Both input coefficients are positive, so the smallest value over
$x_1,x_2\in[0.3,0.7]$ uses $x_1=x_2=0.3$:

$$
m\geq
\frac{1}{2}(0.3)+\frac{3}{2}(0.3)-0.5
=0.1.
$$

The lower bound is positive. We have now proved that April remains classified
as a cat throughout the radius-$0.2$ square.

| Method | What it remembers | Margin lower bound | Result |
| --- | --- | ---: | --- |
| Interval propagation | Separate ranges for $h_1$ and $h_2$ | $-0.1$ | Unknown |
| Linear ReLU relaxation | How $h_1$ and $h_2$ depend on the input | $0.1$ | Verified |

The network and the allowed inputs have not changed. The certificate succeeds
because the summary of their possible values is more informative.

## One geometric viewpoint

The allowed inputs form a square. After each network layer, their possible
neuron values form another geometric set. Tracking that exact set can be hard,
so a verifier carries a simpler set that contains it.

IBP uses axis-aligned boxes. The linear relaxation adds slanted boundaries such
as $h_2\leq\frac{1}{2}z_2+0.2$. These boundaries preserve some relationships
between neurons while keeping the calculations manageable.

This is the central idea of **abstract interpretation** in this setting:
compute with a tractable enclosure of all possible values, while ensuring that
the enclosure never drops a real possibility. Linear ReLU enclosures also form
the basis of the convex relaxation in
[Provable Defenses against Adversarial Examples via the Convex Outer Adversarial Polytope](https://arxiv.org/abs/1711.00851).

## What should we do if the bound is inconclusive?

Increase the radius once more, from $0.2$ to $0.24$. Now

$$
x_1,x_2\in[0.26,0.74],\qquad
z_2\in[-0.48,0.48].
$$

The new upper line for the unstable ReLU joins $(-0.48,0)$ and
$(0.48,0.48)$:

$$
h_2\leq\frac{1}{2}z_2+0.24.
$$

The first ReLU remains active because
$z_1=x_1+x_2-0.5\in[0.02,0.98]$. Repeating the margin calculation gives

$$
\begin{aligned}
m
&\geq0.2+(x_1+x_2-0.5)
       -\left(\frac{1}{2}(x_1-x_2)+0.24\right)\\
&=\frac{1}{2}x_1+\frac{3}{2}x_2-0.54\\
&\geq\frac{1}{2}(0.26)+\frac{3}{2}(0.26)-0.54\\
&=-0.02.
\end{aligned}
$$

The linear relaxation is now inconclusive. It has neither proved the property
nor found an input that violates it.

We do not have to abandon the calculation. We can divide the input square into
smaller regions and analyze each one separately. A ReLU bound fitted to a
smaller region can follow its graph more closely.

## Takeaway

Intervals forgot that April's hidden neurons were tied to the same input.
Linear ReLU bounds retained enough of that relationship to improve the margin
lower bound from $-0.1$ to $0.1$ and certify the radius-$0.2$ square.

At radius $0.24$, the new lower bound is $-0.02$. Part 5 asks: **can splitting
the input region turn this unknown into a proof?**
