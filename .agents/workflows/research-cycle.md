---
name: research-cycle
description: Primary entry point for the TwoCascade project. Runs one full Plan → Execute → Verify research cycle with human approval gates and the propose-don't-write guardrails.
---

# Research Cycle

The standard loop for any change to the TwoCascade project. Run this for every
non-trivial task. Honor all guardrails in GEMINI.md and AGENTS.md throughout.

## Step 0 — Context load (always)
1. Read `docs/PROJECT_TRACKER.md` — §2 North Star, §8 Status, §9 Open Questions,
   §10 Next Actions, plus the §3/§5 sections relevant to the task.
2. Read `docs/LESSONS_LEARNED.md` and cross-reference the task against known pitfalls.
3. Restate the task in one line and name the research question (Q#) or conjecture (F#/D#)
   it touches. If the task conflicts with the North Star or a prior decision, STOP and
   surface the tension before going further.

## Step 1 — Plan (propose only)
1. Call `/plan` to draft and red-team the implementation plan (≤5 rounds, fresh blind
   adversary each round; proposes only, edits nothing).
2. **Approval gate:** present the Final Brief to Gary. Do not proceed until he approves.

## Step 2 — Execute (only after approval)
1. Call `/execute` to implement the approved plan. It delegates to `python-simulation`
   and/or `cpp-engine`, presents every diff for approval before writing, and never touches
   `reference.py`, frozen sections, or `results/` directly.

## Step 3 — Verify
1. Call `/verify`, which runs the three-agent gate: `reviewer` (design & contracts) →
   `critic` (adversarial tests, and the `cross-validation` skill's two prongs if C++ was
   touched) → `auditor` (the mandatory §5.6 / §5.4 integrity gate).
2. The Auditor verdict is binary. Do not mark done until it returns AUDIT PASS; on FAIL,
   route its required-to-pass list back to the owning agents and re-run.

## Step 4 — Wrap up
1. Call `/wrapup` to draft §8–§10 live-state updates, append-only §11/§12 entries, and any
   LESSONS_LEARNED additions — drafts for Gary's approval.
2. Only the orchestrator (PI) applies approved tracker edits, via the §14 protocol.

## Notes
- Pass the `walkthrough.md` from Step 2 as input context when calling `/verify`.
- Prefer New Worktree Mode for any change to `src/` or `cpp/src/`.
- For long multi-step runs, invoke `/self-succession` at the budget threshold so context
  limits don't degrade the orchestration.
