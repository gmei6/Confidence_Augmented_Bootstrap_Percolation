# Two-Channel Cascade Model of Bank Failure

This repository houses the simulation environment and analytical tools for **A Two-Channel Cascade Model of Bank Failure**. The project investigates the propagation of systemic failures on financial networks by coupling a local threshold rule (solvency failure) with a self-reinforcing global feedback field (panic/fear channel).

---

## 📖 Theoretical Overview

The model propagates failures through two distinct channels on an interbank network represented by an Erdős–Rényi random graph $G(n,p)$:

1. **Channel 1 — Solvency (Janson local rule):**
   A solvent bank fails if at least $r$ of its neighbors have failed:
   $$\bigl|\{\, j \in N(i) : j \text{ failed} \,\}\bigr| \ge r$$
   Here, $r$ represents the capital-buffer depth.

2. **Channel 2 — Fear (Global self-referential feedback):**
   A solvent bank $i$ fails via the fear channel in round $t$ with probability:
   $$P(\text{fear failure}) = f_i \cdot g_t$$
   * **Global fear field ($g_t$):** The fraction of banks that failed in the *previous* round ($g_t = a_{t-1}/n$).
   * **Individual fear sensitivity ($f_i$):** Drawn once at $t=0$ from a Beta distribution $\text{Beta}(\alpha, \beta)$ calibrated such that $E[f] = \mu$ exactly.

---

## 📂 Repository Layout

The codebase follows the two-language split (Python for orchestration, C++ for performance-critical simulation blocks) as defined below:

```
two-channel-cascade/
├── cpp/                          # C++ Core (Hot Path)
│   ├── CMakeLists.txt            # CMake build file
│   ├── include/twocascade/       # C++ header definitions
│   ├── src/                      # C++ implementation files
│   └── tests/                    # C++ unit tests
├── configs/                      # Experiment config definitions (JSON/YAML)
├── docs/                         # Literature, notes, and agent specifications
├── results/                      # Simulation outputs
│   ├── raw/                      # Raw per-realization output (git-ignored)
│   └── figures/                  # Plotted figures (git-ignored)
├── src/twocascade/               # Python Orchestration Package
│   ├── reference.py              # Pure-Python validation engine (Oracle)
│   ├── model.py                  # Parameter mappings and analytical equations
│   ├── runner.py                 # Simulation job orchestrator
│   ├── analysis.py               # Post-processing analytics
│   ├── meanfield.py              # Theoretical saddle-node tangency curves
│   └── plotting.py               # Figure generation
├── tests/                        # Python test suites and scratch scripts
│   ├── test_mu0_bootstrap_threshold.py  # Validation check at mu=0
│   ├── test_window_len.py        # Memory-window validation
│   └── scratch_check.py          # Scaling exponent verification script
├── pyproject.toml                # Project metadata and package configuration
├── pytest.ini                    # Pytest configuration
├── requirements.txt              # Pinned Python dependencies
└── README.md                     # This documentation file

```

---

## 🛠️ Getting Started

### Prerequisites

Ensure you have Python 3.11+ installed. Verify your installation by running:
```bash
python3 --version
```

### Installation

1. Clone the repository to your local workspace.
2. Initialize a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install the pinned dependencies and the package in editable mode:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

---

## 🧪 Running Tests

Unit tests are written using the `pytest` framework. To run the validation tests:

```bash
# Execute all Python tests
python3 -m pytest

# Run specific validation tests in verbose mode
python3 -m pytest tests/test_mu0_bootstrap_threshold.py -v
```

All implementations are validated against Janson et al. (2012) bootstrap percolation thresholds at $\mu=0$.
