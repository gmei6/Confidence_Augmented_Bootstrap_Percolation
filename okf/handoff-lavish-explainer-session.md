---
type: Concept
title: "Handoff — Lavish explainer walkthrough, 2026-07-21"
description: "Resume Gary's card-by-card walkthrough of the advisor explainer in Lavish. Covers where he stopped, the misconceptions that keep recurring, the poll-loop mechanic the last session kept breaking, and the open threads. Delete once the walkthrough is done."
mutability: live
---

# Handoff — Lavish explainer walkthrough (2026-07-21)

**Temporary** — delete when the walkthrough finishes. Not indexed (handoffs never are).

**Advisor meeting is 2026-07-22.** Gary is reading a companion explainer card by card and
restating his understanding; the assistant corrects it. That is the whole loop. Resume it.

---

## 1. Resume the Lavish session — read this before anything else

```bash
lavish-axi                                          # lists open sessions
lavish-axi poll /Users/garymei/Downloads/projects/CABP/.lavish/advisor-explainer.html
```

Two files, **both gitignored** (`.gitignore:48`), so they are on disk but not in git:

| file | what it is |
|---|---|
| `.lavish/advisor-explainer.html` | the companion Gary is reading — **all the session's work** |
| `.lavish/advisor-site-review.html` | byte-identical copy of the real advisor site (SHA-256 `2ad38a44…`), for annotation only |

⚠️ **The real site `advisor-update-2026-07-22/index.html` was deliberately NOT rebuilt.** It is
verified (hashes, tag balance, every number checked against committed JSON). Gary asked for a
reconstruction; it was copied instead, to avoid destroying that verification the night before the
meeting. Keep it that way unless he says otherwise.

### The mistake the last session made three times

After reading an annotation, it answered **in the terminal only** and did not re-run
`lavish-axi poll ... --agent-reply "..."`. The browser then shows **"working…"** indefinitely and
Gary has to ask why. **Re-run the poll immediately after every reply, every time.** Answering in
chat is not enough — the page is a loop and it stays open until you close it.

### Known cosmetic issue, unfixed by choice

The layout audit reports the **real advisor site's hero `<h1>` clipped by 5px at a 792px
viewport** (`.hero h1 { line-height: 1.12 }`, italic serif descenders). The review copy was left
untouched to preserve the byte-identical guarantee. Gary knows; it is his call. One-line fix is
`line-height: 1.12` → `1.24`.

---

## 2. Where Gary stopped

Covered and understood: **configuration model + erasure**, **tilted fear (γ)**, **GIRG**,
**card 1** (global vs local fear), **card 2** (the ignition gate), **card 3** (tilt monotonicity).

**Next up: cards 4–9** — clock-collapse bias, ν / transition width, the single super-hub negative,
sub-ballistic decay, size-biased collapse refuted, and the tautological instrument (D-035).

---

## 3. Misconceptions that recurred — check for these actively

1. **τ direction inverted THREE times.** He has twice stated the heavy-tail case backwards, once
   as *"we'd be better off with τ=3.5 for a cascade"* — which inverts the headline result.
   **τ=2.5 = heavy tail = ignites. τ=3.5 = light tail = 0/3000.** The anchor that finally worked:
   *τ=3 is where a power law's second moment diverges; below 3 is wild, above 3 is tame.* Verify
   any statement he makes about τ before agreeing with it.
2. **Read computed values as measured.** He said *"when testing, we determined"* about
   Janson-formula predictions. Always mark derived numbers as derived when they sit beside
   simulation outcomes.
3. **Read "both rows decline" as "fear stops mattering."** Fear's impact is the **ratio** between
   the rows (~3.2×, no trend in n), not the level of either.

## 4. How he wants to be talked to — see `okf/lessons.md` §3, three entries tagged (S-058)

- **Plain language, but do not strip the terms.** He is a researcher who needs *sub-ballistic*,
  *finite variance*, *configuration model* in the room with Dhara. Gloss a term once, then keep
  using it. He pushed back on over-correction: *"I don't want the text to read like a
  middle-school explanation."* A metaphor is scaffolding, not a replacement.
- **State an objection before defending it.** One plain sentence saying what might be wrong, then
  stop until it lands. The last session named a confound in one compressed clause and spent four
  rounds defending it; Gary's reaction was *"I am beginning to believe continuing down this line
  is a waste of time,"* and he was right.
- **Weigh insurance against his time.** An objection the advisor has not raised is insurance. Say
  so before elaborating it further.
- **Tables: one row per condition, verdict in the row label.** He caught that a τ-as-columns table
  forces reading across, which is exactly when values get transposed — plausibly a contributor to
  the τ inversions.

---

## 5. Open threads

### ⚠️ NEW RESULT — fear DOES break the τ=3.5 gate at extreme μ̄. Assistant's prediction was wrong.

Gary asked for the degenerate case. A subagent swept μ̄ at τ=3.5, n=4000, seed a=2, **2000
trials/cell**. The assistant predicted zero everywhere. **It is not zero.**

| μ̄ | 0.4 | 0.6 | **0.8** | **0.9** | **0.95** | **0.99** | **0.999** |
|---|---|---|---|---|---|---|---|
| P(systemic) | 0.000 | 0.000 | **0.023** | **0.095** | **0.162** | **0.245** | **0.230** |

This **does not contradict** the committed 0/3000 — that only ever tested μ̄ ∈ {0, 0.4}, and the
pilot reproduces it exactly (0/2000 at μ̄=0.4). Everything at μ̄ ≥ 0.8 was simply never tested.

**But fear alone still cannot ignite.** The subagent isolated the channels by rerunning with
r=10⁹ (solvency unfireable):

