---
type: Session Change
title: "S-059: Advisor-explainer walkthrough (cards 4–9); Task P demoted (D-037)"
mutability: append-only
timestamp: 2026-07-21
tags: [advisor-prep, explainer, lavish, task-p, demotion, q6, lessons]
---

# S-059: Advisor-explainer card-by-card walkthrough; Task P demotion

Continued Gary's card-by-card walkthrough of `.lavish/advisor-explainer.html` in Lavish (resume
of the `okf/handoff-lavish-explainer-session.md` handoff), covering cards 4–9 and the foundations.
Gary restated each card; each was corrected against committed data before agreeing. All corrections
were written back into the HTML via the Lavish poll loop (`--agent-reply`).

## Card outcomes (full per-card record in `okf/cache/advisor-explainer-walkthrough-2026-07-21.md`, temporary)

- **Card 4 (clock-collapse):** implication validated, not the assumption; a_k=o(n) is false at
  macroscopic generations. Clarified power-form = shortcut/theory, product-form = what the sim runs
  (`reference.py:162-164`); substitution buys independence, not speed. ΔP is derived, not measured.
- **Card 5 (ν / width):** ν is about the slope, not the width at fixed n; per-n table shows fear
  makes the window 16% WIDER at n=1000 (4.4σ), sign flips across n; robust signal only in the slope
  (ν 5.61→4.82). ν is inverted and is not lattice ν.
- **Card 6 (super-hub): DEMOTED → D-037.** Outcome is forced by arithmetic (single seed vs r=2), not
  measured; hub degree irrelevant; `hub fear=1.0` causally inert. Retitled "Single-seed sanity check,"
  do-not-present banner added. Q6 reopened. `okf/status.md` and `okf/open-questions.md` updated.
- **Card 7 (sub-ballistic):** it is duration (ballistic ratio), not cascade probability; slope runs
  in n at fixed μ̄; "slope decreased" is a sign-trap. Gary's revised reading ("fear speeds up the
  collapse") confirmed correct.
- **Card 8 (size-biased): explained in full (genuine REFUTED).** μ* re-indexing inverts the ordering
  (spread 1.51→3.11, ratio 2.05); magnitude grid-limited, sign robust. Answered Gary's "I don't see
  the value": μ* is the quantity the analytic edge-map forces (`q4_config_model_scoping.md` §5, vdH
  Vol II) — conditional insurance aimed at Dhara, back-pocket not slide.
- **Card 9 (tautological instrument):** was next in queue at session close; tie to the D-035/D-037
  tautology pair when walked through.

## Task P demotion (D-037)
`okf/decisions/d-037-demote-task-p-super-hub.md` written (append-only). Task P's "super-hub
insufficient" claim demoted from a negative result to a sanity check — the outcome is parameter-forced
(seed size a=1), the hub's degree never enters, and provenance (single GIRG run, no ensemble) never
met §5.6. Q6 returned to OPEN. `s-044`'s original entry is superseded by D-037, not edited.

## Lessons (`okf/lessons.md` §5, two new entries)
1. A result forced by the parameters is not a finding — name the input you'd have to change to get a
   different answer; if it's one you never varied, the run demonstrated a rule, not a phenomenon.
   Explicit *parameter-forced* sibling of the S-057 *selection-forced* tautology.
2. A statement about a rate is not a statement about a level (ν slope vs width); print the per-cell
   values the fit was made from; name the variable every claim is stable in; ν/τ/slopes are inverted —
   state the plain-language effect first, signed number second.

## Live files touched
- `okf/status.md` (Task P line → DEMOTED), `okf/open-questions.md` (Q6 → OPEN), `okf/lessons.md`
  (§5 ×2), `okf/cache/advisor-explainer-walkthrough-2026-07-21.md` (new, temporary) + `cache/index.md`,
  `okf/next-actions.md` (item 2 layout-check BLOCKED on Chrome extension; item 2b HTML restructure).
- `.lavish/advisor-explainer.html` — cards 4–8 corrected in place (gitignored; not a src/results/okf edit).

## Open at session close
- **Layout eyeball of the real site (next-actions #2): BLOCKED** — Chrome extension not connected.
- **HTML restructure (next-actions #2b):** Gary's plan; cache file is the source of truth.
- **Card 9** not yet walked through.
- **`docs/queue/reports/task_p_report.md`** given an appended SUPERSEDED-by-D-037 note (not rewritten).
- **`okf/handoff-lavish-explainer-session.md`** — the handoff says to delete when the walkthrough is
  done; walkthrough is complete but card 9 pending, so left in place. Deletion needs Gary's ok.

## [Files Changed · Validation Status · New Decisions]
- **Files:** +`okf/decisions/d-037-*.md`, +`okf/cache/advisor-explainer-walkthrough-2026-07-21.md`,
  +this change file; edits to `okf/status.md`, `okf/open-questions.md`, `okf/lessons.md`,
  `okf/next-actions.md`, `okf/cache/index.md`, `okf/decisions/index.md`, `.lavish/advisor-explainer.html`,
  `docs/queue/reports/task_p_report.md` (appended note).
- **Validation:** N/A — no `src/`, `cpp/src/`, config, or `results/` change; no new simulation run.
  All corrections cite already-committed artifacts (`task_a_nu_n10000.json`, `task_o_duration_report.md`,
  `task_x_report.md`, `task_p_report.md`).
- **New Decisions:** D-037 (demote Task P; reopen Q6).
