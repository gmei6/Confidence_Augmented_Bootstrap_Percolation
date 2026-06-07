---
name: harden
description: Bounded review-and-fix loop for one existing target. Runs reviewer/critic review, fix, re-review in a worktree until sign-off or a 5-round cap, then the /verify auditor gate, then one diff for approval. Not for planning new work.
---

# Harden

Iteratively hardens a TARGET the user names in the prompt. Honor all guardrails in
GEMINI.md and AGENTS.md throughout. This loop edits real files, so it runs isolated
and converges to a single approval — it does NOT ask for approval every round.

## Step 0 — Setup
1. Read `docs/PROJECT_TRACKER.md` (§2 North Star, §8 Status, plus the §3/§5 sections
   relevant to the TARGET) and `docs/LESSONS_LEARNED.md`.
2. Confirm the TARGET in one line and name the Q#/F#/D# it touches. If the TARGET is
   `reference.py`, a 🔒 frozen tracker section, or anything under `results/`, STOP —
   those require a standalone, explicitly approved instruction, not this loop.
3. Enter **New Worktree Mode** so all edits stay isolated from the validation baseline.
4. Establish the baseline: run the pytest suite (and, if the TARGET is C++, the
   `cross-validation` skill). Record the starting state; if the baseline is already
   broken, report that and STOP before changing anything.

## Step 1 — Loop (max 5 rounds; stop early on sign-off)
For each round `i = 1..5`:

1. **Review (blind, fresh).** Spawn a NEW `reviewer` and a NEW `critic`, each with no
   memory of prior rounds, so each critique is unbiased. Give them the current TARGET and
   the relevant tracker sections. The `reviewer` returns ranked design/contract/edge-case
   issues; the `critic` returns failures/breakages, coverage gaps, memory/complexity and
   C++ portability issues — or they sign off.
2. **Stop check.** If the review raises no material issue (only nits or an explicit
   sign-off), exit the loop and go to Step 2. Do not keep editing a clean target.
3. **Fix.** The orchestrator delegates the material issues to the necessary agents —
   `python-simulation`, `cpp-engine`, `research-analysis`, or `documentation-publishing`
   — by ownership. Apply edits in the worktree only.
4. **Guardrail abort.** If addressing an issue would require editing `reference.py`, a
   frozen section, or writing to `results/` directly, do NOT do it — stop the loop and
   surface the issue for a human decision instead.
5. **Gate.** Re-run pytest (and the `cross-validation` skill if C++ changed). The round
   is not complete until the gate is green; if a fix breaks the suite, revert that fix
   within the round before continuing.

Record each round's critique, the fixes applied, and the gate result for the walkthrough.

## Step 2 — Converge and hand off
1. Produce one consolidated **diff** of all worktree changes versus the baseline.
2. **Integrity gate.** Spawn a blind `auditor` (Step 3 of `/verify`) over the converged
   change. Do not proceed to the approval gate until it returns AUDIT PASS; on FAIL, route
   its required-to-pass list back into the loop.
3. Summarize: rounds run, issues found vs. resolved, any guardrail aborts, the auditor
   verdict, final validation status, and any issue the loop deliberately left for the human.
4. **Single approval gate:** present the diff to Gary. Apply to the main branch only
   after explicit approval. Nothing merges automatically.
5. After approval, invoke `session-wrapup` to draft §8–§10 / §11 / §12 updates and any
   `LESSONS_LEARNED` additions (drafts only, per the §14 protocol).

## Notes
- The cap of 5 is a ceiling, not a target — most targets converge in 1–2 rounds.
- Pass each round's `walkthrough.md` context to the next round's gate, but NOT to the
  next round's adversary (keep the adversary blind).
- For planning new work rather than hardening existing work, use `/research-cycle`.
