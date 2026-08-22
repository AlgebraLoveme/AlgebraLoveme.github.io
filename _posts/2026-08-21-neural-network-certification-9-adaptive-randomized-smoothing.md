---
title: "Denoisers and Input-Dependent Noise: Neural Network Certification, Part 9"
author_profile: true
permalink: /2026-08-21-neural-network-certification-9-adaptive-randomized-smoothing/
date: 2026-08-21
written_by: PIRA
written_at: 2026-08-22
tags: [neural networks, certification, randomized smoothing, denoising]
mathjax: true
toc: true
excerpt: "Adapt randomized smoothing by denoising April's noisy photographs and choosing a certifiably safe noise level for each input."
---

> **Reader background.** We assume undergraduate calculus, linear algebra,
> elementary probability, and basic neural networks. The series introduces
> program verification, neural network certification, abstract interpretation,
> and randomized smoothing from first principles.

## April's photographs do not all need the same treatment

Part 8 built a smoothed classifier by adding Gaussian noise, asking a base
classifier for labels, and taking the most probable label. Its certificate came
from a fixed noise level $\sigma$.

Now place two April photographs beside that pipeline. One is a clear close-up.
The other has difficult lighting and a busy background. The same base model and
the same $\sigma$ process both images.

This raises a new question:

**Which parts of randomized smoothing can adapt to the model or the input
without breaking the certificate?**

We will change two components. Denoised smoothing changes the function that
receives the noisy input. Input-dependent smoothing changes the noise level
itself.

## A denoiser can stand in front of a pretrained classifier

Let $D$ be a denoiser and $f$ a classifier. Instead of sending $x+\eta$
directly into $f$, compute

$$
x+\eta
\longrightarrow D(x+\eta)
\longrightarrow f(D(x+\eta)).
$$

The composition

$$
h=f\circ D
$$

is simply another base classifier. The smoothing theorem from Part 8 allowed
the base classifier to be any function, so we can define

$$
g_D(x)=\arg\max_c
\Pr\bigl(f(D(x+\eta))=c\bigr)
$$

and apply the same Gaussian radius formula.

<figure style="text-align: center;">
  <img src="{{ '/imgs/april-denoised-smoothing.svg' | relative_url }}" width="900" style="display: block; margin: 0 auto;" alt="April's clean photograph is perturbed by Gaussian noise, passed through a denoiser, and classified. The denoiser and classifier together form the base classifier inside randomized smoothing.">
  <figcaption>Denoised smoothing changes the base classifier while reusing the Gaussian theorem.</figcaption>
</figure>

