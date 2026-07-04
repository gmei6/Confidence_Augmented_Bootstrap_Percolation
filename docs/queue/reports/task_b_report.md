# Task B Report: Theta- and Kappa-Robustness Sweeps

**Owner:** Gary Mei (Georgia Tech ISyE, SURS)  
**Verification Date:** Completed in S-027  

## 1. Objective
Verify that the systemic cascade boundary is robust to variations in the systemic-event threshold parameter $\theta$ (the default failed fraction to classify a systemic event) and the Beta fear concentration parameter $\kappa$ (which controls the variance of individual susceptibility $f_i$ independently of the mean $\mu$).

## 2. Experimental Setup
*   **Engine:** Standalone C++ engine (`twocascade_run`).
*   **Runner Script:** [scripts/run_task_b.py](file:///Users/garymei/Downloads/projects/CABP_copy_for_antigravity/scripts/run_task_b.py)
*   **Configs:** 
    *   `sweep_wk3_4_r{r}.json` ($r \in \{2, 3, 4\}$, $n=1000$, $\text{trials}=500$, seed `20260611`)
    *   `kappa_sweep_r2_k{kappa}.json` ($\kappa \in \{2.0, 10.0, 50.0, 200.0\}$, $n=2000$, $\text{trials}=300$, seed `20260611`)
*   **Grids:** 
    *   $\theta \in [0.2, 0.35, 0.5, 0.65, 0.8]$ (Theta robustness)
    *   $\kappa \in [2.0, 10.0, 50.0, 200.0]$ (Kappa robustness)

## 3. Results & Verification
*   **Theta Robustness:** 
    *   Changing $\theta$ from $0.2$ to $0.8$ results in negligible shifts of the boundary curves $P(\text{systemic})$ vs. seed size.
    *   This occurs because the cascade final size distribution is strongly bimodal: cascades either terminate very early (fraction $\ll 0.1$) or expand to near-total system collapse (fraction $\approx 1.0$). Therefore, the classification boundary is invariant to the choice of $\theta$.
    *   Visualized in: `results/figures/theta_robustness_r2.png`, `theta_robustness_r3.png`, `theta_robustness_r4.png`.
*   **Kappa Robustness:**
    *   Varying individual fear heterogeneity via $\kappa$ (where lower $\kappa$ indicates higher variance) shows that the cascade boundary shifts only marginally.
    *   A slight reduction in the threshold occurs at high variance (low $\kappa$) because the system contains a small subpopulation of highly susceptible individuals who fail very easily, triggering early cascade take-off.
    *   Visualized in: `results/figures/kappa_robustness_r2.png`.
