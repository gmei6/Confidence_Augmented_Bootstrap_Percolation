# Two-Channel Cascade Model of Bank Failure

[![Interactive Visualizer](https://img.shields.io/badge/Interactive%20Visualizer-Live%20on%20GitHub%20Pages-blue?style=for-the-badge)](https://gmei6.github.io/Confidence_Augmented_Bootstrap_Percolation/)
[![Section 2 Study Site](https://img.shields.io/badge/Section%202%20Proofs-Live%20on%20GitHub%20Pages-green?style=for-the-badge)](https://gmei6.github.io/Confidence_Augmented_Bootstrap_Percolation/section2-reformulation/)
[![Advisor Update](https://img.shields.io/badge/Advisor%20Update-Live%20on%20GitHub%20Pages-orange?style=for-the-badge)](https://gmei6.github.io/Confidence_Augmented_Bootstrap_Percolation/advisor-update-2026-07-22/)

This repository houses the simulation environment and analytical tools for **A Two-Channel Cascade Model of Bank Failure**. The project investigates the propagation of systemic failures on financial networks by coupling a local threshold rule (solvency failure) with a self-reinforcing global feedback field (panic/fear channel).

👉 **[Interactive Visualizer & Guided Tutorial](https://gmei6.github.io/Confidence_Augmented_Bootstrap_Percolation/)** — step through a worked cascade example and explore the sandbox.

👉 **[Section 2 Reformulation Study Site](https://gmei6.github.io/Confidence_Augmented_Bootstrap_Percolation/section2-reformulation/)** — the two-channel Janson §2 reformulation with proofs, annotation mode, and audience mode.
👉 **[Advisor Update — Changes Since July 1, 2026](https://gmei6.github.io/Confidence_Augmented_Bootstrap_Percolation/advisor-update-2026-07-22/)** — implementation changes, experiment results (several marked preliminary), scope decisions, and open questions since the last meeting.

> 📌 **TODO (reminder):** Run a full validation pass with **Opus** over `section2-reformulation/index.html` — check the $B_k$ reformulation (definitions, fear field, Sequential Bridge), the newly added derivation `<details>` blocks, and the SVG figures for mathematical correctness before the next Pages deploy.

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

The connectivity scales as $p_n = \beta n^{-\alpha}$ with $\alpha \in (1/r, 1)$ (Janson regime), so $np \to \infty$ and the sharp-threshold dichotomy of Janson et al. (2012) applies at $\mu = 0$.

---

## 📊 Key Validated Results

| Result | Finding |
|--------|---------|
| **Critical seed scaling** | $a_c(\mu) = a_c(0)\,(1-\mu)^{r/(r-1)}$ — validated numerically for $r \in \{2,3,4\}$ |
| **θ-robustness** | Cascade boundary invariant across $\theta \in [0.2, 0.8]$ (bimodal final-size distribution) |
| **κ-robustness** | Fear heterogeneity (Beta concentration $\kappa \in [2, 200]$) shifts the boundary only at 2nd order |
| **Targeted seeding** | High-degree seeding shifts the boundary by $< 0.15\%$ of $n$ on $G(n,p)$; effect vanishes as $n \to \infty$ |
| **Window invariance** | Normalized memory window $X \in \{1,4,8\}$: max $|\Delta P| = 0.015 \le 0.03$; cascade duration grows with $X$ |
| **Finite-size ν (preliminary)** | Transition-width exponent $\nu \approx 8.4$ at $\mu=0$; $\nu \approx 5.3$ at $\mu=0.3$ — fear accelerates sharpening |

---

## 📂 Repository Layout

```
two-channel-cascade/
├── cpp/                          # C++ core (hot path)
│   ├── CMakeLists.txt
│   ├── include/twocascade/       # C++ header definitions
│   ├── src/                      # C++ implementation files
│   └── tests/                    # C++ unit tests
├── configs/                      # Experiment config JSON files
│   ├── sweep_wk3_4_r{2,3,4}.json       # Main (r,μ) phase-diagram sweeps
│   ├── kappa_sweep_r2_k{K}.json        # κ-robustness sweeps
│   ├── finite_size_r2_n{N}.json        # Finite-size ν sweeps (n=1000,2000,5000)
│   ├── seed_{random,targeted}_r2_n{N}.json  # Targeted-seeding comparison
│   └── window_r2_X{X}.json             # Memory-window invariance (X=1,4,8)
├── docs/                         # Research notes, tracker, and agent specs
│   ├── PROJECT_TRACKER.md        # Single source of truth for project state
│   ├── LESSONS_LEARNED.md        # Codebase gotchas and modeling pitfalls
│   └── research/                 # Research documents and proofs
├── results/                      # Simulation outputs (raw/ and figures/ git-ignored)
├── scripts/                      # Sweep runner and plotting entry points
│   ├── run_finite_size_sweeps.py
│   ├── plot_finite_size_scaling.py
│   ├── run_task_c.py / plot_task_c.py
│   ├── run_task_d.py
│   └── plot_wk3_4.py
├── section2-reformulation/       # Static study site: Janson §2 reformulation with proofs
│   ├── index.html
│   ├── style.css
│   └── script.js
├── src/twocascade/               # Python orchestration package
│   ├── reference.py              # Pure-Python validation oracle (do not modify)
│   ├── model.py                  # Parameter mappings and analytical equations
│   ├── runner.py                 # Sweep orchestrator
│   ├── analysis.py               # Post-processing: transition width, ν estimation
│   ├── meanfield.py              # Theoretical saddle-node tangency curves
│   └── plotting.py               # Figure generation (read-only on raw/analysis)
├── tests/                        # Python and JS test suites
│   ├── test_mu0_bootstrap_threshold.py  # μ=0 Janson validation
│   ├── test_cpp_validation.py           # C++↔Python cross-language parity (§5.4)
│   ├── test_cpp_window_validation.py    # C++ windowed fear cross-validation
│   ├── test_analysis.py                 # estimate_transition_width unit tests
│   ├── test_window_len.py               # Memory-window engine tests
│   ├── test_pairwise_decoupling.py      # Pairwise decoupling conjecture checks
│   ├── test_viz_walkthrough.js          # FIFO walkthrough trace (Node.js)
│   └── test_viz_cascade.js             # Cascade §3.4 behavioral invariants (Node.js)
├── viz/                          # Interactive GitHub Pages teaching site
│   ├── index.html                # Scroll page: Explainer → Glossary → Walkthrough → Sandbox
│   ├── walkthrough.js            # FIFO step-trace engine (Part A: μ=0, Part B: fear)
│   ├── tutorial.js               # Walkthrough renderer
│   └── cascade.js                # Cascade simulation engine
├── pyproject.toml
├── pytest.ini
├── requirements.txt
└── README.md
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

### Building the C++ engine

```bash
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
```

The compiled binary `twocascade_run` is required for C++-engine sweeps.

---

## 🧪 Running Tests

```bash
# All Python tests
python3 -m pytest

# Cross-language C++↔Python validation (§5.4)
python3 -m pytest tests/test_cpp_validation.py -v

# Viz correctness (requires Node.js)
node tests/test_viz_walkthrough.js
node tests/test_viz_cascade.js
```

All Python implementations are validated against Janson et al. (2012) bootstrap percolation thresholds at $\mu=0$. C++ parity is verified via Prong A (identical failed sets at $\mu=0$ on a shared graph) and Prong B (statistical agreement of $P(\text{systemic})$ for $\mu>0$, thresholded by p-value).

---

## 🔬 Running Sweeps

Sweeps are orchestrated via `twocascade.runner.run_sweep(config_path, engine=...)`. Each run stamps its output with the config, random seed, and git commit hash.

```python
from twocascade.runner import run_sweep

# C++ engine (fast, recommended for large n)
run_sweep("configs/sweep_wk3_4_r2.json", engine="cpp")

# Python engine (required for target_high_degree=True)
run_sweep("configs/seed_targeted_r2_n1000.json", engine="python")
```

Raw outputs land in `results/raw/` (git-ignored, regenerable). Figures are produced by the scripts in `scripts/`.
