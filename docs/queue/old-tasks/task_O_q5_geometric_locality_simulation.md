# Task O: Q5 Geometric Graph Locality Simulation

**Objective:** Implement the Random Geometric Graph (RGG) and Soft RGG variants, alongside the local fear field, to evaluate the locality of panic cascades (C-Q5).

**Reference:** `docs/research/q5_geometric_graph_scoping.md`

## 1. Implementation
- Create `src/twocascade/geometry.py` with `sample_torus_points`, `build_rgg_adjacency`, `build_soft_rgg_adjacency`, and `build_fear_adjacency`.
- Implement `run_cascade_local_fear` as an experimental variant engine in `geometry.py`. Do NOT modify the oracle `reference.py`.
- Implement the locality statistics (remote failures, remote nucleation, front radius, coverage entropy, duration scaling).
- Update `runner.py` to support `"type": "rgg" | "soft_rgg"`, `"fear_field": {"type": "local"}`, and `"seed_layout": "disc"`.

## 2. Validation
- Run exact same-graph $\mu=0$ match (both engines must produce the exact same failed set given the graph).
- Statistical agreement at $\mu>0$ (with $\ell \ge \sqrt{2}$ torus diameter) vs global field.

## 3. Simulation Sweep
- Run the hard RGG at $\bar D = 2\log n$.
- Sweep $\bar\mu$ and test the global field vs the local field at $\ell/r_n \in \{1, 4, 16, \infty\}$.
- Evaluate the C-Q5 nucleation law, duration dichotomy, and coverage entropy homogenization.
