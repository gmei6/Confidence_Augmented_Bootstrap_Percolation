# Task N: Q4 Configuration Model Simulation

**Objective:** Implement the erased configuration model with power-law degrees and degree-dependent fear, and run the first simulation sweep to test C-Q4.

**Reference:** `docs/research/q4_config_model_scoping.md`

## 1. Implementation
- Create `src/twocascade/graphs.py` with `sample_powerlaw_degrees`, `sample_configuration_model`, and `sample_degree_dependent_fears`.
- Do NOT modify the oracle `reference.py`.
- Update `src/twocascade/runner.py` to support `"graph": {"type": "configuration_model"}` and `"fear": {"gamma": ...}`.
- Implement strict RNG discipline (separate streams for degrees, pairing, fears, and cascades).

## 2. Validation
- Validate degree moments, tail exponent, and erased fraction vs target laws.
- Perform Prong A (exact $\mu=0$ match) and Prong B (statistical $\mu>0$ match) cross-validation as specified in the scoping doc.
- Verify the numerical fixed-point benchmark.

## 3. Simulation Sweep (Phase 1)
- Sweep $n \in \{4000, 10000, 20000\}$, $\tau \in \{2.5, 3.5\}$, $\gamma \in \{-1, 0, 1\}$, $\bar\mu \in \{0, 0.1, \dots, 0.7\}$.
- Record results through the runner and evaluate C-Q4 clauses (tilt monotonicity, size-biased collapse, tail-gated small-seed collapse).
