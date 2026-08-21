---
title: "How Many Bits Does a Discrete Vector Need?"
author_profile: true
permalink: /MY_INSIGHTS/2019-08-19-Some_thoughts_about_dimension_representation/
date: 2019-08-19
last_modified_at: 2026-08-21
last_modified_by: PIRA
tags: [information theory, encoding, data representation]
mathjax: true
header:
    image: "/imgs/discrete-vector-encoding-hero.jpg"
excerpt: "A counting argument reveals the minimum storage required for categorical vectors and images."
---

A categorical value is often represented as a vector. If a vocabulary contains only “hot” and “dog,” for example, their one-hot vectors are $[1,0]$ and $[0,1]$. This representation is convenient for computation, but it is not necessarily a compact way to store the underlying value.

The storage question is simpler: **how many bits are required to distinguish every possible vector without losing information?** A counting argument gives the answer.

## Binary pixels: no wasted states

Consider a $4\times4$ image whose pixels are either $0$ or $1$. Flattening the image produces a vector of length $L=16$. Because each pixel has two possible values, one bit per pixel is sufficient, for a total of $16$ bits.

There are $2^{16}$ possible images, and $16$ bits also have exactly $2^{16}$ possible patterns. Every bit pattern can therefore represent one image, with no unused patterns.

## Ternary pixels: independent storage wastes space

Now suppose each pixel can be $0$, $1$, or $2$. If we encode every pixel separately, each one needs two bits: one bit distinguishes only two values, while two bits distinguish four. The $16$ pixels then occupy $32$ bits.

That representation offers $2^{32}=4^{16}$ bit patterns, but the image has only $3^{16}$ possible states. Most of the available patterns are never used because each two-bit pixel code leaves one of its four patterns unused.

We can avoid most of this waste by encoding the entire vector as one block. Treat the pixel sequence as a base-$3$ number, convert that number to binary, and store the result. Since there are $3^{16}$ possible vectors, the block needs only $\lceil\log_2 3^{16}\rceil=26$ bits rather than $32$.

For a smaller example, consider the ternary vector $[1,2,0]$. It is the base-$3$ numeral $120$, whose decimal value is $15$. All $3^3=27$ ternary vectors fit into a fixed five-bit block, so this vector is stored as $01111$. Encoding the three entries independently would use six bits: $01$, $10$, and $00$.

## The general lower bound

Suppose a vector has length $L$ and each coordinate can take one of $N$ values. The number of possible vectors is $N^L$. A code using $b$ bits has only $2^b$ distinct patterns, so a lossless encoding requires $2^b\geq N^L$. Equivalently, it requires at least $b=\lceil L\log_2 N\rceil$ bits.

This bound follows from the pigeonhole principle. If fewer bit patterns than vectors were available, at least two vectors would share a code, and decoding could not distinguish them. Encoding the whole vector as a base-$N$ number reaches the bound, apart from the fraction of a bit introduced by rounding upward.

The two examples fit the same formula:

| Values per coordinate | Vector length | Independent fixed-width code | Block lower bound |
|---:|---:|---:|---:|
| $N=2$ | $L=16$ | $16$ bits | $16$ bits |
| $N=3$ | $L=16$ | $32$ bits | $26$ bits |

## One-hot vectors are computational representations

The same distinction applies to words. A dense one-hot vector for a vocabulary of size $V$ contains $V$ coordinates, but only one coordinate is nonzero. To store the word identity, we need only store the position of that nonzero entry, which takes $\lceil\log_2 V\rceil$ bits.

For $V=2^{15}$ words, the index needs $15$ bits, whereas a dense one-hot vector contains $32{,}768$ binary entries. One-hot vectors remain useful for computation because their shape exposes the category to linear-algebra operations. Software can still store the category as a compact index and materialize the vector only when an operation needs it.

## When symbols are not equally likely

The counting bound above assumes a fixed-length code that must represent every vector. If some symbols occur much more often than others, a variable-length code can assign shorter codes to frequent symbols and longer codes to rare ones.

For a symbol with probability $p(x)$, its information content is $-\log_2 p(x)$ bits. Averaging over the distribution gives the entropy $H(X)=-\sum_x p(x)\log_2 p(x)$, the fundamental target rate for lossless compression over long sequences. This is the central insight of [Shannon's source-coding theory](https://doi.org/10.1002/j.1538-7305.1948.tb01338.x).

The main lesson is therefore not that vectors must be stored coordinate by coordinate. Storage depends on how many states must be distinguished and, when probabilities are available, how frequently those states occur.
