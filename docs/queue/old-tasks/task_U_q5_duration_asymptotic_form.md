# Task U — Q5 duration dichotomy: asymptotic form of the global-field sub-ballistic decay

**Queued:** 2026-07-18. **Question / conjecture:** Q5, refinement of **C-Q5(ii)** (duration
dichotomy). **This is a refinement, not the original open item.**

> **Read this first — the base clause is already SUPPORTED.** `okf/open-questions.md` (Q5) still
> reads "C-Q5(ii) … deferred to an n-sweep (C++/PACE)", but that line is **stale**: the Task O
> follow-up (S-048, `docs/queue/reports/task_o_duration_report.md`) already ran the n-sweep at
> n∈{4000, 8000, 16000, 32000} and found **C-Q5(ii) SUPPORTED** (local field ballistic, global
> field sub-ballistic, global-vs-control slope t≈−46). Do **not** re-run that as if it were open.
> This task asks a *new* question the existing 4-point sweep cannot answer, and its wrap-up should
> also fix the stale `okf/open-questions.md` line (draft only, via `/wrapup` — the PI applies it).

## Problem

On the existing 4-point grid the global-field ballistic ratio
$R(n) = T_\theta / \sqrt{n/\log n}$ falls with a **log-ratio-vs-log-n slope of about −0.26**
(0.461 → 0.393 → 0.325 → 0.273 at $\bar\mu=0.2$; similar at $\bar\mu=0.4$). That slope was
enough to declare the global field *sub-ballistic relative to the control* (the local/control
slope is ≈−0.011). But it does **not** tell us the asymptotic form of the global-field growth:

- If the −0.26 ratio slope is **stable**, then $T_\theta^{\text{global}} \sim n^{0.24}/\sqrt{\log n}$
  — a clean sub-ballistic power law (secondary nucleation gives a genuinely faster-than-front
  short-circuit that scales as a power of $n$).
- If the ratio slope **flattens** at larger $n$ (ratio bending toward a smaller positive
  constant), the "sub-ballistic" reading is a finite-size transient and the global field is
  asymptotically ballistic-with-a-smaller-constant.

Distinguishing these matters because **the same flattening question is open for two other series
this session** — the Q3 ν width and the Q4 μ̄=0.4 ignition curve both flatten after n=20000 (see
Task W and `okf/next-actions.md` item 1). Whether the Q5 global-field slope *also* flattens near
the same scale is a direct cross-experiment test of a shared finite-size crossover.

## Autonomous-safe: LOW-RISK, but NOT blind-overnight

New driver + analysis **scripts** (copies of existing Task O ones with a wider n-grid and new
output paths) — no `src/` or `cpp/src/` changes, so **Local Mode**, not New Worktree Mode. This
is the exact Tasks E–P precedent (script-only additions under `scripts/`, still gated by the
`/verify` reviewer→critic→auditor cycle before "done"). It is **not** in the S/T config-only
tier because it adds new scripts and because of the compute-cost check below — run it through
`/research-cycle` with a human at the verify gate, not via a fire-and-forget overnight batch.

**Compute feasibility (checked): OK.** `build_rgg_adjacency` (`src/twocascade/geometry.py:20-45`)
uses cell-bucketing (spatial hash), so it is ~O(n) at bounded mean degree — n=128000 is feasible
on one machine. The cascade is the Python `run_cascade_local_fear`. Budget check before the full
run: time a single n=128000 trial first (§ "Method" step 2); if one trial exceeds ~2 min, drop
the top point to n=64000 and report the reduced grid rather than blocking.

## Method

**1. New driver script `scripts/run_task_u_duration_wide.py`.** Copy
`scripts/run_task_o_duration.py` verbatim, then make exactly these changes:

- `CONFIG["n_grid"] = [16000, 32000, 64000, 128000]` — overlap the existing sweep at 16000 and
  32000 (sanity cross-check against `results/q5_duration_raw.json`), extend to 64000, 128000.
- `CONFIG["trials_per_cell"] = 60` (up from 30) — the ratio SEs at the new large-n points need to
  be small enough to resolve a slope change; 60 keeps runtime bounded while roughly halving the SE.
