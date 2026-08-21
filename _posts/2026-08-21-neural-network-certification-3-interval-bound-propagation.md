---
title: "How Can Bounds Travel Through a Network? Neural Network Certification, Part 3"
author_profile: true
permalink: /2026-08-21-neural-network-certification-3-interval-bound-propagation/
date: 2026-08-21
written_by: PIRA
written_at: 2026-08-21
tags: [neural networks, certification, interval bound propagation, robustness]
mathjax: true
toc: true
excerpt: "Follow ranges through April's tiny classifier and turn a lower bound on its output margin into a certificate."
---

## How can we follow every allowed input at once?

In [Part 2]({{ '/2026-08-21-neural-network-certification-2-writing-the-guarantee/' | relative_url }}),
we proved that April's output margin remains positive when either input feature
changes by at most $0.1$. The proof bounded two hidden neurons by hand. A larger
network needs the same reasoning applied systematically across every layer.

<figure style="text-align: center;">
  <a href="{{ '/imgs/April_the_cat.jpg' | relative_url }}">
    <img src="{{ '/imgs/April_the_cat.jpg' | relative_url }}" width="280" style="display: block; margin: 0 auto;" alt="April, a cream-colored Siberian cat with gray ears, sitting beside a tree in sunlight.">
  </a>
  <figcaption>Instead of following one feature pair for April, we will follow a range of possible values through every neuron.</figcaption>
</figure>

Attach a lower and upper bound to each input, then calculate new bounds after
every network operation. One pass through the network can then cover the entire
allowed set.

## Give each input a lower and upper bound

An **interval** $[\underline v,\overline v]$ represents every value $v$ satisfying

$$
\underline v\leq v\leq\overline v.
$$

For April's reference input $x_0=(0.5,0.5)$ and radius $0.1$, the
$\ell_\infty$ input set is

$$
x_1\in[0.4,0.6],\qquad x_2\in[0.4,0.6].
$$

These two intervals describe the same square used in Part 2. We now propagate
them through the fixed classifier

$$
\begin{aligned}
z_1 &= x_1+x_2-0.5,
& h_1 &= \operatorname{ReLU}(z_1),\\
z_2 &= x_1-x_2,
& h_2 &= \operatorname{ReLU}(z_2),\\
f_{\mathrm{cat}} &= 0.2+h_1+h_2,
& f_{\mathrm{other}} &= 2h_2.
\end{aligned}
$$

## Carry the bounds through an affine layer

Start with $z_1=x_1+x_2-0.5$. Its smallest value uses both lower input bounds,
and its largest value uses both upper bounds:

$$
z_1\in
[0.4+0.4-0.5,\;0.6+0.6-0.5]
=[0.3,0.7].
$$

The subtraction in $z_2=x_1-x_2$ reverses which endpoint of $x_2$ we use. To
make $z_2$ small, choose a small $x_1$ and a large $x_2$. To make it large,
choose a large $x_1$ and a small $x_2$:

$$
z_2\in
[0.4-0.6,\;0.6-0.4]
=[-0.2,0.2].
$$

The same endpoint rule handles any affine neuron. To compute the lower output
bound, use the lower input endpoint for a positive weight and the upper input
endpoint for a negative weight. Reverse those choices for the upper output
bound, then add the bias.

## Carry the bounds through ReLU

ReLU is monotone, so applying it to an interval gives

$$
v\in[\underline v,\overline v]
\quad\Longrightarrow\quad
\operatorname{ReLU}(v)
\in[\max(0,\underline v),\max(0,\overline v)].
$$

The interval's position relative to zero determines one of three cases:

- If $\overline v\leq0$, the neuron is always inactive and its output is $[0,0]$.
- If $\underline v\geq0$, the neuron is always active and keeps the interval
  $[\underline v,\overline v]$.
- If $\underline v<0<\overline v$, the ReLU is **unstable**: it may be active or
  inactive, and its output interval is $[0,\overline v]$.

For April's first neuron, $z_1\in[0.3,0.7]$ is always positive. Therefore,

$$
h_1\in[0.3,0.7].
$$

The second interval $z_2\in[-0.2,0.2]$ crosses zero, so this ReLU is unstable:

$$
h_2\in[0,0.2].
$$

## Bound the margin directly with last-layer elision

We could continue one score at a time. Using $h_1\in[0.3,0.7]$ and
$h_2\in[0,0.2]$ gives

