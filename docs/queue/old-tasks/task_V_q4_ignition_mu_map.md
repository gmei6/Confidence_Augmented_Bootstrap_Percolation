# Task V — Q4 ignition gate: intermediate-μ̄ map across the 5-point n-grid

**Queued:** 2026-07-18. **Conjecture under test:** C-Q4(iii) tail-gating clause — specifically
the **shape of the τ=2.5 ignition branch as a function of fear μ̄**, filling the gap between the
two μ̄ values currently on file.

## Problem

Every Q4 ignition run to date (S-048 report + Task S extension) uses only **two** fear values,
$\bar\mu \in \{0.0, 0.4\}$:

| series | n=4000 | n=10000 | n=20000 | n=40000 | n=80000 |
|---|---|---|---|---|---|
| τ=2.5, μ=0.0 | 0.038 | 0.024 | 0.028 | (Task S) | (Task S) |
| τ=2.5, μ=0.4 | 0.134 | 0.116 | 0.062 | 0.050 | 0.044 |

So we know ignition is **flat ~0.03 (Θ(1))** at μ=0 and **elevated-but-declining** at μ=0.4, but
the entire interior of the μ̄ axis is unmapped. We cannot say whether fear enhances ignition
**monotonically** in μ̄, whether the "elevated then declines in n" pattern turns on gradually or
at a threshold μ̄, or where the crossover from "Θ(1)-flat" to "declining" sits. This is a clean,
cheap gap to close and it directly supports the Task W flattening story (is the n-decline present
at all μ̄>0, or only near μ̄=0.4?).

## Autonomous-safe: YES (config-only + one read-only analysis script)

No `src/` or `cpp/src/` changes. Five new configs (schema-identical to the existing
`q4_ignition_tau25_n*.json`) plus one small **read-only-on-raw** analysis script. Local Mode.
Same tier as Tasks S/T — safe to launch unattended and gate at `/verify` afterward. Uses
`engine="python"` (configuration-model + degree-fear path is Python-only, per
`docs/queue/README.md`).

## Method

**1. Five new configs `configs/q4_ignition_tau25_mumap_n{4000,10000,20000,40000,80000}.json`.**
Each is a **byte-for-byte copy** of the corresponding existing `q4_ignition_tau25_n{N}.json`,
with exactly two edits:

- `sweep.mean_fear_grid`: change `[0.0, 0.4]` → **`[0.0, 0.1, 0.2, 0.3, 0.4]`**. (Keep the
  endpoints 0.0 and 0.4 in the grid: with the same `base_seed=42` and the same per-n
  `seed_multiple`, those two cells reproduce the existing raws **exactly** — a free
  cross-validation that the new configs are wired correctly.)
- `output.raw_filepath`: change to `results/q4_ignition_tau25_mumap_n{N}_raw.json` (new path —
  never overwrite the existing `..._n{N}_raw.json`).

Everything else stays identical. In particular **do not touch `seed_multiples`** — it is per-n
and depends only on n (it forces the bounded seed `a=2`), not on μ̄. The correct per-n values are
already in the source configs and must be carried over unchanged:

| n | seed_multiples (carry over verbatim) |
|---|---|
| 4000 | `[0.0076872]` |
| 10000 | `[0.0064]` |
| 20000 | `[0.0055715]` |
| 40000 | `[0.0048503]` |
| 80000 | `[0.0042224]` |

Also carry over verbatim: `pinned_params` (r=2, κ=50, θ=0.5, window 5 × weights 0.2,
`graph={type: configuration_model, tau: 2.5, d_min: 2}`, `fear={gamma: 0.0}`),
`scaling={target_mean_degree: 4.0, n_ref: 10000, alpha: 0.6}`, `trials_per_cell: 500`,
`base_seed: 42`, `engine: "python"`.

**2. Run all five** (arm64 required — see `okf/lessons.md`). A tiny batch driver in the
`scripts/run_overnight_s051.py` mold is the cleanest reproducible launcher:

```
nohup arch -arm64 python3 -c "
import sys; sys.path.insert(0,'src')
from twocascade.runner import run_sweep
for n in (4000,10000,20000,40000,80000):
    run_sweep(f'configs/q4_ignition_tau25_mumap_n{n}.json')
" > task_v.log 2>&1 &
```

(Or add a `scripts/run_task_v_mumap.py` following the S-051 driver pattern if you prefer a
committed launcher — either is fine; the configs are the reproducible artifact.)

**3. New analysis script `scripts/analyze_q4_mumap.py`** (read-only on the raws). Model it on
`scripts/analyze_q4_ignition.py`, but the readout is a **μ̄ × n grid of P(systemic)**, not a
tail-gate verdict:

- For each n, load `results/q4_ignition_tau25_mumap_n{n}_raw.json` and call
  `twocascade.analysis.analyze_sweep(raw)` — it returns `processed_cells` each with `mean_fear`
  and `p_systemic`. (Same call `analyze_q4_ignition.py` uses.)
- Compute the **Wilson 95%** interval per cell (copy the exact snippet from
  `analyze_q4_ignition.py:47-51`, `z=1.96`, `trials=500` — it is robust at p=0).
- Emit a table `p_systemic[μ̄][n]` (5×5) and, per μ̄ series, the sign of the n-trend
  (increasing / decreasing / flat), reusing the `direction` logic from
  `analyze_q4_ignition.py:76-79`.
- Write `results/processed/q4_mumap_analysis.json` (stamp `get_git_commit_hash()` + source
  commits + timestamp, same metadata block as the sibling script). Do **not** hand-edit
  `results/`.

## Expected output

- `results/q4_ignition_tau25_mumap_n{4000,10000,20000,40000,80000}_raw.json` (runner-stamped).
- `results/processed/q4_mumap_analysis.json` — the 5×5 P(systemic) grid with Wilson intervals and
  per-μ̄ n-directions.
- A short readout in the wrap-up answering: (a) is ignition **monotone increasing in μ̄** at each
  fixed n? (b) does the **n-decline** appear at all μ̄>0 or only near μ̄=0.4? (c) where is the
  crossover from "flat Θ(1)" to "declining"? Cross-link to Task W (flattening theme).
- **Cross-check to report:** the μ̄∈{0.0,0.4} columns must match the existing
  `results/q4_ignition_tau25_n{N}_raw.json` cells to the trial (same seed) — confirm this
  explicitly in the walkthrough; a mismatch means the configs are miswired.

## Reports / context

`docs/queue/reports/q4_ignition_report.md`, `docs/queue/task_S_q4_ignition_wider_n_grid.md` (the
n-grid this reuses), `scripts/analyze_q4_ignition.py` (the sibling analysis to model on),
`okf/open-questions.md` Q4, Task W (`docs/queue/task_W_finite_size_crossover.md`).
