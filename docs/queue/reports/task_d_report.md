# Task D Report: Memory-Window X-Invariance Robustness

**Owner:** Gary Mei (Georgia Tech ISyE, SURS)  
**Verification Date:** 2026-06-29 (Session 35)  
**Related Walkthrough:** [walkthrough.md](file:///Users/garymei/.gemini/antigravity-cli/brain/ed4c8c98-2d65-40a8-9504-956ec1197ffc/walkthrough.md)

## 1. Objective
Confirm that the normalized fear memory-window length $X \in \{1, 4, 8\}$ leaves the cascade boundary $P(\text{systemic})$ essentially unchanged (invariant within $\pm 0.03$), while the cascade duration grows monotonically with $X$.

## 2. Experimental Setup
*   **Engine:** Standalone C++ engine.
*   **Runner Script:** [scripts/run_task_d.py](file:///Users/garymei/Downloads/projects/CABP_copy_for_antigravity/scripts/run_task_d.py)
*   **Configs:** 
    *   `configs/window_r2_X1.json` (weights `[1.0]`)
    *   `configs/window_r2_X4.json` (weights `[0.5, 0.25, 0.15, 0.10]`)
    *   `configs/window_r2_X8.json` (weights `[0.4201680672, 0.2100840336, 0.1260504202, 0.0840336134, 0.0588235294, 0.0420168067, 0.0336134454, 0.0252100840]`)
*   **Sweep Parameters:** $n=2000, r=2, \alpha=0.7, n_{\mathrm{ref}}=1000$, $\text{trials}=5000$ per cell, shared seed `20260629`.

## 3. Results & Verification
*   **Boundary Invariance:**
    *   Max absolute difference in $P(\text{systemic})$ across all 50 matched coordinates: **$0.0146 \le 0.03$** (**PASS**).
    *   Visualized in: `results/figures/window_r2_invariance.png` (demonstrates perfect collapse of curves).
*   **Duration Growth:**
    *   At the pilot point ($a=6$, $\mu=0.5$): $X=1 \to 8.61$ rounds; $X=4 \to 13.24$ rounds; $X=8 \to 17.80$ rounds (**PASS**).
    *   Overall average duration at $\mu=0.5$: $X=1 \to 7.62$ rounds; $X=4 \to 11.02$ rounds; $X=8 \to 14.51$ rounds.
    *   Visualized in: `results/figures/window_r2_duration.png` (shows monotonic duration growth vs. $X$).
*   **Cross-Language Parity (Prong B):**
    *   Added [tests/test_cpp_window_validation.py](file:///Users/garymei/Downloads/projects/CABP_copy_for_antigravity/tests/test_cpp_window_validation.py).
    *   Statistical validation at $X=4$ passes successfully: Z-test $p = 0.8268 > 0.005$ and KS-test $p = 1.0000 > 0.005$.
