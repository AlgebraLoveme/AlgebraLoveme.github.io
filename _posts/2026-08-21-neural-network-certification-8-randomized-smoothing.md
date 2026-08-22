---
title: "How Can Random Noise Produce a Certificate? Neural Network Certification, Part 8"
author_profile: true
permalink: /2026-08-21-neural-network-certification-8-randomized-smoothing/
date: 2026-08-21
written_by: PIRA
written_at: 2026-08-22
tags: [neural networks, certification, randomized smoothing, probabilistic methods]
mathjax: true
toc: true
excerpt: "Follow noisy copies of April's photo from majority vote to a probabilistic robustness certificate, then examine training and evaluation."
---

> **Reader background.** We assume undergraduate calculus, linear algebra,
> elementary probability, and basic neural networks. The series introduces
> program verification, neural network certification, abstract interpretation,
> and randomized smoothing from first principles.

## One photograph of April becomes a cloud

The previous posts certified a deterministic neural network by propagating an
entire input region through it. That approach follows the network's internal
computations. Randomized smoothing takes a different route.

Start with April's photograph. Add independent Gaussian noise to every pixel,
classify each noisy copy, and count the labels. Some copies may look grainy,
but suppose “Siberian cat” wins a large majority.

<figure style="text-align: center;">
  <a href="{{ '/imgs/April_the_cat.jpg' | relative_url }}">
    <img src="{{ '/imgs/April_the_cat.jpg' | relative_url }}" width="240" style="display: block; margin: 0 auto;" alt="April, a cream-colored Siberian cat with gray ears, sitting beside a tree in sunlight.">
  </a>
  <figcaption>Randomized smoothing asks how April is classified after Gaussian noise is repeatedly added to this image.</figcaption>
</figure>

This creates the central question:

**How can agreement across random noisy inputs guarantee the prediction for
every adversarial input inside a fixed radius?**

## Build a new classifier from noisy votes

Let $f$ be any base classifier and let

$$
\eta\sim\mathcal N(0,\sigma^2I).
$$

The vector $\eta$ contains one independent Gaussian noise value per input
coordinate. The parameter $\sigma$ controls the spread: larger $\sigma$ creates
a wider cloud around the original input.

The **smoothed classifier** is

$$
g(x)=\arg\max_c\Pr\bigl(f(x+\eta)=c\bigr).
$$

Read the formula from the inside out:

1. sample a noisy input $x+\eta$;
2. ask the base classifier $f$ for its label;
3. compute the probability of each class across the noise;
4. let $g$ return the most probable class.

The classifier being certified is $g$. The base classifier $f$ supplies the
votes.

<figure style="text-align: center;">
  <img src="{{ '/imgs/april-randomized-smoothing-cloud.svg' | relative_url }}" width="880" style="display: block; margin: 0 auto;" alt="A point representing April is surrounded by Gaussian noisy samples in three base-classifier decision regions. Most samples fall in the Siberian cat region, so the smoothed classifier predicts Siberian cat.">
  <figcaption>The base classifier may vary across the cloud; the smoothed classifier returns its most probable label.</figcaption>
</figure>

## A probability gap becomes a certified radius

Let $c_A$ be the most probable class. Suppose we know

$$
\Pr(f(x+\eta)=c_A)\geq p_A
$$

