---
title: "Hardness of a variant of shortest path problem"
author_profile: true
permalink: /MY_INSIGHTS/2019-11-21-Hardness_of_a_variant_of_Shortest_Path/
date: 2019-11-21
tags: [complexity theory]
mathjax: "true"
header:
    image: "/imgs/complexity.jfif"
excerpt: "MY_INSIGHTS, complexity theory"
---

When I was solving one of my homework problem, I found a very fascinating question. This blog aims to setting it down.

First let me state the fine-looking problem. Given a graph with no constraint on the edge weight(as long as it $\in R$), our goal is to find the shortest path in such a manner that the absolute value of the sum of all the weighted edges this path covered is minimized.

$$
\min_{P} |\sum_{w_i \in P} w_i|\\
\text{s.t. $P$ is a path of graph $G$}\\
\text{$P$ starts from a specific vertex $w_0$ to another specific vertex $w_d$}
$$

Here is the background of this problem. Recently in China and many other parts of the world, shared bikes become more and more popular. However, to maintain bicycle amount each station keeps, public bike monitoring center has to remove or add some bikes to each station. Every day they get a graph of station states(number of bikes they keep now) and a problem station(full or empty) and decide a route to send/remove bikes to/from it. In the meantime, all the station they passed would be adjusted so that extra bikes would be taken and stations with insufficient supply would get enough bikes. It is natural and practical that they neither want to take many bikes from the monitoring center nor collect many bikes. Our problem is how to decide such a route.

Unfortunately, this blog proves that our problem is NP-hard. There are some preliminaries you have to know about this proof.

1. The set division problem. This problem requires to divide a set of positive numbers into two subsets so that the sum of each subset is exactly half of the total. This problem is proven to be NP-hard.
2. The variant of set division. This problem requires the same but wants the difference of two subset sums to be as small as possible. Since if we have a polynomial time algorithm to solve this problem, then we would know whether the set division problem is solvable and get a solution if so, this variant is also NP-hard.
3. For the variant of set division, it is equivalent to get the sum of one subset to be as near as possible to the half total sum since it would make the difference smallest.

Our proof follows to construct a subproblem of the bike problem to be equivalent to the variant of set division problem. Let $W = \frac{1}{2}sum(S)$, where $S = \{a_i \text{ for some }i\}$ is an arbitrary set of positive numbers. Take $w_0 = -W$ to be the weight of the start point and $w_i = a_i$ to be other points and those points are all directly connected to each other. Now suppose we have a path given by our solver to the bike problem, then if we take one subset of the whole to be vertexes covered by this solution and traverse all those vertexes by setting them to destination point(only increases time complexity by $N$ times) and get the best one, it solves the variant of set division by *preliminary 3*. And by preliminary 2, it cannot be done if the solver takes polynomial time unless $NP=P$. Thus it completes the proof.

The main idea of the proof comes from my treasured roommate, Runze Wang.

<script async src="//busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js">
</script>

<h3 id="busuanzi_container_page_pv" style="align-content: center; color:brown; font: 200">
  Total readers: <span id="busuanzi_value_page_pv"></span>
</h3>
