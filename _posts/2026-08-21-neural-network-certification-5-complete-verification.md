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

DeepPoly therefore returns **unknown**. Its lower bound comes from a
relaxation: a simpler enclosure that contains every real network behavior and
additional artificial behaviors. The artificial part of the enclosure can
pull the bound below zero.

The next question is: **can we cover every allowed input with smaller regions
whose bounds are positive?**

## Divide at the unstable ReLU

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

A standard neural-network branch-and-bound move is to branch on the phase of
this unstable ReLU. The ReLU has two phases:

$$
\begin{aligned}
R_{\mathrm{off}}
&=R\cap\{z_2\leq0\}
 =R\cap\{x_1\leq x_2\},\\
R_{\mathrm{on}}
&=R\cap\{z_2\geq0\}
 =R\cap\{x_1\geq x_2\}.
\end{aligned}
$$

The boundary $z_2=0$ is the diagonal $x_1=x_2$. It divides April's square into
two triangles whose union equals $R$, preserving complete coverage of the
allowed region.

The split follows **divide and conquer**: divide one unresolved problem at the
source of its uncertainty, then conquer each simpler phase separately. Fixing
the phase makes $h_2$ linear in each child, which lets us analyze both triangles
exactly.

<figure class="wide-diagram" style="text-align: center;">
  <div class="wide-diagram__viewport" tabindex="0" role="group" aria-label="Scrollable diagram">
  <img src="{{ '/imgs/april-split-tightens-relu.svg' | relative_url }}?v=relu-phase" width="820" style="display: block; margin: 0 auto;" alt="April's input square divided along the diagonal x1 equals x2. Above the diagonal the second ReLU is off and equals zero; below the diagonal it is on and equals x1 minus x2.">
  </div>
  <figcaption>Branching at $z_2=0$ replaces one unstable ReLU with two exact linear phases.</figcaption>
</figure>

### Conquer the off phase

On $R_{\mathrm{off}}$, we know $z_2\leq0$, so

$$
h_2=\operatorname{ReLU}(z_2)=0.
$$

The margin is now linear:

$$
\begin{aligned}
m
&=0.2+(x_1+x_2-0.5)-0\\
&=x_1+x_2-0.3\\
&\geq0.26+0.26-0.3=0.22.
\end{aligned}
$$

Every input in the off triangle is safe.

### Conquer the on phase

On $R_{\mathrm{on}}$, we know $z_2\geq0$, so

$$
h_2=\operatorname{ReLU}(z_2)=z_2=x_1-x_2.
$$

The margin is linear:

$$
\begin{aligned}
m
&=0.2+(x_1+x_2-0.5)-(x_1-x_2)\\
&=2x_2-0.3\\
&\geq2(0.26)-0.3=0.22.
\end{aligned}
$$

Every input in the on triangle is safe. The phase split has removed the loose
ReLU chord entirely, turning the inconclusive bound $-0.02$ into the exact
bound $0.22$ on both children.

The two children also reveal the network's geometry. A ReLU network is
**piecewise linear**: fixing its ReLU phases selects one affine formula. Here
the off and on triangles are two connected pieces of the exact margin
function. Each piece is a plane, and the planes meet continuously along
$x_1=x_2$.

<figure class="wide-diagram" style="text-align: center;">
  <div class="wide-diagram__viewport" tabindex="0" role="group" aria-label="Scrollable diagram">
  <img src="{{ '/imgs/april-branch-and-bound.svg' | relative_url }}?v=margin-surface" width="820" style="display: block; margin: 0 auto;" alt="The exact margin function shown as two connected planar patches, one for the off ReLU phase and one for the on phase, alongside a search tree whose two children are verified with margin bound 0.22.">
  </div>
  <figcaption>The surface shows the two local affine formulas. The tree groups them into two verified subproblems.</figcaption>
</figure>

## Read the proof from the tree

The left side of the figure shows the exact function that the global
relaxation tried to enclose. The right side organizes its two linear pieces as
a search tree. The root bound is $-0.02$, so its status remains unresolved. We
divide it into two phase children and bound each child separately.

