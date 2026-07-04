# Task E Report: Fear-field trajectory concentration

**Owner:** Crewmate E (Antigravity)
**Verification Date:** 2026-07-04

## 1. Objective
Measure how the variance of the fear-field trajectory across trials behaves as system size $n$ grows, validating the core concentration assumption of the Asymptotic Decoupling Conjecture. Frame the report as empirical measurement, not proof support.

## 2. Experimental Setup
*   **Engine:** Python engine (full round-by-round histories).
*   **Runner Script:** `scripts/run_task_e.py`
*   **Configs:** 
    *   `configs/fear_concentration_n1000.json`
    *   `configs/fear_concentration_n2000.json`
    *   `configs/fear_concentration_n4000.json`
    *   `configs/fear_concentration_n8000.json`
*   **Sweep Parameters:** $r=2, \text{concentration}=50.0, \theta=0.5, \text{target\_mean\_degree}=8.0, \alpha=0.7$, $\mu \in \{0.3, 0.5\}$, seed multiples $\in \{0.8, 1.1\}$, 1000 trials per cell.

## 3. Results & Verification
*   **Self-Audit against DoD:**
    *   All configs committed. Raw output generated via script.
    *   Relative variance figure regenerates from raw results via `scripts/run_task_e.py`.
    *   `analyze_fear_field_concentration` has a passing unit test in `tests/test_analysis.py`, and the full suite is green.
*   **Observations:**
    *   The relative variance decays monotonically as $n$ increases, but the decay rate $\gamma$ from the fit $\log(\text{rel\_var}) \sim -\gamma \log n$ is shallower than $1/n$. Measured values for $\gamma$ fall between $\sim 0.1$ and $\sim 0.45$ across different rounds and regimes, rather than $\gamma \approx 1$.
    *   The decay is consistent in both subcritical and near-critical seeding regimes, but the rate of concentration weakens slightly at later rounds (e.g., $k=3$ vs $k=1$).
    *   **Note**: This task was originally started by a Claude agent which got blocked by a rate limit. An Antigravity native agent took over to finish the script, fix history tracking in the Python runner, execute the simulation sweeps, and generate the final report.
