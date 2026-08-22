---
title: "Denoisers and Input-Dependent Noise: Neural Network Certification, Part 9"
author_profile: true
permalink: /2026-08-21-neural-network-certification-9-adaptive-randomized-smoothing/
date: 2026-08-21
written_by: PIRA
written_at: 2026-08-21
tags: [neural networks, certification, randomized smoothing, denoising]
toc: true
published: false
excerpt: "Adapt randomized smoothing by denoising April's noisy photographs and choosing a certifiably safe noise level for each input."
---

<!--
Status: outline only.

Reader outcome:
The reader can explain how denoised smoothing certifies a pretrained classifier,
why an input-dependent noise level requires a new soundness argument, and how
Dual RS certifies both its variance choice and its final prediction.
-->

## April's photographs do not all need the same treatment

<!--
Recall the Part 8 pipeline and place two April photographs beside it: a clear
close-up and a difficult image with a busy background. The same base classifier
and global Gaussian variance process both images.

Ask the central question:

**Which parts of randomized smoothing can adapt to the model or the input
without breaking the certificate?**

Preview two answers. A denoiser changes the base classifier seen by the smoothing
theorem. Input-dependent smoothing changes the noise distribution and therefore
needs an additional proof.
-->

## Denoised smoothing reuses a pretrained classifier

<!--
Place a denoiser before the classifier:

\[
x+\eta \longrightarrow D(x+\eta) \longrightarrow f(D(x+\eta)).
\]

Use a three-panel April figure: noisy photograph, denoised photograph, and
classification. Explain the key compositional idea: randomized smoothing can
treat \(f\circ D\) as its base classifier, so the Part 8 theorem applies to the
composition. The classifier's parameters can remain unchanged while the
denoiser learns to remove the injected noise.

Primary source:
https://arxiv.org/abs/2003.01908
-->

## Diffusion models become smoothing denoisers

<!--
Present diffusion denoised smoothing as the same composition with a powerful
pretrained diffusion model in the denoising position. Reuse the three-panel
April figure and change only the denoiser box, making the relationship to the
previous section immediate.

Explain why the modular view matters: an off-the-shelf denoiser and an
off-the-shelf classifier can be combined under the smoothing theorem without
fine-tuning either model in the cited construction.

Primary source:
https://arxiv.org/abs/2206.10550
-->

## One global noise level creates conflicting goals

<!--
Return to \(\sigma\). A small value tends to preserve accuracy near the clean
input, while a large value can support predictions at larger certified radii.
One global value forces the clear and difficult April photographs to use the
same trade-off.

Plan a certified-accuracy-versus-radius figure for two global noise levels. One
curve leads at small radii and the other at large radii. Let this crossing create
the motivation for choosing \(\sigma\) by input.
-->

## Why can we not simply substitute an input-dependent variance?

<!--
Compare standard smoothing at neighboring inputs \(x\) and \(x'\). With global
\(\sigma\), both predictions shift the same Gaussian distribution. With an
arbitrary \(\sigma(x)\), moving the input can also change the distribution's
shape, so the Part 8 theorem does not directly compare the two classifiers.

Use overlapping one-dimensional Gaussian curves to make the proof gap visible.
Then introduce data-dependent randomized smoothing and the later analysis of
the conditions required for sound input-dependent certificates.

Data-dependent randomized smoothing:
https://arxiv.org/abs/2012.04351

Analysis of input-dependent smoothing guarantees:
https://arxiv.org/abs/2110.05365
-->

## Local constancy makes the variance choice certifiable

<!--
State the key condition before naming the method: if every input throughout the
certified neighborhood selects the same variance, the standard smoothing
theorem can reason about one fixed Gaussian distribution there.

Draw a one-dimensional input line partitioned into regions labeled by their
selected \(\sigma\). Put April's input strictly inside one region and show a
certified ball that does not cross a variance boundary. This figure prepares
the Dual RS construction.
-->

## Dual RS certifies the noise selector

<!--
Present Dual RS as two connected smoothed components:

1. A variance estimator selects a useful noise level for the current input.
2. A standard smoothed classifier makes the final prediction at that level.

Explain how independently smoothing the variance estimator certifies that its
choice remains locally constant. The final radius must stay inside both
guarantees: the region where the variance choice is fixed and the region where
the selected RS classifier keeps April's label.

Plan a routing figure with easy and difficult April photographs sent to
different noise levels. Highlight the two certificates before combining them.

Primary source:
https://arxiv.org/abs/2512.01782
-->

## One framework, two kinds of adaptation

<!--
Complete a comparison table:

- Denoised smoothing changes the base mapping inside the standard smoothing
  construction.
- Diffusion denoised smoothing supplies that mapping with pretrained models.
- Input-dependent smoothing changes the noise distribution and requires a
  condition connecting neighboring inputs.
- Dual RS certifies a locally constant routing decision before applying a
  standard smoothed classifier.

For each row, identify the changed component, the theorem that supports it, and
the figure in which April travels through the pipeline.
-->

## Takeaway

<!--
Return to the two April photographs. A denoiser can adapt how noisy inputs are
interpreted. A certified variance selector can adapt how much noise each input
receives. Both methods preserve a clear route back to the probability theorem
from Part 8.
-->
