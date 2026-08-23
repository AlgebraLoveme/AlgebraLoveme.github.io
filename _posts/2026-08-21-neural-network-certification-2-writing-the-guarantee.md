---
title: "What Would Count as a Proof? Neural Network Certification, Part 2"
series_nav_title: "What Would Count as a Proof?"
author_profile: true
permalink: /2026-08-21-neural-network-certification-2-writing-the-guarantee/
date: 2026-08-21
show_initial_release: false
written_by: PIRA
written_at: 2026-08-21
tags: [neural networks, certification, specifications, robustness, "Certification Series: 02"]
mathjax: true
toc: true
excerpt: "April meets a tiny ReLU classifier as we turn an informal promise into a mathematical statement and prove it by hand."
---

## Can we prove that April remains a cat?

In [Part 1]({{ '/2026-08-21-neural-network-certification-1-what-are-we-proving/' | relative_url }}),
an attack could disprove robustness by finding one allowed input that changes a
prediction. When no attack succeeded, however, unexamined inputs remained. A
proof must cover them too.

Let us try to build such a proof for April.

<figure style="text-align: center;">
  <a href="{{ '/imgs/April_the_cat.jpg' | relative_url }}">
    <img src="{{ '/imgs/April_the_cat.jpg' | relative_url }}" width="320" style="display: block; margin: 0 auto;" alt="April, a cream-colored Siberian cat with gray ears, sitting beside a tree in sunlight.">
  </a>
  <figcaption>We will represent the photograph with two feature values so that every step of the proof fits on the page.</figcaption>
</figure>

A practical image classifier may receive hundreds of thousands of color-channel
values. Our teaching model receives only two normalized features:

- $x_1$ measures the response to April's pointed ears.
- $x_2$ measures the response to April's fluffy coat.

For the original photo, both feature values are $0.5$, so

$$
x_0=(0.5,0.5).
$$

The classifier has two hidden neurons. Each uses the rectified linear unit

$$
\operatorname{ReLU}(z)=\max(0,z).
$$

The complete network is

$$
\begin{aligned}
z_1 &= x_1+x_2-0.5,
& h_1 &= \operatorname{ReLU}(z_1),\\
z_2 &= x_1-x_2,
& h_2 &= \operatorname{ReLU}(z_2),\\
f_{\mathrm{cat}}(x) &= 0.2+h_1+h_2,
& f_{\mathrm{other}}(x) &= 2h_2.
\end{aligned}
$$

The larger output score determines the predicted class. At $x_0$, the hidden
values are $h_1=0.5$ and $h_2=0$. The two output scores are therefore
$f_{\mathrm{cat}}(x_0)=0.7$ and $f_{\mathrm{other}}(x_0)=0$. The model predicts
cat on April's original feature vector.

## Measure the decision with one margin

The predicted class depends only on which output score is larger. Subtracting
the scores reduces that comparison to the sign of one number. Define the
**margin**

$$
m(x)=f_{\mathrm{cat}}(x)-f_{\mathrm{other}}(x)
    =(0.2+h_1+h_2)-2h_2
    =0.2+h_1-h_2.
$$

If $m(x)>0$, the cat score is strictly larger and the model predicts cat. If
$m(x)<0$, the other score is larger. We require strict positivity, so a tie at
$m(x)=0$ also violates the property we want to certify.

For the original input, $m(x_0)=0.7$. That calculation checks one point. Our
robustness claim concerns all nearby points.

## State the claim for every allowed input

Allow either feature to change by at most $0.1$. Using the $\ell_\infty$ set from
Part 1 gives

$$
\begin{aligned}
S_\infty(x_0,0.1)
&=\left\{x\in[0,1]^2:\lVert x-x_0\rVert_\infty\leq0.1\right\}\\
&=[0.4,0.6]\times[0.4,0.6].
\end{aligned}
$$

The allowed set is a square. It contains every pair formed by choosing
$x_1\in[0.4,0.6]$ and $x_2\in[0.4,0.6]$, not only its four corners.

The statement we want to prove is

$$
\boxed{\text{for every }x\in S_\infty(x_0,0.1),\qquad m(x)>0.}
$$

The words **for every** are what separate this claim from an attack. An attack
checks selected points in the square. A certificate must cover the entire
square.

## Build our first certificate by hand

We do not need to evaluate every point. We need inequalities that hold
everywhere in the square.

### 1. Bound the first hidden neuron

Every allowed input satisfies $x_1\geq0.4$ and $x_2\geq0.4$. Therefore,

$$
z_1=x_1+x_2-0.5\geq0.4+0.4-0.5=0.3.
$$

