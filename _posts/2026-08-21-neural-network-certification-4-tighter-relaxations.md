---
title: "Why Do Simple Bounds Lose Information? Neural Network Certification, Part 4"
author_profile: true
permalink: /2026-08-21-neural-network-certification-4-tighter-relaxations/
date: 2026-08-21
written_by: PIRA
written_at: 2026-08-22
tags: [neural networks, certification, linear relaxation, DeepPoly, abstract interpretation]
mathjax: true
toc: true
excerpt: "Triangle first recovers a relationship that intervals forgot; DeepPoly then carries useful linear bounds without a global constraint system."
---

## Why did April's margin cross zero?

In [Part 3]({{ '/2026-08-21-neural-network-certification-3-interval-bound-propagation/' | relative_url }}),
interval bound propagation followed April's entire input square through the
network. At radius $0.2$,

$$
x_1,x_2\in[0.3,0.7].
$$

IBP found

$$
h_1\in[0.1,0.9],\quad h_2\in[0,0.4].
$$

After last-layer elision, the margin is $m=0.2+h_1-h_2$. Treating the two
hidden intervals independently gives

$$
m\geq0.2+0.1-0.4=-0.1.
$$

The bound crosses zero, so IBP returns **unknown**. But the calculation combines
two hidden values that cannot occur together. The value $h_1=0.1$ comes from
$x_1=x_2=0.3$, whereas $h_2=0.4$ comes from $x_1=0.7$ and $x_2=0.3$.

Neither interval is wrong. The missing information is the relationship between
each hidden neuron and April's input.

## Keep the relationship, not just the endpoints

For the second hidden neuron, IBP remembers only

$$
0\leq h_2\leq0.4.
$$

The network tells us more:

$$
z_2=x_1-x_2,\quad h_2=\operatorname{ReLU}(z_2).
$$

The value of $h_2$ therefore changes with $x_1-x_2$; it is not free to move
independently inside $[0,0.4]$. We need a sound description that keeps some of
this relationship.

## First repair: enclose ReLU with Triangle

Over April's radius-$0.2$ square,

$$
z_2=x_1-x_2\in[-0.4,0.4].
$$

This interval crosses zero, so the ReLU is unstable. Three lines enclose its
graph over the interval:

$$
\begin{aligned}
h_2&\geq0, & h_2&\geq z_2,\\
h_2&\leq\frac{1}{2}z_2+0.2.
\end{aligned}
$$

<figure style="text-align: center;">
  <img src="{{ '/imgs/relu-linear-relaxation.svg' | relative_url }}" width="640" style="display: block; margin: 0 auto;" alt="The ReLU graph between minus 0.4 and 0.4 enclosed by two lower lines and an upper line, forming a shaded triangular region.">
  <figcaption>Together, the blue upper line and the black ReLU branches form the shaded enclosure.</figcaption>
</figure>

The upper line joins the ReLU endpoints $(-0.4,0)$ and $(0.4,0.4)$. Because
ReLU is convex, the segment between those endpoints stays above its graph. For
any unstable ReLU with $z\in[\ell,u]$ and $\ell<0<u$, the same chord is

$$
\operatorname{ReLU}(z)\leq\frac{u}{u-\ell}(z-\ell).
$$

