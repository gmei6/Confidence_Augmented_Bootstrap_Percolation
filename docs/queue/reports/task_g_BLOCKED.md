# Task G — BLOCKED (environment cannot run simulations)

**Date:** 2026-07-04 (fable overnight run) · **Task file left in place:** `docs/queue/task_G_scaling_law_extended_validation.md`

## Where I stopped and why

Stopped at **Plan step 1–2 (configs / run)** before writing any files. Same environment gap
as Task E (full diagnosis in `task_e_BLOCKED.md`), with one Task-G-specific twist:

- Task G wants `engine="cpp"`. The committed `cpp/build/twocascade_run` is a macOS arm64
  Mach-O binary — unrunnable on this Linux container (`exec format error`). The container
  does have `g++ 12` and `make` (no `cmake`), so a native rebuild was *plausible* —
  but it would be pointless here because:
- `run_sweep` itself imports numpy (seeding via `SeedSequence.spawn`, multiprocessing
  orchestration), the $a_c(\mu)$ interpolation/fitting analysis needs numpy/scipy, the
  figure needs matplotlib, and the DoD's §5.4 cross-validation gate needs the *Python
  reference engine* (numpy) to compare against. None of those exist here and there is no
  network to install them.

No DoD item can be met, so no partial/untested artifacts were written.

## Notes for whoever resumes

- This is ~13,000+ cells' worth of trials (3 r-values × 3 n-values × 6 μ × ~21 seed
  multiples × 1000 trials) — genuinely wants the C++ engine; don't fall back to Python.
- If the resume happens on a Linux host, note LESSONS_LEARNED §2's CMake flag dispatch
  (`-mcpu=native` vs `-march=native`) is Apple-specific; a plain Linux build should be fine.
- Apply the D-021/D-023 empirical clamping filter (`a_emp > grid_floor`, strict inequality)
  before fitting, per the task's watch-out.

## Exact resume point

1. Fix the environment (scientific Python + a natively built `cpp/build/twocascade_run`).
2. Then follow the task file from Plan step 1 unchanged.