[Denoised smoothing](https://arxiv.org/abs/2003.01908) trains $D$ so that noisy
images recover features useful to an existing classifier. The classifier's
parameters can remain fixed. This makes it possible to add a certified
robustness wrapper around a pretrained or even black-box image service.

Human-visible reconstruction quality can remain imperfect. The certificate
depends on whether the composed classifier $f\circ D$ predicts consistently
across the Gaussian cloud.

## Diffusion models provide powerful off-the-shelf denoisers

A diffusion model learns to reverse a gradual noising process. That skill fits
the denoising position in the previous pipeline.

The method
[(Certified!!) Adversarial Robustness for
Free!](https://arxiv.org/abs/2206.10550) combines a pretrained diffusion model
with a pretrained image classifier. For each Gaussian-perturbed input, the
diffusion model performs a denoising step and the classifier supplies a vote.
The published construction requires no fine-tuning of either pretrained model.

The logical chain stays short:

1. the diffusion denoiser and classifier form one base mapping;
2. Gaussian smoothing turns that mapping into a smoothed classifier;
3. the noisy class probability produces the certified $\ell_2$ radius.

This modular view lets advances in generative denoising contribute to
certification without changing the smoothing theorem.

## One global noise level creates conflicting goals

The noise scale $\sigma$ appears both in the data distribution and in the
radius:

$$
R=\sigma\Phi^{-1}(p_A)
$$

for the common one-probability form of the certificate.

A smaller $\sigma$ perturbs April's image less, so the base classifier often
retains higher noisy accuracy $p_A$. A larger $\sigma$ multiplies the normal
quantile by a larger number and explores a wider neighborhood, but it can make
classification harder. Different inputs balance these effects at different
noise levels.

<figure style="text-align: center;">
  <img src="{{ '/imgs/april-global-noise-tradeoff.svg' | relative_url }}" width="900" style="display: block; margin: 0 auto;" alt="A clear April image favors a small Gaussian cloud for high accuracy at small radii, while another image favors a larger cloud for stronger performance at larger radii. One global sigma must choose one cloud for both inputs.">
  <figcaption>A global noise level asks every input to accept the same accuracy–radius trade-off.</figcaption>
</figure>

This is a routing problem in disguise. For each photograph, we would like to
select the noise level that gives the most useful certificate.

## Why can we not substitute an arbitrary $\sigma(x)$?

The standard proof compares the Gaussian distribution centered at $x$ with the
same distribution shifted to $x+\delta$. A global $\sigma$ ensures that only
the center moves.

If we replace it with an arbitrary function $\sigma(x)$, a nearby input may
change both the center and the spread:

$$
\mathcal N(x,\sigma(x)^2I)
\quad\hbox{versus}\quad
\mathcal N(x+\delta,\sigma(x+\delta)^2I).
$$

The Part 8 theorem does not compare this pair. A method that chooses a useful
variance per test point therefore needs an argument connecting the choices at
neighboring points.

[Data-dependent randomized smoothing](https://arxiv.org/abs/2012.04351) uses
piecewise-constant choices together with stored robust regions to make its
construction certifiable. A later
[analysis of input-dependent smoothing](https://arxiv.org/abs/2110.05365)
formalizes why rapidly changing variance functions cannot inherit the ordinary
certificate and studies conditions that restore a sound guarantee.

## Local constancy supplies the missing connection

Suppose the selected noise level remains constant throughout a ball around
$x$:

$$
\sigma(x')=\sigma(x)
\qquad\text{for every }x'\text{ with }
\lVert x'-x\rVert_2<R_\sigma.
$$

Inside that ball, all inputs invoke the same Gaussian variance. The standard
smoothing comparison is available again.

The
[Dual Randomized Smoothing theorem](https://arxiv.org/abs/2512.01782) states
this precisely. If $\sigma(\cdot)$ is constant throughout the classifier's
certified neighborhood, the input-dependent smoothed classifier preserves its
label there. In practice, both the constancy claim and the class-probability
claim are estimated statistically. If their failure probabilities are
$\alpha_\sigma$ and $\alpha_c$, the union bound gives joint confidence at least

$$
1-(\alpha_\sigma+\alpha_c).
$$

No independence assumption is needed for that confidence calculation.

## Dual RS certifies the selector and the prediction

Dual RS implements the idea with two smoothed models.

1. A **variance estimator** predicts one value from a finite set such as
   $\{0.25,0.5,1.0\}$. It is independently smoothed, so it returns both a
   selected variance and a radius $R_\sigma$ within which that selection cannot
   change.
2. A **classification model** is smoothed with the selected variance. It
   returns April's label and a classification radius $R_c$.

The final certified radius is

$$
R=\min(R_\sigma,R_c).
$$

The minimum has a direct meaning. Before reaching $R_\sigma$, the route stays
on the same noise level. Before reaching $R_c$, that route's smoothed classifier
keeps the same label. Staying inside both radii preserves the entire two-stage
decision.

<figure style="text-align: center;">
  <img src="{{ '/imgs/april-dual-rs.svg' | relative_url }}" width="940" style="display: block; margin: 0 auto;" alt="Dual randomized smoothing first uses a smoothed variance estimator to choose sigma and certify radius R sigma. It then uses a classifier smoothed at that sigma to predict Siberian cat and certify radius R c. The final radius is the smaller of the two.">
  <figcaption>One certificate protects the route; the other protects the class prediction.</figcaption>
</figure>

The estimator can also route inputs among pretrained expert RS models, each
specialized for one noise level. Improving an expert then improves the inputs
routed to it without redesigning the certification theorem.

## Two kinds of adaptation, one proof discipline

The two method families change different parts of randomized smoothing.

| Method | What adapts? | Why the certificate remains valid |
| --- | --- | --- |
| Denoised smoothing | The base mapping becomes $f\circ D$. | The smoothing theorem permits any base classifier. |
| Diffusion denoised smoothing | A pretrained diffusion model supplies $D$. | The same composition argument applies. |
| Input-dependent smoothing | The variance becomes $\sigma(x)$. | Neighboring variance choices must be connected by an additional soundness condition. |
| Dual RS | A smoothed estimator selects the variance or expert. | Local constancy is certified first; the selected classifier is certified second. |

April's noisy photograph now follows a complete adaptive pipeline. A denoiser
can change how the image is interpreted. A certified selector can change how
much noise the image receives. Every adaptation keeps a visible route back to
the probability theorem from Part 8.
