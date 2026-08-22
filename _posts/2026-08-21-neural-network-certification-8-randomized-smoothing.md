---
title: "How Can Random Noise Produce a Certificate? Neural Network Certification, Part 8"
author_profile: true
permalink: /2026-08-21-neural-network-certification-8-randomized-smoothing/
date: 2026-08-21
written_by: PIRA
written_at: 2026-08-21
tags: [neural networks, certification, randomized smoothing, probabilistic methods]
toc: true
published: false
excerpt: "Follow noisy copies of April's photo from majority vote to a probabilistic robustness certificate, then examine training and evaluation."
---

<!--
Status: outline only.

Reader outcome:
The reader can construct a Gaussian-smoothed classifier, interpret its certified
radius theorem, and explain why practical certificates carry a statistical
confidence level. The reader will also recognize the main training objectives
and understand why average certified radius can mislead.
-->

## One photograph of April becomes a cloud

<!--
Begin with April's original photograph and many copies perturbed by Gaussian
noise. The base classifier may disagree on individual copies, yet most copies
still receive the label "Siberian cat." Let the vote motivate the central
question:

**How can agreement across random noisy inputs guarantee the prediction for
every adversarial input inside a fixed radius?**

Connect to Part 7: deterministic relaxations reason about a region through
bounds, whereas randomized smoothing reasons about how a noise distribution
shifts when the input moves.
-->

## Build the smoothed classifier from votes

<!--
Let the base classifier be f and draw
\(\eta \sim \mathcal{N}(0, \sigma^2 I)\). Define

\[
g(x)=\arg\max_c \Pr\bigl(f(x+\eta)=c\bigr).
\]

Explain every symbol through April's noisy photographs before interpreting the
formula. The noise scale \(\sigma\) controls how widely the cloud spreads. The
smoothed classifier \(g\) returns the class with the largest share of that cloud.

Plan a figure with one input point, its circular Gaussian cloud, and colored
decision regions from the base classifier. Show the majority class as area
under the cloud rather than as a finite collection of arbitrary test points.

Primary source:
https://arxiv.org/abs/1902.02918
-->

## The certified-radius theorem

<!--
Introduce \(c_A\) as the most probable class. Let \(p_A\) be a lower bound on
its probability and \(p_B\) an upper bound on every competing class. When
\(p_A>p_B\), state the Gaussian randomized-smoothing theorem:

\[
R=\frac{\sigma}{2}
\left(\Phi^{-1}(p_A)-\Phi^{-1}(p_B)\right),
\]

and for every \(\delta\) satisfying \(\lVert\delta\rVert_2<R\),
\(g(x+\delta)=c_A\).

First demonstrate the binary simplification
\(R=\sigma\Phi^{-1}(p_A)\) when \(p_B=1-p_A\), using concrete vote
probabilities for April. Then return to the multiclass formula.

Explain the theorem geometrically: moving the Gaussian center changes the
probability mass available to each decision region. The normal quantiles
measure how far the center can move before the top class can lose its lead.
Keep the proof idea visual and use the Neyman–Pearson argument only by name at
the end.
-->

## Where probability enters the practical certificate

<!--
Separate two layers that newcomers can easily conflate:

1. If the class probabilities were known exactly, \(g\) and its radius theorem
   would give a deterministic statement about every input in the \(\ell_2\)
   ball.
2. A computer estimates those probabilities from finitely many noisy samples.
   Binomial confidence bounds make the reported certificate valid with a chosen
   confidence such as \(1-\alpha\).

Follow the standard CERTIFY procedure: sample votes, compute a lower confidence
bound for the leading class, return a certified radius when the evidence is
strong enough, and abstain otherwise. Use two April examples with the same
number of votes but different vote margins so the reason for abstention is
visible.
-->

## How do we train a classifier that stays accurate under noise?

<!--
Present the common methods as responses to one problem: the certificate grows
when the correct class keeps a large probability under Gaussian noise.

Build one compact table with columns "training signal," "what it encourages,"
and "extra computation":

- Gaussian augmentation trains on \(x+\eta\), the direct baseline.
- SmoothAdv attacks the smoothed classifier during adversarial training.
- MACER directly optimizes a surrogate for the certified radius.
- Consistency regularization aligns predictions across noisy copies.
- SmoothMix trains on mixtures along adversarial directions to calibrate the
  smoothed classifier's confidence.
- CAT-RS adjusts the training pressure sample by sample using confidence under
  Gaussian noise.

Show these objectives on the same three noisy copies of April's image. Focus on
the information each loss extracts rather than presenting five detached paper
summaries.

SmoothAdv:
https://arxiv.org/abs/1906.04584

MACER:
https://arxiv.org/abs/2001.02378

Consistency regularization:
https://arxiv.org/abs/2006.04062

SmoothMix:
https://arxiv.org/abs/2111.09277

CAT-RS:
https://arxiv.org/abs/2212.09000
-->

## Why average certified radius can reward the wrong progress

<!--
Define average certified radius (ACR) only after readers understand a radius for
one image. Construct a tiny April dataset with several difficult photographs
and one easy close-up. Increasing the easy image's already-large radius can
raise the average while none of the difficult photographs improves.

Present the main findings: a trivial classifier can attain arbitrarily large
ACR under the paper's construction; ACR is much more sensitive to improvements
on easy samples; and its comparisons depend strongly on the certification
budget. Connect this to training by showing how an ACR-oriented objective can
shift attention away from hard samples.

Conclude with evaluation that retains the distribution: certified accuracy as
a curve over radii and the empirical distribution of the correct-class noisy
probability \(p_A\), rather than one average.

Primary source:
https://arxiv.org/abs/2410.06895
-->

## Put the probabilistic pipeline together

<!--
Finish with one end-to-end diagram:

base classifier -> Gaussian noise -> noisy votes -> confidence bounds ->
certified radius or abstention -> evaluation across the full radius curve.

Ask the reader to identify which component changes in Gaussian training,
SmoothAdv, MACER, consistency regularization, SmoothMix, and CAT-RS. This turns
the method list into one reusable mental model.
-->

## Takeaway

<!--
Return to April's cloud of noisy photographs. A probability gap between the top
two classes becomes a geometric \(\ell_2\) radius through the Gaussian
quantiles. Finite sampling adds a stated confidence level, training shapes the
probability gap, and evaluation must retain how robustness is distributed across
inputs. Part 9 will adapt the framework by changing the base classifier and the
noise level while preserving the conditions required for certification.
-->