Both child bounds are positive:

$$
\min_{x\in R_{\mathrm{off}}}m(x)\geq0.22,
\qquad
\min_{x\in R_{\mathrm{on}}}m(x)\geq0.22.
$$

Because $R=R_{\mathrm{off}}\cup R_{\mathrm{on}}$, every allowed input belongs
to at least one verified leaf. The tree is therefore a proof for the entire
radius-$0.24$ square. The smallest leaf bound, $0.22$, is a valid lower bound
for the original region.

April has only one unstable ReLU, so each child is already one connected
linear region. In a larger network, an off/on child may still contain several
linear regions created by other unstable ReLUs. Further phase branches
continue the division until every leaf receives a decisive bound.

## Bound, split, and repeat

April needed only one cut. A harder network may leave one or both children
inconclusive. We can apply the same cycle again:

1. **Bound** the margin over the current region.
2. If the lower bound is positive, mark the whole region verified.
3. If the bound is inconclusive, **split** the region into children.
4. Repeat until every leaf is verified or a failing input is found.

**Branch and bound** applies divide and conquer with sound bounds. Branching
divides one unresolved case. Bounding tries to conquer each child while
reasoning about the entire region at once. Neural network verifiers commonly
branch on whether an unstable ReLU is off or on, as we did. Some methods also
branch on input coordinates.

A certificate consists of regions that cover the allowed set, together with a
sound bound for every region declared safe. A unified account of
neural-network branch and bound appears in
[A Unified View of Piecewise Linear Neural Network Verification](https://arxiv.org/abs/1711.00455).

## Search for a failing input at the same time

While bounds reason about whole regions, an attack searches for promising
individual inputs and evaluates them with the exact network. The two jobs
complement each other:

- a positive lower bound proves that an entire region is safe.
- one concrete input with $m(x)\leq0$ disproves the claim immediately.

The completed radius-$0.24$ tree proves every allowed input safe. Enlarging the
radius to $0.36$ brings the following input into the allowed set:

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

The exact network produces this negative margin at an allowed input. The input
is a **counterexample**, so the claim that April's cat score remains largest
throughout the radius-$0.36$ square is false.

## How exact verifiers organize the search

The piecewise-linear structure also explains how complete verifiers finish the
search. Once every relevant ReLU is fixed as active or inactive, the remaining
problem contains only linear equations and inequalities. Complete verifiers
explore enough of these cases to settle the property.

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

- **verified** means sound bounds cover every allowed input.
- **falsified** means a concrete allowed input violates the property.

A verification procedure is **complete** when it is guaranteed to reach one
of those two conclusions for every supported problem if allowed to run to
completion. For a ReLU verifier, this may require exploring enough activation
cases that every remaining leaf is linear and can be solved exactly.

Completeness guarantees an eventual decision when the procedure runs to
completion. Runtime may still be long. If a time or memory limit stops the
search while unresolved leaves remain, the correct result is **unknown**.

| Reported result | Evidence | What it means |
| --- | --- | --- |
| Verified | Verified leaves cover the allowed set | Every allowed input preserves April's prediction |
| Falsified | A concrete allowed input has $m\leq0$ | The robustness claim is false |
| Unknown | At least one region remains unresolved | The claim remains unresolved |

## Takeaway

One DeepPoly pass gave April the inconclusive bound $m\geq-0.02$ at radius
$0.24$. Branching on the unstable ReLU at $z_2=0$ divided the square along
$x_1=x_2$. The off and on phases both give the exact bound $m\geq0.22$.
Because the two verified triangles cover the original square, their search
tree is a certificate.

Branch and bound turns an inconclusive whole-region calculation into smaller
problems that the same bounding machinery may solve. Sound bounds certify
regions. Concrete counterexamples falsify claims. Unfinished trees leave the
claim unresolved.

Part 6 asks a different question: **can we train April's classifier so that
strong bounds appear without so much search?**