and every competing class has probability at most $p_B$, with $p_A>p_B$.
For Gaussian noise, the
[randomized smoothing theorem](https://arxiv.org/abs/1902.02918) gives the
radius

$$
R=\frac{\sigma}{2}
\left(\Phi^{-1}(p_A)-\Phi^{-1}(p_B)\right),
$$

where $\Phi$ is the cumulative distribution function of a standard normal
random variable. Its inverse $\Phi^{-1}(p)$ converts a probability into the
corresponding position on the normal curve.

The theorem states that

$$
\lVert\delta\rVert_2<R
\quad\Longrightarrow\quad
g(x+\delta)=c_A.
$$

One probability calculation therefore covers **every** perturbation $\delta$
inside an $\ell_2$ ball.

For the April vote in the figure, take $\sigma=0.25$, $p_A=0.80$, and
$p_B=0.10$. Since

$$
\Phi^{-1}(0.80)\approx0.842,
\qquad
\Phi^{-1}(0.10)\approx-1.282,
$$

the certified radius is

$$
R\approx\frac{0.25}{2}(0.842+1.282)=0.265.
$$

The geometry behind the theorem is a shift of probability mass. An adversarial
perturbation moves the center of the Gaussian cloud. The two normal quantiles
measure how far the center can move before the leading class could lose its
probability advantage. The formal proof uses the Neyman–Pearson lemma to find
the decision region whose probability changes most under that shift.

<figure style="text-align: center;">
  <img src="{{ '/imgs/randomized-smoothing-radius.svg' | relative_url }}" width="880" style="display: block; margin: 0 auto;" alt="A three-stage diagram converts class probabilities 0.90, 0.07, and 0.03 through Gaussian quantiles into a certified radius of approximately 0.345 around April's input.">
  <figcaption>The probability lead is converted into distance by Gaussian quantiles.</figcaption>
</figure>

## Where does probability enter the certificate?

There are two layers of probability, and separating them prevents a common
misreading.

First, Gaussian noise defines the ideal classifier $g$. If its class
probabilities were known exactly, the radius theorem would make a deterministic
statement: every input in the ball receives the same label from $g$.

Second, a computer cannot evaluate the exact probabilities of a modern neural
network. It draws a finite sample of noisy inputs and counts the votes. A
binomial confidence interval turns those counts into a lower bound
$\underline p_A$ and, when needed, an upper bound $\overline p_B$.

The practical certificate therefore says:

> with confidence at least $1-\alpha$, every perturbation inside the reported
> radius preserves the smoothed classifier's label.

The standard certification procedure uses many noisy samples, computes the
confidence bound, and either returns a radius or **abstains**. A narrow vote
margin may identify the winning class while providing insufficient statistical
evidence for a positive radius. Abstention keeps sampling uncertainty inside
the stated guarantee.

## How should the base classifier be trained?

The radius grows when the correct class remains highly probable under Gaussian
noise. Training methods differ in how they create that probability advantage.

| Method | Training signal | Main idea |
| --- | --- | --- |
| Gaussian training | Cross-entropy on $x+\eta$ | Teach the base classifier directly on the noise used at certification time. |
| [SmoothAdv](https://arxiv.org/abs/1906.04584) | Adversarial training against a differentiable approximation of the smoothed classifier | Search for inputs whose noisy vote is difficult, then train on them. |
| [MACER](https://arxiv.org/abs/2001.02378) | A surrogate derived from the certified radius | Increase the probability margin without an inner adversarial attack. |
| [Consistency](https://arxiv.org/abs/2006.04062) | Agreement between predictions on noisy copies | Make the model's output stable across the Gaussian cloud. |
| [SmoothMix](https://arxiv.org/abs/2111.09277) | Mixup along adversarial directions | Calibrate confidence near difficult decision regions. |
| [CAT-RS](https://arxiv.org/abs/2212.09000) | Confidence-aware, sample-dependent losses | Adjust robust training pressure according to noisy accuracy. |

These methods modify training. The certificate is still computed afterward
from noisy class probabilities and the smoothing theorem. This mirrors Part 6:
the training signal and the final evaluation guarantee are separate objects.

## A single average can reward the wrong progress

Each correctly classified input receives a certified radius. A common summary
is the **average certified radius** (ACR): add those radii, using radius zero for
an incorrect input, and divide by the dataset size.

The average hides how the radii are distributed. More subtly, the radius

$$
R=\sigma\Phi^{-1}(p_A)
$$

for the common one-probability certificate is highly nonlinear in $p_A$.
Improving an already easy input can change the radius much more than the same
probability improvement on a hard input.

Take $\sigma=0.5$. Increasing $p_A$ from $0.60$ to $0.61$ changes the ideal
radius from about $0.127$ to $0.140$, a gain of $0.013$. Increasing $p_A$ from
$0.98$ to $0.99$ changes it from about $1.027$ to $1.163$, a gain of $0.136$.
Both probability improvements are $0.01$; the easy input contributes more than
ten times as much radius gain.

<figure style="text-align: center;">
  <img src="{{ '/imgs/acr-easy-sample-bias.svg' | relative_url }}" width="880" style="display: block; margin: 0 auto;" alt="Two equal increases of 0.01 in the leading-class probability are compared. A hard input's certified radius grows by 0.013, while an easy input's radius grows by 0.136 when sigma is 0.5.">
  <figcaption>Equal probability improvements receive very different weight in average certified radius.</figcaption>
</figure>

The paper
[“Average Certified Radius is a Poor Metric for Randomized
Smoothing”](https://arxiv.org/abs/2410.06895) proves stronger results. With a
large enough sampling budget, a classifier that always predicts one class can
obtain arbitrarily large ACR. Under common budgets, ACR is extremely sensitive
to easy samples and can change method rankings when the budget changes. The
study also finds that several training methods with improved ACR reduce noisy
accuracy on hard samples relative to Gaussian training.

A more informative evaluation retains the distribution. Two useful views are:

- **certified accuracy at radius $r$:** the fraction of the dataset that is
  correctly certified at least up to $r$, plotted for many radii;
- **the empirical distribution of $p_A$:** how noisy accuracy is spread across
  easy and difficult inputs.

These curves reveal whether progress reaches many April photographs or mostly
extends radii that were already large.

## Put the probabilistic pipeline together

Randomized smoothing can now be read as one chain:

$$
\text{base classifier}
\longrightarrow \text{Gaussian noisy votes}
\longrightarrow \text{confidence bounds}
\longrightarrow \text{certified radius or abstention}.
$$

The smoothing theorem converts a probability gap into an $\ell_2$ radius.
Finite sampling adds an explicit confidence level. Training shapes the
probability gap, and evaluation should show how the resulting robustness is
distributed across inputs.

Part 9 will adapt two components of this chain. A denoiser will change how the
base classifier sees noisy inputs, and a certified selector will let different
inputs use different noise levels.
