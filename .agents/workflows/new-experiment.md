---
name: new-experiment
description: Scaffold and run a new simulation experiment reproducibly: create a config, run the runner with a logged seed, save raw outputs, and regenerate the figure, satisfying the §5.6 Definition of Done. Use for any new sweep or parameter study.
---

# New Experiment

Stand up a new experiment so it is reproducible from the start (§5.4–§5.6). Honor GEMINI.md
and AGENTS.md.

## Steps
1. **Define:** state the question, the parameter grid (`r, μ, n, seed_size, θ, ...`), and the
   Q#/F#/D# it touches. Confirm parameters sit in the Janson regime (§4) — `p` scales as
   `p_n = β·n^{-α}`, `α ∈ (1/r, 1)`; never hold `p` fixed across `n`.
2. **Config:** create ONE file in `configs/` for this experiment — no magic numbers in code
   (§5.3). Include every parameter and the base seed. `python-simulation` owns this.
3. **Run:** invoke the runner so it writes per-realization outcomes to `results/raw/`, each
   stamped with config + seed(s) + git commit hash + timestamp. Never write `results/` by hand.
4. **Figure:** regenerate the figure from `results/raw/` via `plotting.py` — never recompute
   the simulation inside plotting.
5. **Validate:** load the `reproducible-run` skill and confirm every checklist item holds.
6. **Record:** draft the §8 status update and any §11 entry (via /wrapup).

## Report
[Config created] · [Raw outputs path] · [Figure path] · [Validation Status] · [New Decisions].