The input to the first ReLU is always positive. ReLU leaves positive values
unchanged, so

$$
h_1\geq0.3.
$$

### 2. Bound the second hidden neuron

The largest possible value of $x_1-x_2$ occurs when $x_1$ is largest and $x_2$
is smallest:

$$
z_2=x_1-x_2\leq0.6-0.4=0.2.
$$

ReLU is monotone, so

$$
h_2=\operatorname{ReLU}(z_2)
\leq\operatorname{ReLU}(0.2)
=0.2.
$$

### 3. Bound the margin

To obtain a guaranteed lower bound, replace the positive term $h_1$ by its lower
bound and the subtracted term $h_2$ by its upper bound:

$$
\begin{aligned}
m(x)
&=0.2+h_1-h_2\\
&\geq0.2+0.3-0.2\\
&=0.3>0.
\end{aligned}
$$

Every inequality used only conditions that hold throughout
$S_\infty(x_0,0.1)$. We have therefore proved

$$
\boxed{m(x)\geq0.3\quad\text{for every }x\in S_\infty(x_0,0.1).}
$$

The exact smallest margin is not needed. A guaranteed positive lower bound is
enough to prove that every allowed input is classified as cat. The derivation
above is our first certificate.

## Name the pieces of the proof

During inference, a fixed neural network is a numerical program. It takes an
input, follows a fixed sequence of operations, and returns an output. Program
verification gives names to the pieces of the claim we just proved:

- The **precondition** $P(x)$ specifies the allowed inputs. Here,
  $P(x)$ means $x\in S_\infty(x_0,0.1)$.
- The **program** is the fixed collection of affine operations and ReLUs above.
- The **postcondition** $Q(f(x))$ specifies the required output. Here, $Q(f(x))$
  means $m(x)>0$.

With this notation, the verification problem is

$$
\text{for every }x,\qquad P(x)\Longrightarrow Q(f(x)).
$$

A **counterexample** satisfies the precondition but violates the postcondition.
For April's classifier, it would be a point inside the square with $m(x)\leq0$.
A **certificate** establishes that no such point exists. Our lower bound
$m(x)\geq0.3$ is such a certificate.

Larger networks require automation. **Bound-based verifiers** enclose all
possible neuron values and use those bounds to prove an output property. For
example, [Fast-Lin and Fast-Lip](https://arxiv.org/abs/1804.09699) compute
certified robustness bounds for ReLU networks. **Solver-based verifiers** search
for a violation of the postcondition while respecting every network equation.
[Reluplex](https://arxiv.org/abs/1702.01135), for example, can prove supported
properties or return counterexamples for ReLU networks.

## What can a verifier report?

A verification run can end in three ways:

- **Verified:** it produces a valid certificate. For our example,
  $m(x)\geq0.3$ verifies the claim.
- **Falsified:** it produces a concrete allowed input with $m(x)\leq0$. Anyone can
  evaluate the network on that input and check the failure.
- **Unknown:** it produces neither. The robustness claim is still either true or
  false, but this run has not determined which.

A verifier is **sound** if it never labels a false property as verified. A sound
method may still return unknown when its bounds are inconclusive.

A method is **complete** if it is guaranteed to return verified or falsified for
every supported instance when allowed to run to completion. Part 5 will connect
this promise to search and timeouts.

## April's specification, in one box

The next three posts will use exactly the same classifier. Here is the complete
specification in one place:

| Piece | April classifier |
| --- | --- |
| Input | $x=(x_1,x_2)$ |
| Reference input | $x_0=(0.5,0.5)$ |
| Allowed set | $S_\infty(x_0,0.1)=[0.4,0.6]^2$ |
| Hidden neurons | $h_1=\operatorname{ReLU}(x_1+x_2-0.5)$ and $h_2=\operatorname{ReLU}(x_1-x_2)$ |
| Scores | $f_{\mathrm{cat}}=0.2+h_1+h_2$ and $f_{\mathrm{other}}=2h_2$ |
| Margin | $m=f_{\mathrm{cat}}-f_{\mathrm{other}}$ |
| Property | $m(x)>0$ for every $x\in S_\infty(x_0,0.1)$ |
| Certificate | $m(x)\geq0.3$ throughout the allowed set |

## Takeaway

Simple bounds on $x_1$ and $x_2$ covered infinitely many points in our square. By
carrying those bounds through two ReLUs, we proved that April's margin never
falls below $0.3$.

Doing this neuron by neuron would be tedious in a larger network. Part 3 asks the
next question: **how can bounds travel through an entire network automatically?**
