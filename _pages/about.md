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
<details style="margin:0.05em 0 0.12em 0;padding-left:2.2em;font-size:0.85em;color:#666;">
  <summary style="cursor:pointer;font-style:italic;margin:0;padding:0;">General audience summary</summary>
  <div style="margin:0.08em 0 0;padding:0;color:#555;">
We examine fundamental limits of a popular family of techniques (''convex relaxations'') used to prove that neural networks behave reliably under small input changes. These techniques rely on simplifying a complex, nonlinear model into a convex approximation that is easier to analyze. We show that even very powerful versions of these approximations—those that reason about many neurons together—can still fail to prove certain cases, no matter how much computational effort is invested. We then identify two principled ways to overcome this limitation: either by restructuring the network in a mathematically equivalent way, or by breaking the input space into smaller regions that can be analyzed more precisely. Our results clarify both the strengths and the inherent limitations of these verification methods, and point to more reliable directions for future robustness analysis.
  </div>
</details>
- Chenhao Sun, **Yuhao Mao**, Martin Vechev, [Dual Randomized Smoothing: Beyond Global Noise Variance](https://arxiv.org/abs/2512.01782), [The Fourteenth International Conference on Learning Representations](https://iclr.cc/Conferences/2026) (ICLR'26).
<details style="margin:0.05em 0 0.12em 0;padding-left:2.2em;font-size:0.85em;color:#666;">
  <summary style="cursor:pointer;font-style:italic;margin:0;padding:0;">General audience summary</summary>
  <div style="margin:0.08em 0 0;padding:0;color:#555;">
We improve a popular way to give provable robustness guarantees for neural networks that works by adding random noise to an input and checking whether the prediction stays the same. The standard approach uses noise from one fixed Gaussian distribution for every input, but a single fixed choice cannot work well across all situations: some cases need little noise to keep predictions accurate, while others benefit from more noise to obtain stronger guarantees. The key idea is to let another model choose the Gaussian noise level for each input, while still keeping the guarantee valid by requiring that this chosen noise level does not change within the neighborhood where the guarantee is claimed. Based on this, we build a two-step system: one component selects the noise level, and the other makes the final prediction and robustness certificate using that noise. We also show how the same idea can be used as a routing mechanism—selecting among several existing robust models—to better balance accuracy and robustness.
  </div>
</details>
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
We argue that a widely used headline number for comparing certifiably robust neural networks—average certified radius (ACR)—is a poor indicator of real progress. We show that ACR can be made arbitrarily large in theory, even for a trivial classifier given sufficient evaluation budget, and that in realistic settings it disproportionately rewards improvements on easy cases while underweighting hard ones. Empirically, we find that several state-of-the-art training methods increase ACR while consistently reducing robustness on harder inputs, and that simple strategies can achieve state-of-the-art ACR without improving robustness across the full data distribution. We therefore conclude that ACR should be discontinued for evaluation and recommend reporting more informative alternatives.
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
<details style="margin:0.05em 0 0.12em 0;padding-left:2.2em;font-size:0.85em;color:#666;">
  <summary style="cursor:pointer;font-style:italic;margin:0;padding:0;">General audience summary</summary>
  <div style="margin:0.08em 0 0;padding:0;color:#555;">
We build CTBench, a unified open-source library and benchmark for training neural networks that come with provable robustness guarantees against small input perturbations. A major problem in this area is that methods are often reported under incompatible training schedules, verification procedures, and under-tuned hyperparameters, so headline numbers can reflect evaluation choices rather than real algorithmic progress. CTBench enforces fair, apples-to-apples comparisons by standardizing the training and certification setup and systematically tuning hyperparameters across methods; under these fair settings, most methods substantially outperform their originally reported results, and the apparent advantage of several recent methods shrinks once strong baselines are properly implemented and tuned. Using the resulting trained models, we also analyze what certified training changes about model behavior, finding patterns such as smoother optimization landscapes, shared error modes across different robust models, sparser activations, the importance of carefully reducing regularization when targeting stronger guarantees, and evidence that certified training can improve generalization under certain distribution shifts.
  </div>
</details>
- Stefan Balauca, Mark Niklas Müller, **Yuhao Mao**, Maximilian Baader, Marc Fischer, Martin Vechev, [Gaussian Loss Smoothing Enables Certified Training with Tight Convex Relaxations](https://arxiv.org/abs/2403.07095), [Transactions on Machine Learning Research 07/2025](https://jmlr.org/tmlr/) (TMLR'25).
<span style="display:inline-flex; align-items:center; gap:4px; position:relative; top:-0.1em;">
  <a href="https://github.com/stefanrzv2000/GLS-Cert-Training">
    <img src="../assets/github-mark.png" alt="GitHub" style="height:1em;"/>
  </a>
</span>
<details style="margin:0.05em 0 0.12em 0;padding-left:2.2em;font-size:0.85em;color:#666;">
  <summary style="cursor:pointer;font-style:italic;margin:0;padding:0;">General audience summary</summary>
  <div style="margin:0.08em 0 0;padding:0;color:#555;">
We address a puzzling issue in methods that aim to train neural networks with provable guarantees against small input changes: using a more accurate (tighter) mathematical approximation should help, but in practice it often makes training worse than using a cruder approximation. The core reason is that tighter approximations can make the training objective behave erratically, with abrupt jumps and extreme sensitivity, which breaks standard gradient-based optimization. A simple fix is introduced: smooth the training objective by averaging it over small random perturbations, which makes the optimization landscape continuous and well-behaved while still targeting strong guarantees. This idea is instantiated in two practical training approaches: one that does not require backpropagating through the approximation (so it can handle non-differentiable procedures), and a more efficient gradient-based variant when gradients are available. Across a wide range of settings, combining this loss-smoothing strategy with tight approximations yields stronger provable robustness than prior methods trained on the same model families.
  </div>
</details>
- **Yuhao Mao**, Mark Niklas Müller, Marc Fischer, Martin Vechev, [Understanding Certified Training with Interval Bound Propagation](https://arxiv.org/abs/2306.10426), [The Twelfth International Conference on Learning Representations](https://iclr.cc/Conferences/2024) (ICLR'24).
<span style="display:inline-flex; align-items:center; gap:4px; position:relative; top:-0.1em;">
  <a href="https://github.com/eth-sri/ibp-propagation-tightness">
    <img src="../assets/github-mark.png" alt="GitHub" style="height:1em;"/>
  </a>
  <a href="../assets/files/PI_ICLR_poster.pdf">
    <img src="../assets/poster-icon.png" alt="Poster" style="height:1em;"/>
  </a>
</span>
<details style="margin:0.05em 0 0.12em 0;padding-left:2.2em;font-size:0.85em;color:#666;">
  <summary style="cursor:pointer;font-style:italic;margin:0;padding:0;">General audience summary</summary>
  <div style="margin:0.08em 0 0;padding:0;color:#555;">
Interval Bound Propagation (IBP) checks robustness by tracking simple minimum and maximum values that each part of a neural network can take when the input is slightly perturbed. Although this simplification may seem too crude to be reliable, we show that training with IBP progressively reshapes the network so that these rough bounds become much more accurate, especially when stronger robustness is targeted. Our analysis further shows that making such bounds perfectly accurate requires very strong constraints on the model, helping explain why improving provable robustness often comes at the expense of standard accuracy. We confirm these insights empirically for both IBP itself and state-of-the-art methods built on IBP.
  </div>
</details>
- Maximilian Baader\*, Mark Niklas Müller\*, **Yuhao Mao**, Martin Vechev, [Expressivity of ReLU-Networks under Convex Relaxations](https://arxiv.org/abs/2311.04015), [The Twelfth International Conference on Learning Representations](https://iclr.cc/Conferences/2024) (ICLR'24).
<span style="display:inline-flex; align-items:center; gap:4px; position:relative; top:-0.1em;">
  <a href="../assets/files/Expressivity_ICLR_poster.pdf">
    <img src="../assets/poster-icon.png" alt="Poster" style="height:1em;"/>
  </a>
</span>
<details style="margin:0.05em 0 0.12em 0;padding-left:2.2em;font-size:0.85em;color:#666;">
  <summary style="cursor:pointer;font-style:italic;margin:0;padding:0;">General audience summary</summary>
  <div style="margin:0.08em 0 0;padding:0;color:#555;">
Proving that a neural network is safe or robust often relies on convex relaxations, which replace the network's nonlinear behavior with a simplified convex approximation that is easier to analyze. This work studies a basic question: even if a network can represent a desired function, can it be represented in a way that these convex approximations can analyze precisely? The results show a sharp split: for one-dimensional functions, more advanced relaxations remove limitations seen in simpler ones and can even admit exponentially more network representations for the same function; however, for multi-dimensional functions, even the strongest commonly used neuron-by-neuron relaxations provably fail to precisely capture some very simple convex and monotone functions. The takeaway is that some accuracy gaps in certified training and verification are not just due to optimization or tuning, but can reflect fundamental limits of widely used convex-approximation tools, motivating richer analyses that reason about multiple neurons jointly.
  </div>
</details>
- **Yuhao Mao**, Mark Niklas Müller, Marc Fischer, Martin Vechev, [Connecting Certified and Adversarial Training](https://arxiv.org/abs/2305.04574), [The Thirty-seventh Conference on Neural Information Processing Systems](https://nips.cc/Conferences/2023) (NeurIPS'23).
<span style="display:inline-flex; align-items:center; gap:4px; position:relative; top:-0.1em;">
  <a href="https://github.com/eth-sri/taps">
    <img src="../assets/github-mark.png" alt="GitHub" style="height:1em;"/>
  </a>
  <a href="../assets/files/TAPS_NIPS_poster.pdf">
    <img src="../assets/poster-icon.png" alt="Poster" style="height:1em;"/>
  </a>
</span>
<details style="margin:0.05em 0 0.12em 0;padding-left:2.2em;font-size:0.85em;color:#666;">
  <summary style="cursor:pointer;font-style:italic;margin:0;padding:0;">General audience summary</summary>
  <div style="margin:0.08em 0 0;padding:0;color:#555;">
We propose a training method that improves provable robustness by combining two complementary ways of approximating worst-case behavior: fast but overly conservative bound propagation, and targeted adversarial search, which is typically optimistic. The method splits the network into an early feature extractor and a later classifier. It first applies bound propagation to determine the minimum and maximum values that features can take, and then performs adversarial search within these feature-space bounds to identify inputs that are most damaging to the classifier. This produces a substantially tighter estimate of the worst-case loss than either end-to-end bound propagation or end-to-end adversarial search alone. As a result, models trained in this way can be certified using standard verification tools and achieve markedly improved trade-offs between standard accuracy and certifiable robustness.
  </div>
</details>
- Yuyou Gan\*, **Yuhao Mao**\*, Xuhong Zhang, Shouling Ji, Yuwen Pu, Meng Han, Jianwei Yin, Ting Wang, [``Is your explanation stable?'': A Robustness Evaluation Framework for Feature Attribution](https://arxiv.org/abs/2209.01782), [ACM SIGSAC Conference on Computer and Communications Security 2022](https://www.sigsac.org/ccs/CCS2022/) (CCS'22).
<span style="display:inline-flex; align-items:center; gap:4px; position:relative; top:-0.1em;">
  <a href="https://github.com/sweet-shark/MeTFA-A-Robustness-Evaluation-Framework-for-Feature-Attribution">
    <img src="../assets/github-mark.png" alt="GitHub" style="height:1em;"/>
  </a>
</span>
<details style="margin:0.05em 0 0.12em 0;padding-left:2.2em;font-size:0.85em;color:#666;">
  <summary style="cursor:pointer;font-style:italic;margin:0;padding:0;">General audience summary</summary>
  <div style="margin:0.08em 0 0;padding:0;color:#555;">
Explanations for neural network predictions often look convincing but can be unreliable: they may change substantially even when the input is very similar and the prediction remains unchanged, or they may be deliberately manipulated. We propose a framework that makes such explanations more stable and explicitly measures how uncertain an explanation is. The approach works by generating many explanations for slightly perturbed inputs and using a robust, median-based statistical test to identify features that are consistently important. This produces clearer explanations that emphasize only well-supported features and provides a principled way to quantify uncertainty. Experiments show that the method improves stability while preserving the connection between explanations and model behavior, with further successful applications to context-bias detection and defenses against attacks that target explanations.
  </div>
</details>
- **Yuhao Mao**, Chong Fu, Saizhuo Wang, Shouling Ji, Xuhong Zhang,
Zhenguang Liu, Jun Zhou, Alex X. Liu, Raheem Beyah, Ting Wang, [Transfer Attack Revisited: A Large-Scale Empirical Study in Real Computer Vision Settings](https://arxiv.org/abs/2204.04063), [IEEE Symposium on Security & Privacy 2022](https://www.ieee-security.org/TC/SP2022/program-papers.html) (SP'22).
<span style="display:inline-flex; align-items:center; gap:4px; position:relative; top:-0.1em;">
  <a href="https://github.com/AlgebraLoveme/Transfer-Attacks-Revisited-A-Large-Scale-Empirical-Study-in-Real-Computer-Vision-Settings">
    <img src="../assets/github-mark.png" alt="GitHub" style="height:1em;"/>
  </a>
</span>
<details style="margin:0.05em 0 0.12em 0;padding-left:2.2em;font-size:0.85em;color:#666;">
  <summary style="cursor:pointer;font-style:italic;margin:0;padding:0;">General audience summary</summary>
  <div style="margin:0.08em 0 0;padding:0;color:#555;">
We examine transfer attacks against real cloud vision services, where an attacker crafts a slightly modified image using a locally available model and hopes the same modification will also fool a different, remote model accessed through an API. A key challenge in studying this in the real world is that cloud services often return multiple labels with confidence scores, and their label sets do not match the labels available to the attacker's local model, so standard academic success measures do not apply; we therefore introduce practical evaluation metrics that handle these mismatches. Using a large systematic study across many attack settings and multiple major platforms, we find that several common lab takeaways do not carry over: choosing a simpler local model does not reliably help, no single local model architecture consistently transfers best, and stronger iterative attack algorithms do not necessarily transfer better than simpler single-step ones. We also identify factors that matter more in practice, such as the choice of attack algorithm and the target platform, the usefulness of larger L2-bounded changes for transfer compared with L-infinity-bounded ones, and the importance of testing on images that are intrinsically hard to classify. Overall, while transfer attacks may look weak on average, the study shows they can be systematically configured to achieve stable success against real deployed services.
  </div>
</details>


### Artificial Intelligence for Science

- Chenhao Chu, **Yuhao Mao**, Hua Wang, [Transfer Learning Assisted Fast Design Migration Over Technology Nodes: A Study on Transformer Matching Network](https://arxiv.org/abs/2502.18636), [IEEE MTT-S International Microwave Symposium 2024](https://ims-ieee.org/welcomeIMS2024) (IMS'24). 
<span style="display:inline-flex; align-items:center; gap:4px; position:relative; top:-0.1em;">
  <a href="https://github.com/ChenhaoChu/RFIC-TL">
    <img src="../assets/github-mark.png" alt="GitHub" style="height:1em;"/>
  </a>
</span>
<details style="margin:0.05em 0 0.12em 0;padding-left:2.2em;font-size:0.85em;color:#666;">
  <summary style="cursor:pointer;font-style:italic;margin:0;padding:0;">General audience summary</summary>
  <div style="margin:0.08em 0 0;padding:0;color:#555;">
We propose a way to reuse a learned design model to speed up circuit redesign when the same millimeter-wave circuit must be adapted to different chip manufacturing processes, such as changes in fabrication technology, metal stack options, or operating frequency. These changes normally require building a new predictive model from scratch, because the underlying design parameters and simulation grids shift across manufacturing settings. Our approach transfers a neural network trained in one manufacturing setting to a new one and adapts it using only a small amount of new simulation data. Experiments show that this transfer greatly accelerates training and improves prediction quality: using only a small fraction of new data with transfer learning can outperform training from scratch with up to 4x more data. This demonstrates that knowledge learned in one chip manufacturing setting can be effectively reused to reduce simulation cost and speed up design iteration in others.
  </div>
</details>

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