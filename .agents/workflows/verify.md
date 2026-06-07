---
name: verify
description: Three-agent verification gate: Reviewer (design), Critic (adversarial tests + §5.4), then a blind Auditor (binary §5.6 integrity gate, must pass before done). Replaces the old adversarial-review step in /research-cycle and /harden.
---

# Verify

The three-agent verification gate for the TwoCascade project. Replaces the old single
`adversarial-review` invocation with a separation of concerns: **design** (reviewer),
**robustness** (critic), and **integrity** (auditor). Honor all guardrails in GEMINI.md
and AGENTS.md throughout. This workflow proposes and validates; it does not apply
tracker edits (that is the PI via §14).

**Input:** the `walkthrough.md` and the diff from the preceding `/execute` or `/harden`
session, plus the plan/spec the change claims to satisfy.

## Step 0 — Context
Read `docs/PROJECT_TRACKER.md` (§2, §5.4, §5.6, plus the §3/§5 sections relevant to the
change) and `docs/LESSONS_LEARNED.md`. Restate the change in one line and name the
Q#/F#/D# it touches.

## Step 1 — Reviewer (design & contracts)
Spawn a **blind, fresh** `reviewer` with the diff, walkthrough, and spec. It returns
ranked design/contract/edge-case issues or signs off.
- If material design issues are found, route them back to the owning agent
  (`python-simulation` / `cpp-engine`) for a fix, then re-run this step. Do not proceed
  to the Critic on a design that is known-wrong.

## Step 2 — Critic (robustness & cross-validation)
Spawn a **blind, fresh** `critic`. It writes/runs adversarial tests, probes boundary and
memory failures, and — if C++ changed — runs the `cross-validation` skill's two prongs.
- Material breakages route back to the owning agent for a fix; re-run Step 2 after.
- Bit-identical C++/Python output is never required (§5.4).

> Steps 1–2 are the loop that `/plan` and `/harden` already run round-to-round. Inside
> those loops, spawn the `reviewer` and/or `critic` directly and skip Step 3 until the
> final convergence. Run the full /verify (including the Auditor) **once**, at the end.

## Step 3 — Auditor (integrity gate; mandatory, runs last)
Once Reviewer and Critic are satisfied, spawn a **blind** `auditor` — independent of the
prior two agents' findings. It verifies the §5.6 Definition of Done and §5.4 prongs
actually hold from artifacts on disk, checks for laziness/fabrication, and confirms no
LESSONS_LEARNED trap or oracle violation.
- **AUDIT FAIL → the change is not done.** Surface the auditor's required-to-pass list,
  route fixes to the owning agents, and re-run from the lowest affected step. Never
  override a FAIL.
- **AUDIT PASS →** the change is eligible to be marked done.

## Step 4 — Hand off
Summarize: reviewer issues found/resolved, critic breakages found/resolved, the auditor
verdict and evidence, and any item deliberately referred to a human. Pass this summary to
`/wrapup`, which drafts the §8–§10 / §11 / §12 updates (drafts only; PI applies via §14).

## Notes
- Keep each agent **blind**: do not feed the reviewer's report to the critic, or either to
  the auditor. Independence is the point.
- The cap and fix-routing mirror `/harden`; this workflow is the *verification* half, not a
  planning loop. For new work, use `/research-cycle`.
