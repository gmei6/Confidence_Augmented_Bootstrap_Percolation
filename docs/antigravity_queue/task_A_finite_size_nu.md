# Task A — Finite-size transition-width exponent ν

**One-line task.** Measure how sharply $P(\text{systemic})$ rises through the cascade
boundary as system size grows, and estimate the transition-width scaling exponent $\nu$ via
width $\sim n^{-1/\nu}$.

**Touches:** §6 Wk 6–7 (finite-size analysis). **Informs (does not commit to)** advisor
question **Q3** (critical-window framing). Stays on $G(n,p)$ + decided model — no fork opened.

> ⚠️ **Framing constraint.** §10 lists this as "begin once aligned" with the advisor. Produce
> this as a **preliminary** estimate to *inform* the Q3 conversation on 2026-07-01 — label all
> outputs "preliminary, pending advisor alignment." Do **not** rewrite the roadmap or claim a
> resolved critical-window result.

## Why this is low-human-input

The runner, the Janson `p_n` scaling, and per-`n` `a_c`-relative seeding already exist. The
only new code is one analysis function (width estimate) + one fit + one plot. Gary reviews at
the `/verify` and `/wrapup` gates.

## Plan

1. **Configs.** Create one config per `n` in `configs/finite_size_r2_n{N}.json` for
   `N ∈ {1000, 2000, 5000}` (add `n=10000` only if runtime is comfortable; otherwise note it
   as a PACE follow-up — do **not** block on it). For every config:
   - `pinned_params`: `r=2`, `concentration=50.0`, `theta=0.5`, `window_len=1`,
     `weights=null`, `target_high_degree=false`; set `n` to the target `N`.
   - `scaling`: **fixed across all configs** — `n_ref=1000`, `target_mean_degree=8.0`,
     `alpha=0.7`. (Keeping `n_ref` fixed is what makes `np` grow correctly with `n`.)
   - `sweep`: a single representative `mean_fear_grid` (start with `[0.0]`; optionally also a
     paired set of configs at `[0.3]` to check $\nu$'s $\mu$-dependence), a **fine**
     `seed_multiples` grid centered on the boundary — `[0.6, 0.65, …, 1.4]` (step 0.05),
     `trials_per_cell` ≥ 1000 (the budget must sit *near the boundary*, §6),
     a distinct `base_seed` per config.
   - `engine: "cpp"` (build first if needed); `output.raw_filepath:
     "results/raw/finite_size_r2_n{N}.json"`.
2. **Run.** `run_sweep(config_path, engine="cpp")` for each config. Confirm the metadata
   stamp (git hash, seed, timestamp) is present in each raw file.
3. **Analyze (new code, worktree).** Add to `src/twocascade/analysis.py`:
   - `estimate_transition_width(failed_fractions_by_multiple, theta, ...) -> dict`: convert
     each cell to $P(\text{systemic})$ at `theta`, fit $P$ vs `seed_multiple` to a logistic,
     and return the 10–90% rise width (in seed-multiple units, dimensionless and comparable
     across `n`) with a bootstrap CI.
   - A small driver that loads the per-`n` raw files, gets each width, and fits
     $\log(\text{width})$ vs $\log n$ → slope $=-1/\nu$ → report $\nu$ with its fit error.
4. **Figure (worktree).** In `plotting.py` add a read-only figure: (left) the $P$-vs-multiple
   curves for all `n` on one axis showing the sharpening; (right) the log–log width-vs-$n$ fit
   with the $\nu$ estimate annotated. Save under `results/figures/`.
5. **Tests.** Add a `tests/test_analysis.py` case for `estimate_transition_width` on a
   synthetic logistic (known width) to lock the estimator.

## Parameter grid (summary)

| knob | value |
|------|-------|
| `r` | 2 |
| `n` | 1000, 2000, 5000 (10000 optional/PACE) |
| `alpha`, `n_ref`, `target_mean_degree` | 0.7, 1000, 8.0 (fixed across n) |
| `mean_fear` | 0.0 (optionally also 0.3 as a paired check) |
| `seed_multiples` | 0.6 → 1.4 step 0.05 (fine, boundary-centered) |
| `trials_per_cell` | ≥ 1000 |
| `theta` | 0.5 (reuse Task B to check θ-robustness of ν) |

## Definition of Done (§5.6) + what Gary checks

- [ ] Each config committed; each raw file in `results/raw/` carries seed + git hash + timestamp.
- [ ] Figure regenerates from raw via `plotting.py` (no simulation inside plotting).
- [ ] `estimate_transition_width` has a passing synthetic-logistic unit test; full suite green.
- [ ] `/verify` returns **AUDIT PASS** (no C++ touched, so the §5.4 cross-language prongs are
      N/A — make sure the auditor isn't asked to run them).
- [ ] `/wrapup` drafts a §8 status line + a §11 decision entry if a width-estimation method is
      adopted. **Gary checks:** the $\nu$ value + CI, the sharpening trend (does width shrink
      monotonically with `n`?), and that everything is labeled *preliminary*.

## Watch-outs (from LESSONS_LEARNED)

- Keep `n_ref` fixed; do **not** pin `BETA` to live `n` (that silently collapses to constant
  `np` — the S-007 erratum trap).
- If the boundary sits at the edge of the `seed_multiples` grid for some `n`, widen the grid
  rather than extrapolating the logistic fit.
- Three `n` values across ~0.7 decade is thin for a clean exponent (§7) — report the CI
  honestly and flag `n=10000`/PACE as the way to tighten it. Don't overstate precision.
