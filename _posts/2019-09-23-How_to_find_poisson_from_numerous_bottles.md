---
title: "How to find poisson from some bottles using minimal lab mice"
author_profile: true
permalink: /learning_notes/2019-09-23-How_to_find_poisson_from_numerous_bottles/
date: 2019-09-23
tags: [binary, encoding, dimension, FUN math]
mathjax: "true"
header:
    image: "/imgs/lab_mouse.jpeg"
excerpt: "binary, encoding, dimension, FUN math"
---

Here is an interesting but not straightforward question. Suppose there are 1000 bottles of liquid. One of them is poisonous while others are normal water. You have some mice in hand and the task is to find poison in 24 hours using these mice. However, you can only tell whether a mouse drank poison after 24 hours. Now, how many mice do you have to use to find the poison?

It is not simple to most of people, if you don't have the insight. Let me state the result here: **If you have $$N$$ bottles, you need $$\log_2 N$$ mice at least.**

But why?
