---
title: "About"
permalink: /about/
mathjax: "true"
header:
    image: "/imgs/main_photo_cc_self.jpg"
---

Hello, Yuhao here! Starting September 2023, I join [SRI lab](https://www.sri.inf.ethz.ch) at ETH Zürich as a PhD student. I got my MSc in Computer Science majoring Machine Intelligence and minoring Theoretical Computer Science at ETH Zürich, and my BSc in Mathematics and Applied Mathematics with a dual degree in Finance at [CKC Honors College](http://ckc.zju.edu.cn/ckcen/_t1906/main.psp), Zhejiang University. I am lucky to work with:
- [Dr. G. Zhou](https://flzhou.weebly.com), who leads me to the fantastic world of macroeconomics and encouraged me during my early stage of research, which benefits me deeply even after I left the field;
- [Dr. S. Ji](https://nesa.zju.edu.cn/webpage/people.html) and [Dr. X. Zhang](https://person.zju.edu.cn/zhangxuhong), who showed me the excitement and challenges of trustworthy artificial intelligence and offered valuable guidance and suggestions for years;
- [Dr. Y. Zhang](https://yangzhangalmo.github.io), who has always been kind and helpful, especially when I feel lost;
- [Dr. F. Yang](https://sml.inf.ethz.ch/group/fannyy/), who welcomed me since my first semester in a foreign country and continues to help;
- [Dr. M. Vechev](https://www.sri.inf.ethz.ch/people/martin), who shares numerous good days and continues to be a good friend.

My favorite formula includes: 

$$e^{\pi i}=-1$$

$$\hat{f}(\xi) = \int_{-\infty}^{\infty}f(x)e^{2\pi i x\xi}dx$$

Find my CV [here](../CV_en.pdf).

Feel free to contact me if you have any questions or interests.

**Working Ethics**

I solemnly swear that I put 120% effort into making the proofs in all my publications, including those I am not the (co-)first author, *correct*, *rigorous* and *readable*.

**Research Interests**

I am interested in making AI generally safe and trustworthy. Meanwhile, I am trying to use the current "unsafe" AI to do good things, e.g., advancing various science domains.

## Publication

Equal contributions are marked by *. All published works are open-sourced (if applicable) on GitHub and the manuscripts are publicly accessible on Arxiv.

### Trustworthy Artificial Intelligence

- Shengpu Wang, **Yuhao Mao**, Yani Zhang, Martin Vechev, [Learning Compact Boolean Networks](https://arxiv.org/abs/2602.05830), preprint
- Ping He, **Yuhao Mao**, Changjiang Li, Lorenzo Cavallaro, Ting Wang, Shouling Ji, [On the Security Risks of ML-based Malware Detection Systems: A Survey](https://arxiv.org/abs/2505.10903), preprint.
- **Yuhao Mao**\*, Yani Zhang\*, Martin Vechev, [On the Expressiveness of Multi-Neuron Convex Relaxations](https://arxiv.org/abs/2410.06816), [The Fourteenth International Conference on Learning Representations](https://iclr.cc/Conferences/2026) (ICLR'26).
- Chenhao Sun, **Yuhao Mao**, Martin Vechev, [Dual Randomized Smoothing: Beyond Global Noise Variance](https://arxiv.org/abs/2512.01782), [The Fourteenth International Conference on Learning Representations](https://iclr.cc/Conferences/2026) (ICLR'26).
- Chenhao Sun\*, **Yuhao Mao**\*, Mark Niklas Müller, Martin Vechev, [Average Certified Radius is a Poor Metric for Randomized Smoothing](http://arxiv.org/abs/2410.06895), [The Forty-Second International Conference on Machine Learning](https://icml.cc/Conferences/2025) (ICML'25).
<span style="display:inline-flex; align-items:center; gap:4px; position:relative; top:-0.1em;">
  <a href="https://github.com/eth-sri/acr-weakness">
    <img src="../assets/github-mark.png" alt="GitHub" style="height:1em;"/>
  </a>
  <a href="../assets/files/ACR_ICML_poster.pdf">
    <img src="../assets/poster-icon.png" alt="Poster" style="height:1em;"/>
  </a>
</span>
<details style="margin:0.05em 0 0.12em 0;padding-left:2.2em;font-size:0.85em;color:#666;">
  <summary style="cursor:pointer;font-style:italic;margin:0;padding:0;">General audience summary</summary>
  <div style="margin:0.08em 0 0;padding:0;color:#555;">
    The commonly used metric to evaluate model robustness can be easily manipulated without improving the robustness. This effect has been introduced into the community. Simple manipulation beats the state-of-the-art on this metric. Better metrics are suggested.
  </div>
</details>
- **Yuhao Mao**, Stefan Balauca, Martin Vechev, [CTBENCH: A Library and Benchmark for Certified Training](https://arxiv.org/abs/2406.04848), [The Forty-Second International Conference on Machine Learning](https://icml.cc/Conferences/2025) (ICML'25).
<span style="display:inline-flex; align-items:center; gap:4px; position:relative; top:-0.1em;">
  <a href="https://github.com/eth-sri/ctbench">
    <img src="../assets/github-mark.png" alt="GitHub" style="height:1em;"/>
  </a>
  <a href="../assets/files/CTBench_ICML_poster.pdf">
    <img src="../assets/poster-icon.png" alt="Poster" style="height:1em;"/>
  </a>
</span>
- Stefan Balauca, Mark Niklas Müller, **Yuhao Mao**, Maximilian Baader, Marc Fischer, Martin Vechev, [Gaussian Loss Smoothing Enables Certified Training with Tight Convex Relaxations](https://arxiv.org/abs/2403.07095), [Transactions on Machine Learning Research 07/2025](https://jmlr.org/tmlr/) (TMLR'25).
<span style="display:inline-flex; align-items:center; gap:4px; position:relative; top:-0.1em;">
  <a href="https://github.com/stefanrzv2000/GLS-Cert-Training">
    <img src="../assets/github-mark.png" alt="GitHub" style="height:1em;"/>
  </a>
</span>
- **Yuhao Mao**, Mark Niklas Müller, Marc Fischer, Martin Vechev, [Understanding Certified Training with Interval Bound Propagation](https://arxiv.org/abs/2306.10426), [The Twelfth International Conference on Learning Representations](https://iclr.cc/Conferences/2024) (ICLR'24).
<span style="display:inline-flex; align-items:center; gap:4px; position:relative; top:-0.1em;">
  <a href="https://github.com/eth-sri/ibp-propagation-tightness">
    <img src="../assets/github-mark.png" alt="GitHub" style="height:1em;"/>
  </a>
  <a href="../assets/files/PI_ICLR_poster.pdf">
    <img src="../assets/poster-icon.png" alt="Poster" style="height:1em;"/>
  </a>
</span>
- Maximilian Baader\*, Mark Niklas Müller\*, **Yuhao Mao**, Martin Vechev, [Expressivity of ReLU-Networks under Convex Relaxations](https://arxiv.org/abs/2311.04015), [The Twelfth International Conference on Learning Representations](https://iclr.cc/Conferences/2024) (ICLR'24).
<span style="display:inline-flex; align-items:center; gap:4px; position:relative; top:-0.1em;">
  <a href="../assets/files/Expressivity_ICLR_poster.pdf">
    <img src="../assets/poster-icon.png" alt="Poster" style="height:1em;"/>
  </a>
</span>
- **Yuhao Mao**, Mark Niklas Müller, Marc Fischer, Martin Vechev, [Connecting Certified and Adversarial Training](https://arxiv.org/abs/2305.04574), [The Thirty-seventh Conference on Neural Information Processing Systems](https://nips.cc/Conferences/2023) (NeurIPS'23).
<span style="display:inline-flex; align-items:center; gap:4px; position:relative; top:-0.1em;">
  <a href="https://github.com/eth-sri/taps">
    <img src="../assets/github-mark.png" alt="GitHub" style="height:1em;"/>
  </a>
  <a href="../assets/files/TAPS_NIPS_poster.pdf">
    <img src="../assets/poster-icon.png" alt="Poster" style="height:1em;"/>
  </a>
</span>
- Yuyou Gan\*, **Yuhao Mao**\*, Xuhong Zhang, Shouling Ji, Yuwen Pu, Meng Han, Jianwei Yin, Ting Wang, [``Is your explanation stable?'': A Robustness Evaluation Framework for Feature Attribution](https://arxiv.org/abs/2209.01782), [ACM SIGSAC Conference on Computer and Communications Security 2022](https://www.sigsac.org/ccs/CCS2022/) (CCS'22).
<span style="display:inline-flex; align-items:center; gap:4px; position:relative; top:-0.1em;">
  <a href="https://github.com/sweet-shark/MeTFA-A-Robustness-Evaluation-Framework-for-Feature-Attribution">
    <img src="../assets/github-mark.png" alt="GitHub" style="height:1em;"/>
  </a>
</span>
- **Yuhao Mao**, Chong Fu, Saizhuo Wang, Shouling Ji, Xuhong Zhang,
Zhenguang Liu, Jun Zhou, Alex X. Liu, Raheem Beyah, Ting Wang, [Transfer Attack Revisited: A Large-Scale Empirical Study in Real Computer Vision Settings](https://arxiv.org/abs/2204.04063), [IEEE Symposium on Security & Privacy 2022](https://www.ieee-security.org/TC/SP2022/program-papers.html) (SP'22).
<span style="display:inline-flex; align-items:center; gap:4px; position:relative; top:-0.1em;">
  <a href="https://github.com/AlgebraLoveme/Transfer-Attacks-Revisited-A-Large-Scale-Empirical-Study-in-Real-Computer-Vision-Settings">
    <img src="../assets/github-mark.png" alt="GitHub" style="height:1em;"/>
  </a>
</span>



### Artificial Intelligence for Science

- Chenhao Chu, **Yuhao Mao**, Hua Wang, [Transfer Learning Assisted Fast Design Migration Over Technology Nodes: A Study on Transformer Matching Network](https://arxiv.org/abs/2502.18636), [IEEE MTT-S International Microwave Symposium 2024](https://ims-ieee.org/welcomeIMS2024) (IMS'24). 
<span style="display:inline-flex; align-items:center; gap:4px; position:relative; top:-0.1em;">
  <a href="https://github.com/ChenhaoChu/RFIC-TL">
    <img src="../assets/github-mark.png" alt="GitHub" style="height:1em;"/>
  </a>
</span>


## Talk

- Training Certifiably Robust Neural Networks. January 2024 at Zhejiang University, China.
 <span style="display:inline-flex; align-items:center; gap:4px; position:relative; top:-0.1em;">
  <a href="../230122_ZJU.pdf">
    <img src="../assets/keynote-icon.png" alt="Slide" style="height:1em;"/>
  </a>
</span>

## Teaching

- [Rigorous Software Engineering](https://www.sri.inf.ethz.ch/teaching/rse2025) (Bachelor's), Spring 2024/2025, ETH Zürich, TA on exercises and lectures.
- [Reliable and Trustworthy Artificial Intelligence](https://www.sri.inf.ethz.ch/teaching/rtai24) (Master's), Fall 2023-2025, ETH Zürich, TA on exercises and projects.
- [Computational Intelligence Lab](https://da.inf.ethz.ch/teaching/2023/CIL/) (Master's), Spring 2023, ETH Zürich, TA on exercises.
- [Introduction to Machine Learning](https://las.inf.ethz.ch/teaching/introml-s23) (Bachelor's), Spring 2023, ETH Zürich, TA on exercises.

## Community Contribution
Review for NeurIPS (since 2024, acknowledged as [Top Reviewers 2024](https://neurips.cc/Conferences/2024/ProgramCommittee#top-reviewers) and [Top Reviewers 2025](https://neurips.cc/Conferences/2025/ProgramCommittee#top-reviewers)), ICLR (since 2025), TMLR (since 2025), ICML (since 2025).

## Learning

I made public some of my cheatsheets, based on standard textbooks and courses provided by ETH Zürich, for personal reference and general interest. Many thanks to the original authors that enlightened me with the great knowledge.

- [Advanced Machine Learning](https://github.com/AlgebraLoveme/AML-cheatsheet/blob/main/main.pdf)
- [Advanced Graph Algorithm and Optimization](https://github.com/AlgebraLoveme/AGAO-cheatsheet/blob/master/main.pdf)
- [Guarantee for Machine Learning](https://github.com/AlgebraLoveme/GML-cheatsheet/blob/master/main.pdf)
- [Information Theory](https://github.com/AlgebraLoveme/InfoTheory-cheatsheet/blob/master/main.pdf)
- [Network Modeling](https://github.com/AlgebraLoveme/NetModel-cheatsheet/blob/master/main.pdf)
- [Natural Language Processing](https://github.com/AlgebraLoveme/NLP-cheatsheet/blob/main/main.pdf)
- [Optimization for Data Science](https://github.com/AlgebraLoveme/ODS-cheatsheet/blob/master/main.pdf)
- [Probablistic Artificial Intelligence](https://github.com/AlgebraLoveme/PAI-cheatsheet/blob/main/main.pdf)
- [Randomized Algorithms and Probabilistic Method](https://github.com/AlgebraLoveme/RandAlgProbMethod-Formulas/blob/master/main.pdf)
- [Reliable and Trustworthy Artificial Intelligence](https://github.com/AlgebraLoveme/RTAI-cheatsheet/blob/main/main.pdf)