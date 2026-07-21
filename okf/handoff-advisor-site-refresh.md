---
type: Concept
title: "Handoff — advisor-update-2026-07-22 site refresh"
description: "Task-scoped handoff for updating advisor-update-2026-07-22/index.html: exact stale claims with line numbers, correct replacement values, and what must not go on the site. Delete once the refresh ships."
mutability: live
---

# Handoff — `advisor-update-2026-07-22/index.html` refresh

**Purpose.** Everything needed to start the site refresh in a fresh session without re-deriving
context. **Temporary** — delete this file once the refresh ships and the email goes out.

**Prerequisite state (already true as of `b24f9c9` on `antigravity`):** the queue is empty, all
results are gated, and `okf/next-actions.md` item 1 carries the correct numbers. Nothing needs to
be run or verified before starting.

---

## 1. Working with the file (read this first)

`advisor-update-2026-07-22/index.html` is **1.5 MB**, but only **~40 KB is real content** — the
rest is 3 base64-embedded PNGs. **Do not read it whole**; it will consume the context window
before any work begins.

Strip the base64 into the scratchpad and work from that:

```bash
sed 's/data:image\/png;base64,[A-Za-z0-9+/=]*/[IMG]/g' \
    advisor-update-2026-07-22/index.html > /tmp/site_nobase64.html
```

Then edit the **real** file with targeted `Edit` calls against exact strings. Line numbers below
refer to the stripped version but the surrounding text is unique enough to match directly.

**Structure:** one `<h1>` + 4 chapters — *Implementation ideas that changed*, *Hypotheses &
experiments*, *Scope decisions*, *Open questions & decisions needed*. Cards are `<details>`
blocks. Site was built S-051-era (2026-07-17) via Ultraplan and predates Tasks Q/R/S/T/U/V/W/X.

**Note the HTML uses entities** (`&mu;`, `&plusmn;`, `&tau;`, `&#772;` for the μ̄ macron,
`&rarr;`). Match the existing convention when editing.

---

## 2. Confirmed stale claims — with locations

### 2a. The Θ(1) caveat — `~line 748-754`, "Hypotheses & experiments"

Current text (a `<div class="callout">`):

> **Caveat** At μ̄=0.4 the τ=2.5 branch *decreases* with *n* (0.134→0.062). Θ(1) behavior is only
> clean at μ=0; three *n* points can't separate slow decay from a positive limit, so this needs a
> wider *n*-grid before citing the μ̄>0 direction.

**Status: SUPERSEDED.** The wider n-grid was run. Replace with the settled result:

- The branch declines **0.134→0.116→0.062→0.050→0.044→0.034** over n∈{4000..160000}.
- **μ=0 is NOT Θ(1)-flat** — counts 19,12,14,9,7,6 /500, Cochran–Armitage trend **z=−3.11,
  p=0.0019** (committed in `results/processed/q4_ignition_analysis.json`, `trend_test_full`).
- The decline is present at **every** μ̄ **including 0**, so it is **not fear-specific**. Fear acts
  as an approximately **constant ~3× multiplier** on ignition rather than changing its n-scaling.
- Ignition is **monotone increasing in μ̄** at every n (no threshold at 0.1 resolution).

This is a strictly better story than the caveat it replaces: an open worry becomes a clean
characterization of what fear does.

### 2b. The ν table — `~line 871-879`, "Hypotheses & experiments"

Current table reads `ν (4-pt, n≤10000)` vs `ν (earlier, 3-pt)`:

| μ | 8.65 ± 1.04 | 8.39 ± 1.57 |
| 0.3 | 4.54 ± 0.26 | 5.33 ± 0.51 |

**Status: SUPERSEDED** (these are S-048-era values). Current committed fit is **7-point**,
n∈{1000..80000}, from `results/processed/task_a_nu_n10000.json`:

- **ν(μ=0) = 5.61 ± 0.18** (R² = 0.953)
- **ν(μ=0.3) = 4.82 ± 0.15** (R² = 0.978)

Fear-accelerated sharpening still holds and is now far tighter. ⚠️ Do **not** cite either the
8.65/4.54 pair **or** Task T's intermediate n=20000 pair (6.29±0.39, 4.90±0.22) — both retired
under **D-036**. Widths keep shrinking through n=80000 with residuals not one-signed.

### 2c. "Open questions" chapter — 2 of its 3 items are resolved

