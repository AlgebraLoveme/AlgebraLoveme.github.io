---
title: "Why Do Simple Bounds Lose Information? Neural Network Certification, Part 4"
series_nav_title: "Why Do Simple Bounds Lose Information?"
author_profile: true
permalink: /2026-08-21-neural-network-certification-4-tighter-relaxations/
date: 2026-08-21
show_initial_release: false
written_by: PIRA
written_at: 2026-08-22
tags: [neural networks, certification, linear relaxation, DeepPoly, CROWN-IBP, abstract interpretation, "Certification Series: 04"]
mathjax: true
toc: true
excerpt: "Triangle recovers relationships that intervals forgot. DeepPoly carries selected linear bounds, while CROWN-IBP trades some information for speed."
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

We can eliminate the final affine layer and write the score difference directly
as $m=0.2+h_1-h_2$. This rewrite is called **last-layer elision**. Treating the
two hidden intervals independently gives

$$
m\geq0.2+0.1-0.4=-0.1.
$$

This lower bound is negative, so IBP returns **unknown**. The calculation
combines two hidden values that cannot occur together. The value $h_1=0.1$
comes from $x_1=x_2=0.3$, whereas $h_2=0.4$ comes from $x_1=0.7$ and
$x_2=0.3$.

Each interval is sound on its own. What is missing is the relationship between
each hidden neuron and April's input.

## Keep the input relationship

To recover that missing dependency, start with the second hidden neuron. IBP
remembers only

$$
0\leq h_2\leq0.4.
$$

The network tells us more:

$$
z_2=x_1-x_2,\quad h_2=\operatorname{ReLU}(z_2).
$$

The value of $h_2$ therefore changes with $x_1-x_2$. Its feasible value remains
tied to the input even though the interval $[0,0.4]$ no longer records that
relationship. The next step is a sound description that retains this dependence
while remaining tractable.

## First repair: enclose an unstable ReLU with three lines

Over April's radius-$0.2$ square,

$$
z_2=x_1-x_2\in[-0.4,0.4].
$$

This interval crosses zero, so the ReLU is unstable: its active phase can change
within the input region. Three lines enclose its graph over the interval:

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
</figure>

The upper line joins the ReLU endpoints $(-0.4,0)$ and $(0.4,0.4)$. Convexity
of ReLU guarantees that the segment between those endpoints stays above its
graph. For any unstable ReLU with $z\in[\ell,u]$ and $\ell<0<u$, the same chord is

$$
\operatorname{ReLU}(z)\leq\frac{u}{u-\ell}(z-\ell).
$$

