---
title: "Why there must exist 2 people that have the same number of friends in a group"
author_profile: true
permalink: /learning_notes/2019-08-25-Why_same_number_of_friends/
date: 2019-08-25
tags: [learning notes, Graph_Theory_Bondy_Murty]
mathjax: "true"
header:
    image: "/imgs/friends.jpeg"
excerpt: "learning notes, Graph_Theory_Bondy_Murty"
---

Here is an interesting phenomenon. In any group of two or more people, there are always
at least two with exactly the same number of friends. What's going on?

First, let's rewrite this problem. We want to represent each individual with a node(or vertex) respectively
 and friendship between two people is denoted by a line(or edge) connecting these vertexes. It is worth
 mentioning that this graph(say $$G$$) is simple, i.e. no loop in the graph. Now the problem
  is: why there always exist 2 nodes that have the same degree in a simple graph.

We prove it by induction. 

Suppose $$|G|=2$$, then either there is a edge connecting the two vertexes or is not.
 In each case, our claim is verified.

Now suppose $$|G|=k$$ for some $$k \in N^+$$, our claim is true. Then in the case $$|G|=k+1$$,
 I will complete the proof by contradiction. If each vertex has different degree and none has degree of zero,
  then those degrees must be $$\{1,2,...,k+1\}$$. Then sum of degrees $$\epsilon=\frac{1}{2}(k+2)(k+1)$$.
  However, $$\epsilon_{max}=\binom{k+1}{2}=\frac{1}{2}(k+1)k$$ which is a complete graph, i.e. there is an edge between each pair of vertexes. A contradiction. If one of vertexes has degree of zero, then we can delete this vertex and the case becomes such that $$|G|=k$$ and none has degree of zero, which is certified by induction assumption.

<script async src="//busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js">
</script>

<h3 id="busuanzi_container_page_pv" style="align-content: center; color:brown; font: 200">
  Total readers: <span id="busuanzi_value_page_pv"></span>
</h3>
