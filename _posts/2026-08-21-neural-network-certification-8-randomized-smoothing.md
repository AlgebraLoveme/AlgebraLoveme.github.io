---
title: "How Can Random Noise Produce a Certificate? Neural Network Certification, Part 8"
series_nav_title: "How Can Random Noise Certify?"
author_profile: true
permalink: /2026-08-21-neural-network-certification-8-randomized-smoothing/
date: 2026-08-21
written_by: PIRA
written_at: 2026-08-22
tags: [neural networks, certification, randomized smoothing, probabilistic methods, "Certification Series: 08"]
mathjax: true
toc: true
excerpt: "Follow noisy copies of April's photo from majority vote to a probabilistic robustness certificate, then examine training and evaluation."
---

## One photograph of April becomes a cloud

Earlier methods tracked every allowed perturbation through every network layer.
Randomized smoothing instead treats a neural network as a black box and
certifies a new classifier built from its noisy votes.

We now leave April's two-class teaching model and let the black-box base
classifier use a richer label set: **Siberian cat**, **tree**, and **other
animal**.

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
coordinate, and $I$ is the identity matrix. The parameter $\sigma$ is the
noise standard deviation: larger $\sigma$ creates a wider cloud around the
original input.

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

<figure class="wide-diagram" style="text-align: center;">
  <div class="wide-diagram__viewport" tabindex="0" role="group" aria-label="Scrollable diagram">
  <img src="{{ '/imgs/april-randomized-smoothing-cloud.svg' | relative_url }}" width="880" style="display: block; margin: 0 auto;" alt="A point representing April is surrounded by Gaussian noisy samples in three base-classifier decision regions. Most samples fall in the Siberian cat region, so the smoothed classifier predicts Siberian cat.">
  </div>
  <figcaption>The base classifier may vary across the cloud; the smoothed classifier returns its most probable label.</figcaption>
</figure>

## A probability gap becomes a certified radius

The 20 dots above illustrate a Gaussian cloud; their visible frequencies are
not probability estimates for certification. For the idealized calculation
below, assume the exact class probabilities admit the bounds $p_A=0.80$ and
$p_B=0.10$. A finite-sample certificate will replace those assumed bounds with
statistical confidence bounds in the next section.

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

An **adversarial input** is $x+\delta$, deliberately chosen subject to a norm
limit. The theorem states that

$$
\lVert\delta\rVert_2<R
\quad\Longrightarrow\quad
g(x+\delta)=c_A.
$$

One probability calculation therefore covers **every** perturbation $\delta$
inside an $\ell_2$ ball: all changes whose total Euclidean length is below
$R$.

Assume pixel coordinates are scaled to $[0,1]$, so $\sigma$ and $R$ use those
normalized units. For this idealized example, take $\sigma=0.25$,
$p_A=0.80$, and $p_B=0.10$. Since

$$
\Phi^{-1}(0.80)\approx0.842,
\qquad
\Phi^{-1}(0.10)\approx-1.282,
$$

the certified radius is

$$
R\approx\frac{0.25}{2}(0.842+1.282)=0.265.
$$

Here is the bridge from a vote gap to a distance. Write
$r=\lVert\delta\rVert_2$. After the Gaussian center moves by $\delta$, the
leading-class probability is at least

$$
\Phi\!\left(\Phi^{-1}(p_A)-\frac r\sigma\right),
$$

while any competitor's probability is at most

$$
\Phi\!\left(\Phi^{-1}(p_B)+\frac r\sigma\right).
$$

The first remains larger whenever
$r<\frac{\sigma}{2}(\Phi^{-1}(p_A)-\Phi^{-1}(p_B))$. The Neyman–Pearson lemma
justifies these worst-case bounds: among decision regions with the stated
original probability, a half-space perpendicular to $\delta$ changes the most
when the Gaussian center shifts.

<figure class="wide-diagram" style="text-align: center;">
  <div class="wide-diagram__viewport" tabindex="0" role="group" aria-label="Scrollable diagram">
  <img src="{{ '/imgs/randomized-smoothing-radius.svg' | relative_url }}" width="880" style="display: block; margin: 0 auto;" alt="A three-stage diagram converts a lower bound p A equals 0.80 and competitor upper bound p B equals 0.10 through Gaussian quantiles into a certified radius of approximately 0.265 around April's input.">
  </div>
  <figcaption>The probability lead is converted into distance by Gaussian quantiles.</figcaption>