The two lower lines and the upper chord form the **Triangle relaxation**, the
convex hull of the ReLU graph over its known interval. Every exact ReLU value
lies inside the triangle, so the enclosure is sound. This relaxation appears in
[Formal Verification of Piece-Wise Linear Feed-Forward Neural Networks](https://arxiv.org/abs/1705.01320).

## Let Triangle certify April's larger square

Now apply this enclosure to the full input square. April's first ReLU stays active because

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

The calculation is small because April's network has only one unstable ReLU.
A larger network must carry a triangle for every unstable ReLU, which creates a
scaling question.

## Why does Triangle become expensive?

With many unstable ReLUs, we face two computational choices. We can retain every
hidden variable and solve one growing global linear program, or eliminate
hidden variables so that each bound refers only to earlier variables.

With $k$ unstable ReLUs, retaining them adds $3k$ inequalities, plus the
variables and affine equations for the network. The initial constraint count
grows linearly, but the resulting linear program can become large. Eliminating
a hidden variable instead projects the feasible set, a **polytope** (a region
defined by linear inequalities), onto the remaining variables. This projection
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
inequalities. The choice is therefore between a large global program and
potentially explosive projection. A middle strategy keeps a small, selected set
of linear relationships.

</details>

## Avoid constraint explosion by keeping selected lines

[**DeepPoly**](https://www.sri.inf.ethz.ch/publications/singh2019domain) records
a numerical interval, one affine (linear-plus-constant) lower expression, and
one affine upper expression for each neuron. For an unstable ReLU, it stores
exactly one of Triangle's two lower lines, $h\geq0$ or $h\geq z$, together with
the upper chord.

### Why DeepPoly's constraints do not multiply

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

Each substitution produces one affine expression. DeepPoly keeps a fixed number
of summaries per neuron: one lower expression, one upper expression, and one
interval. An expression may involve many earlier neurons, but the number of
stored expressions does not multiply. DeepPoly therefore avoids constructing
the up to $pq$ pairwise inequalities produced by explicit projection. This
fixed-size summary prevents the projection explosion.

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

This finishes the certificate.

The fixed-size summary controls the number of stored constraints, yet an
unstable ReLU still offers two possible lower lines. DeepPoly decides which one
to retain with its **min-area heuristic**. Both candidates share the same upper
chord, so it compares the area between each candidate and that chord. This area
is a geometric proxy for how much spurious region the relaxation admits. A point
in that region satisfies the relaxed inequalities while falling outside the
exact ReLU graph. Choosing the smaller-area candidate heuristically reduces
this spurious region and preserves more information.

### Optional: How DeepPoly chooses its lower ReLU line

April's certificate needed only the upper bound on $h_2$. Other output
expressions can depend on its lower bound. The following optional derivation
explains the geometric basis of DeepPoly's min-area switch rule.

<details markdown="1">
<summary>Derive DeepPoly's min-area switch rule</summary>

For any unstable ReLU with $z\in[\ell,u]$, every slope
$\lambda\in[0,1]$ gives a sound lower line:

$$
\operatorname{ReLU}(z)\geq\lambda z.
$$

The candidate lower line and the fixed upper chord enclose the shaded
trapezoid below. Its vertical side lengths are the endpoint gaps
$-\lambda\ell$ and $(1-\lambda)u$. The distance between them is $u-\ell$.

<figure class="wide-diagram" style="text-align: center;">
  <div class="wide-diagram__viewport" tabindex="0" role="group" aria-label="Scrollable diagram">
  <img src="{{ '/imgs/deeppoly-min-area.svg' | relative_url }}?v=20260822-2" width="700" style="display: block; margin: 0 auto;" alt="A shaded trapezoid between a DeepPoly lower line and the ReLU upper chord. Its width is u minus ell, and its endpoint gaps are minus lambda ell and one minus lambda times u.">
  </div>
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

At equality, every $\lambda\in[0,1]$ has the same area. The concrete rule above
breaks the tie with $\lambda=0$.

If the interval reaches farther into the negative side, $u<-\ell$, the
flat lower line $0$ leaves less area. If it reaches farther into the positive
side, the diagonal lower line $z$ leaves less area.

| ReLU input interval | $A(0)$ | $A(1)$ | Selected lower line |
| --- | ---: | ---: | --- |
| $[-0.6,0.2]$ | $0.08$ | $0.24$ | $0$ ($\lambda=0$) |
| $[-0.4,0.4]$ | $0.16$ | $0.16$ | Tie. Choose $0$ |
| $[-0.2,0.6]$ | $0.24$ | $0.08$ | $z$ ($\lambda=1$) |

April's interval $[-0.4,0.4]$ is the tie case. DeepPoly's concrete rule chooses
$\lambda=0$. The radius-$0.2$ certificate remains the same because its margin
uses only the upper bound on $h_2$.

</details>

DeepPoly avoids multiplying constraints, yet it still back-substitutes to
tighten intervals for many hidden values. [CROWN-IBP](https://arxiv.org/abs/1906.06316)
reduces this cost by using IBP for hidden intervals and reserving
back-substitution for the final margins.

## Scaling back-substitution with CROWN-IBP

April's certificate required one backward calculation for the final margin.
DeepPoly must also obtain a numerical interval $[\ell,u]$ for each hidden
pre-activation before relaxing its ReLU. The interval identifies whether the
ReLU is stable (always active or always inactive) or unstable, and determines
the upper chord. To tighten such an intermediate interval, DeepPoly treats that
hidden value as a temporary output and back-substitutes its lower and upper
expressions toward the input. The
[GPUPoly analysis of DeepPoly](https://arxiv.org/abs/2007.10868) makes this
all-layer back-substitution cost explicit.

The cost of this all-layer back-substitution grows with the width of the hidden
layers. Bounding every value in a layer of width $n_m$ creates $2n_m$ backward
targets: one lower and one upper bound per value. By comparison, a $C$-class
classifier has only $C-1$ margins against the true class. A feature map with
$64$ channels of size $32\times32$
contains

$$
n_m=64\cdot32\cdot32=65{,}536
$$

hidden values, while a ten-class prediction has nine relevant margins. Carrying
linear expressions backward for every intermediate bound can therefore cost
far more than bounding the final safety questions.

CROWN-IBP uses three steps:

1. Run IBP forward to obtain an interval $[\ell,u]$ for every hidden
   pre-activation.
2. Use those intervals to choose sound linear ReLU relaxations.
3. Run the same sign-directed affine back-substitution used above only for the
   final class margins.

For April's one-hidden-layer network, the IBP pass already obtains the exact
pre-activation intervals $z_1\in[0.1,0.9]$ and $z_2\in[-0.4,0.4]$.
CROWN-IBP therefore builds the same ReLU lines and repeats the margin
calculation above, giving $m\geq0.1$. This matching bound is specific to
April's shallow network, where IBP computes exact intervals for the first
affine layer.

The forward IBP pass is cheap because it carries two numbers per hidden value.
In a deeper network, its intervals may already combine incompatible hidden
extrema and discard their relationships. The final affine back-substitution
pass uses those intervals to construct its ReLU lines and cannot retroactively
tighten them. The result remains sound and can admit more spurious values than
a calculation that tightens every intermediate bound through linear
back-substitution.

This exchange of precision for speed becomes especially useful in
[certified training]({{ '/2026-08-21-neural-network-certification-6-certified-training/' | relative_url }}),
where the bounds must be recomputed after every parameter update.

Triangle, DeepPoly, and CROWN-IBP give the same certificate for April's tiny
network. Triangle retains a joint constraint system. DeepPoly back-substitutes
one sign-selected bound at each step without generating projected pairwise
inequalities. CROWN-IBP obtains hidden intervals with IBP and reserves linear
back-substitution for the final margin.

| Method | Representation | Margin lower bound | Result |
| --- | --- | ---: | --- |
| IBP | Independent intervals | $-0.1$ | Unknown |
| Triangle | Joint linear constraints | $0.1$ | Verified |
| DeepPoly | Selected affine bounds and back-substitution | $0.1$ | Verified |
| CROWN-IBP | IBP hidden intervals and final-margin back-substitution | $0.1$ | Verified |

The methods agree on April's tiny network despite representing reachable
values differently. Why can we trust each positive result?

## Why are all three certificates trustworthy?

The table compares four methods built from three representation ideas: boxes,
joint linear constraints, and selected affine bounds. CROWN-IBP combines IBP
intervals for hidden bounds with affine relaxations for final margins. The
comparison above measures how tightly each representation bounded April's
margin. Every certificate also depends on a shared validity condition: it must
contain every value the exact network can reach.

The allowed inputs form a square. As they pass through a network, the possible
neuron values form new geometric sets. A verifier works with simpler sets that
contain every exact value.

IBP uses boxes. Triangle uses a polytope cut out by linear constraints.
DeepPoly uses intervals together with selected affine bounds. These are
different forms of **abstract interpretation**, a framework for reasoning about
complicated reachable sets through simpler enclosures. They obey the same
safety rule: never discard a value that the network can actually produce.

Soundness makes a positive bound trustworthy. Precision determines whether the
bound becomes positive in the first place. The distinction becomes concrete
when we enlarge April's input region and see DeepPoly remain inconclusive.

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
found an input that violates it. The next remedy is to divide the input square
and analyze each smaller region separately, where a ReLU bound can follow its
graph more closely.

## Tighter relaxations preserve relationships without losing soundness

IBP lost the relationship between April's hidden neurons and returned unknown
at radius $0.2$. Triangle restored that relationship and proved
$m\geq0.1$. After seeing why a full Triangle system becomes expensive,
DeepPoly retained selected affine bounds and recovered the same certificate by
back-substitution, without constructing the facets created by explicit
projection. CROWN-IBP reduced the cost of intermediate bounds by computing them
with IBP, then spent linear back-substitution only on the final margins.

At radius $0.24$, the new lower bound is $-0.02$. Part 5 applies this remedy:
**can splitting the input region turn this unknown into a proof?**
