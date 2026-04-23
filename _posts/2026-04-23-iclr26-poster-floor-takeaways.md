---
title: "[PIRA Blog] What ICLR 2026 Is Really About"
author_profile: true
permalink: /2026-04-23-iclr26-poster-floor-takeaways/
date: 2026-04-23
tags: [ICLR, conference, LLMs, safety, robustness, evaluation]
toc: true
excerpt: "My read of ICLR 2026: foundation models still dominate, but reliability, agents, evaluation, and security increasingly define the conference."
---

After going through the ICLR 2026 posters, I came away with a fairly clear impression: foundation models still sit at the center of the conference, but the conference is no longer organized around capability alone.

What now feels central is a different question: how do we turn these models into systems that can **reason, act, and interact with the world** without becoming impossible to evaluate, monitor, or trust?

This should be read as a take on the conference through its posters rather than every talk, workshop, or side conversation. The quantitative categories below are **overlapping signals**, so they do not add up to 100%. Even with that caveat, the overall direction felt quite clear.

## The quick picture

Across the posters I went through, the biggest themes looked like this:

| Topic bucket | Count | Share |
|---|---:|---:|
| LLMs / foundation models | 2,260 | 41.8% |
| Agents / agent security | 1,533 | 28.3% |
| Robustness / adversarial / OOD | 1,520 | 28.1% |
| Multimodal / vision-language / audio | 1,396 | 25.8% |
| Reasoning / test-time compute | 1,330 | 24.6% |
| Safety / alignment / jailbreaks | 953 | 17.6% |
| Diffusion / generative media | 935 | 17.3% |
| RL / RLHF | 920 | 17.0% |
| Uncertainty / conformal / calibration | 461 | 8.5% |
| Causality / interventions | 334 | 6.2% |
| Security attacks / backdoors / poisoning | 334 | 6.2% |
| Privacy / unlearning / memorization | 291 | 5.4% |

Even this table already tells a story. Foundation models remain the main substrate, but several adjacent themes now sit unusually close to the center. In particular, agents and robustness are nearly tied in this poster set—**1,533 vs. 1,520 posters**, a gap of only **13**—which is a strong hint that the conference is no longer asking only what models can do, but also what can go wrong once they start doing it.

## 1. Foundation models are still the base layer, but they are no longer the whole destination

The most obvious headline is still the dominance of foundation-model work: **2,260 out of 5,410 posters**, or **41.8%**, carry an LLM or foundation-model signal.

But that number matters less on its own than in combination with the surrounding themes. Much of the work is no longer simply asking whether models can do something impressive. Instead, it is asking whether they can do it **reliably, cheaply, safely, and in a way that survives contact with deployment**.

That is the broader shift ICLR 2026 seems to capture. Foundation models are still the common substrate, but they are increasingly being treated as components inside larger systems. The research frontier is therefore moving outward: from raw capability to **capability under constraints**, and from isolated model performance to system behavior in the wild.

## 2. Reliability has become a full-stack concern

One of the clearest conference-level patterns is that reliability is no longer a niche corner of machine learning.

The numbers make that visible. In the poster set I went through:

- **28.1%** had a robustness / adversarial / OOD signal,
- **17.6%** had a safety / alignment / jailbreak signal,
- **8.5%** had an uncertainty / conformal / calibration signal,
- **6.2%** had a security-attacks / backdoors / poisoning signal, and
- **5.4%** had a privacy / unlearning / memorization signal.

No single one of these categories defines the conference. Together, however, they show that reliability has become a broad stack: robustness, auditing, calibration, distribution shift, security, privacy, and evaluation validity now sit much closer to the center of the conversation.

The deeper point is that this is not just a thematic expansion. It reflects a change in what failure means. When models are used as agents, judges, copilots, and multimodal interfaces, the relevant question is no longer only whether they are accurate. It is whether they are stable under shift, monitorable under uncertainty, and defensible under attack. Reliability therefore stops being a side constraint and becomes part of the core problem definition.

## 3. Agent papers increasingly look like security papers

If I had to pick one theme that makes ICLR 2026 feel especially current, it would be this: **agent research increasingly reads like systems security research**.

At the conference level, **1,533 posters (28.3%)** had an agent or agent-security signal. Inside the LLM subset, **750 out of 2,260 papers (33.2%)** involved agents or tool use.

That is large enough to be structurally important. Agents are no longer peripheral; they are one of the main ways LLM work is connecting to real deployment concerns.

Once models begin acting through tools and APIs, the attack surface becomes much more concrete. That is why prompt injection, tool misuse, protocol-level attacks, human-oversight tradeoffs, and monitoring or control mechanisms appear so often.

For that reason, agent work no longer feels like a simple extension of chatbot demos. In many cases it now looks like a mix of:

- distributed systems,
- security engineering,
- evaluation design, and
- reliability under partial observability.

The interesting shift is not merely that agents are popular. It is that agency collapses several previously separate concerns into one object: capability, evaluation, safety, and security all become entangled once a model can take actions rather than only emit text. That is one reason the conference feels more security-aware than a raw count of “safety” papers might suggest.

## 4. Safety is getting more operational

This is where the tone of the conference also seems to have changed. The strongest safety-oriented work did not feel like vague rhetoric. It felt operational.

The recurring topics were concrete: jailbreaks, catastrophic-risk certification, backdoors, API auditing, privacy extraction, watermarking, memorization, and unlearning. The numbers help calibrate that picture as well. Within the LLM subset, **225 papers (10.0%)** had a direct safety / jailbreak / red-teaming signal, and **127 papers (5.6%)** had a privacy / unlearning / memorization signal.

