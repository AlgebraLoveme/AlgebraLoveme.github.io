---
title: "Appendix for adversarial examples paper summary: part 1"
author_profile: true
permalink: /2020-02-16-appendix-for-paper-summary1/
date: 2020-02-16
tags: [paper summary]
mathjax: "true"
excerpt: "paper summary: part 1"
---

<font size='+2'><i>Solution to the FGSM optimization:</i></font>

$$
\max_{\eta} \|w^T \eta\|_\infty \\
\text{ subject to }\|\eta\|_\infty<\epsilon
$$

*Solution*:

$$\|w^T \eta\|_\infty 
= \max_{i}\{|w_i^T \eta|\} \\
\le \max_{i}\{\|w_i^T\|_1 \|\eta\|_\infty\} 
= \max_{i}\{\epsilon \|w_i^T\|_1\}
$$

Here we use *Holder's inequality*. In particular, when $\eta = sign(w_i^T)$ the equality holds, where $i=\max_{i}\{\|w_i^T\|_1\}$.