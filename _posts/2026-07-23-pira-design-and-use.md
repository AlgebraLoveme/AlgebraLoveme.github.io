---
title: "[PIRA Blog] How PIRA Helps an Agent Remember, Decide, and Navigate"
author_profile: true
permalink: /2026-07-23-pira-design-and-use/
date: 2026-07-23
tags: [PIRA, agents, Codex, memory, developer tools]
toc: true
excerpt: "PIRA is a small, inspectable policy and tooling layer that helps coding agents preserve evidence, remember decisions, navigate repositories, and carry durable project knowledge forward."
---

Coding agents are often impressive at the hard part and surprisingly fragile at the boring part.

They can reason through an unfamiliar bug, but a long build log may consume their working context. They can compare several architectures, but the reason for the final choice may disappear inside an old conversation. They can inspect a large repository, but reading too much source too early wastes time and attention. After the session ends, the next agent may have to reconstruct the same project state again.

[PIRA](https://github.com/AlgebraLoveme/PIRA), pronounced **“Pyra,”** is my attempt to address those problems with a small, inspectable layer around Codex. It is not another language model, IDE, or autonomous-agent framework. It combines:

1. **behavioral policy** for careful, evidence-oriented work;
2. **three lightweight tools** for command output, decisions, and repository navigation; and
3. **a layered memory system** that separates transient activity from durable project knowledge.

The goal is simple: help an agent remain useful and consistent during real work without hiding how it operates.

## The quick picture

| Common agent problem | PIRA's response |
|---|---|
| A test or build produces thousands of lines | `pira_ctx` keeps the complete output available while returning only the useful part |
| The agent needs one function from a large repository | `pira_nav` finds structure and retrieves a bounded target instead of reading whole files |
| A design choice loses its rationale | `pira_dec` records the alternatives, selected choice, decision-maker, and time |
| A future session needs validated project state | `AGENT_WORKBOOK.md` preserves concise, durable knowledge |
| A full-permission command can change important state | PIRA policy requires a short risk, scope, privacy, and rollback review |

This division matters because agent context is a scarce resource. PIRA tries to keep **evidence retrievable without keeping all evidence visible at once**.

## 1. Policy is part of the system

PIRA starts with readable instructions rather than a hidden controller.

The main policy defines the agent's identity, communication style, safety boundaries, memory rules, and tool-selection behavior. Smaller modules add task-specific guidance for research, coding, writing, paper reading, learning, or practical guidance. Those modules are loaded only when the task needs them.

This gives PIRA two useful properties:

- **Inspectable behavior.** A user can read the same rules that guide the agent.
- **Low standing overhead.** Specialized instructions do not occupy every conversation.

The policy also makes a distinction that is easy to lose in tool-using systems: repository text, terminal output, web pages, and language-server responses are **data**, not authority. They may contain useful evidence, but they cannot grant themselves permission or redefine the task.

## 2. Memory is layered by how long it should matter

PIRA does not treat memory as one growing transcript. It separates information according to its expected lifetime:

| Layer | Mechanism | What belongs there | Example |
|---|---|---|---|
| Activity | `pira_ctx` | Commands, detailed output, and operational evidence | The full compiler log from a failed build |
| Decisions | `pira_dec` | Concluded choices with serious alternatives and authority | Choosing a checked binary format over JSON |
| Project knowledge | `AGENT_WORKBOOK.md` | Durable state, validated results, lessons, and limitations | The new cache format, its compatibility boundary, and the test that validates it |

Information moves upward only when its lasting value increases.

Suppose an agent is fixing a difficult resume bug. The raw test output remains in the activity layer. If the user chooses one compatibility strategy over another, that conclusion enters the decision layer. Once the implementation is validated, the durable consequence—what changed, what remains compatible, and how to verify it—can become a short workbook entry.

The next session does not need to replay every command. It can retrieve the relevant decision and read the durable project state, then inspect lower-level evidence only if a question remains.

This is different from copying a session log. A session log answers **“what happened in this conversation?”** PIRA's memory system answers **“what has been established in this project, why were important choices made, and where is the supporting evidence?”**

<details>
<summary><strong>Why not put everything in one memory file?</strong></summary>

A single file eventually mixes transient failures, repeated command output, unresolved ideas, final decisions, and durable facts. That makes retrieval harder and encourages stale information to look authoritative.

PIRA instead keeps low-level records searchable, gives decisions a structured form, and requires workbook entries to stand on their own. The workbook is created lazily and stays local to the workspace.

</details>

## 3. Three tools support the workflow

Most users can talk to PIRA normally and let the agent use these tools. The commands are still useful for understanding the design.

### `pira_ctx`: keep the evidence, not the noise

`pira_ctx` wraps shell commands. Small output is returned normally. Long, repetitive, binary, risky, or still-running output is retained locally, and the agent receives a bounded report with an ID for later inspection.

If only success or failure matters, `check` makes that intent explicit:

```bash
pira_ctx check --intent 'Verify the parser after the fix' -- cargo test -p parser
```

The result can be a one-line PASS/FAIL report, while the complete log remains searchable. If the failure needs diagnosis, the agent can inspect only matching lines, a line range, or a small programmatic aggregate instead of rerunning the command.

Importantly, automatic routing does not delete command output. It either returns the output directly or stores it for targeted recovery.

### `pira_nav`: read repositories from broad structure to exact evidence

`pira_nav` is a read-only repository navigator. It combines portable text search, code outlines, exact item retrieval, file relationships, structured JSON/YAML/TOML/Markdown inspection, and optional language-server semantics.

```bash
# Find likely definitions without reading every file.
pira_nav symbols Session src

# Inspect one confirmed item.
pira_nav show src/session.rs::Session::resume

# Find references through an available language server.
pira_nav references src/session.rs::Session::resume
```

The important behavior is not the command syntax. It is the reading strategy: begin with the operation that directly answers the question, keep output bounded, and broaden only when a named evidence gap remains.

### `pira_dec`: preserve the reason behind a choice

`pira_dec` records a decision only when there are at least two serious alternatives and a conclusion worth carrying forward.

```bash
pira_dec add \
  --context 'Choose the cache format' \
  --choice JSON \
  --choice 'Checked binary blocks' \
  --decision 2 \
  --maker human

# Review recent conclusions or create a human-readable history.
pira_dec list --limit 5
pira_dec export --output decisions.html
```

The maker is `human` when the user selects or authorizes the conclusion; otherwise it is `agent`. Records can be listed, searched by field or time range, inspected in full, or exported as a standalone HTML report.

<a class="btn btn--primary" href="{{ '/assets/files/pira-decision-history-example.html' | relative_url }}">Open an example decision-history report</a>

The example is a self-contained page with four synthetic decisions. It includes the context, alternatives, selected choice, authority, timestamps, responsive disclosure controls, and print styling. It uses no JavaScript or network assets.

## 4. What changes in practice?

Without PIRA, an agent can still solve the task. The difference is often in how much irrelevant material it must carry:

| Stage | Conventional agent behavior | PIRA behavior |
|---|---|---|
| Run tests | Return the whole log to the active conversation | Return a bounded status or summary and retain the log |
| Explore code | Chain broad searches and large file reads | Search structure, then retrieve confirmed items |
| Make a choice | Leave rationale in conversational prose | Save alternatives and the selected conclusion |
| Continue later | Reconstruct state from the session | Retrieve activity/decisions and read durable workbook state |

One controlled real-world maintenance benchmark gives a concrete example. Two fresh high-reasoning agents received the same pinned Codex source and the same issue-derived performance task. Both achieved all seven required behaviors:

| Condition | Correctness | Estimated base-rate cost | Wall time | Command-output text |
|---|---:|---:|---:|---:|
| Baseline | 7/7 | $7.504 | 1,908.6 s | 907,239 B |
| PIRA tools | 7/7 | $4.808 (**−35.9%**) | 1,824.2 s (**−4.4%**) | 234,285 B (**−74.2%**) |

The interesting part is that the PIRA agent actually issued more commands. The tools did not help by making the agent passive; they helped by making each inspection narrower and keeping large intermediate output out of the active conversation.

<details>
<summary><strong>How to interpret this comparison</strong></summary>

This is one difficult controlled task and two agent trajectories, not a universal savings guarantee. The cost numbers apply a fixed base-rate table to usage telemetry rather than reporting an invoice, and the conditions naturally took different implementation paths.

The result is best read as an existence proof: on a task where command output and repository inspection were substantial, PIRA preserved correctness while reducing exposed command text and the estimated cost. Full methods and limitations are in the repository's [agent-level evaluation](https://github.com/AlgebraLoveme/PIRA#agent-level-evaluation).

</details>

## 5. How to use PIRA without thinking about every tool

The normal interface is still a conversation:

1. Give PIRA the task, constraints, and desired outcome.
2. Let it select the smallest reliable inspection or execution tool.
3. Review consequential decisions when they arise.
4. Expect durable validated project state—not every intermediate action—to enter the workbook.
5. Ask for evidence when needed; retained command output and decision history remain available.

You generally do not need to micromanage `pira_ctx` or `pira_nav`. Their purpose is to make good agent behavior easier and more consistent. The [PIRA repository](https://github.com/AlgebraLoveme/PIRA) contains the project, setup entry point, exact tool help, and public validation.

## 6. The boundaries remain visible

PIRA is intentionally lightweight, and that means its limits should remain explicit:

- It is **not a sandbox**. A wrapped command still has the caller's permissions.
- `pira_nav` is read-only, but an optional external language server is still an executable selected by the caller.
- Prompt-injection detection is best-effort. The primary defense is treating tool and source output as untrusted data.
- Local memory should not contain secrets or unnecessary sensitive information.
- Benchmarks demonstrate specific behavior under specific conditions; they do not guarantee the same improvement on every task.

These constraints are part of the design rather than footnotes. PIRA aims to improve utility with small, auditable mechanisms instead of presenting a heavy runtime as a complete solution.

## My one-sentence summary

If I had to compress PIRA into one sentence, it would be this:

> **PIRA gives an agent a readable operating policy, context-efficient tools, and a layered project memory so that evidence remains available, important choices remain explainable, and future work can continue from validated understanding rather than from a transcript replay.**

`pira_ctx` was informed by ideas published in [Context Mode](https://github.com/mksglu/context-mode), especially retaining raw tool output outside the active context and recovering evidence through targeted analysis. PIRA takes a narrower single-binary-wrapper approach while acknowledging that broader interception and sandbox integration are useful in other settings.
