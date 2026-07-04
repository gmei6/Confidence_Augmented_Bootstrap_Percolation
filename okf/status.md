---
mutability: live
type: concept
---

# §8 — Current Status 🟢 *(overwrite each session)*

- **Phase:** Post-first-advisor-meeting. First advisor meeting held 2026-07-01 2:00pm with Prof. Dhara; five extension directions logged (D-028) — degree-heterogeneous (power-law configuration model) graphs, geometric graphs (random geometric graphs → geometric inhomogeneous random graphs), the combination of the two, an optional recovery/healing phase, and weighted edges. Next meeting 2026-07-15; advisor wants simulation results emailed beforehand.
- **Task A — Finite-size ν (S-035, preliminary):** ν≈8.39±1.57 at μ=0.0 (R²=0.83); ν≈5.33±0.51 at μ=0.3 (R²=0.97). Fear materially accelerates boundary sharpening. Figure: `results/figures/finite_size_scaling_r2.png` (watermarked "Preliminary, pending advisor alignment"). New code: `estimate_transition_width` + `fit_finite_size_exponent` in `src/twocascade/analysis.py`; unit tests in `tests/test_analysis.py`; scripts: `scripts/run_finite_size_sweeps.py`, `scripts/plot_finite_size_scaling.py`.
- **Task C — Targeted seeding (S-035):** Confirmed deliberate negative result. Boundary shift 0.13% at n=1000 shrinks to 0.08% at n=2000 — vanishes in scaling limit on $G(n,p)$. Research doc: `docs/research/targeted_seeding_negative_result.md`. Figure: `results/figures/targeted_seeding_comparison.png`.
- **Task D — Window invariance (S-035):** Max $|\Delta P|=0.0146\le0.03$ ✓; duration grows monotonically with $X$ ✓. C++ cross-language validation at X=4: Z-test p=0.83, KS p=1.00 ✓. Figures: `results/figures/window_r2_invariance.png`, `results/figures/window_r2_duration.png`. New test: `tests/test_cpp_window_validation.py`.
- **Task B — θ/κ robustness (S-027):** Boundary invariant across θ∈[0.2,0.8]; κ enters only at 2nd order.
- **Viz (S-031–S-033):** Interactive teaching website live on GitHub Pages. Part A/B walkthroughs; Node.js tests 17/17 pass.
- **Section 2 reformulation website (S-034/S-036):** Static study site at `section2-reformulation/`. Now live on GitHub Pages alongside viz/. Illustrative/reference only.
- **Advisor briefing packet:** draft complete — `docs/research/other/advisor_brief_2026_07_01.md`. Send before 2026-07-01 2:00pm.