So safety is clearly visible, but it is still smaller than reasoning, evaluation, or efficiency by raw count. That is precisely why the more important point is structural rather than numerical: safety is increasingly being absorbed into mainstream model evaluation, agent design, and system testing.

In other words, the field seems less interested in talking about safety as a separate moral category, and more interested in turning it into an engineering discipline with attack models, benchmarks, audits, monitors, and measurable defenses. That is a healthier place for the conversation to move.

## 5. Evaluation is becoming one of the field's main products

This may be the biggest surprise if you have not looked closely at recent poster titles: a large share of the field is not just building models. It is building **measuring instruments**.

Within the LLM/foundation-model subset, the strongest recurring themes looked like this:

| LLM subfield | Count | Share within LLM papers |
|---|---:|---:|
| Efficiency / inference / compression | 1,062 | 47.0% |
| Evaluation / benchmarks | 1,005 | 44.5% |
| Reasoning / test-time scaling | 941 | 41.6% |
| Agents / tool use | 750 | 33.2% |
| Multimodal / VLM / audio | 615 | 27.2% |
| Alignment / RLHF / preference optimization | 503 | 22.3% |
| Mechanistic interpretability / representation analysis | 415 | 18.4% |
| Safety / jailbreaks / red-teaming | 225 | 10.0% |
| Math / theorem proving / formal reasoning | 195 | 8.6% |
| Privacy / unlearning / memorization | 127 | 5.6% |

The logic of that table is important. Evaluation is now at least as central to LLM work as reasoning: **1,005 LLM papers (44.5%)** had an evaluation / benchmark signal, compared with **941 (41.6%)** for reasoning / test-time scaling.

So the LLM story is not merely that reasoning is fashionable. It is closer to this:

> We want stronger reasoning, but we also want it to be measurable, affordable, and deployable.

Two additional benchmark statistics make that even clearer. A conservative estimate suggests that **183 out of 2,260 LLM papers (8.1%)** are essentially benchmark-building papers—about **1 in 12**. A broader evaluation-infrastructure estimate rises to **789 out of 2,260 (34.9%)**, meaning that **more than 1 in 3 LLM posters** is substantially about measurement rather than just model improvement.

There is another useful comparison here: eval-heavy LLM work is about **4.5 times** as common as explicitly safety / jailbreak-heavy LLM work (**1,005 vs. 225 papers**). That does not make safety unimportant. If anything, it suggests that the field is increasingly trying to govern ambitious claims through evaluation infrastructure.

That, to me, is one of the deepest shifts in the conference. The community is not only scaling models; it is building the epistemic machinery that decides which claims about those models should count as credible. Benchmark construction therefore no longer looks like a side activity. It looks like one of the field's main research products.

## 6. Multimodality and diffusion are still active, but the emphasis has matured

Multimodal work is now clearly part of the core conversation rather than a decorative add-on. At the conference level, **1,396 posters (25.8%)** had a multimodal / vision-language / audio signal. Inside the LLM subset, **615 papers (27.2%)** were multimodal.

What seems different from a couple of years ago is not the presence of multimodality, but the emphasis. The interesting questions are less about showing that a model can produce flashy outputs and more about **control, evaluation, editing, safety, generalization, and deployment behavior**.

The same is true for diffusion-related work. Diffusion / generative-media signals appeared in **935 posters (17.3%)**, which is still a substantial share of the conference. But the tone feels more mature: less “look what this model can generate,” more “how do we control it, measure it, watermark it, and understand its failure modes?”

That shift matters because multimodal and generative systems expose weaknesses that text-only benchmarks can hide. As soon as a model sees, acts, edits, or generates across modalities, questions of evaluation, provenance, robustness, and misuse become much harder. So multimodality is not just another capability frontier; it is also a stress test for the field's measurement culture.

## 7. Theory and AI-for-math are not the center of gravity, but they are clearly real currents

Theory and AI-for-math are not the conference center, but both are clearly present.

A stricter theory-like signal showed up in **1,037 of 5,410 posters (19.2%)**. A stricter AI-for-math signal showed up in **397 of 5,410 (7.3%)**—about **1 in 14 posters**. Inside the LLM subset, **195 papers (8.6%)** had a math / theorem-proving / formal-reasoning signal.

Those are not dominant numbers, but they are too large to dismiss as side curiosities. More importantly, both areas feel more mature than they did a couple of years ago. Theory often appears in hybrid form, tied to practical concerns such as transformer generalization, certification, interpretability guarantees, reinforcement learning, and scientific machine learning. AI for math likewise feels less like a novelty theme and more like a growing subcommunity, with increasing attention to infrastructure, proof quality, formalization, and evaluation.

What I find interesting here is that both theory and AI-for-math now function less as opposites to the foundation-model mainstream than as selective complements to it. They are places where the field tries to recover rigor, structure, and verifiability inside an otherwise fast-moving systems landscape.

That is encouraging. It suggests that even in a conference dominated by foundation-model systems, there is still real appetite for work that sharpens concepts, guarantees, and standards of evidence.

## My one-sentence summary

If I had to compress the whole picture into one sentence, it would be this:

> **ICLR 2026 is about turning foundation models into deployable systems that can reason, act, and handle multimodal inputs—while the field simultaneously builds the evaluation, safety, and theoretical infrastructure needed to keep those claims honest.**

That last clause matters. The conference is not only building models; it is also building the tests, audits, and conceptual tools needed to judge those models.

To me, that is one of the most encouraging signals in ICLR 2026.
