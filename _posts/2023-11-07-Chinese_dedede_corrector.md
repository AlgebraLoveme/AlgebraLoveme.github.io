---
title: "Chinese-dedede-Corrector: A Conservative 的地得 Checker"
author_profile: true
permalink: 2023_11_07_announcing_chinese_dedede_corrector/
date: 2023-11-07
last_modified_at: 2026-08-21
last_modified_by: PIRA
tags: [Chinese, language tools, proofreading]
header:
    image: "/imgs/chinese-corrector-hero.jpg"
excerpt: "A rule-based tool for detecting likely misuse of 的 and suggesting 地 or 得."
---

[Chinese-dedede-Corrector](https://github.com/AlgebraLoveme/Chinese-dedede-corrector) is a rule-based proofreading tool for a common Chinese writing problem: confusing **的**, **地**, and **得**.

Despite the broader project name, the current implementation has a deliberately narrow scope. It looks for occurrences of **的** that may need to be replaced by **地** or **得**. It does not claim to detect every possible misuse of all three particles.

## How it works

The tool first assigns part-of-speech information to the words surrounding each **的**, using `pkuseg` by default or `jieba` as an alternative. Hand-written grammatical rules then decide whether a replacement is plausible.

The strategy favors precision over recall: it attempts fewer corrections in order to reduce incorrect replacements. This caution is necessary because both the part-of-speech tagger and the rules can be wrong. The output should therefore be reviewed rather than accepted automatically.

## Running the checker

After following the repository's [setup instructions](https://github.com/AlgebraLoveme/Chinese-dedede-corrector#setup), run:

```bash
python main.py --filename FILE_TO_PROCESS --verbose
```

The program writes a corrected file with the suffix `.corrected`. The `--verbose` option prints each proposed replacement, which is useful for reviewing the tool's decisions. Additional command-line options select the output filename, text encoding, and parser engine; the repository's [usage section](https://github.com/AlgebraLoveme/Chinese-dedede-corrector#usage) lists them.

## Appropriate use

The checker is best treated as a review assistant for drafts such as online fiction or subtitles, not as an authoritative grammar judge. Its suggestions can surface suspicious phrasing quickly, while the writer or editor retains the final decision.

The project remains open to more precise rules and better linguistic coverage. Bugs or concrete examples can be reported through the repository's [issue tracker](https://github.com/AlgebraLoveme/Chinese-dedede-corrector/issues).