</figure>

## Where does probability enter the certificate?

There are two layers of probability, and separating them prevents a common
misreading.

First, Gaussian noise defines the ideal classifier $g$. If its class
probabilities were known exactly, the radius theorem would make a deterministic
statement: every input in the ball receives the same label from $g$.

Second, a computer cannot evaluate the exact probabilities of a modern neural
network. A standard sound procedure separates selection from estimation:

1. use a pilot batch of noisy inputs to choose a candidate class $c_A$;
2. use a fresh, larger batch to compute a one-sided confidence lower bound
   $\underline p_A$ for that class;
3. set $\overline p_B=1-\underline p_A$;
4. return $R=\sigma\Phi^{-1}(\underline p_A)$ when
   $\underline p_A>1/2$, and abstain otherwise.

The shortcut follows because
$\Phi^{-1}(1-p)=-\Phi^{-1}(p)$ in the two-bound formula.

The practical certificate therefore says:

> Over the Monte Carlo sampling, the chance of returning an invalid
> label-radius pair is at most $\alpha$.

The standard certification procedure uses many noisy samples, computes the
confidence bound, and either returns a radius or **abstains**. A narrow vote
margin may identify the winning class while providing insufficient statistical
evidence for a positive radius. Abstention keeps sampling uncertainty inside
the stated guarantee.

## How should the base classifier be trained?

The radius grows when the correct class remains highly probable under Gaussian
noise. Training methods differ in how they create that probability advantage.

Three broad strategies appear repeatedly:

- **Learn from Gaussian noise.** Ordinary Gaussian training teaches $f$ on the
  same noisy inputs used at certification time.
- **Directly enlarge the useful vote or radius margin.** [MACER](https://arxiv.org/abs/2001.02378)
  optimizes a radius-based objective, while [Consistency](https://arxiv.org/abs/2006.04062)
  encourages noisy copies to produce similar predictions.
- **Emphasize difficult or uncertain inputs.** [SmoothAdv](https://arxiv.org/abs/1906.04584)
  searches for perturbations that weaken the noisy vote; [SmoothMix](https://arxiv.org/abs/2111.09277)
  mixes examples along such directions; [CAT-RS](https://arxiv.org/abs/2212.09000)
  adjusts the training pressure using confidence.

These methods modify training. The certificate is still computed afterward
from noisy class probabilities and the smoothing theorem. This mirrors Part 6:
the training signal and the final evaluation guarantee are separate objects.

## A single average can reward the wrong progress

Each correctly classified input receives a certified radius. A common summary
is the **average certified radius** (ACR): add those radii, using radius zero for
an incorrect input, and divide by the dataset size.

The average hides how the radii are distributed. More subtly, the ideal radius

$$
R=\sigma\Phi^{-1}(p_A)
$$

for the common one-probability certificate is highly nonlinear in $p_A$.
Improving an already easy input can change the radius much more than the same
probability improvement on a hard input.

Here $p_A$ means the top-class noisy-vote probability. To isolate the formula's
nonlinearity, ignore sampling for this numerical comparison. Take $\sigma=0.5$.
Increasing $p_A$ from $0.60$ to $0.61$ changes the ideal radius from about
$0.127$ to $0.140$, a gain of $0.013$. Increasing $p_A$ from
$0.98$ to $0.99$ changes it from about $1.027$ to $1.163$, a gain of $0.136$.
Both probability improvements are $0.01$; the easy input contributes more than
ten times as much radius gain.

<figure class="wide-diagram" style="text-align: center;">
  <div class="wide-diagram__viewport" tabindex="0" role="group" aria-label="Scrollable diagram">
  <img src="{{ '/imgs/acr-easy-sample-bias.svg' | relative_url }}" width="880" style="display: block; margin: 0 auto;" alt="Two equal increases of 0.01 in the leading-class probability are compared. A hard input's certified radius grows by 0.013, while an easy input's radius grows by 0.136 when sigma is 0.5.">
  </div>
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

Actual ACR replaces the ideal probabilities in our calculation with confidence
bounds, so it also depends on the sample count and confidence level. The
curves reveal whether progress reaches many inputs, including difficult ones,
or mostly extends radii that were already large.

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
