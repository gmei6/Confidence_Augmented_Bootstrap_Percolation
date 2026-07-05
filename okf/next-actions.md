---
mutability: live
type: concept
---

# §10 — Next Actions 🟢 *(overwrite each session — keep it to the next few concrete steps)*

1. **Overnight batch (S-047, queued 2026-07-04):** a sandbox agent runs `scripts/run_overnight_s047.py` (Q5 duration n-sweep for C-Q5(ii), Q4 ignition gates for C-Q4(iii), n=10000 tilt grid + tau=3.5 slice, Task E history regen + Task H, Q3 nu at n=10000). Handoff prompt: `okf/changes/s-047-overnight-batch-handoff.md`. Morning follow-up: triage the driver summary, fold results into status/reports, reconcile the sandbox copy.
2. **Email Prof. Dhara before 2026-07-15** with the three simulation results now in hand: the Q6 super-hub negative (S-044), the Q4 tilt-monotonicity readout (cap-free pair passes 7/7; ε-cap artifact flagged — `results/figures/q4_tilt_monotonicity_r2.png`), and the Q5 locality result (global fear homogenizes, ℓ=r_n locality fully preserved, nucleation is a constant leak not a g² barrier — `results/figures/q5_locality_r2.png`).
3. **Review and commit the S-046/S-047 working tree** (all work is uncommitted pending Gary's review: new configs, sweeps, analysis/plot scripts, geometry.py instrumentation+optimization, new q5 tests, the test_q4_prong_a fix, the overnight driver, OKF updates).
4. **Q4 Phase 2 sampler fix:** make `sample_degree_dependent_fears` cap-aware (renormalize Z_n post-cap) so the γ>0 tilt is testable at moderate/high μ̄; then re-test the (0,+1) pair and C-Q4(ii) size-biased collapse.
5. **Q5 follow-up:** build a remote-ignited-growth tracker (cross-round pair ignition) before treating the C-Q5(i) refutation as final. (The C-Q5(ii) duration n-sweep is in the S-047 overnight batch.)
6. TODO (machine setup, not research): install the assistant tooling Gary deferred on 2026-07-04 — `npm install -g gh-axi && gh-axi setup hooks` (GitHub ops), `npm install -g tasks-axi` (backlog), `npm install -g chrome-devtools-axi && chrome-devtools-axi setup hooks` (browser ops). Environment note: this machine's default `python3` runs x86_64 under Rosetta while numpy is arm64 — run simulations with `arch -arm64 python3` (or `/opt/miniconda3/bin/python3`), which also unblocks the deferred Task H.
