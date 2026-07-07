# Task P: Q6 Geometric Inhomogeneous Random Graph (GIRG) Implementation

**Objective:** Combine the power-law degree heterogeneity of Q4 with the geometric locality of Q5 using a GIRG.

**Reference:** `docs/research/q5_geometric_graph_scoping.md` Section 1(c)

## 1. Preparation
- Review the results of Tasks N and O to determine which parameters to focus on.
- Formally draft the analytical scoping for GIRG in `docs/research/q6_girg_scoping.md` (which was left as a pointer in the Q5 doc).

## 2. Implementation
- Implement the GIRG generator using the weighted distance probability $\mathbb P(i\sim j)\approx\min\{1,(w_iw_j/(n\|x_i-x_j\|^2))^{\alpha_g}\}$.
- Integrate the degree-dependent fear module from Task N with the local fear engine from Task O.

## 3. Simulation
- Run simulations to test whether a highly central hub (high weight) positioned in a local geometric neighborhood can cause a global cascade when the fear field is local but highly tilted ($\gamma > 0$).
