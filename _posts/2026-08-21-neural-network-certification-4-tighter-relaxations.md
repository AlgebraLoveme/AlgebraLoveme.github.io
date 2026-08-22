---
title: "Why Do Simple Bounds Lose Information? Neural Network Certification, Part 4"
author_profile: true
permalink: /2026-08-21-neural-network-certification-4-tighter-relaxations/
date: 2026-08-21
written_by: PIRA
written_at: 2026-08-22
tags: [neural networks, certification, linear relaxation, DeepPoly, abstract interpretation]
mathjax: true
toc: true
excerpt: "Triangle first recovers a relationship that intervals forgot; DeepPoly then carries useful linear bounds without a global constraint system."
---

## Why did IBP's margin bound become negative?

In [Part 3]({{ '/2026-08-21-neural-network-certification-3-interval-bound-propagation/' | relative_url }}),
interval bound propagation followed an entire input square through April the
Siberian cat's tiny classifier. At radius $0.2$,

$$
x_1,x_2\in[0.3,0.7].
$$

Recall that $z_i$ is the input to ReLU $i$, while
$h_i=\operatorname{ReLU}(z_i)=\max(0,z_i)$ is its output. IBP found

$$
h_1\in[0.1,0.9],\quad h_2\in[0,0.4].
$$

Combining the final layer with the score difference---a rewrite called
**last-layer elision**---gives the margin $m=0.2+h_1-h_2$. Treating the two
hidden intervals independently gives

$$
m\geq0.2+0.1-0.4=-0.1.
$$

This lower bound is negative, so IBP returns **unknown**. But the calculation
combines two hidden values that cannot occur together. The value $h_1=0.1$
comes from $x_1=x_2=0.3$, whereas $h_2=0.4$ comes from $x_1=0.7$ and
$x_2=0.3$.

Neither interval is wrong. The missing information is the relationship between
each hidden neuron and April's input.

## Keep the input relationship

For the second hidden neuron, IBP remembers only

$$
0\leq h_2\leq0.4.
$$

The network tells us more:

$$
z_2=x_1-x_2,\quad h_2=\operatorname{ReLU}(z_2).
$$

The value of $h_2$ therefore changes with $x_1-x_2$; it is not free to move
independently inside $[0,0.4]$. We need a sound description that keeps some of
this relationship.

## First repair: enclose ReLU with Triangle

Over April's radius-$0.2$ square,

$$
z_2=x_1-x_2\in[-0.4,0.4].
$$

This interval crosses zero, so the ReLU is unstable. Three lines enclose its
graph over the interval:

$$
\begin{aligned}
h_2&\geq0, & h_2&\geq z_2,\\
h_2&\leq\frac{1}{2}z_2+0.2.
\end{aligned}
$$

<figure class="wide-diagram" style="text-align: center;">
  <div class="wide-diagram__viewport" tabindex="0" role="group" aria-label="Scrollable diagram">
  <img src="{{ '/imgs/relu-linear-relaxation.svg' | relative_url }}" width="640" style="display: block; margin: 0 auto;" alt="The ReLU graph between minus 0.4 and 0.4 enclosed by two lower lines and an upper line, forming a shaded triangular region.">
  </div>
  <figcaption>Together, the blue upper line and the black ReLU branches form the shaded enclosure.</figcaption>
</figure>

The upper line joins the ReLU endpoints $(-0.4,0)$ and $(0.4,0.4)$. Because
ReLU is convex, the segment between those endpoints stays above its graph. For
any unstable ReLU with $z\in[\ell,u]$ and $\ell<0<u$, the same chord is

$$
\operatorname{ReLU}(z)\leq\frac{u}{u-\ell}(z-\ell).
$$

