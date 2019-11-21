---
title: "Some thoughts about dimension representation"
author_profile: true
permalink: /MY_INSIGHTS/2019-08-19-Some_thoughts_about_dimension_representation/
date: 2019-08-19
tags: [dimension, data science, encoding]
mathjax: "true"
header:
    image: "/imgs/thoughts.jpg"
excerpt: "MY_INSIGHTS, dimension"
---

It is common to use dimension representation in many fields, especially in Data Science to which I am devoted now. For example, we usually treat a dictionary as a vector of thousands of dimensions. Suppose there is a dictionary $$D$$ consisting of two words, e.g. 'hot' and 'dog'. Following the sequence, 'hot' can be denoted as $$[1,0]$$ while 'dog' represented as $[0,1]$. This is called **one-hot representation** of words. I will dig into memory efficiency of word representation in this blog.

One simple numerical example. Suppose we have a  picture with size $$4\times 4 $$ in terms of pixels. Each pixel takes $$N = 2$$ possible values, e.g. $$\{0,1\}$$. Keep in mind that we can *expand* $$4 \times 4$$ pixel matrix to $$1 \times 16$$ vector. In this example, we can easily figure out an *efficient* way to represent this vector, i.e. a binary sequence of length $$L=16$$(something only consists of 0 and 1). This is exactly what computers do to store this vector. 16 bits will be occupied to store it.

What if each pixel can take $$N=3$$ possible values like $$\{0,1,2\}$$?

In this case, binary sequence will result in capacity waste. To be more specific, consider how many states that occupied bits are able to represent. First, we should know how many bits are used. Computers know pixels by parts, so each pixel is stored respectively though they are arranged adjacent to each other in general. That means one pixel will take two bits since one bit can only represent two states while it has three. Therefore, 32 bits will be occupied. However, if we consider deeper, we will notice 32 bits can actually represent $$4^{16}$$ different states while pictures of this size only has $$3^{16}$$. That is roughly 100 times larger!

Although it seems shocking to know how inefficient our representation is, it is worth emphasizing that in reality we only use 64 bits, an amount we merely notice in modern disks which easily have memory of gigabytes(over 8 billion bits).

As discussed before, we waste almost 99% of capacity when we want to store the vector in this case. Does there exist any other better way to represent this vector? The answer is *Yes*. Let's begin investigating deeper. Above two cases have shown that when $$N\ne 2^k$$ for all $$k$$, significant waste occurs. However, if $$N=2^k$$ for some $$k$$, there is no waste at all!
That is why we only choose $$N=256=2^8$$ for RGB pictures.

Apart from enforcing $$N=2^k$$, other ways can also handle capacity waste. We only discuss **base-N** method, i.e. use base $$N$$ instead of $$2$$. It is trivial in math but rather tricky for computers. Actually we need to convert base-N numbers to base-2 at storage.

Look at $$N=3$$ case again. To simplify, we suppose $$L=2$$, i.e. only two pixels are considered. Say those two pixels take value 1 and 2 respectively. Using base-3, the sequence is 12 which is 5 in base-10 and 101 in base-2. However, if you convert those pixels directly to base-2, you will get 0110(*the first 0 is maintained to specify the first pixel is not 3 but 1*). Thus you save 1 bit(25% storage room) to store it.

Now let's consider a more interesting and tricky problem: **Is there any other way to store the vector using less room?** Unfortunately, it can be proven that no such method exists. In base-N method, room occupied has capacity $$\in (N\times L, 2\times N\times L)$$, resulting in possibly less than one bit waste. To guarantee each picture matches one memory state, no bit can be removed. In fact, suppose we get 'hot' in the first place with dictionary length $$L$$, we get information $$-log_2 {\frac{1}{L}}=log_2 L$$, therefore $$\lceil log_2 L \rceil$$ bits must be used to hold 'hot'. Commonly a dictionary can be really large, so we suppose $$L\approx 2^{15}$$. Then 15 bits is used to represent only one word. How expressive one word is!

Last but not least, I want to point out that not every word has the same probability of occurrence. Usually, *adverbs* contain far less information than *nouns*, e.g. *'dog'* specifies the information more than *'the'*.


<script async src="//busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js">
</script>

<h3 id="busuanzi_container_page_pv" style="align-content: center; color:brown; font: 200">
  Total readers: <span id="busuanzi_value_page_pv"></span>
</h3>
