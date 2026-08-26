---
title: "Three Research Frontiers: Neural Network Certification, Part 7"
series_nav_title: "Three Research Frontiers"
author_profile: true
permalink: /2026-08-21-neural-network-certification-7-frontiers/
date: 2026-08-21
show_initial_release: false
written_by: PIRA
written_at: 2026-08-22
tags: [neural networks, certification, theory, abstract interpretation, "Certification Series: 07"]
mathjax: true
toc: true
excerpt: "Three surprising results separate which functions certifiable networks can approximate, which models training can find, and which facts a verifier can prove."
---

## April's classifier leads to three different questions

The first six posts built a certification pipeline around one small classifier
for April the Siberian cat. We stated a robustness property, propagated and
tightened bounds, split inconclusive cases, and trained models whose robustness
is easier to prove.

That pipeline can encounter three fundamentally different obstacles:

1. **Exist:** Can we choose a network whose predictions and certified bounds
   approximate the behavior we want as closely as needed?
2. **Find:** Can a training algorithm reach accurate and certifiable weights?
3. **Prove:** For a fixed network, can a verifier recover the relationships
   needed to prove its exact output bounds?

The first and third questions are especially easy to conflate. The existence
question lets us choose a suitable network and an arbitrarily small positive
error tolerance. The proof question keeps the network fixed and asks for exact
bounds. Training sits between them: a useful network may exist even when
optimization cannot find it.

Each question also challenges a plausible intuition. IBP looks too coarse to
support both accurate predictions and arbitrarily precise interval bounds. A
tighter bound seems like it should provide a better training objective. The
tightest possible relaxation of every ReLU seems like it should be enough to
bound the whole network exactly. The three frontiers below test these
intuitions one at a time.

## Frontier 1: Can an IBP-certified network approximate any continuous function?

Part 3 showed why the first intuition is reasonable. IBP propagates a separate
interval for each value and loses relationships between values. Those lost
relationships can make its bounds widen through the network. Could this
coarseness prevent any network from being both accurate and tightly bounded by
IBP, regardless of its size?

The ordinary universal approximation theorem gives only the accuracy half of
the answer. It says that sufficiently large neural networks can approximate
any continuous function on a compact input domain. In ordinary Euclidean
space, a compact domain is closed and bounded, such as an input box. A
certificate also needs useful bounds for every allowed input region inside
that domain.

Suppose brightness is summarized by one number $t$, and $s(t)$ is April's cat
score. For an interval $B=[t_1,t_2]$, the exact range of target scores is

$$
S(B)=\left[\min_{t\in B}s(t),\ \max_{t\in B}s(t)\right].
$$

An **interval-certified approximator** must control two errors:

- **Prediction error:** $n(t)$ stays close to $s(t)$ at every input $t$.
- **Range error:** the lower and upper endpoints of the IBP interval
  $n^{\sharp}(B)$ stay close to the endpoints of $S(B)$ for every input interval
  $B$.

The notation $n^{\sharp}(B)$ means that we start from $B$ and run the interval rules
from [Part 3]({{ '/2026-08-21-neural-network-certification-3-interval-bound-propagation/' | relative_url }})
through $n$. The resulting interval is sound: it contains every value that $n$
can actually produce on $B$. Small prediction error makes the network accurate.
Small range error makes its simple IBP certificate precise.