The two lower lines and the upper chord form the **Triangle relaxation**: the
convex hull of the ReLU graph over its known interval. Every exact ReLU value
lies inside the triangle, so the enclosure is sound. This relaxation appears
in
[Formal Verification of Piece-Wise Linear Feed-Forward Neural Networks](https://arxiv.org/abs/1705.01320).

## Let Triangle certify April's larger square

April's first ReLU stays active because

$$
z_1=x_1+x_2-0.5\in[0.1,0.9].
$$

It therefore keeps the exact relationship

$$
h_1=x_1+x_2-0.5.
$$

To find the smallest margin, the Triangle calculation keeps the input box, the
network equations, and all three constraints on $h_2$. Since
$m=0.2+h_1-h_2$ subtracts $h_2$, the smallest margin uses the upper face of
the triangle:

$$
h_2\leq\frac{1}{2}z_2+0.2
      =\frac{1}{2}(x_1-x_2)+0.2.
$$

Substitute both hidden-neuron relationships into the margin:

$$
\begin{aligned}
m
&\geq0.2+(x_1+x_2-0.5)
       -\left(\frac{1}{2}(x_1-x_2)+0.2\right)\\
&=\frac{1}{2}x_1+\frac{3}{2}x_2-0.5.
\end{aligned}
$$

Both coefficients are positive, so the minimum over
$x_1,x_2\in[0.3,0.7]$ occurs at $x_1=x_2=0.3$:

$$
m\geq\frac{1}{2}(0.3)+\frac{3}{2}(0.3)-0.5=0.1.
$$

The lower bound is positive. Triangle has turned IBP's unknown into a
certificate for the radius-$0.2$ square.

## Why does Triangle become expensive?

For April, one triangle is easy to carry. A modern network may contain
thousands of unstable ReLUs. With $k$ unstable ReLUs, Triangle adds $3k$
inequalities, plus the variables and affine equations for the network. A
verifier can retain this whole system and minimize the margin with a linear
program. The initial constraint count grows linearly, but the programs become
large.

Another option is to eliminate hidden variables and describe the resulting
polytope directly in terms of earlier variables. This is where the number of
constraints can multiply.

### How eliminating one variable multiplies constraints

Consider four inequalities involving the same hidden value:

$$
\begin{aligned}
h&\geq x, & h&\geq0,\\
h&\leq y, & h&\leq1-y.
\end{aligned}
$$

To remove $h$, every lower bound must be no larger than every upper bound.
Pairing the two lower bounds with the two upper bounds gives

$$
\begin{aligned}
x&\leq y, & x&\leq1-y,\\
0&\leq y, & 0&\leq1-y.
\end{aligned}
$$

In general, eliminating a variable with $p$ lower bounds and $q$ upper bounds
can generate $pq$ constraints:

| Lower $p$ | Upper $q$ | Before: $p+q$ | After: up to $pq$ |
| ---: | ---: | ---: | ---: |
| $2$ | $2$ | $4$ | $4$ |
| $4$ | $4$ | $8$ | $16$ |
| $16$ | $16$ | $32$ | $256$ |
| $100$ | $100$ | $200$ | $10{,}000$ |

In a worst case where all generated constraints remain relevant, one projection
can turn four lower and four upper bounds into $16$ constraints. If the next
hidden variable appears in $16$ lower and $16$ upper bounds, the next
projection can generate $256$. Repeated multiplication creates the explosion.

This pairwise operation is called **Fourier–Motzkin elimination**. Retaining
all hidden variables avoids the projection explosion but leaves a large global
linear program. Explicitly eliminating them risks creating a polytope with many
facets. We now have a reason to keep only selected linear relationships.

## Keep selected lines with DeepPoly

**DeepPoly** records a concrete interval, one affine lower expression, and one
affine upper expression for each neuron. For April's unstable ReLU, its
symbolic bounds can be written as

$$
\lambda z_2\leq h_2
\leq\frac{1}{2}z_2+0.2,
\quad \lambda\in\{0,1\}.
$$

Choosing $\lambda=0$ keeps $h_2\geq0$; choosing $\lambda=1$ keeps
$h_2\geq z_2$. DeepPoly keeps one of these lower lines and the upper chord
rather than sending all three Triangle constraints to a global linear program.

To bound a later neuron, DeepPoly substitutes the selected affine expressions
backward until only input variables remain. This is **back-substitution**. For
April's margin, the coefficient of $h_2$ is negative, so only its upper bound is
needed:

$$
\begin{aligned}
h_1&=x_1+x_2-0.5,\\
h_2&\leq\frac{1}{2}(x_1-x_2)+0.2.
\end{aligned}
$$

Back-substitution immediately recovers

$$
m\geq\frac{1}{2}x_1+\frac{3}{2}x_2-0.5\geq0.1.
$$

Triangle and DeepPoly give the same certificate for April's tiny network. The
difference is how they organize the calculation: Triangle retains a joint
constraint system, while DeepPoly propagates selected affine bounds. DeepPoly
was introduced in
[An Abstract Domain for Certifying Neural Networks](https://www.sri.inf.ethz.ch/publications/singh2019domain).

| Method | Representation | Margin lower bound | Result |
| --- | --- | ---: | --- |
| IBP | Independent intervals | $-0.1$ | Unknown |
| Triangle | Joint linear constraints | $0.1$ | Verified |
| DeepPoly | Selected affine bounds and back-substitution | $0.1$ | Verified |

## Three abstractions, one safety rule

The allowed inputs form a square. As they pass through a network, the possible
neuron values form new geometric sets. A verifier works with simpler sets that
contain every exact value.

IBP uses boxes. Triangle uses a polytope cut out by linear constraints.
DeepPoly uses intervals together with selected affine bounds. These are
different forms of **abstract interpretation**, but they obey the same safety
rule: never discard a value that the network can actually produce.

## What should we do if the bound is inconclusive?

Increase the radius from $0.2$ to $0.24$. Now

$$
x_1,x_2\in[0.26,0.74],\quad z_2\in[-0.48,0.48].
$$

The DeepPoly upper line becomes

$$
h_2\leq\frac{1}{2}z_2+0.24.
$$

The first ReLU remains active because
$z_1=x_1+x_2-0.5\in[0.02,0.98]$. Back-substitution gives

$$
\begin{aligned}
m
&\geq\frac{1}{2}x_1+\frac{3}{2}x_2-0.54\\
&\geq\frac{1}{2}(0.26)+\frac{3}{2}(0.26)-0.54\\
&=-0.02.
\end{aligned}
$$

The DeepPoly bound is inconclusive. It has neither proved the property nor
found an input that violates it.

We can now divide the input square into smaller regions and analyze each one
separately. A ReLU bound fitted to a smaller region can follow its graph more
closely.

## Takeaway

IBP lost the relationship between April's hidden neurons and returned unknown
at radius $0.2$. Triangle restored that relationship and proved
$m\geq0.1$. After seeing why a full Triangle system becomes expensive,
DeepPoly retained selected affine bounds and recovered the same certificate by
back-substitution.

At radius $0.24$, the new lower bound is $-0.02$. Part 5 asks: **can splitting
the input region turn this unknown into a proof?**