| μ̄ | r=2, coupled | r=10⁹, fear only |
|---|---|---|
| 0.9 | 103/1000 | **0/1000** |
| 0.999 | 243/1000 | **0/1000** |

So `okf/lessons.md`'s "R_fear ≈ μ̄ < 1, fear is an amplifier not a primary igniter" is
**confirmed, not refuted** — each failure's total fear offspring is μ̄·Σwₖ = μ̄ exactly,
subcritical below 1 and merely *critical* at the 0.999 cap. **The correct framing: the gate holds
against fear alone; it does not hold against fear-plus-solvency at extreme μ̄.** A near-critical
amplifier manufactures its own supercritical seed for the r=2 channel.

**Main caveat — the effect drifts down with n:** 0.230 (n=4000) → 0.202 (10000) → 0.154 (20000).
Three points cannot rule out decay to zero. *Do not repeat the Θ(1) mistake here.*

Also confirmed: water-filling is a **no-op at γ=0** (`graphs.py:115-122` takes the
`mu_d = np.full(n, mu_bar)` branch; `cap_hits=0`, `realized_mu_bar=0.999`), answering Gary's
redistribution question — redistribution is not what limits anything at γ=0. And the mean-field
formula checks out: predicted first-round fear failures 0.3996, measured 0.3910.

**Status: EXPLORATORY.** Nothing in `results/`, no committed config, no stamped seed, no
`/verify`. **Not a §5.6 result, must not be cited as one.** The established finding remains the
committed 0/3000 at μ̄ ∈ {0, 0.4}. To promote it: configs at τ=3.5 for μ̄ ∈ {0.6…0.99}, a
runner-owned stamped run, and an n-arm to 50k–100k at μ̄=0.999 to settle the drift.
Scripts: `$CLAUDE_JOB_DIR/tmp/fear_gate_pilot.py`, `mech.py`.

⚠️ **Gary must not say "fear cannot override the gate" flatly at the meeting.** It is true of the
fear channel in isolation and false of the coupled system above μ̄≈0.8. Note μ̄≥0.8 means
essentially every bank at maximum panic — an extreme regime, not a realistic one.

### OPEN QUESTION (Gary's, 2026-07-21) — "systemic" (θ=0.5) is not Janson percolation

Gary raised that Janson defines percolation as reaching **n − β** with β = o(n) (the nodes with
fewer than r edges, which can never activate via solvency). This project instead calls a run
systemic at `final_failed_fraction ≥ θ = 0.5`. Those are **not the same criterion**, and the gap
is large. Measured this session:

| | value |
|---|---|
| β (realized degree < r=2), n=4000 | ~9 nodes = **0.21%** of n |
| β, n=20000 | ~15 nodes = **0.08%** of n → genuinely o(n), Janson's condition holds |
| structural ceiling n−β | ~**99.8%** of n |
| **max fraction any cascade actually reached**, μ=0 | **0.732** |
| **max**, μ̄=0.4 | **0.8975** |

Outcomes are cleanly **bimodal** — either <1% or >50%, nothing between (n=4000: 481/500 died at
μ=0; the survivors sit at 0.50–0.73). **So θ=0.5 is operationally harmless** — any threshold in
(0.01, 0.50) gives identical ignition numbers, and nothing quoted this session is
threshold-sensitive.

**But the cascades stop ~25 points short of the structural ceiling, and not because the survivors
are incapable** — most have degree ≥ 2. The run hits an intermediate absorbing state: survivors
have fewer than r failed neighbours, the window empties, it halts. **By a strict Janson criterion
almost none of these runs percolate at all.**

⚠️ **No mechanism is claimed for the 73%.** Partial activation is a known feature of bootstrap
percolation on heavy-tailed graphs (active set converges to a fixed point of a recursion that need
not be everything), but that has *not* been checked against these parameters. Observation solid,
explanation open — do not let a plausible story get written up as a finding (`okf/lessons.md` §3).

**Cost to test: near zero.** Every raw file stores `failed_fractions[]` per trial (see
`docs/queue/README.md` — θ re-thresholding needs no re-runs). Re-analysing every committed sweep
against an n−β criterion is an analysis script over data already on disk, not a new sweep.

**Why it matters for the meeting:** Dhara is a configuration-model percolation theorist. "What do
you mean by systemic?" → "half the network" invites "why not n − o(n)?". Better raised by Gary
with β already measured. It is also a real research question — is the ~73% stable in n, does fear
raise it (0.73 → 0.90 suggests yes), does it match the theoretical fixed point? That is
theoretical-route material.

**Task Y retracted** (`ce9f9b0`) — its pre-registered w₁ test does not discriminate; falsified by
pilot the same day it was queued. Correction appended, not rewritten. See `okf/next-actions.md`
item 4.

**Task Z queued** — wider γ grid, `okf/next-actions.md` item 3.

**Not yet done:** three reports still carry superseded numbers with no marker —
`task_n_phase2_report.md:14`, `task_n_report.md:18`, `task_a_report.md:25-26`. The third is a
judgment call: D-036's citation ban names the S-048 and Task T values but not the 3-point ones.

---

## 6. Git state

Three commits tonight, **none pushed**: `4408f4a` queue hygiene, `c179e0d` lessons,
`ce9f9b0` Task Y retraction + Task Z. Working tree clean except untracked `docs/human_notes/`
(one empty 0-byte file, deliberately left out).

## 7. What Gary actually needs before the meeting

Model diagram, the τ orientation panel, the headline numbers, the four "we don't know"s, and the
publication-route question — **the only item where Dhara's answer changes what happens next**.
Everything else is detail he can look up if asked.
