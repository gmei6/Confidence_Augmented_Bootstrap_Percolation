# Q1 Adversary Review: Reviewer Attack Surfaces & Edge Cases

This document takes the perspective of a critical reviewer evaluating the two-channel cascade model. It flags major vulnerabilities in both the rigorous and heuristic approaches and provides strategies to preemptively neutralize these attacks.

## 1. Scenario A: Reviewer Attacks if Attempting "Full Rigor"
If the paper claims to prove theorems extending Janson to the fear setup:

### A. Vulnerabilities and Edge Cases
- **The Beta Distribution Boundaries**: The Beta distribution $\text{Beta}(\alpha, \beta)$ has support $[0, 1]$. Near the boundary $\mu \to 0$ or $\mu \to 1$, or when concentration $\kappa \to 0$, the probability density functions are highly non-uniform (e.g., U-shaped or highly concentrated). A reviewer will ask: *Does your proof hold for the boundary parameters where the density diverges?*
- **The $r=2$ vs $r \ge 3$ Discontinuity**: Bootstrap percolation behaviors differ qualitatively between $r=2$ and $r \ge 3$. Under $r=2$, the critical seed is $a_c \sim 1/(2np^2)$, whereas for $r \ge 3$ the scaling is different. The reviewer will check if the proof implicitly assumes $r=2$ details that break for higher thresholds.
- **Absorbing State and Halting Rule**: The halting rule assumes the cascade halts when $a_t = 0$. If there is a memory window $X > 1$ (D-006), the process can continue if there are failures in the window. Does the proof handle the generalized halting rule rigorously, or does it only work for the memoryless $X=1$ case?
- **RNG Dependency and Realized Heterogeneity**: The proof assumes independent drawings of $f_i$. In practice, the finite sample size $n$ could cause the realized mean fear to deviate from $\mu$. The reviewer might argue that the proof relies on asymptotic properties that are not realized at small $n$.

### B. Prevention Strategies
- **Acknowledge boundaries explicitly**: State exactly which parameter ranges are covered (e.g., $\mu \in (0, 1)$, $\kappa > 0$).
- **Prove stochastically bounded properties**: Instead of aiming for exact asymptotical distributions of cascade sizes, prove stochastic dominance relationships (e.g., $A^*(\mu_1) \le_{\text{st}} A^*(\mu_2)$ for $\mu_1 \le \mu_2$), which are mathematically easier to lock down and very robust.

---

## 2. Scenario B: Reviewer Attacks if Attempting "Heuristic Mean-Field Only"
If the paper relies on "heuristic mean-field validated by simulation":

### A. Vulnerabilities and Attacks
- **"Finite-size effects confound your results"**: The reviewer will argue: *"At $n=1000$ or $n=2000$, the system is far from the thermodynamic limit. Your bimodality is just noise, and the match with the analytical curve is coincidental."*
- **"The threshold $\theta=0.5$ is arbitrary"**: *"Why 0.5? If you set $\theta = 0.2$ or $\theta = 0.8$, does the transition still occur at the same place? Is there a true discontinuity or just a smooth crossover?"*
- **"The mean-field approximation assumes independence"**: The mean-field map assumes that the states of a node's neighbors are independent. In a real cascade, failures cluster locally, causing correlations that the Poisson approximation ignores. The reviewer will demand: *Quantify the error introduced by this independence assumption.*
- **"Data dredging on parameters"**: *"You have swept $\mu$ and $a$, but you held $r=2$ and fixed the graph degree. How do we know this behavior isn't highly sensitive to the specific degree distribution or seed selection?"*

### B. Preemptive Countermeasures
- **Multi-Decade Finite Size Scaling**: Run simulations for $n$ from $1000$ up to $10000$ (using the fast C++ implementation). Show that the transition width shrinks as $n \to \infty$ according to a clean power law, and show that the empirical threshold converges to the mean-field prediction.
- **Bimodality and Robustness Sweeps**:
  - Plot the bimodality coefficient showing it peaks precisely at the transition boundary.
  - Run a $\theta$-sensitivity analysis demonstrating that $P(\text{systemic})$ is invariant to the choice of $\theta \in [0.2, 0.8]$.
- **Quantify Mean-Field Gap**: Measure the difference between the empirical transition threshold and the analytical saddle-node prediction. Show that the gap decreases as $n$ increases (which proves the mean-field approximation becomes exact asymptotically).

---

## 3. Scenario C: The Risks of a "Tiered Approach"
If the paper mixes rigor and heuristics:
- **The "Why not both?" Trap**: If we prove some parts rigorously (e.g., the fear-only subcriticality) and leave others as conjectures, the reviewer might expect the same level of rigor for the entire paper and reject it because the main result (the combined cascade threshold) is only a conjecture.
- **Mitigation**: We must frame the paper carefully:
  - Position the work as a **numerical and heuristic exploration** of a novel coupled model.
  - Frame the rigorous proofs as **auxiliary safety lemmas** (e.g., proving that fear cannot explode on its own) to justify the validity of the numerical simulations, rather than claiming to write a pure probability-theory paper.
