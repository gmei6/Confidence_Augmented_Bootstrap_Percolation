# Task C — Random vs. targeted (high-degree) seeding: a deliberate negative result

**One-line task.** Show that seeding the initial shock at the highest-degree banks does **not**
materially shift the cascade boundary on $G(n,p)$, and report it as a clean negative result.

**Touches:** §3.1 (seed selection; the high-degree-targeting variant), §6 Wk 9. The expected
near-null on $G(n,p)$ is anticipated in §6/§9 — on an Erdős–Rényi graph degrees are
near-homogeneous, so "targeting" ≈ random. No fork opened.

## Why this is low-human-input

Targeted seeding is **already implemented**: `choose_seed(..., target_high_degree=True)` picks
the top-degree nodes, and the runner threads `pinned_params.target_high_degree` through. This
is config + run + compare + a short write-up. Likely **no `src/` change** → Local Mode is fine
(use a worktree only if you end up adding an analysis helper).

## Plan

1. **Engine choice.** The C++ engine **raises** on `target_high_degree=True`, so both arms of
   this comparison must run with `engine="python"`. Keep `n` and trials modest to stay fast:
   `n ∈ {1000, 2000}`, `trials_per_cell` ~200–300.
2. **Paired configs** at matched parameters (`r=2, alpha=0.7, n_ref=1000,
   target_mean_degree=8.0`, standard `mean_fear_grid`, `seed_multiples` `[0.6 … 1.4]`,
   `theta=0.5`, `concentration=50.0`, `window_len=1`):
   - `configs/seed_random_r2_n{N}.json` → `target_high_degree: false`
   - `configs/seed_targeted_r2_n{N}.json` → `target_high_degree: true`
   - both `engine: "python"`; **same `base_seed`** across the pair so the only difference is
     the seeding rule; distinct `output.raw_filepath` under `results/raw/`.
3. **Run** both via `run_sweep(config_path, engine="python")`.
4. **Compare.** Overlay the two $P(\text{systemic})$ boundaries; compute the boundary shift
   (e.g. difference in the seed-multiple at $P=0.5$) and a simple significance check per cell.
   Expectation: indistinguishable within Monte-Carlo error.
5. **Write-up.** A short `docs/research/targeted_seeding_negative_result.md` stating the
   research question, the expectation, the result, and the interpretation (degree homogeneity
   on $G(n,p)$ ⇒ targeting has no purchase; this is *why* the configuration-model pivot, Q2,
   is where targeting would matter). **Before editing/creating that research doc, state the
   Q#/F# it addresses** per the AGENTS.md research-document rule (here: §3.1 variant + Q2
   motivation).

## Parameter grid (summary)

| knob | value |
|------|-------|
| `r` | 2 |
| `n` | 1000, 2000 |
| `engine` | **python** (required for targeting) |
| `mean_fear_grid` | standard wk3_4 grid |
| `seed_multiples` | 0.6 → 1.4 step 0.05 (or 0.1 to save time) |
| `trials_per_cell` | 200–300 |
| arms | `target_high_degree` ∈ {false, true}, shared `base_seed` |

## Definition of Done (§5.6) + what Gary checks

- [ ] Paired configs committed; raw files stamped (seed + git hash + timestamp); none written
      by hand.
- [ ] Comparison figure regenerates from raw.
- [ ] Negative-result write-up names its Q#/F# and states the expectation *before* the result.
- [ ] `/verify` returns **AUDIT PASS**. **Gary checks:** is the boundary shift genuinely within
      noise? Is it framed as a deliberate, informative negative result (not a failure), and does
      it correctly motivate Q2?

## Watch-outs (from LESSONS_LEARNED)

- Python engine is the slow path — keep the grid lean; this is a confirmation, not a precision
  study.
- Use `SeedSequence.spawn` (the runner already does) so the two arms aren't accidentally
  correlated beyond the shared base seed.
- Don't overclaim: "no effect *on $G(n,p)$*." On heterogeneous graphs (Q2) the story differs —
  say so.
