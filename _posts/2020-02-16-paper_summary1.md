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

<p style="text-align: center;"><font size='+3'><i>Preliminary</i></font></p>

Neural networks(NNs): a kind of approximation of functions. Its universal approximation property is given in  *Multilayer feedforward networks are universal approximators* by Hornik et al.

Deep neural networks(DNNs): a kind of neural network which is deeper than NNs in early stages. Actually it has no official definition. Be aware that DNNs are only realizable, or precisely, trainable in recent years thanks to the development of computation resources. DNNs have achieved large success in numerous fields which are traditionally seen as privilege of humans, such as image recognition and text understanding.

<p style="text-align: center;"><font size='+3'><i>Intriguing properties of neural networks<br> by Szegedy et al, 2014</i></font></p>


This paper literally is the first to report the existence of adversarial examples. 

It argues that DNNs may not work as expected to encode a non-local generalization of input space. In other words, as people won't notice a small perturbation in the picture, for a small enough $\epsilon$, any samples in the rigion of input space should have the same label, i.e. 

$$DNN(\{x+\epsilon|x\in t\}) = t$$ 

However, this smoothness assumption, as discuss by experiment, does not hold in general.

They formalize the attacker problem as:

$$
\min \|r\|_{2}\\
\text{ subject to }f(x+r)=l\\
x+r \in[0,1]^{m}
$$

As it has highly non-linear constraints, they use a approximation known as **L-BFGS**:

$$
\min c|r|+\operatorname{loss}_{f}(x+r, l)\\
\text{ subject to }x+r \in[0,1]^{m}
$$

They find that the perturbation generated has no human-aware features yet are able to create a new image which is undistinguishable but is misclassified by DNNs. The generated images are called *adversarial examples*. They also find that adversarial examples have intriguing *transferable* property which means adversarial examples generated for a certain DNN can cause misclassification by DNNs with different architectures. They show that a white noise, Gaussian in the paper, can not effectively generate adversarial examples.

They further studied how to certify robustness of DNNs. For a DNN stacked by multiple layers, the output can be written as:

$$\phi(x)=\phi_{K}\left(\phi_{K-1}\left(\ldots \phi_{1}\left(x ; W_{1}\right) ; W_{2}\right) \ldots ; W_{K}\right)$$

where $\phi_i$ are function represented by layer and $W_i$ are weights of layer $i$. Using Lipschitz property, i.e. if

$$\forall x, r,\left\|\phi_{k}\left(x ; W_{k}\right)-\phi_{k}\left(x+r ; W_{k}\right)\right\| \leq L_{k}\|r\|$$

for some constant $L_{k}$, then 

$$\|\phi(x)-\phi(x+r)\| \leq L\|r\|$$

where $L=\prod_{k=1}^{K} L_{k}$. In this way, the change in output is bounded by $L \|r\|$ and we are able to know in what range of $\|r\|$ adversarial examples cannot exist. Unfortunately, they show this lower bound of $\|r\|$ is rather small.

<p style="text-align: center;"><font size='+3'><i>Explaining and Harnessing Adversarial Examples<br> by Goodfellow et al, 2015</i></font></p> 

First they consider a special case: linear classifier, i.e. the classifier get output vector by:

$$\boldsymbol{w}^{\top} \tilde{\boldsymbol{x}}=\boldsymbol{w}^{\top} \boldsymbol{x}+\boldsymbol{w}^{\top} \boldsymbol{\eta}$$

and our aim is to maximize the change in the output vector. Therefore, our problem is:

$$
\max_{\eta} w^T \eta\\
\text{ subject to }\|\eta\|_\infty<\epsilon
$$

The solution(refer to [appendix](https://algebraloveme.github.io/2020-02-16-appendix-for-paper-summary1/)) is $\eta = sign(w_i^T)$,  where $i=\max_{i}\{\|w_i^T\|_1\}$.

They hypothesized that it is the linearity that makes the DNNs vulnerable to adversarial examples. Therefore, follow the linear case, they proposed a new attack method, also known as **FGSM**:

$$\boldsymbol{\eta}=\epsilon \operatorname{sign}\left(\nabla_{\boldsymbol{x}} J(\boldsymbol{\theta}, \boldsymbol{x}, y)\right)$$

Their result shows a small perturbation would fail the classifiers. In this way, they suggest it is the linearity rather than nonlinearity that should be to blame.

As pointed out in the paper, NNs are not supposed to be vulnerable to adversarial examples by nature as they are proven to be universal approximators. In particular, DNNs have more capacity and should be able to learn a more robust representation of functions. Therefore, there must be something wrong with the training algorithm. Following the intuition of adversarial examples, they proposed **adversarial training(AT)**. Basically, AT could be viewed as adding adversarial examples to training data and therefore get a more robust approximation. However, as experimented in last paper(Szegedy 2014), simply train NNs on a joint dataset is not enough to get a robust network.

They realized the intuition by modifying loss function. Specifically, they change the loss to:

$$\bar{J}(\boldsymbol{\theta}, \boldsymbol{x}, y)=\alpha J(\boldsymbol{\theta}, \boldsymbol{x}, y)+(1-\alpha) J\left(\boldsymbol{\theta}, \boldsymbol{x}+\operatorname{\epsilon sign}\left(\nabla_{\boldsymbol{x}} J(\boldsymbol{\theta}, \boldsymbol{x}, y)\right)\right.$$

which is a combination of original part and adversarial part. This methods can be viewed as constantly supply up-to-date adversarial examples to the training dataset. In this way, they even get higher precision in original test set. I should remind readers that it is not guaranteed that AT would increase precision. Actually, as discussed in later works, there is a contradiction between them and we need to trade off. Technically, the precision increasing here might be the contribution of enlarged training data.

AT shows great defense ability. Adversarial rate drops dramatically and AT-trained models are more resistant to transferable adversarial examples. As already shown in last paper, although theoretically adding all data points in the neighborhood should do the same, it is not efficient to train robust models by adding randomly sampled noises. Therefore, AT is pretty useful. Actually, many works focus on AT after that.



<script async src="//busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js">
</script>

<h3 id="busuanzi_container_page_pv" style="align-content: center; color:brown; font: 200">
  Total readers: <span id="busuanzi_value_page_pv"></span>
</h3>
