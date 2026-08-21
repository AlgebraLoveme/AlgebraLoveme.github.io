---
title: "Testing Is Not Proof: A First Look at Neural Network Certification"
author_profile: true
permalink: /2026-08-21-neural-network-certification-1-what-are-we-proving/
date: 2026-08-21
written_by: PIRA
written_at: 2026-08-21
tags: [neural networks, certification, formal verification, robustness]
mathjax: true
toc: true
excerpt: "A beginner-friendly introduction to what neural network certification proves, why testing is not enough, and how certification connects neural networks to program verification."
---

Neural network certification starts from a familiar idea: testing asks what
happened on chosen inputs, while certification uses mathematical reasoning to
cover **every** input allowed by a precise specification.

That difference matters whenever an average result is not enough. A classifier
may achieve high accuracy on a test set, yet behave unpredictably near one
particular input. A controller may work in thousands of simulations, yet fail on
one sensor configuration that the simulations missed. More testing can improve
our empirical evidence, but it does not turn a universal claim into a proof.

Certification addresses this gap. It does not prove that a neural network is
safe in every possible sense. It proves one stated property, for one stated
model, over one stated set of inputs. Understanding that scope is the first step
toward reading any certification result correctly.

## The question accuracy cannot answer

Suppose an image classifier correctly labels 9,800 of 10,000 test images. Its
test accuracy is 98%. This number answers an important statistical question:
how often did the classifier succeed on this particular sample?

Now choose one image of a handwritten 7. Ask a different question:

> If every pixel changes by at most a small amount, must the classifier still
> predict 7?

The accuracy number cannot answer this question. The 10,000 test images probably
do not include every small modification of the chosen image. Even if we generate
a million modifications, there may be an untested one between two sampled
points.

The two questions therefore need different evidence:

- **Testing** evaluates the network on selected inputs.
- **Certification** establishes a property for all inputs in a specified set.

Neither replaces the other. Testing helps us study typical behavior, find bugs,
and evaluate assumptions about data. Certification covers a sharply defined
worst-case claim that sampling alone cannot establish.

## A certificate is a proof of a scoped claim

A certification problem has three essential parts:

1. **A fixed neural network.** Its architecture, parameters, and supported
   operations determine the function being analyzed.
2. **A set of allowed inputs.** This set describes the cases covered by the
   claim.
3. **A required output property.** This property states what the network must do
   for every allowed input.

We can summarize the task in one sentence:

> For every allowed input, prove that this network satisfies this output
> property.

Each phrase carries weight. Changing the network invalidates a result about the
old network. Enlarging the input set creates a stronger claim. Weakening the
output property makes the claim easier to prove, but potentially less useful.

The word *certificate* is used somewhat broadly in this literature. It often
means that a sound procedure has established the claim, perhaps by computing a
provable bound. In the narrower proof-system sense, a certificate is an artifact
that another checker can validate. A paper or tool should make clear which
meaning it uses.

## A running example: keeping one prediction unchanged

Let the classifier be a function $f$. Given an image $x$, it produces one score
$f_j(x)$ for each class $j$. The classifier chooses the class with the highest
score.

Take a reference image $x_0$ whose predicted class is $y$. We allow each
normalized pixel to change by at most $\epsilon$, while keeping every pixel
between 0 and 1. The allowed set is

$$
S(x_0,\epsilon)
=\left\{x\in[0,1]^d:\left|x_i-(x_0)_i\right|\leq\epsilon
\text{ for every pixel }i\right\}.
$$

Here, $d$ is the number of pixels, including color channels when present. The
desired property is

$$
\text{for every }x\in S(x_0,\epsilon),\qquad
f_y(x)>f_j(x)\quad\text{for every }j\neq y.
$$

In plain language, class $y$ must keep a strictly higher score than every other
class throughout the allowed region. A proof of this statement certifies **local
robustness** around $x_0$ at radius $\epsilon$.

This is already a meaningful guarantee, but notice what it does not say. It does
not cover larger pixel changes, rotations, camera noise, or other transformations
unless the input set includes them. It does not say that $y$ is the correct
label. A classifier can be robustly wrong. It also says nothing about images far
from $x_0$.

## Why testing many inputs is still not a proof

Imagine checking whether a curve stays above zero on an interval. Evaluating the
curve at 100 evenly spaced points may reveal a negative value. If it does, we
have disproved the claim. If all 100 values are positive, however, the curve may
still dip below zero between two samples.

Neural network testing has the same logical limitation. One violating input is
enough to falsify a universal property. Passing a finite test suite is not enough
to prove it.