- ❌ *"A sampler bug currently caps how much panic can concentrate on the best-connected banks…
  needs a fix before those cases can be tested at all."* → **RESOLVED.** Task Q fixed it
  (iterative water-filling, merged `c4ef634`), and Task X then confirmed the γ=0→+1 tilt leg is
  cap-free and supports C-Q4(i). Move to results; C-Q4(ii) size-biased collapse was **refuted**.
- ❌ *"Whether to run an even larger network size to further tighten the confidence interval…
  nothing is queued yet."* → **RESOLVED.** Task W ran it; the 7-point fit in 2b is the answer.
- ✅ *"Publication route still undecided: empirical vs. theoretical."* → **genuinely still open**,
  keep as-is. This is the one real decision to put to Prof. Dhara.

---

## 3. ⚠️ Do NOT put this on the site

**There is no "shared n≈20000 crossover."** Two series appeared to flatten after n=20000, and
that looked like a citable cross-experiment finding. **Task W tested exactly this and concluded
the opposite:** not a shared crossover — ν widths, ignition point estimates, and the Task U slope
**all fail to flatten**. The earlier "same flattening pattern / notable cross-experiment
observation" framing is **retracted**.

Likewise do not carry the "finite-size transient flattening after n=20000 (χ²=1.70, p≈0.43)"
reading — it came from a single 500-trial series and does not survive doubling the trials.

This is the single highest-risk item in the refresh: it is the most *interesting-sounding* claim
in the recent record and it is false.

---

## 4. New results worth adding

Nothing here is required, but all of it is gated and citable:

- **Task X (C-Q4):** tilt monotonicity C-Q4(i) SUPPORTED cap-free including the γ=0→+1 leg;
  **C-Q4(ii) size-biased collapse REFUTED** (μ* *increases* cross-γ spread, ratio 2.05 — μ̄, not
  μ*, organizes the boundary). `docs/queue/reports/task_x_report.md`.
- **Task R (C-Q5(i)):** the cross-round strict-r_n-clique metric is **structurally blind** — a
  tautology of the measurement, not a physics result; z-test retired (**D-035**). C-Q5(i)
  cross-round question stays **OPEN**. A good "what we learned by being careful" item.
  `docs/queue/reports/task_r_cross_round_report.md`.
- **Task U (C-Q5(ii)):** global-field sub-ballistic decay is a **stable power law** (slope −0.28
  vs Task O's −0.26, moving away from control); C-Q5(ii) SUPPORTED robustly at large n.
- **Known-defects list:** the `plot_fear_field_concentration` savefig/close bug is fixed
  (`df0575d`) — drop it if the site lists it.

---

## 5. Figures

Convention: base64-embedded, 3 currently present (alt text: tilt monotonicity at n=10000;
clock-collapse bias; finite-size scaling of the transition width).

- **`results/figures/finite_size_scaling_r2_n10000.png` — re-embed.** Verified regenerated
  `Jul 18 19:01`, same minute as the 7-point `task_a_nu_n10000.json`, so it **is** the 7-point
  figure. Filename kept for lineage continuity despite the `n10000` suffix. Untracked by design
  (`9497425`), regenerable.
- A **Q4 μ̄×n ignition-map figure** does not exist and would be the strongest new visual — the
  monotone-in-μ̄ / declining-in-n grid is the session's cleanest result. Would need generating via
  the runner/plotting path; **do not hand-write into `results/`**.

---

## 6. One judgment call

The pooled **z=−3.31, p=0.0009** (μ̄=0.4, n≥20000, from pooling Task V's independent replicate)
is the strongest version of the "still declining" claim, but it is **unverified** — it carries no
AUDIT PASS and is not regenerable from a committed script (`scripts/analyze_q4_mumap.py` emits
the p-grid and Wilson intervals but no inferential layer).

- **To cite it:** fold the inferential layer into `analyze_q4_mumap.py`, then run `/verify`.
- **To avoid the work:** cite Task W's gated **z=−2.12, p=0.034** instead, which W's own critic
  recorded as marginal and endpoint-sensitive.
- **Or:** cite neither and use the μ=0 trend test (**z=−3.11, p=0.0019**), which *is* committed
  and gated, and which carries the more interesting claim anyway (the decline is not fear-specific).

The third option is cheapest and strongest. Details in `docs/queue/reports/task_v_report.md`.

---

## 7. After the refresh

1. **Email Prof. Dhara** (`okf/next-actions.md` item 2) — send once the site is updated so the
   email and the leave-behind tell the same story.
2. **Delete this handoff file** and drop its index line.
3. If a Q4 figure was generated, note it in `okf/status.md`.
