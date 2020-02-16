---
title: "Adversarial examples paper summary: part 1"
author_profile: true
permalink: /2020-02-16-paper_summary1/
date: 2020-02-16
tags: [paper summary]
mathjax: "true"
excerpt: "paper summary: part 1"
---

Time flies and over a half year has gone by since I read the first adversarial example paper. Recently, I happen to have to look back at these papers I read and find that only a vague impression remains in my memory. Therefore, I want to record my notes in the blog series. Be noticed that what I write only represents my opinions and everything needs not to be true.

<p style="text-align: center;"><i>Preliminary</i></p>

Neural networks(NNs): a kind of approximation of functions. Its universal approximation property is given in  *Approximation theory of the MLP model in neural networks* by Pinkus.

Deep neural networks(DNNs): a kind of neural network which is deeper than NNs in early stages. Actually it has no official definition. Be aware that DNNs are only realizable, or precisely, trainable in recent years thanks to the development of computation resources. DNNs have achieved large success in numerous fields which are traditionally seen as privilege of humans, such as image recognition and text understanding.

<p style="text-align: center;"><i>Intriguing properties of neural networks<br> by Szegedy et al, 2014</i></p>


This paper literally is the first to report the existence of adversarial examples. 

It argues that DNNs may not work as expected to encode a non-local generalization of input space. 

In other words, as people won't notice a small perturbation in the picture, for a small enough $epsilon$,

 any samples in the rigion of input space should have the same label, i.e. $DNN(\{x+epsilon|x\in t\}) = t$. 

However, this smoothness assumption, as discuss by experiment, does not hold in general.

They formalize the attacker problem as:

$$
\min \|r\|_{2}\text{ subject to:}\\
f(x+r)=l\\
x+r \in[0,1]^{m}
$$

As it has highly non-linear constraints, they use a approximation known as **L-BFGS**:

$$
\min c|r|+\operatorname{loss}_{f}(x+r, l)\text{ subject to:}\\
x+r \in[0,1]^{m}
$$

They find that the perturbation generated has no human-aware features yet are able to create a new image which is undistinguishable but is misclassified by DNNs. The generated images are called *adversarial examples*. They also find that adversarial examples have intriguing *transferable* property which means adversarial examples generated for a certain DNN can cause misclassification by DNNs with different architectures. They show that a white noise, Gaussian in the paper, can not effectively generate adversarial examples.

They further studied how to certify robustness of DNNs. For a DNN stacked by multiple layers, the output can be written as:

$$\phi(x)=\phi_{K}\left(\phi_{K-1}\left(\ldots \phi_{1}\left(x ; W_{1}\right) ; W_{2}\right) \ldots ; W_{K}\right)$$

where $\phi_i$ are function represented by layer and $W_i$ are weights of layer $i$. Using Lipschitz property, i.e. if

$$\forall x, r,\left\|\phi_{k}\left(x ; W_{k}\right)-\phi_{k}\left(x+r ; W_{k}\right)\right\| \leq L_{k}\|r\|$$

for some constant $L_{k}$, then 

$$\|\phi(x)-\phi(x+r)\| \leq L\|r\|$$

where $L=\prod_{k=1}^{K} L_{k}$. In this way, the change in output is bounded by $L \|r\|$ and we are able to know in what range of $\|r\|$ adversarial examples cannot exist. Unfortunately, they show this lower bound of $\|r\|$ is rather small.

<p style="text-align: center;"><i>Explaining and Harnessing Adversarial Examples by Goodfellow et al, 2015</i></p>

First I have to mention Szegedy and Goodfellow are both coauthors of this paper and the last one. Actually they make highly constructive contribution to this area of research.