- `CONFIG["base_seed"] = 2028` — a **new** seed, distinct from Task O's 2027, so the extended run
  is statistically independent (do NOT reuse 2027; overlapping n-points must be independent draws
  for the cross-check to mean anything).
- `OUTPUT_PATH = "results/q5_duration_wide_raw.json"` — new path, never overwrite
  `results/q5_duration_raw.json`.
- Update the module docstring to say "Task U (Q5 C-Q5(ii) asymptotic-form refinement)".

Everything else — the cells (control μ=0; global μ∈{0.2,0.4}; local_1 μ∈{0.2,0.4}), the hard-RGG
geometry ($\bar D = 2\log n$, disc seeding a=30, r=2, κ=50, θ=0.5, window 5 × weights 0.2), the
per-trial `SeedSequence(base_seed).spawn(...)` structure, the durations-only output (D-014
JSON-bloat rule) — stays **identical** to Task O. Do not add position logging or per-round stats.

Run (arm64 required on this machine — see `okf/lessons.md`):

```
nohup arch -arm64 python3 scripts/run_task_u_duration_wide.py > task_u.log 2>&1 &
```

Before the full launch, do the **budget check**: temporarily set `CONFIG["n_grid"]=[128000]` and
`trials_per_cell=1`, time it, then restore the real grid. Report the per-trial time in the
walkthrough.

**2. New analysis script `scripts/analyze_task_u_duration_wide.py`.** Copy
`scripts/analyze_task_o_duration.py` verbatim and change only:

- `RAW_PATH = "results/q5_duration_wide_raw.json"`
- `OUTPUT_PATH = "results/processed/task_u_duration_wide_analysis.json"`

The analysis logic is reused unchanged: per (n, field, μ) it computes $R(n)$ and its SE, fits
log R vs log n per series (weighted LS), and reports each field series' slope **relative to the
μ=0 control slope** (regime = ballistic / sub-ballistic / super-ballistic at |t|=2). That is
exactly the readout we want.

**3. The actual new question (do this by hand on the two analyses).** Compare the **global-field
log-ratio-vs-log-n slope on the new large-n grid** against the same slope on the old grid:

- Old grid (from `results/processed/task_o_duration_analysis.json`, or the report table):
  global slope ≈ −0.255 (μ=0.2), −0.280 (μ=0.4) over n∈{4000..32000}.
- New grid (from step 2): global slope over n∈{16000..128000}.
- **Verdict logic:** if the new-grid global slope is statistically consistent with the old-grid
  slope (overlapping 2·SE), the sub-ballistic decay is a **stable power law** → report the
  power-law exponent. If the new-grid slope is significantly *shallower* (closer to the control's
  −0.011), the decay is **flattening** → a finite-size crossover, and record the approximate n at
  which it bends. Use the μ=0 control and the local_1 series as the null: those must stay flat on
  the new grid too, or the whole large-n run is suspect (flag, don't paper over).

## Expected output

- `results/q5_duration_wide_raw.json` (runner-stamped by the driver: config, base_seed 2028, git
  commit, timestamp).
- `results/processed/task_u_duration_wide_analysis.json` (per-series slopes + regimes on the wide
  grid).
- A one-paragraph verdict in the wrap-up: stable-power-law vs flattening, the fitted global slope
  with SE on the wide grid, and an explicit statement of whether the Q5 global-field flattening
  (if any) coincides in n with the Q3-ν / Q4-ignition flattening (cross-link to Task W).
- Optional figure: R(n) vs n log-log for all five series, old + new grids overlaid. Follow the
  `scripts/plot_task_o.py` style if made; do not hand-edit `results/`.

## Reports / context

`docs/queue/reports/task_o_duration_report.md` (base C-Q5(ii) SUPPORTED result and the 4-point
table), `scripts/run_task_o_duration.py` / `scripts/analyze_task_o_duration.py` (the scripts to
copy), `okf/open-questions.md` Q5 (the stale "deferred" line to fix in wrap-up), Task W
(`docs/queue/task_W_finite_size_crossover.md`, the shared-flattening theme).
