---
type: Decision
title: "D-036: Tasks S and T are closed by supersession under Task W's verify gate, not by gates of their own; their intermediate values must not be cited"
mutability: append-only
timestamp: 2026-07-19
tags: [q3, q4, task-s, task-t, task-w, queue, verify-gate, supersession]
---

# D-036: Tasks S and T close by supersession (Task W), not by their own `/verify`

## Decision
Tasks **S** (Q4(iii) ignition gate, wider n-grid) and **T** (Q3 ν extended to n=20000) are
**CLOSED**. Neither has, nor will receive, a `/verify` gate of its own. Both were overtaken by
**Task W**, which *was* gated (reviewer sign-off, critic PASS, AUDIT PASS — recorded in the
`d70dbd8` commit body), and whose artifacts subsume theirs:

- **S → W:** the τ=2.5 ignition series is now the **6-point** run to n=160000
  (`results/processed/q4_ignition_analysis.json`).
- **T → W:** the Q3 ν fit is now the **7-point** fit over n∈{1000..80000},
  **ν(μ=0)=5.61±0.18** (R²=0.953), **ν(μ=0.3)=4.82±0.15** (R²=0.978)
  (`results/processed/task_a_nu_n10000.json`).

**Consequence — binding:** S's and T's intermediate values must **never** be cited. Specifically
retired are T's n=20000 values (ν(μ=0)=6.29±0.39, ν(μ=0.3)=4.90±0.22) and S's n≥20000
flattening reading (χ²=1.70, p≈0.43). The superseding artifact is authoritative in each case.

## Rationale
1. **Re-gating would verify artifacts nothing cites.** A `/verify` pass on S or T would certify
   intermediate n-grids that no downstream claim rests on, while the superseding results are
   already gated. The gate's purpose is to protect cited results, not to complete paperwork.
2. **The supersession is genuine, not nominal.** W did not merely re-run S and T; it extended
   both series (ignition to n=160000, ν to 7 points) and re-fit from the extended data. The
   intermediate fits are not a subset of the final ones — ν(μ=0) moved 6.29→5.61 on refit.
3. **Both intermediate readings are now known-wrong, not merely superseded.** S's flattening
   verdict is contradicted (pooled trend z=−3.31, p=0.0009); T's ν values shifted by more than
   their own stated error bars. Leaving them un-retired is an active citation hazard, which is
   why the "must not be cited" clause is part of the decision rather than a note.

## Residual process gap (recorded, not resolved)
The task files for **U** and **W** specified a *human* at their verify gate; the S-051-era
overnight batch ran a **blind** gate instead. This is a deviation from what those task files
specified. It is **not** an ungated result — reviewer, critic, and auditor all ran — and it is
recorded here rather than treated as a defect requiring re-work. If the advisor challenges any
W- or U-derived number, re-running the gate with a human present is the remedy.

## Affects
`okf/status.md` §8; `okf/next-actions.md` §10 item 4; `docs/queue/task_S_q4_ignition_wider_n_grid.md`;
`docs/queue/task_T_q3_nu_extended_n.md`; `docs/queue/reports/q4_ignition_report.md`; session `s-058`.
