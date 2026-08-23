---
title: "Denoisers and Input-Dependent Noise: Neural Network Certification, Part 9"
author_profile: true
permalink: /2026-08-21-neural-network-certification-9-adaptive-randomized-smoothing/
date: 2026-08-21
written_by: PIRA
written_at: 2026-08-22
tags: [neural networks, certification, randomized smoothing, denoising, "Certification Series: 09"]
mathjax: true
toc: true
excerpt: "Adapt randomized smoothing by denoising April's noisy photographs and choosing a certifiably safe noise level for each input."
---

## April's photographs do not all need the same treatment

[Part 8]({{ '/2026-08-21-neural-network-certification-8-randomized-smoothing/' | relative_url }})
built a smoothed classifier by adding Gaussian noise, asking a base
classifier for labels, and taking the most probable label. Its certificate came
from a fixed noise level $\sigma$.

Now place two April photographs beside that pipeline. The classifier's noisy
votes around one image are fragile, while its votes around the other remain
stable under stronger perturbations. The same base model and the same $\sigma$
process both images.

This raises a new question:

**Which parts of randomized smoothing can adapt to the model or the input
without breaking the certificate?**

We will change two components. Denoised smoothing changes the function that
receives the noisy input. Input-dependent smoothing changes the noise level
itself.

## A denoiser can stand in front of a pretrained classifier

Recall the ingredients. Let $\eta\sim\mathcal N(0,\sigma^2I)$. Randomized
smoothing predicts the class most likely under $x+\eta$. A radius $R$
certifies that this prediction cannot change for any $x'$ with
$\lVert x'-x\rVert_2<R$. If $p_A>1/2$ is a statistically valid lower bound on
the winning-class probability, the common certificate is

$$
R=\sigma\Phi^{-1}(p_A),
$$

where $\Phi^{-1}$ is the inverse standard-normal cumulative distribution
function.

Let $D$ be a denoiser and $f$ a classifier. Denoised smoothing inserts $D$
between the noisy input and $f$:

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

<figure class="wide-diagram" style="text-align: center;">
  <div class="wide-diagram__viewport" tabindex="0" role="group" aria-label="Scrollable diagram">
  <img src="{{ '/imgs/april-denoised-smoothing.svg' | relative_url }}" width="900" style="display: block; margin: 0 auto;" alt="April's clean photograph is perturbed by Gaussian noise, passed through a denoiser, and classified. The denoiser and classifier together form the base classifier inside randomized smoothing.">
  </div>
  <figcaption>Denoised smoothing changes the base classifier while reusing the Gaussian theorem.</figcaption>
</figure>

