---
title: "What Should We Do If the Bound Is Inconclusive? Neural Network Certification, Part 5"
author_profile: true
permalink: /2026-08-21-neural-network-certification-5-complete-verification/
date: 2026-08-21
written_by: PIRA
written_at: 2026-08-22
tags: [neural networks, certification, branch and bound, complete verification]
mathjax: true
toc: true
excerpt: "Split April's input region, bound each piece, and assemble the local results into a complete certificate."
---

## One bound cannot settle April's square

[Part 4]({{ '/2026-08-21-neural-network-certification-4-tighter-relaxations/' | relative_url }})
left April the Siberian cat with an unresolved question. We allowed both input
coordinates to move within

$$
R=[0.26,0.74]\times[0.26,0.74],
$$

which is the $\ell_\infty$ ball of radius $0.24$ around $(0.5,0.5)$. April's
tiny classifier has margin

$$
m=0.2+h_1-h_2,
$$

where a positive margin means that the cat score remains larger than the other
score. DeepPoly bounded the whole square at once and obtained

$$
m\geq-0.02.
$$

This is **unknown**, not a failing input. DeepPoly computed the bound over a
relaxation: a simpler enclosure that contains every real network behavior and
some extra ones. Those extra behaviors can pull the bound below zero.

The next question is: **can we cover every allowed input with smaller regions
whose bounds are positive?**

## Cut the square where the bound is loose

Recall April's two hidden neurons:

$$
\begin{aligned}
h_1&=\operatorname{ReLU}(x_1+x_2-0.5),\\
h_2&=\operatorname{ReLU}(x_1-x_2).
\end{aligned}
$$

The first ReLU stays active throughout $R$, so
$h_1=x_1+x_2-0.5$. The loose step is the upper bound on $h_2$. Over the whole
square, its input $z_2=x_1-x_2$ ranges from $-0.48$ to $0.48$, giving

$$
h_2\leq\frac{1}{2}z_2+0.24.
$$

Because $z_2=x_1-x_2$, narrowing either input coordinate narrows the range
used to build this line. Split the $x_1$ interval at its midpoint, $0.5$:

$$
\begin{aligned}
R_L&=[0.26,0.5]\times[0.26,0.74],\\
R_R&=[0.5,0.74]\times[0.26,0.74].
\end{aligned}
$$

These two rectangles cover the original square. We have not removed a single
allowed input.

### Bound the left half

On $R_L$, the ReLU input has the narrower, asymmetric range

$$
z_2=x_1-x_2\in[-0.48,0.24].
$$

The upper chord fitted to these endpoints is

$$
h_2\leq\frac{1}{3}z_2+0.16.
$$

Substitute this line and the exact expression for $h_1$ into the margin:

$$
\begin{aligned}
m
&\geq0.2+(x_1+x_2-0.5)
       -\left(\frac{1}{3}(x_1-x_2)+0.16\right)\\
&=\frac{2}{3}x_1+\frac{4}{3}x_2-0.46.
\end{aligned}
$$

Both coefficients are positive. The smallest value therefore occurs at
$x_1=x_2=0.26$:

$$
m\geq\frac{2}{3}(0.26)+\frac{4}{3}(0.26)-0.46=0.06.
$$

Every input in $R_L$ is safe.

### Bound the right half

On $R_R$,

$$
z_2=x_1-x_2\in[-0.24,0.48],
$$

so the fitted upper chord becomes

$$
h_2\leq\frac{2}{3}z_2+0.16.
$$

Back-substitution now gives

$$
\begin{aligned}
m
&\geq0.2+(x_1+x_2-0.5)
       -\left(\frac{2}{3}(x_1-x_2)+0.16\right)\\
&=\frac{1}{3}x_1+\frac{5}{3}x_2-0.46.
\end{aligned}
$$

The minimum over $R_R$ occurs at $x_1=0.5$ and $x_2=0.26$:

$$
m\geq\frac{1}{3}(0.5)+\frac{5}{3}(0.26)-0.46=0.14.
$$

Every input in $R_R$ is also safe.

Splitting changed the ReLU ranges, allowing each upper chord to follow the
ReLU more closely. The intercept fell from $0.24$ on the whole square to
$0.16$ on each half. That improvement turned one inconclusive bound into two
positive bounds.

<figure style="text-align: center;">
  <img src="{{ '/imgs/april-branch-and-bound.svg' | relative_url }}" width="760" style="display: block; margin: 0 auto;" alt="April's square split vertically into left and right rectangles, alongside a search tree whose root has an inconclusive margin bound and whose two children have positive bounds.">
  <figcaption>The two verified leaves cover the entire original square, so together they form one certificate.</figcaption>
