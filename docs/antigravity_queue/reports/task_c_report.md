# Task C Report: Random vs. Targeted Seeding Negative Result

**Owner:** Gary Mei (Georgia Tech ISyE, SURS)  
**Verification Date:** 2026-06-29 (Session 35)  
**Related Write-up:** [docs/research/targeted_seeding_negative_result.md](file:///Users/garymei/Downloads/projects/CABP_copy_for_antigravity/docs/research/targeted_seeding_negative_result.md)

## 1. Objective
Confirm the theoretical conjecture that choosing the initial seed nodes from the highest-degree banks (targeted seeding) does **not** materially shift the critical cascade boundary $a_c(\mu)$ compared to random seeding on Erdős–Rényi graphs $G(n,p)$ in the scaling limit.

## 2. Experimental Setup
*   **Engine:** Python reference engine (`reference.py` is required since C++ raises on `target_high_degree=True`).
*   **Runner Script:** [scripts/run_task_c.py](file:///Users/garymei/Downloads/projects/CABP_copy_for_antigravity/scripts/run_task_c.py)
*   **Configs:** 
    *   `configs/seed_random_r2_n1000.json` vs. `configs/seed_targeted_r2_n1000.json`
    *   `configs/seed_random_r2_n2000.json` vs. `configs/seed_targeted_r2_n2000.json`
*   **Sweep Parameters:** $r=2, \alpha=0.7, n_{\mathrm{ref}}=1000$, $\text{trials}=300$, shared base seed `20260629`.

## 3. Results & Verification
*   **Absolute Shifts:** The mean boundary crossing difference $\Delta a_{\mathrm{emp}}$ is extremely tiny:
    *   $N=1000$: $-1.31$ nodes (a shift of **$0.13\%$** of the network).
    *   $N=2000$: $-1.58$ nodes (a shift of **$0.08\%$** of the network).
*   **Asymptotic Collapse:** The fractional shift $\Delta a_{\mathrm{emp}} / n$ shrinks from $0.13\% \to 0.08\%$ as $n$ doubles, verifying that the degree homogeneity of $G(n,p)$ concentrates the degrees, eliminating targeted seeding advantages in the scaling limit.
*   **Low-Fear Leverage:** At low fear ($\mu \le 0.35$), targeted seeding provides a local $\approx 50\%$ relative threshold reduction at finite sizes due to finite-size degree variance, but this effect is transient.
*   **Visual Artifact:** [results/figures/targeted_seeding_comparison.png](file:///Users/garymei/Downloads/projects/CABP_copy_for_antigravity/results/figures/targeted_seeding_comparison.png) shows the two boundaries collapsing onto each other.
*   **Secondary Analysis:** Saved in `results/analysis/targeted_seeding_adherence.json`.
