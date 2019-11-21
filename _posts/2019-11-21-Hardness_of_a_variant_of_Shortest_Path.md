---
title: "Hardness of a variant of shortest path problem"
author_profile: true
permalink: /MY_INSIGHTS/2019-11-21-Hardness_of_a_variant_of_Shortest_Path/
date: 2019-11-21
tags: [complexity theory]
mathjax: "true"
header:
    image: "/imgs/thoughts2.jpg"
excerpt: "MY_INSIGHTS, complexity theory"
---

When I was solving one of my homework problem, I found a very fascinating question. This blog aims to setting it down.

First let me state the fine-looking problem. Given a graph with no constraint on the edge weight(as long as it $\in R$), our goal is to find the shortest path in such a manner that the absolute value of the sum of all the weights of edges this path covered is minimized.

$$
\min_{P} |\sum_{w_i \in P} w_i|\\
\text{s.t. $P$ is a path of graph $G$}
$$

Here is the background of this problem. Recently in China and many other parts of the world, shared bikes become more and more popular. However, to maintain bicycle amount each station keeps, public bike monitoring center has to remove or add some bikes to each station. Every day they get a graph of station states(number of bikes they keep now) and a problem station(full or empty) and decide a route to send/remove bikes to/from it. In the meantime, all the station they passed would be adjusted so that extra bikes would be taken and insufficient stations would get enough bikes. It is natural and practical that they neither want to take many bikes from the monitoring center nor collect many bikes. Our problem is how to decide such a route.

Unfortunately, this blog proves that our problem is NP-hard. There are some preliminaries you have to know about this proof.

1. The set division problem. This problem requires to divide a set of positive numbers into two groups so that the sum of each group is exactly hale of the total sum. This problem is proven to be NP-hard.
2. The variant of set division. This problem requires the same but wants the difference of those sums to be as small as possible. Since if we have a polynomial time algorithm to solve this problem, then we would know whether the set division problem is solvable and get a solution if so, this variant is also NP-hard.

Our proof follows to construct a subproblem of the bike problem to be equivalent to the variant of set division problem. Let $W = \frac{1}{2}sum(S)$, where $S = \{a_i \text{ for some }i\}$ is an arbitrary set of positive numbers. Take $w_0 = -W$ to be the weight of the start point and $w_i = a_i$
