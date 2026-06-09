---
description: End-of-session agent tuning. Audits which skills/workflows were used, then drafts surgical SKILL.md edits from observed friction (bad triggers, repeated corrections, role confusion). Drafts only; Gary approves each diff. Companion to /wrapup.
---

# Improve Agents

Make the agent definitions a little better after every session. Where `/wrapup` synchronizes
*project* memory (§8–§12, `docs/LESSONS_LEARNED.md`), this synchronizes *agent* memory — the
`.agents/skills/<skill>/SKILL.md` files, and `.agents/workflows/<flow>.md` when relevant.
Honor all guardrails in GEMINI.md and AGENTS.md. Propose-don't-write throughout: this workflow
drafts edits and writes nothing until Gary approves each diff.

## Scope
- **In scope:** `.agents/skills/*/SKILL.md` and `.agents/workflows/*.md`.
- **Out of scope:** never touches `src/`, `cpp/`, `results/`, `reference.py`,
  `docs/PROJECT_TRACKER.md`, or any frozen section. Project-memory updates remain `/wrapup`'s job.

## Step 1 — Identify what was used
List every `.agents` skill and workflow actually exercised this session — invoked by name,
delegated to, or whose rules clearly governed a step. For each, note *how* it was used and who
drove it (PI vs. subagent). Skip anything that never came into play; don't speculate about
unused agents.

## Step 2 — Gather friction signals (per used item)
For each used skill/workflow, scan the session for concrete evidence its definition could be
clearer or more complete:

- **Triggering misses** — it fired when it shouldn't have, or should have fired and didn't
  (`description:` too broad or too narrow — this is the line the router reads).
- **Repeated corrections** — Gary had to clarify, redirect, or re-explain something the
  definition could have stated up front.
- **Role / ownership confusion** — overlap or a gap between agents, ambiguous file ownership,
  or a fumbled hand-off.
- **Guardrail near-misses** — a moment the agent nearly edited a protected file, skipped an
  approval gate, or under-reported. Anything the definition should harden against.
- **Reporting drift** — the triplet `[Files Changed, Validation Status, New Decisions]` (plus
  any role-specific fields) was missing or malformed.

Cite the evidence — what actually happened — for every signal. No signal, no edit.

## Step 3 — Draft edits
For each item with real signals, draft a *minimal, surgical* edit that fixes the observed
problem and nothing more:

- Tighten the `description:` when triggering was off.
- Add or clarify a single Responsibility, Requirement, or Reporting-Contract line when an
  instruction was missing.
- Prefer one or two precise sentences over broad rewrites; keep the existing structure and voice.
- If two items conflict or overlap, propose the boundary explicitly rather than editing both blindly.

Present each change as a labeled before → after diff, grouped by file.

## Step 4 — Approval gate
Present all drafted diffs together. Apply **nothing** until Gary approves. He may accept, edit,
or reject each diff independently; apply only the approved diffs, exactly as approved.

## Report
Drafts only by default. Map the standard triplet as
[Files Changed: none (until approved) · Validation Status: n/a · New Decisions: none], then list:
items used this session, items with proposed edits (one-line reason each), and items reviewed but
left unchanged. If a friction signal points at the *project* rather than an agent — a real bug, a
decision, or a lesson — hand it to `/wrapup` instead of editing a SKILL.md here.

## Notes
- Standalone end-of-session workflow; runs independently of `/wrapup`. To make it part of the
  standard loop, add it as a sibling call in `/research-cycle` Step 4 (after `/wrapup`).
- It edits agent definitions, which are config, not research artifacts — but the same honesty
  rule applies: never record an unverified improvement as proven; describe what the evidence shows.