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
1. Invoke the `plan-refinement` agent.
2. It drafts a step-by-step plan and red-teams it (≤5 iterations) against algorithmic/
   memory risks, edge cases, C++ portability, and testing blindspots.
3. Output the Final Brief: proposed §11/§12 entries, the implementation plan, and the
   debate summary. For any C++ change, state whether the Python reference needs a parallel
   update; for any Python change, state whether C++ parity is in scope.
4. **Approval gate:** present the plan to Gary. Do not proceed until he approves.

## Step 2 — Execute (only after approval)
1. Invoke the `plan-execution` agent to drive the approved changes.
2. Delegate code to `python-simulation` and/or `cpp-engine`. Never modify
   `src/twocascade/reference.py` (the oracle) as a side effect — if implicated, STOP and ask.
3. Never write to `results/raw/` or `results/figures/` directly — the runner script owns
   all output and stamps seed + params + commit hash.
4. Present every diff in chat and get explicit permission before writing to disk.

## Step 3 — Verify
1. Invoke the `adversarial-review` agent.
2. If the C++ engine was touched, load the `cross-validation` skill and run its two
   prongs: identical failed set at μ=0, plus statistical agreement of P(systemic) and
   |A*|/n within Monte Carlo error for μ>0.
3. Load the `reproducible-run` skill and confirm every item of its §5.6 Definition-of-Done
   checklist holds. Do not mark done until all hold.

## Step 4 — Wrap up
1. Invoke the `session-wrapup` agent.
2. It drafts §8–§10 live-state updates, append-only §11/§12 entries, and any
   LESSONS_LEARNED additions — as drafts for Gary's approval.
3. Only the orchestrator (PI) applies approved tracker edits, via the §14 protocol.

## Notes
- Pass the `walkthrough.md` from Step 2 as input context when invoking `adversarial-review`.
- Prefer New Worktree Mode for any change to `src/` or `cpp/src/`.
