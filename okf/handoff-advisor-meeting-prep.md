---
type: Concept
title: "Handoff — advisor meeting prep, 2026-07-22"
description: "Two-part brief for Gary: a fast layout check on the refreshed site, then talk-through prep — the numbers to have at hand, the questions likely to be asked, and where the honest 'we don't know' boundaries sit. Delete after the meeting."
mutability: live
---

# Handoff — advisor meeting prep (2026-07-22)

**Temporary** — delete after the meeting.

Everything on the site is verified: hashes, tag balance, and every cited number checked against
committed JSON. What has *not* been checked is how it renders, and what you'll say about it.

---

# Part A — Layout check (~5 minutes)

```bash
open advisor-update-2026-07-22/index.html
```

**The two things most likely to be wrong**, because they're the widest elements on the page:

1. **The Q4 μ̄×n figure** (5 panels side by side) — in the card *"A small initial shock can
   snowball into a full collapse on a highly unequal network, but never on a more evenly-connected
   one."* It sits inside `.table-wrap`-style overflow handling and *should* scroll rather than
   squash. Check the panel titles (μ̄=0 … μ̄=0.4) are legible and the three caption lines under it
   aren't clipped.
2. **The 7-column ν table** — in *"Panic sharpens the network's tipping point faster as it
   grows."* Should scroll horizontally, not break the card.

**Sanity counts** (verified programmatically, confirm by eye): 4 chapters; 9 cards under
*Hypotheses & experiments*; 4 figures total; 1 item under *Open questions*.

**Also worth a glance:** the *Open questions* chapter should now contain **only** the publication
route. If you see anything about a sampler bug or about running a larger network size, the page
didn't save — both were closed by Tasks Q/X and W.

**Known cosmetic risk:** the Q4 figure is 13 inches wide at 200 dpi. On a narrow window it will
scroll. That's expected, not a bug — but if you'd rather it fit, say so and it's a one-line
`figsize` change plus a regenerate/re-embed.

---

# Part B — Talking it through

## The through-line

Last meeting left a set of open experiments. **Every one now has an answer**, and two of those
answers came back *negative* — which is the strongest thing on the page, because both negatives
were found by your own follow-up work rather than by a reviewer.

If you lead with one sentence, lead with the ignition result: **the τ=2.5 / τ=3.5 gate holds, and
within it, fear raises the ignition rate by up to ~3× without changing how that rate scales with
network size.**

## Numbers to have at hand

**Q4(iii) — the ignition gate (the headline)**
- τ=3.5: **0 systemic events in 3000 trials**. τ=2.5: ignites in every cell. The gate is stark.
- μ=0 series over n=4000→160000: 0.038, 0.024, 0.028, 0.018, 0.014, 0.012 — **trend z=−3.11,
  p=0.0019**.
- μ̄=0.4 series: 0.134 → 0.034 — **z=−7.51, p<10⁻¹³**.
- Multiplier vs control: **1.5× at μ̄=0.1, 1.9×, 2.6×, 3.2× at μ̄=0.4.** Constant **in n**,
  growing **in μ̄**. Do not say "constant 3× multiplier" flatly — that's the imprecision we fixed.
- Monotone increasing in μ̄ at every n; no threshold visible at 0.1 resolution.

**Q3 — transition width exponent ν** (7-point fit, n=1000..80000)
- **ν(μ=0) = 5.61 ± 0.18** (R²=0.953); **ν(μ=0.3) = 4.82 ± 0.15** (R²=0.978).
- Fear-accelerated sharpening holds; the μ=0 interval tightened from ±1.57 (3-pt) to ±0.18.

**Q4(i)/(ii) — the tilt results**
- C-Q4(i) tilt monotonicity **SUPPORTED cap-free**, including the γ=0→+1 leg that was previously
  artifact-blocked (7/7 μ̄ rows, both γ pairs).
- C-Q4(ii) size-biased collapse **REFUTED** — rescaling by μ* *increases* cross-γ spread
  (ratio 2.05). Plain μ̄ is what organizes the boundary.

**Q5 — duration and locality**
- C-Q5(ii) **SUPPORTED**: global-field decay is a stable sub-ballistic power law (slope −0.277 at
  μ̄=0.2, −0.291 at μ̄=0.4, both *steeper* than Task O's −0.255/−0.280 — moving away from control,
  so not a small-network artifact).
- C-Q5(iii) homogenization supported. C-Q5(i) nucleation law is an **honest negative** (constant
  leak, not the pre-registered g²), and its cross-round question is **open** (see below).

**Q6:** a single super-hub failing, even with panic concentrated on it, does not trigger a
cascade at r=2.

## Questions you should expect

**"Why does fear act as a multiplier rather than changing the scaling?"**
We don't know. It is a measured regularity across 25 cells, not a derived result — there's no
mechanism behind it yet. That's the honest answer, and it's a good one to have ready rather than
improvise. A natural follow-up to offer: it would be tested by checking whether the multiplier
survives a different graph family or a different threshold rule.

**"Didn't you say this was Θ(1) before?"**
Yes — on a three-point grid, where it was defensible. Extending to six points reversed it. Frame
it as the grid improving, not the story changing: the earlier caveat explicitly said three points
couldn't separate slow decay from a positive limit, and it was right to flag that.

**"Isn't ignition declining with n just what you'd expect at a bounded seed?"**
Plausible — the seed is a vanishing fraction of the network. But the pre-registered expectation
was "Θ(1) or growing," so the model isn't doing what was predicted. Don't retrofit the
prediction; say it came out differently and that's what the wider grid was for.

**"Why is C-Q5(i) still open after you built a test for it?"**
Because the test was structurally incapable of answering it — the metric selected nodes for being
far from prior failures, then asked whether they were near prior failures, which is impossible by
construction. Retired under D-035. This is a strong story: you caught a tautology in your own
instrument rather than publishing its null as a finding.

**If you mentioned the n≈20000 "shared crossover" to him previously — raise it yourself.**
Task W tested it and it doesn't hold; three independent series all fail to flatten. Better from
you than found by him.

## Where to say "we don't know"

Being crisp about these is worth more than hedging everywhere:

1. **No mechanism for the multiplier** (above).
2. **"Not flat" is not "decays to zero."** The trend test refutes Θ(1)-flatness. It does *not*
   distinguish decay to zero from decay to a small positive plateau. If he pushes on the
   asymptote, that's the honest boundary — the data rule out flat, not much more.
3. **Cross-round nucleation is unmeasured**, not measured-and-null. The valid instrument is a
   supra-r_n cross-K statistic (Task R "Option B"), deferred.

## The one decision to put to him

The site's *Open questions* chapter is down to a single item, and it's the real one:
**publication route — empirical (real network data + the fear channel, aiming at a
counterintuitive finding) vs. theoretical (simplified model + proof).** Everything else on that
list was closed. This is the question worth his time.

---

## Loose end you may want to close first

`docs/queue/reports/q3_nu_n10000_report.md` still shows **8.65 ± 1.04** and **4.54 ± 0.26** in
its result table with no supersession marker, even though `okf/status.md` records those as stale.
Its sibling `q4_ignition_report.md` got a SUPERSEDED note; this one didn't. Anyone opening it
sees retired numbers presented as current. Two-minute fix, same append-don't-rewrite treatment —
worth doing if he's likely to open the reports.

## After the meeting

1. Delete this file and drop nothing from the index (it was never indexed).
2. `okf/next-actions.md` should get whatever he decides on the publication route.
3. If the crossover retraction or the multiplier question generated follow-up work, queue it in
   `docs/queue/`.