In the real-valued mathematical model used for verification, the region around
an image contains infinitely many points. A digital implementation uses finite
precision, but the number of possible inputs is still far too large for ordinary
enumeration. A certifier must therefore reason about **sets of inputs at once**
rather than execute the network independently on every point.

This distinction also explains why an unsuccessful adversarial attack is not a
certificate. An attack searches for a counterexample. If it finds one, the
property is false. If it does not, we only know that this particular search did
not find one.

## The bridge to program verification

During inference, a fixed neural network is a numerical program. It applies a
known sequence of operations, such as matrix multiplication, addition, and
nonlinear activation, to an input. This lets us borrow the central idea of
program verification: specify what may enter the program and what must be true
when it finishes.

Program verification calls these two statements a **precondition** and a
**postcondition**:

- The precondition $P(x)$ describes the allowed inputs.
- The postcondition $Q(f(x))$ describes the required outputs.

The verification claim is

$$
\text{for every }x,\qquad P(x)\Longrightarrow Q(f(x)).
$$

For our image example, the precondition says that $x$ lies in
$S(x_0,\epsilon)$. The postcondition says that class $y$ has a higher score than
every competing class.

There is another useful way to read the same claim. The property is verified
exactly when there is **no** input that satisfies the precondition and violates
the postcondition. A verifier can therefore try to rule out all counterexamples.
Solver-based methods such as
[Reluplex](https://arxiv.org/abs/1702.01135) follow this perspective and can
either prove supported properties or produce counterexamples. Bound-based
methods instead prove that a violation cannot occur by enclosing all possible
network outputs. For example,
[Fast-Lin and Fast-Lip](https://proceedings.mlr.press/v80/weng18a.html) compute
certified lower bounds on the size of a perturbation needed to change a ReLU
network's decision.

## What answers can a verifier give?

A verification run may end in three practically important ways:

- **Verified.** The method proves that the stated property holds throughout the
  allowed input set.
- **Falsified.** The method produces a valid input that violates the property.
- **Unknown or unresolved.** The method cannot establish either conclusion. Its
  approximation may be too loose, it may run out of time or memory, or it may not
  support part of the model.

A trustworthy *verified* result requires **soundness**. A sound method does not
certify a false property, provided that its mathematical and numerical
assumptions match the system being analyzed. Soundness does not mean the method
can prove every true property. Some sound methods deliberately return unknown
when their inexpensive reasoning is inconclusive.

It is therefore wrong to interpret unknown as unsafe. The network may violate
the property, or the property may be true but difficult for that method to
prove. Later posts will show why this happens and how tighter reasoning or search
can resolve some unknown cases.

## What the guarantee does not cover

A formal proof can be mathematically correct and still answer the wrong practical
question. Before treating a certificate as evidence about a deployed system,
check its boundary:

- **Specification.** Does the formal property capture the behavior we actually
  care about?
- **Input model.** Does the allowed set include the realistic changes and
  disturbances we expect?
- **System boundary.** Does the verified model include preprocessing,
  normalization, control logic, and other relevant components?
- **Model identity.** Are the deployed architecture, parameters, and operations
  exactly those that were verified?
- **Numerical assumptions.** Does the implementation preserve the arithmetic
  assumptions used by the verifier?

Certification is not a synonym for safety. It is evidence for one link in a
larger safety or reliability argument. Its value depends on both the correctness
of the proof and the relevance of the claim being proved.

## A checklist for reading certification claims

When a paper, tool, or product says that a neural network is certified, ask:

1. **Which exact model is covered?**
2. **Which inputs does the guarantee quantify over?**
3. **Which output property is proved?**
4. **What does the method mean by verified, falsified, and unknown?**
5. **Which assumptions and system components remain outside the proof?**

If these questions have no clear answers, the word *certified* does not yet tell
us enough to judge the result.

## Where the series goes next

This post established the central question. The rest of the series will build
the answer in small steps:

1. **Writing the guarantee:** turn an informal goal into input and output
   specifications.
2. **Proof by propagating bounds:** use interval arithmetic to reason about a
   whole input region.
3. **Tighter bounds with relaxations:** preserve more information with linear
   bounds and abstract domains.
4. **Search for a complete answer:** combine bounds with splitting,
   branch-and-bound, and solver-based reasoning.
5. **Training models to be certifiable:** make provable robustness part of the
   learning objective.
6. **Reading results critically:** compare certified models and verifiers under
   matched assumptions.

## Takeaway

Neural network certification replaces “we tried many cases” with a scoped
mathematical statement about **every input in a defined set**. The guarantee is
only as broad as its specification, but within that boundary it can say
something testing alone cannot.