</figure>

## Read the proof from the tree

The top box in the figure represents the original region $R$. Its lower bound
is $-0.02$, so it cannot yet be marked safe. We divide it into two child
regions and bound each child separately.

Both child bounds are positive:

$$
\min_{x\in R_L}m(x)\geq0.06,
\qquad
\min_{x\in R_R}m(x)\geq0.14.
$$

Because $R=R_L\cup R_R$, every allowed input belongs to at least one verified
leaf. The tree is therefore a proof for the entire radius-$0.24$ square. The
smallest leaf bound, $0.06$, is a valid lower bound for the original region.

## Bound, split, and repeat

April needed only one cut. A harder network may leave one or both children
inconclusive. We can apply the same cycle again:

1. **Bound** the margin over the current region.
2. If the lower bound is positive, mark the whole region verified.
3. If the bound is inconclusive, **split** the region into children.
4. Repeat until every leaf is verified or a failing input is found.

This procedure is **branch and bound**. Branching creates smaller cases;
bounding tries to settle each case without examining every point inside it.
A verifier may branch on an input coordinate, as we did, or on whether an
unstable ReLU is active or inactive.

The important object is not a long list of sampled inputs. It is a collection
of regions that covers the allowed set, together with a sound bound for every
region declared safe. A unified account of neural-network branch and bound
appears in
[A Unified View of Piecewise Linear Neural Network Verification](https://arxiv.org/abs/1711.00455).

## Search for a failing input at the same time

While bounds reason about whole regions, an attack searches for promising
individual inputs and evaluates them with the exact network. The two jobs
complement each other:

- a positive lower bound proves that an entire region is safe;
- one concrete input with $m(x)\leq0$ disproves the claim immediately.

No such input exists in April's radius-$0.24$ square, as the completed tree
proves. If we enlarge the radius to $0.36$, however, the allowed set contains

$$
x=(0.86,0.14).
$$

At this input,

$$
\begin{aligned}
h_1&=\operatorname{ReLU}(0.86+0.14-0.5)=0.5,\\
h_2&=\operatorname{ReLU}(0.86-0.14)=0.72,\\
m&=0.2+0.5-0.72=-0.02.
\end{aligned}
$$

This negative margin is attached to a real input, not to a relaxation. It is a
counterexample: the claim that April's cat score remains largest throughout
the radius-$0.36$ square is false.

## How exact verifiers organize the search

ReLU networks are piecewise linear. Once every relevant ReLU is fixed as
active or inactive, the remaining problem contains only linear equations and
inequalities. Complete verifiers explore enough of these cases to settle the
property.

Different methods organize that exploration differently. A
**satisfiability-modulo-theories (SMT) solver** searches logical choices while
solving the resulting numerical constraints, as in
[Reluplex](https://arxiv.org/abs/1702.01135). A mixed-integer linear program can
represent each ReLU choice with a binary variable, as in
[Evaluating Robustness of Neural Networks with Mixed Integer Programming](https://arxiv.org/abs/1711.07356).
Specialized branch-and-bound verifiers maintain an explicit set of subproblems
and use neural-network bounds to prune them. All three combine continuous
linear reasoning with discrete case choices.

## Soundness, completeness, and timeouts

A verifier is **sound** when every reported result is justified:

- **verified** means sound bounds cover every allowed input;
- **falsified** means a concrete allowed input violates the property.

A verification procedure is **complete** when it is guaranteed to reach one
of those two conclusions for every supported problem if allowed to run to
completion. For a ReLU verifier, this may require exploring enough activation
cases that every remaining leaf is linear and can be solved exactly.

Completeness is a statement about the procedure, not a promise that every run
finishes quickly. If a time or memory limit stops the search while unresolved
leaves remain, the correct result is **unknown**.

| Reported result | Evidence | What it means |
| --- | --- | --- |
| Verified | Verified leaves cover the allowed set | Every allowed input preserves April's prediction |
| Falsified | A concrete allowed input has $m\leq0$ | The robustness claim is false |
| Unknown | At least one region remains unresolved | The run has not settled the claim |

## Takeaway

One DeepPoly pass gave April the inconclusive bound $m\geq-0.02$ at radius
$0.24$. Splitting the input square at $x_1=0.5$ produced two tighter bounds,
$0.06$ and $0.14$. Because the two verified rectangles cover the original
square, their search tree is a certificate.

Branch and bound turns an inconclusive whole-region calculation into smaller
problems that the same bounding machinery may solve. Sound bounds certify
regions; concrete counterexamples falsify claims; unfinished trees remain
unknown.

Part 6 asks a different question: **can we train April's classifier so that
strong bounds appear without so much search?**
