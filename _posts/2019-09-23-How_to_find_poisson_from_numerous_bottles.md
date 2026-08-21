---
title: "How to Find One Poisoned Bottle with the Fewest Mice"
author_profile: true
permalink: /learning_notes/2019-09-23-How_to_find_poisson_from_numerous_bottles/
date: 2019-09-23
last_modified_at: 2026-08-21
last_modified_by: PIRA
tags: [binary, encoding, dimension, FUN math]
mathjax: "true"
header:
    image: "/imgs/lab-mouse-hero-v2.jpg"
excerpt: "A binary-encoding solution to a one-round identification puzzle."
---

Suppose exactly one of 16 bottles contains poison. You have only one testing round, and the result takes 24 hours: a mouse dies if and only if it drinks from the poisoned bottle. Each mouse may drink samples from any subset of the bottles. What is the smallest number of mice needed to identify the poisoned bottle?

The answer is **four mice**. The key is to treat each mouse as one bit of information.

## Four mice are enough

Number the bottles from $0$ to $15$ and write each number as a four-bit binary string. For example, bottle $0$ is $0000$, bottle $10$ is $1010$, and bottle $15$ is $1111$.

In a four-bit code, the positions from left to right have place values $8$, $4$, $2$, and $1$. To encode a number, express it as a sum of these values: write $1$ for each value used and $0$ for each value not used. For example, $10=8+2$, so its code is $1010$: use $8$, skip $4$, use $2$, and skip $1$.

Assign one mouse to each bit position, read from left to right. Mouse $i$ drinks a sample from every bottle whose bit in position $i$ is $1$. Therefore, bottle $10$, encoded as $1010$, is sampled by mice $1$ and $3$ but not by mice $2$ and $4$.

After 24 hours, record $1$ for each mouse that dies and $0$ for each mouse that survives. If the outcome is $1010$, then mice $1$ and $3$ died, so bottle $10$ must be poisoned. The outcome $0000$ identifies bottle $0$: no mouse sampled it, and the assumption that exactly one bottle is poisoned rules out every other bottle.

<figure>
  <a href="{{ '/assets/files/poison-bottle-binary-v2.png' | relative_url }}">
    <img src="{{ '/assets/files/poison-bottle-binary-v2.png' | relative_url }}" alt="A three-stage infographic. Bottle 10 is encoded as 1010, so mice 1 and 3 receive its sample while mice 2 and 4 do not. The outcome dies, lives, dies, lives produces 1010 and identifies bottle 10.">
  </a>
  <figcaption>Bottle $10$ has code $1010$. The same four-bit pattern determines which mice sample it and, if it is poisoned, which mice die.</figcaption>
</figure>

## Why three mice are not enough

Each mouse has two possible outcomes: it lives or dies. With $m$ mice, there are therefore at most $2^m$ distinct outcome patterns.

Three mice produce only $2^3=8$ patterns, fewer than the 16 bottles. At least two bottles would have to share a pattern, so the result could not distinguish between them. Four mice produce $2^4=16$ patterns, exactly enough to assign one pattern to every bottle.

## The general result

For $N$ bottles, the number of mice must satisfy $2^m\geq N$. The smallest integer that satisfies this inequality is $m=\lceil\log_2 N\rceil$.

The binary construction above reaches this minimum: assign each bottle a distinct $m$-bit code and let the outcome reproduce the code of the poisoned bottle. If $N$ is not a power of two, some of the $2^m$ possible patterns simply remain unused.