The [universal approximation theorem for interval-certified ReLU
networks](https://arxiv.org/abs/1909.13846) answers the question affirmatively.
For every continuous target $s$ and every desired error tolerance, a ReLU
network exists that satisfies both requirements. Its predictions approximate
$s$, and its IBP intervals approximate the exact target ranges.

The network's exact output range on $B$ lies inside the sound interval
$n^{\sharp}(B)$. The figure separates that exact network range from the
slightly wider interval computed by IBP.

<figure class="wide-diagram" style="text-align: center;">
  <div class="wide-diagram__viewport" tabindex="0" role="group" aria-label="Scrollable diagram">
  <img src="{{ '/imgs/april-interval-universal-approximation.svg' | relative_url }}" width="860" style="display: block; margin: 0 auto;" alt="A continuous target score and a nearby piecewise-linear network curve. Over each of three input intervals, blue markers identify the network extrema and its exact output range, while a dashed purple IBP-certified range is slightly wider and encloses that network range.">
  </div>
  <figcaption>The curves show pointwise approximation. On each interval, the blue band spans the network's exact outputs, and the dashed IBP-certified band encloses that range.</figcaption>
</figure>

The theorem settles the existence question by allowing us to choose a network
adapted to the target and the desired tolerance. A later [interval universal
approximation theorem](https://arxiv.org/abs/2007.06093) extends the existence
result from ReLU to a broad family of activation functions.

## Existence leads to a construction question

A training algorithm begins with an architecture and initial weights, then
searches a high-dimensional parameter space under a finite compute budget.
The existence theorem guarantees a destination for that search. Its
computational cost is a separate question.

The generalized interval-approximation study makes this gap concrete. Its
proof constructs a network by dividing the input domain into a grid. As the
input dimension grows, the number of grid regions grows exponentially.

The paper then studies a simpler problem. Given a network with outputs in
$[0,1]$, approximate its minimum and maximum within an error
$\delta<1/2$. Solving this **range-approximation problem** requires finding
values near the extrema and ruling out values beyond them. The paper proves
that both directions are hard: the problem is NP-hard and coNP-hard. Under the
standard assumption $\mathsf{coNP}\not\subseteq\mathsf{NP}$, the
[range-approximation theorem](https://arxiv.org/abs/2007.06093) classifies it
as strictly harder than NP-complete problems. An efficient construction of an
interval universal approximator would solve this range problem, so the
hardness transfers to constructing such networks in general.

Universal approximation therefore leaves an algorithmic question:

**How do we reliably find compact, accurate networks that IBP can certify?**

Certified training provides a practical search strategy. It chooses an
architecture, adjusts its weights using a tractable relaxation of the
worst-case loss, and tries to reach a network that IBP can certify. A more
precise relaxation seems like a better guide because its loss lies closer to
the exact worst-case loss. Frontier 2 asks whether that additional precision
actually helps the optimizer find better weights.

## Frontier 2: Why can a tighter training bound produce a worse model?

Fix a trained network. Suppose relaxation $A$ always gives a smaller sound
upper bound than relaxation $B$ for the violation we want to rule out. Then
$A$ is tighter: any case proved safe by $B$ is also proved safe by $A$.

This fixed-network fact suggests a natural training strategy. Use the tighter
relaxation as the loss because it follows the true worst-case value more
closely. The reasoning misses one change: training does not keep the network
fixed.

Each gradient step changes the weights and therefore changes the next bound.
The optimizer must navigate the whole surface

$$
\theta\longmapsto L_{\mathrm{cert}}(\theta),
$$

where $\theta$ contains all trainable weights. Tightness measures the vertical
gap between this certified loss and the exact worst-case loss at one value of
$\theta$. Optimization also depends on how the surface changes between nearby
weight values.

The [paradox of certified training](https://arxiv.org/abs/2102.06700) is the
observed reversal of the fixed-network intuition: loose interval-based
training often produces networks with higher certified robustness than
training with tighter relaxations. The study identifies two properties beyond
tightness that help explain the result:

- **Continuity:** nearby weights should produce nearby bound values. A jump
  gives the current gradient no information about the landscape across the
  discontinuity.
- **Sensitivity:** this measures how algebraically complicated the bound
  becomes as the weights change. High sensitivity can create high-degree
  rational loss surfaces with additional local optima and saddle points.

<figure class="wide-diagram" style="text-align: center;">
  <div class="wide-diagram__viewport" tabindex="0" role="group" aria-label="Scrollable diagram">
  <img src="{{ '/imgs/april-certified-training-paradox.svg' | relative_url }}" width="860" style="display: block; margin: 0 auto;" alt="Two panels compare verification and training. At fixed weights a tighter interval sits closer to the exact loss. Across changing weights a schematic loose loss varies smoothly while a tighter loss has abrupt and sensitive changes that make gradient steps harder to follow.">
  </div>
  <figcaption>Tightness answers a fixed-network question. Continuity and sensitivity shape the training journey.</figcaption>
</figure>

At fixed weights, a tighter sound bound remains better for verification.
During training, the optimizer must also be able to follow the bound as the
weights change. A useful certified-training objective therefore needs both
precision and navigable optimization dynamics.

Training addressed whether we can find good weights. Now freeze the weights
again and ask what information a verifier can retain.

## Frontier 3: Why can the tightest per-ReLU relaxation still miss the exact bound?

Triangle and DeepPoly from [Part 4]({{ '/2026-08-21-neural-network-certification-4-tighter-relaxations/' | relative_url }})
use a **convex relaxation**: a tractable convex superset of the network's exact
behaviors. For every **unstable ReLU**, whose input interval crosses zero, they
add linear inequalities that enclose the ReLU graph. The tightest possible
envelope for one ReLU seems like the best local choice. The question is whether
locally tight choices produce a globally exact bound.

The verifier still retains the shared affine equations between neurons. The
term **single-neuron relaxation** refers to the nonlinear envelope added at
each ReLU: that envelope is derived only from the ReLU's scalar input interval.
It adds no new inequality coupling the ReLU output to a neighboring value.

Consider the network

$$
a=x_1-x_2,\qquad b=x_2,\qquad
c=\operatorname{ReLU}(a),
$$

with output

$$
f=c+b=x_2+\operatorname{ReLU}(x_1-x_2)
=\max(x_1,x_2).
$$

Let $(x_1,x_2)\in[0,1]^2$. Because $f$ is the maximum of two numbers in
$[0,1]$, its exact output range is $[0,1]$.

A single-neuron Triangle relaxation sees only $a\in[-1,1]$ when it relaxes
$c=\operatorname{ReLU}(a)$. Its upper line is

$$
c\leq\frac{a+1}{2}.
$$

At $x_1=x_2=1$, the exact ReLU value is $c=\operatorname{ReLU}(0)=0$.
The Triangle constraints also permit the spurious value $c=0.5$. Pairing it
with $a=0$ and $b=1$ makes the relaxed output reach

$$
f=c+b=1.5,
$$

although the exact network output there is $1$. The envelope is optimal for
$c$ as a function of $a$ alone. Its spurious value survives because the
envelope does not record how $c$ and $b=x_2$ depend on the same inputs.

## Joint constraints remove the spurious value

A multi-neuron relaxation derives constraints for a group of values together.
For the same network, joint reasoning supplies two valid inequalities:

$$
c\leq 1-b,\qquad c\leq a+b.
$$

Their meaning is visible from the original inputs. Since $x_1\leq1$, we have
$c=\max(x_1-b,0)\leq1-b$. Since $x_2\geq0$, we also have
$c=\max(x_1-x_2,0)\leq x_1=a+b$. The first inequality immediately gives

$$
f=c+b\leq 1.
$$

The exact lower bound $f\geq0$ follows from $c\geq0$ and $b\geq0$, so the
multi-neuron relaxation recovers the exact range $[0,1]$.

<figure class="wide-diagram" style="text-align: center;">
  <div class="wide-diagram__viewport" tabindex="0" role="group" aria-label="Scrollable diagram">
  <img src="{{ '/imgs/max-single-vs-multi-relaxation.svg' | relative_url }}" width="900" style="display: block; margin: 0 auto;" alt="The max of two inputs is encoded by a ReLU network. A single-neuron Triangle constraint permits a relaxed output of 1.5 at input 1,1. A joint constraint between the ReLU output and the second input removes that impossible value and proves the exact upper bound 1.">
  </div>
  <figcaption>The ReLU envelope is locally tight. The joint relationship supplies the missing proof.</figcaption>
</figure>

The [expressiveness analysis of multi-neuron convex
relaxations](https://arxiv.org/abs/2410.06816) proves that this example reflects
a genuine separation. No single-neuron relaxation can exactly bound every ReLU
network encoding the two-dimensional maximum, while a suitable multi-neuron
relaxation bounds the construction above exactly.

Computing the joint convex hull of an entire network can be expensive.
Practical methods such as [PRIMA](https://arxiv.org/abs/2103.03638) therefore
approximate convex hulls over small groups of neurons. The convex hull is the
smallest convex set containing all exact feasible points. This raises the next
question: would larger groups eventually make the verifier exact?

## Can larger neuron groups make the verifier exact?

The same study proves a universal convex barrier. Even the optimal convex
description of every neuron in each complete layer is inexact for some
networks. Extending the relaxation across any fixed finite number of
consecutive layers still cannot guarantee exactness. A larger local window
preserves more relationships, but spurious points can reappear when the
verifier convexifies and propagates information through the remaining layers.

Multi-neuron reasoning nevertheless creates two routes to exact bounds that
single-neuron reasoning cannot match as efficiently:

1. **Transform the network.** Add carefully designed ReLU neurons that preserve
   the original function while carrying important input relationships forward.
   The paper proves that a polynomial-size transformation exists for which an
   optimal layerwise multi-neuron relaxation becomes exact.
2. **Partition the input.** Divide the input region into convex pieces whose
   reachable sets remain convex through the network, then bound every piece.
   This reconnects multi-neuron relaxations with the divide-and-conquer method
   from [Part 5]({{ '/2026-08-21-neural-network-certification-5-complete-verification/' | relative_url }}).

The nested maximum makes the potential difference concrete. For
$\max(x_1,\ldots,x_d)$ on $[0,1]^d$, the paper's multi-neuron construction
needs one subproblem and a number of constraints that grows linearly with $d$.
An exact DeepPoly branch-and-bound proof must instead separate all
$2^{d-1}$ activation patterns for this construction.

The frontier is therefore more precise than “larger groups are tighter.” The
research question is:

**Which joint relationships should a verifier preserve, and how can it expose
them without paying for every possible relationship?**

## Put existence, training, and proof back together

The three frontiers describe different stages of the same pipeline.

| Question | What we learned | Research direction |
| --- | --- | --- |
| Can a suitable certifiable model **exist**? | For any continuous target and error tolerance, a network exists whose predictions and IBP ranges achieve that tolerance. | Construct compact interval-friendly architectures efficiently. |
| Can training **find** one? | Bound tightness, continuity, and sensitivity jointly shape the optimization result. | Design precise objectives with navigable loss surfaces. |
| Can a verifier **prove exact bounds for a fixed model**? | Joint relaxations preserve relationships that single-neuron relaxations lose, while every fixed local convex scope has a general barrier. | Select useful groups, transformations, and partitions at manageable cost. |

Existence permits a carefully chosen network and an approximation tolerance.
Training asks for an algorithm that reaches useful weights. Exact verification
fixes those weights and asks whether the abstraction preserves enough
information. Keeping these quantifiers separate prevents progress at one stage
from being mistaken for progress at all three.

Every certificate so far has propagated deterministic bounds over an allowed
input region. Part 8 takes a probabilistic route: add random noise, measure how
often April's label wins, and convert that probability into a certified radius.