[Denoised smoothing](https://arxiv.org/abs/2003.01908) trains $D$ so that noisy
images recover features useful to an existing classifier. The classifier's
parameters can remain fixed. This makes it possible to add a certified
robustness wrapper around a pretrained or even black-box image service.

The certificate depends on how large the winning-class probability is for the
composed classifier $f\circ D$ across the Gaussian cloud.

## Diffusion models provide powerful off-the-shelf denoisers

A diffusion model learns to reverse a gradual noising process. That skill fits
the denoising position in the previous pipeline.

The method
[(Certified!!) Adversarial Robustness for
Free!](https://arxiv.org/abs/2206.10550) combines a pretrained diffusion model
with a pretrained image classifier. For each Gaussian-perturbed input, the
diffusion model performs a denoising step and the classifier supplies a vote.
The published construction requires no fine-tuning of either pretrained model.

The method matches $\sigma$ to a diffusion timestep, rescales the noisy image,
and performs one denoising step before classification. The resulting denoiser
and classifier form the base mapping, so the ordinary smoothing theorem still
converts its noisy votes into an $\ell_2$ certificate.

## One global noise level creates conflicting goals

The noise scale $\sigma$ appears both in the data distribution and in the
radius:

$$
R=\sigma\Phi^{-1}(p_A)
$$

for the common one-probability form of the certificate.

A smaller $\sigma$ perturbs April's image less, so the winning class often has
a higher probability $p_A$. A larger $\sigma$ widens the Gaussian cloud and
multiplies the quantile, but $p_A$ may fall. Different inputs maximize
$R(\sigma)$ at different noise scales depending on their stability under
perturbations.

<figure class="wide-diagram" style="text-align: center;">
  <div class="wide-diagram__viewport" tabindex="0" role="group" aria-label="Scrollable diagram">
  <img src="{{ '/imgs/april-global-noise-tradeoff.svg' | relative_url }}" width="900" style="display: block; margin: 0 auto;" alt="Two schematic certified-radius curves peak at different Gaussian noise scales. A fragile input favors a smaller sigma, while an input stable under stronger perturbations favors a larger sigma. Standard smoothing must choose one global sigma.">
  </div>
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
noise scale per test point therefore needs an argument connecting the choices
at neighboring points.

[Data-dependent randomized smoothing](https://arxiv.org/abs/2012.04351)
chooses $\sigma$ per query and stores previously certified regions. Its
memory-based procedure adjusts predictions or shrinks regions to prevent
overlapping certified regions from carrying different labels. A later
[analysis of input-dependent smoothing](https://arxiv.org/abs/2110.05365)
formalizes why rapidly changing noise-scale functions cannot inherit the ordinary
certificate and studies conditions that restore a sound guarantee.

## Local constancy supplies the missing connection

Suppose the selected noise level remains constant throughout a ball around
$x$:

$$
\sigma(x')=\sigma(x)
\qquad\text{for every }x'\text{ with }
\lVert x'-x\rVert_2<R_\sigma.
$$

Inside that ball, all inputs invoke the same Gaussian noise scale. The standard
smoothing comparison is available again.

The
[Dual Randomized Smoothing theorem](https://arxiv.org/abs/2512.01782) states
this precisely. If the scale selector is constant on $B(x,R_\sigma)$, and
ordinary smoothing at the selected scale certifies $R_c$, the adaptive
classifier is certified to $\min(R_\sigma,R_c)$. In practice, both the
constancy claim and the class-probability claim are estimated statistically.
If their failure probabilities are
$\alpha_\sigma$ and $\alpha_c$, the union bound gives joint confidence at least

$$
1-(\alpha_\sigma+\alpha_c).
$$

No independence assumption is needed for that confidence calculation.

## Dual RS certifies the selector and the prediction

Dual RS implements the idea with two smoothed models.

1. The paper's **variance estimator** predicts one noise standard deviation
   $\sigma$ from a finite set such as $\{0.25,0.5,1.0\}$. It is independently
   smoothed, so it returns both a selected scale and a radius $R_\sigma$ within
   which that selection cannot change.
2. A **classification model** is smoothed with the selected scale. It
   returns April's label and a classification radius $R_c$.

The final certified radius is

$$
R=\min(R_\sigma,R_c).
$$

The minimum has a direct meaning. Before reaching $R_\sigma$, the route stays
on the same noise level. Before reaching $R_c$, that route's smoothed classifier
keeps the same label. Staying inside both radii preserves the entire two-stage
decision.

<figure class="wide-diagram" style="text-align: center;">
  <div class="wide-diagram__viewport" tabindex="0" role="group" aria-label="Scrollable diagram">
  <img src="{{ '/imgs/april-dual-rs.svg' | relative_url }}" width="940" style="display: block; margin: 0 auto;" alt="Dual randomized smoothing first uses a smoothed variance estimator to choose sigma and certify radius R sigma. It then uses a classifier smoothed at that sigma to predict Siberian cat and certify radius R c. The final radius is the smaller of the two.">
  </div>
  <figcaption>One certificate protects the route; the other protects the class prediction.</figcaption>
</figure>

The estimator can also route inputs among pretrained expert RS models, each
specialized for one noise scale. Improving an expert can improve certificates
for inputs routed to it, after recertification, without changing the soundness
argument.

## Two kinds of adaptation, one proof discipline

The two method families change different parts of randomized smoothing.

| What adapts? | Example | Why the certificate remains valid |
| --- | --- | --- |
| The base mapping becomes $f\circ D$. | Diffusion denoised smoothing supplies a pretrained $D$. | The smoothing theorem permits any base classifier. |
| The noise scale becomes $\sigma(x)$. | Dual RS certifies a selector over scales or experts. | Local constancy is certified first; the selected classifier is certified second. |

April's noisy photograph now follows two sound adaptive routes: change the base
mapping while keeping the theorem, or certify the selector before using an
input-dependent noise scale.

## Series takeaway

[Part 1]({{ '/2026-08-21-neural-network-certification-1-what-are-we-proving/' | relative_url }})
began with a gap between testing some inputs and proving a claim for every
allowed input. The [series map]({{ '/2026-08-21-neural-network-certification-1-what-are-we-proving/#series-map' | relative_url }})
now connects two ways to close that gap.

Deterministic verification propagates sound bounds through a network and uses
branch-and-bound when one enclosure is inconclusive. Randomized smoothing
certifies a vote-based classifier through probability bounds. Adaptive methods
add one shared obligation: every choice that can affect the prediction—such as
a ReLU phase, denoiser, or noise scale—must remain covered by the proof.

Neural network certification is therefore a discipline of complete coverage.
The mathematical tools change, while the central question remains: **which
allowed inputs and decisions does this argument prove safe?**
