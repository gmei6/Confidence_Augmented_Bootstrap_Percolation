---
type: Concept
title: "§5 — Coding Standards & Architecture (5.3: repository layout)"
description: "Frozen §5.3 repository layout."
mutability: frozen
---

# §5 — Coding Standards & Architecture (5.3: repository layout)

### 5.3 Repository layout
```
two-channel-cascade/
├── README.md
├── cpp/                          # C++ CORE (the hot path) — see E1 for how Python calls it
│   ├── CMakeLists.txt
│   ├── include/twocascade/
│   │   ├── graph.hpp             # CSR sparse G(n,p) (Batagelj–Brandes); fast neighbor iteration
│   │   ├── rng.hpp               # <random> wrapper; seed = f(base_seed, realization_index)
│   │   └── engine.hpp            # ONE cascade: counter-based, two channels; returns Outcome
│   ├── src/
│   │   ├── engine.cpp
│   │   └── main.cpp              # driver: read params → realization loop → write raw outcomes
│   └── tests/                    # engine unit checks (doctest/Catch2 or assert-based)
├── pyproject.toml / requirements.txt
├── configs/                      # one file per experiment — NO magic numbers in code
├── src/twocascade/               # PYTHON ORCHESTRATION
│   ├── runner.py                 # builds configs, invokes the C++ core (E1), collects raw output
│   ├── reference.py              # PURE-PYTHON engine — the ORACLE the C++ is validated against
│   ├── model.py                  # params, fear distributions (F3), a_c / p_c formulas
│   ├── analysis.py               # P(systemic), bimodality, threshold location, width exponent ν
│   ├── meanfield.py              # combined-map tangency; Janson a_c; overlay curves
│   └── plotting.py               # figures from saved raw results — never recomputes the simulation
├── results/
│   ├── raw/                      # per-realization outcomes — the ground-truth artifact
│   ├── figures/                  # Rendered verification plots
│   └── analysis/                 # Derived analytical compliance artifacts (D-020)
├── tests/                        # incl. μ=0 ↦ a_c, AND the C++-vs-Python agreement check (§5.4)
└── notebooks/                    # exploration ONLY; nothing canonical lives here
```
