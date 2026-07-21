# Task W — Shared finite-size crossover: push the two flattening series past n=20000

**Queued:** 2026-07-18. **Questions:** Q3 (ν width-exponent) **and** Q4(iii) (ignition branch) —
this task tests a **cross-experiment** observation that spans both, so it names both.

## The observation this task is built on

Two independent series measured this session **both flatten after n=20000** (see
`okf/next-actions.md` item 1):

- **Q3 ν (Task T):** ν(μ=0) dropped 8.65±1.04 → 6.29±0.39 when n=20000 was added, but the μ=0.3
  **width itself nearly stopped shrinking** between n=10000 and n=20000 — the finite-size width
  is bending, not continuing its power-law descent.
- **Q4 ignition (Task S):** the μ̄=0.4 branch declines 0.134 → 0.116 → 0.062 → 0.050 → 0.044 over
  n∈{4000..80000}, and a homogeneity χ² on the n≥20000 triple gives p≈0.43 — i.e. it has
  **flattened** to a roughly constant value after n=20000 rather than decaying to zero.

Two unrelated observables bending at the **same n≈20000** is either (a) a genuine shared
finite-size crossover scale $n^\*$ in this model — a real, citable, slightly surprising result —
or (b) a coincidence of two separate transients. **The only way to tell them apart is more n.**
A single flattening series is anecdote; two series that flatten and then track a common $n^\*$ as
n grows is a finding. That is the whole point of this task.

## Autonomous-safe: YES for the Q3 leg / WITH-A-CHECK for the Q4 leg

No `src/` or `cpp/src/` changes. New configs + **one-line edits to two existing read-only-on-raw
analysis scripts**. Local Mode. Gate at `/verify` afterward.

- **Q3 leg (C++ engine): cheap, fully autonomous-safe.** The C++ engine is already built
  (`cpp/build/twocascade_run`, per Task T) and finite-size runs are fast; n=40000 is routine.
- **Q4 leg (Python engine): safe but check the budget.** n=160000 configuration-model sampling +
  cascade at 500 trials is ~2× the n=80000 Task S point (which ran fine overnight). Time one
  n=160000 cell first; if it is impractical, run the leg at n=160000 with `trials_per_cell=300`
  (report the reduced count) rather than dropping the point — the extra n-lever matters more than
  the last 200 trials here.

## Method — two legs plus a synthesis

### Leg 1 — Q3 ν, extend to n=40000 (and optionally 80000)

**New config `configs/finite_size_r2_n40000.json`:** byte-for-byte copy of
`configs/finite_size_r2_n20000.json`, changing only `pinned_params.n` → `40000` and
`output.raw_filepath` → `"results/raw/finite_size_r2_n40000.json"`. Everything else identical and
**unchanged**: `engine="cpp"`, `n_ref=1000`, `target_mean_degree=8.0`, `alpha=0.7`,
`window_len=1`, `weights=null`, the 17-point `seed_multiples` grid (0.6…1.4), `trials_per_cell=1000`,
`base_seed=202607041`. (Same scaling invariant, same seed — only n moves, per the
`docs/queue/README.md` guidance.)

Run:

```
arch -arm64 python3 -c "import sys; sys.path.insert(0,'src'); from twocascade.runner import run_sweep; run_sweep('configs/finite_size_r2_n40000.json')"
```

Then **re-fit ν** by adding the new point to `scripts/analyze_q3_nu.py`:

- Edit the one line `N_LIST = [1000, 2000, 5000, 10000, 20000]` → `[..., 40000]`.
- (Optional second point: also create `configs/finite_size_r2_n80000.json` the same way and add
  80000 to `N_LIST` — do this only if Leg 1's n=40000 fit still looks power-law-ish and a sixth
  point would sharpen the crossover call. C++ at n=80000 is still tractable.)