The two lower lines and the upper chord form the **Triangle relaxation**: the
convex hull of the ReLU graph over its known interval. Every exact ReLU value
lies inside the triangle, so the enclosure is sound. This relaxation appears
in
[Formal Verification of Piece-Wise Linear Feed-Forward Neural Networks](https://arxiv.org/abs/1705.01320).

## Let Triangle certify April's larger square

April's first ReLU stays active because

$$
z_1=x_1+x_2-0.5\in[0.1,0.9].
$$

It therefore keeps the exact relationship

$$
h_1=x_1+x_2-0.5.
$$

To find the smallest margin, the Triangle calculation keeps the input box, the
network equations, and all three constraints on $h_2$. Since
$m=0.2+h_1-h_2$ subtracts $h_2$, the smallest margin uses the upper face of
the triangle:

$$
h_2\leq\frac{1}{2}z_2+0.2
      =\frac{1}{2}(x_1-x_2)+0.2.
$$

Substitute both hidden-neuron relationships into the margin:

$$
\begin{aligned}
m
&\geq0.2+(x_1+x_2-0.5)
       -\left(\frac{1}{2}(x_1-x_2)+0.2\right)\\
&=\frac{1}{2}x_1+\frac{3}{2}x_2-0.5.
\end{aligned}
$$

Both coefficients are positive, so the minimum over
$x_1,x_2\in[0.3,0.7]$ occurs at $x_1=x_2=0.3$:

$$
m\geq\frac{1}{2}(0.3)+\frac{3}{2}(0.3)-0.5=0.1.
$$

The lower bound is positive. Triangle has turned IBP's unknown into a
certificate for the radius-$0.2$ square.

## Why does Triangle become expensive?

For April, one triangle is easy to carry. A modern network may contain
thousands of unstable ReLUs. Triangle then leaves us two computational choices.
We can retain every hidden variable and solve one growing global linear
program, or eliminate hidden variables so that each bound refers only to
earlier variables.

With $k$ unstable ReLUs, retaining them adds $3k$ inequalities, plus the
variables and affine equations for the network. The initial constraint count
grows linearly, but the resulting linear program can become large. Eliminating
a hidden variable instead projects the feasible region cut out by the
inequalities---a **polytope**---onto the remaining variables. This projection
can multiply constraints.

<details markdown="1">
<summary>Why can eliminating one variable multiply constraints?</summary>

Consider four inequalities involving the same hidden value:

$$
\begin{aligned}
h&\geq x, & h&\geq0,\\
h&\leq y, & h&\leq1-y.
\end{aligned}
$$

To remove $h$, every lower bound must be no larger than every upper bound.
Pairing the two lower bounds with the two upper bounds gives

$$
\begin{aligned}
x&\leq y, & x&\leq1-y,\\
0&\leq y, & 0&\leq1-y.
\end{aligned}
$$

In general, eliminating a variable with $p$ lower bounds and $q$ upper bounds
can generate $pq$ constraints:

| Lower $p$ | Upper $q$ | Before: $p+q$ | After: up to $pq$ |
| ---: | ---: | ---: | ---: |
| $2$ | $2$ | $4$ | $4$ |
| $4$ | $4$ | $8$ | $16$ |
| $16$ | $16$ | $32$ | $256$ |
| $100$ | $100$ | $200$ | $10{,}000$ |

In a worst case where all generated constraints remain relevant, one projection
can turn four lower and four upper bounds into $16$ constraints. If the next
hidden variable appears in $16$ lower and $16$ upper bounds, the next
projection can generate $256$. Repeated multiplication creates the explosion.

This pairwise operation is called **Fourier–Motzkin elimination**. Retaining
all hidden variables avoids the projection explosion but leaves a large global
linear program. Explicitly eliminating them can generate many pairwise
inequalities. We now have a reason to keep only selected linear relationships.

</details>

## Keep selected lines with DeepPoly

**DeepPoly** records a numerical interval, one affine (linear-plus-constant)
lower expression, and one affine upper expression for each neuron. For an
unstable ReLU, it keeps the upper chord and one of Triangle's two lower lines:
$h\geq0$ or $h\geq z$.

To compare those two choices, place them inside the sound family

$$
\lambda z_2\leq h_2,
\qquad 0\leq\lambda\leq1.
$$

The two lines that DeepPoly considers are the endpoints: $\lambda=0$ gives
$h_2\geq0$, and $\lambda=1$ gives $h_2\geq z_2$. The values between them make
the selection rule easy to derive. DeepPoly stores only the selected endpoint.

All of these lower lines are sound, but they do not give equally tight
enclosures. Because they share the same upper chord, DeepPoly measures the area
between each lower line and that chord. A smaller area admits fewer points that
lie inside the relaxation but not on the exact ReLU graph, so it preserves more
information. DeepPoly chooses the endpoint with the smaller area; this is its
**min-area heuristic**. We will derive the concrete choice after seeing
back-substitution.

### Why the constraints do not multiply

Suppose DeepPoly has summarized a hidden value $h$ with two affine expressions:

$$
L_h(x)\leq h\leq U_h(x).
$$

Let the expression being lower-bounded contain the term $c h$. The sign of $c$
determines the one bound we need:

$$
c h\geq
\begin{cases}
cL_h(x), & c\geq0,\\
cU_h(x), & c<0.
\end{cases}
$$

For a positive coefficient, the smallest value uses the lower expression. For
a negative coefficient, multiplication reverses the inequality, so the
smallest value uses the upper expression. DeepPoly makes one sign-directed
substitution and avoids pairing every lower constraint with every upper
constraint.

Crucially, each substitution produces one affine expression, not a family of
pairwise constraints. DeepPoly keeps a fixed number of summaries per neuron:
one lower expression, one upper expression, and one interval. An expression
may involve many earlier neurons, but the number of stored expressions does
not multiply. DeepPoly never constructs the up to $pq$ pairwise inequalities
produced by explicit projection. This is how it avoids the projection
explosion.

DeepPoly applies the sign rule to the current margin expression, then repeats
the substitution backward until only input variables remain. This procedure
is **back-substitution**. For April's margin, the coefficient of $h_2$ is $-1$,
so the rule selects the upper bound on $h_2$:

$$
\begin{aligned}
m&=0.2+h_1-h_2\\
&\geq0.2+h_1-\left(\frac{1}{2}z_2+0.2\right)\\
&=h_1-\frac{1}{2}z_2\\
&=(x_1+x_2-0.5)-\frac{1}{2}(x_1-x_2)\\
&=\frac{1}{2}x_1+\frac{3}{2}x_2-0.5.
\end{aligned}
$$

Both input coefficients are positive. Using $x_1,x_2\geq0.3$ therefore gives

$$
m\geq\frac{1}{2}(0.3)+\frac{3}{2}(0.3)-0.5=0.1.
$$

This finishes the certificate. The lower-line rule is useful for other output
expressions, so its geometric derivation remains available below as an
optional deeper step.

<details markdown="1">
<summary>Why does the min-area rule select only 0 or 1?</summary>

We postponed the min-area calculation because April's certificate needed only
the upper bound on $h_2$. A different margin can depend on its lower bound, so
we now derive how DeepPoly chooses between $h_2\geq0$ and $h_2\geq z_2$.

For any unstable ReLU with $z\in[\ell,u]$, every slope
$\lambda\in[0,1]$ gives a sound lower line:

$$
\operatorname{ReLU}(z)\geq\lambda z.
$$

The candidate lower line and the fixed upper chord enclose the shaded
trapezoid below. Its vertical side lengths are the endpoint gaps
$-\lambda\ell$ and $(1-\lambda)u$; the distance between them is $u-\ell$.

<figure class="wide-diagram" style="text-align: center;">
  <div class="wide-diagram__viewport" tabindex="0" role="group" aria-label="Scrollable diagram">
  <img src="{{ '/imgs/deeppoly-min-area.svg' | relative_url }}?v=20260822-2" width="700" style="display: block; margin: 0 auto;" alt="A shaded trapezoid between a DeepPoly lower line and the ReLU upper chord. Its width is u minus ell, and its endpoint gaps are minus lambda ell and one minus lambda times u.">
  </div>
  <figcaption>The continuous family makes the area calculable; DeepPoly selects between its two endpoint lines.</figcaption>
</figure>

The area of a trapezoid is its width times the average of its two parallel side
lengths. Therefore,

$$
\begin{aligned}
A(\lambda)
&=\frac{1}{2}(u-\ell)
  \bigl[-\lambda\ell+(1-\lambda)u\bigr]\\
&=\frac{1}{2}(u-\ell)\bigl[u-\lambda(u+\ell)\bigr].
\end{aligned}
$$

As a function of $\lambda$, $A$ has derivative

$$
\frac{dA}{d\lambda}
=-\frac{1}{2}(u-\ell)(u+\ell).
$$

Because $u-\ell>0$, the area increases with $\lambda$ when $u<-\ell$ and
decreases when $u>-\ell$. When $u=-\ell$, the area is constant. No interior
value of $\lambda$ can be strictly better, so DeepPoly only needs to compare
$\lambda=0$ and $\lambda=1$:

$$
A(0)=\frac{1}{2}u(u-\ell),\qquad
A(1)=\frac{1}{2}(-\ell)(u-\ell).
$$

The resulting switch rule is

$$
\lambda^\star=
\begin{cases}
0, & u\leq-\ell,\\
1, & u>-\ell.
\end{cases}
$$

At equality, every $\lambda\in[0,1]$ has the same area; the concrete rule above
breaks the tie with $\lambda=0$.

If the interval reaches farther into the negative side, $u<-\ell$, the
flat lower line $0$ leaves less area. If it reaches farther into the positive
side, the diagonal lower line $z$ leaves less area.

| ReLU input interval | $A(0)$ | $A(1)$ | Selected lower line |
| --- | ---: | ---: | --- |
| $[-0.6,0.2]$ | $0.08$ | $0.24$ | $0$ ($\lambda=0$) |
| $[-0.4,0.4]$ | $0.16$ | $0.16$ | Tie; choose $0$ |
| $[-0.2,0.6]$ | $0.24$ | $0.08$ | $z$ ($\lambda=1$) |

April's interval $[-0.4,0.4]$ is the tie case. DeepPoly's concrete rule chooses
$\lambda=0$. The radius-$0.2$ certificate remains the same because its margin
uses only the upper bound on $h_2$.

</details>

Triangle and DeepPoly give the same certificate for April's tiny network. The
difference is how they organize the calculation: Triangle retains a joint
constraint system, while DeepPoly back-substitutes one sign-selected bound at
each step without generating projected pairwise inequalities. DeepPoly was
introduced in
[An Abstract Domain for Certifying Neural Networks](https://www.sri.inf.ethz.ch/publications/singh2019domain).

| Method | Representation | Margin lower bound | Result |
| --- | --- | ---: | --- |
| IBP | Independent intervals | $-0.1$ | Unknown |
| Triangle | Joint linear constraints | $0.1$ | Verified |
| DeepPoly | Selected affine bounds and back-substitution | $0.1$ | Verified |

## Three abstractions, one safety rule

The allowed inputs form a square. As they pass through a network, the possible
neuron values form new geometric sets. A verifier works with simpler sets that
contain every exact value.

IBP uses boxes. Triangle uses a polytope cut out by linear constraints.
DeepPoly uses intervals together with selected affine bounds. These are
different forms of **abstract interpretation**, but they obey the same safety
rule: never discard a value that the network can actually produce.

## What should we do if the bound is inconclusive?

Increase the radius from $0.2$ to $0.24$. Now

$$
x_1,x_2\in[0.26,0.74],\quad z_2\in[-0.48,0.48].
$$

The DeepPoly upper line becomes

$$
h_2\leq\frac{1}{2}z_2+0.24.
$$

The first ReLU remains active because
$z_1=x_1+x_2-0.5\in[0.02,0.98]$. Back-substitution gives

$$
\begin{aligned}
m
&\geq\frac{1}{2}x_1+\frac{3}{2}x_2-0.54\\
&\geq\frac{1}{2}(0.26)+\frac{3}{2}(0.26)-0.54\\
&=-0.02.
\end{aligned}
$$

The DeepPoly bound is inconclusive. It has neither proved the property nor
found an input that violates it.

We can now divide the input square into smaller regions and analyze each one
separately. A ReLU bound fitted to a smaller region can follow its graph more
closely.

## Takeaway

IBP lost the relationship between April's hidden neurons and returned unknown
at radius $0.2$. Triangle restored that relationship and proved
$m\geq0.1$. After seeing why a full Triangle system becomes expensive,
DeepPoly retained selected affine bounds and recovered the same certificate by
back-substitution, without constructing the facets created by explicit
projection.

At radius $0.24$, the new lower bound is $-0.02$. Part 5 asks: **can splitting
the input region turn this unknown into a proof?**