$$
f_{\mathrm{cat}}=0.2+h_1+h_2\in[0.5,1.1],
\qquad
f_{\mathrm{other}}=2h_2\in[0,0.4].
$$

Subtracting these two intervals would produce

$$
m\in[0.5-0.4,\;1.1-0]=[0.1,1.1].
$$

That interval is sound, but it has already forgotten that both scores use the
same $h_2$. Its lower endpoint combines the smallest cat score, which uses
$h_2=0$, with the largest other score, which uses $h_2=0.2$. One hidden value
cannot be both numbers at once.

The property asks about the score difference, not the two scores separately.
We can therefore subtract the final-layer formulas first:

$$
\begin{aligned}
m
&=f_{\mathrm{cat}}-f_{\mathrm{other}}\\
&=(0.2+h_1+h_2)-2h_2\\
&=0.2+h_1-h_2.
\end{aligned}
$$

Now propagate the hidden intervals directly into this margin:

$$
m\in[0.2+0.3-0.2,\;0.2+0.7-0]=[0.3,0.9].
$$

This algebraic merge of the final linear layer with the desired score
difference is called **last-layer elision**. We have not removed the layer; we
have rewritten it together with the property before computing bounds. Here it
raises the margin's lower bound from $0.1$ to $0.3$.

Every possible margin is therefore at least $0.3$. The model predicts cat for
every input in $S_\infty(x_0,0.1)$, giving the same certificate we derived by
hand in Part 2.

Applying these interval calculations layer by layer is called **interval bound
propagation**, or **IBP**. Each operation encloses every value that operation can
produce from the preceding intervals. By induction over the layers, the final
interval encloses every possible margin. This containment is why a positive
lower margin bound is a sound certificate.

Last-layer elision and the use of IBP bounds in training are studied in
[On the Effectiveness of Interval Bound Propagation for Training Verifiably Robust Models](https://arxiv.org/abs/1810.12715).
We will revisit that use in Part 6.

## Increase the radius: the bound becomes inconclusive

Now allow each feature to change by $0.2$ instead of $0.1$:

$$
x_1,x_2\in[0.3,0.7].
$$

The propagation rules do not change. Applying them to the larger square gives

| Quantity | Interval at radius $0.2$ |
| --- | --- |
| $z_1=x_1+x_2-0.5$ | $[0.1,0.9]$ |
| $h_1=\operatorname{ReLU}(z_1)$ | $[0.1,0.9]$ |
| $z_2=x_1-x_2$ | $[-0.4,0.4]$ |
| $h_2=\operatorname{ReLU}(z_2)$ | $[0,0.4]$ |
| $f_{\mathrm{cat}}$ | $[0.3,1.5]$ |
| $f_{\mathrm{other}}$ | $[0,0.8]$ |
| Margin from separate score intervals | $[-0.5,1.5]$ |
| Margin after last-layer elision | $[-0.1,1.1]$ |

Last-layer elision improves the lower bound from $-0.5$ to $-0.1$, but even the
tighter margin interval crosses zero. This result does **not** provide an input
with a negative margin, so it does not falsify the property. It also cannot
prove that every margin is positive. This IBP run must report **unknown**.

We can locate where information disappeared. The lower endpoint $h_1=0.1$ is
attained at $x_1=x_2=0.3$. The upper endpoint $h_2=0.4$ is attained at $x_1=0.7$
and $x_2=0.3$. No single input produces both extremes. When the margin
calculation combines them, it treats the two hidden values as if they could vary
independently.

## The propagation rule in one pass

IBP follows the same four steps for a network of any depth:

1. Put a lower and upper bound on every input coordinate.
2. For each affine layer, choose endpoints according to the signs of its weights.
3. For each ReLU, replace $[\underline v,\overline v]$ with
   $[\max(0,\underline v),\max(0,\overline v)]$.
4. Combine the final linear layer with the required score difference, then
   bound that margin directly. This is last-layer elision.

If the resulting margin lower bound is positive, the property is verified. A
nonpositive lower bound cannot certify the property. Falsification still
requires a concrete allowed input that violates it.

## Takeaway

At radius $0.1$, interval propagation and last-layer elision carry April's
entire input square through the network and prove $m\geq0.3$. At radius $0.2$,
the same method combines hidden-neuron extremes that come from different inputs
and returns unknown.

Part 4 asks: **why do simple bounds lose this information?** We will answer by
preserving linear relationships between neuron values.