- Re-run `arch -arm64 python3 scripts/analyze_q3_nu.py`. It regenerates
  `results/processed/task_a_nu_n10000.json` and the figure
  `results/figures/finite_size_scaling_r2_n10000.png` (filenames kept for lineage continuity —
  see that script's docstring; `metadata.n_list` records the real grid). It prints ν(μ=0),
  ν(μ=0.3), CIs, and R². **Do not hand-edit `results/`.**

**What to look for:** does the log w vs log n relation stay linear (constant ν → no crossover, the
n=10000→20000 bend was noise), or does the width visibly **bend away from the power line** at
n≥20000 (a crossover)? Report R² and whether the residuals at the large-n points are one-signed.

### Leg 2 — Q4 ignition μ̄=0.4, extend to n=160000

**New config `configs/q4_ignition_tau25_n160000.json`:** copy of
`configs/q4_ignition_tau25_n80000.json`, changing:

- `pinned_params.n` → `160000`
- `sweep.seed_multiples` → **`[0.0036758]`** (this is the value that forces the bounded seed
  `a=2` at n=160000: it was computed as `2 / janson_a_c(160000, p, r)` the same way as the
  existing n=40000/80000 points, and verified `round(0.0036758 · a_c0) = 2` with a_c0≈544.09).
- `output.raw_filepath` → `"results/q4_ignition_tau25_n160000_raw.json"`

Everything else identical: `engine="python"`, `mean_fear_grid=[0.0, 0.4]`, `trials_per_cell=500`
(or 300 per the budget note above), `base_seed=42`, `n_ref=10000`, `target_mean_degree=4.0`,
`alpha=0.6`, `graph={configuration_model, tau: 2.5, d_min: 2}`, `fear={gamma: 0.0}`.

> **Verify the seed multiple before the full run** (a wrong value silently gives a=3, invalidating
> the comparison). Run this and confirm it prints `2`:
> ```
> arch -arm64 python3 -c "import sys; sys.path.insert(0,'src'); from twocascade.model import calculate_beta, calculate_p_n, janson_a_c; b=calculate_beta(4.0,10000,0.6); p=calculate_p_n(b,160000,0.6); print(round(0.0036758*janson_a_c(160000,p,2)))"
> ```

Run:

```
nohup arch -arm64 python3 -c "import sys; sys.path.insert(0,'src'); from twocascade.runner import run_sweep; run_sweep('configs/q4_ignition_tau25_n160000.json')" > task_w_leg2.log 2>&1 &
```

Then add n=160000 to the ignition analysis:

- Edit `scripts/analyze_q4_ignition.py`: `N_GRID = [4000, 10000, 20000, 40000, 80000]` →
  `[..., 160000]`. (Leave `N_GRID_BY_TAG["tau35"]` alone — τ=3.5 has no wide-n data.)
- Re-run `arch -arm64 python3 scripts/analyze_q4_ignition.py` → regenerates
  `results/processed/q4_ignition_analysis.json` with the 6-point τ=2.5 series.

**What to look for:** does the μ̄=0.4 branch stay flat at ~0.04–0.05 through n=160000 (a genuine
positive plateau — the decline really did arrest at n≈20000), or does it resume falling
(pointing back toward zero after all)? Re-run the n≥20000 homogeneity χ² now including n=160000.

### Leg 3 — Synthesis (the actual finding)

On one page, put the two extended series side by side and answer:

1. Does each series **flatten** (Leg-1 width bending off the power law; Leg-2 ignition holding a
   plateau) when pushed past n=20000, or does the apparent flattening **dissolve** with more n?
2. If both flatten, do they flatten **around a common n\***? Estimate n\* for each (the n where the
   series departs its earlier trend) and state whether they coincide within the grid resolution.
3. State the honest verdict: **shared crossover scale** (both bend near the same n\*, a real
   cross-experiment result worth a dedicated advisor card) vs **coincidence** (they diverge with
   more n) vs **inconclusive** (need still-larger n / more trials — say exactly what).

Optionally cross-link Task U: if the Q5 global-field duration slope *also* flattens near the same
n\*, that is a third series on the same crossover and strengthens the case substantially.

## Expected output

- `results/raw/finite_size_r2_n40000.json` (+ optional `..._n80000.json`), runner-stamped.
- `results/q4_ignition_tau25_n160000_raw.json`, runner-stamped.
- Updated `results/processed/task_a_nu_n10000.json` (6-point ν fit) and
  `results/processed/q4_ignition_analysis.json` (6-point ignition series), both regenerated by the
  edited analysis scripts (never hand-edited).
- Regenerated `results/figures/finite_size_scaling_r2_n10000.png` (now spanning to n≥40000).
- The Leg-3 synthesis paragraph — the deliverable that turns this session's flattening
  *observation* into a tested *claim*, ready for the `advisor-update-2026-07-22` site.

## Reports / context

`okf/next-actions.md` item 1 (the flattening observation), `docs/queue/reports/q3_nu_n10000_report.md`,
`docs/queue/reports/q4_ignition_report.md`, `docs/queue/task_T_q3_nu_extended_n.md` +
`docs/queue/task_S_q4_ignition_wider_n_grid.md` (the two series this extends),
`scripts/analyze_q3_nu.py` + `scripts/analyze_q4_ignition.py` (the two analysis scripts to extend
by one line each), Task U (`docs/queue/task_U_q5_duration_asymptotic_form.md`, the possible third
series on the same crossover).
