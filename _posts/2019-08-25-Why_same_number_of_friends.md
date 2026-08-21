---
title: "Why Two People Must Have the Same Number of Friends"
author_profile: true
permalink: /learning_notes/2019-08-25-Why_same_number_of_friends/
date: 2019-08-25
last_modified_at: 2026-08-21
last_modified_by: PIRA
tags: [learning notes, Graph_Theory_Bondy_Murty]
mathjax: "true"
header:
    image: "/imgs/friends-hero-v2.jpg"
excerpt: "A short graph-theoretic proof using the pigeonhole principle."
---

In every group of at least two people, two people must have exactly the same number of friends within the group. Graph theory makes the reason precise.

## Modeling friendship as a graph

Represent each person by a **vertex**, and join two vertices with an **edge** when the corresponding people are friends. We assume that friendship is mutual, so the graph is undirected: an edge between Alice and Bob has no direction.

The graph is also **simple**:

- It has no loops because a person is not counted as their own friend.
- It has no parallel edges because friendship between the same pair of people is counted only once.

The **degree** of a vertex is the number of edges that meet it. In this model, a person's degree is exactly their number of friends within the group. The original claim therefore becomes:

> Why must a simple graph with at least two vertices contain two vertices of the same degree?

## The key observation

Suppose the group contains $n$ people. Each person can have between $0$ and $n-1$ friends, so the possible degrees initially appear to be $0,1,2,\ldots,n-1$.

This list contains $n$ values for $n$ people, so counting alone does not yet force two people to have the same degree. The key is that the two extreme values, $0$ and $n-1$, cannot occur together.

If someone has degree $n-1$, they are friends with every other person, so nobody has degree $0$. Conversely, if someone has degree $0$, nobody can have degree $n-1$.

<figure>
  <a href="{{ '/assets/files/friends-degree-pigeonhole-v2.png' | relative_url }}">
    <img src="{{ '/assets/files/friends-degree-pigeonhole-v2.png' | relative_url }}" alt="An infographic with two five-vertex graphs. The first has an isolated vertex, which rules out degree four. The second has a vertex connected to all four others, which rules out degree zero. Five vertex symbols then point to four degree-value slots.">
  </a>
  <figcaption>For five people, degree $0$ rules out degree $4$, while degree $4$ rules out degree $0$. Either way, only four degree values remain.</figcaption>
</figure>

At least one extreme must therefore be absent. If degree $n-1$ is absent, every degree lies in $\{0,1,\ldots,n-2\}$. If degree $0$ is absent, every degree lies in $\{1,2,\ldots,n-1\}$. Either way, the $n$ people have only $n-1$ possible degree values.

The **pigeonhole principle** says that if more objects are assigned than there are available categories, at least two objects must share a category. Here the people are the objects and their degree values are the categories. Therefore, at least two people must have the same number of friends.
