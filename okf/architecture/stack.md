---
type: Concept
title: "§5 — Coding Standards & Architecture (5.1–5.2: stack & performance contract)"
description: "Frozen §5.1–5.2: two-language split (C++ core, Python orchestration) and the performance contract."
mutability: frozen
---

# §5 — Coding Standards & Architecture (5.1–5.2: stack & performance contract)

Goal: clean, structured, **reproducible** scientific code. A result that can't be regenerated from a
seed and a config does not count as done.

### 5.1 Stack — two-language split (decision D-001)
The performance-critical core is **C++**; orchestration, analysis, and plotting stay in **Python**.
This is the right-tool split (it mirrors numpy/scipy's own architecture), it puts C++ exactly where
it pays off, and it keeps the science iterable. *Honest scope note:* C++ is **not required for the
MVP** — Python is fast enough for the core diagram (see §5.2). It is justified by the data-hungry
critical-window study and by the C++ learning/résumé goal, and it must **not** delay the Wk 1–2
go/no-go.
- **C++ core (the hot path):** C++17/20, built with **CMake**. `<random>` for RNG, `std::vector` /
  **CSR** adjacency for the graph, optional **OpenMP** to parallelize realizations. Scope is exactly
  three things: $G(n,p)$ generation + the single-cascade engine + the realization loop. *Nothing else
  goes in C++.*
- **Python orchestration:** Python 3.11+, `numpy`, `scipy`, `matplotlib`, `pandas`. Drives the
  $(r,\mu,n)$ sweeps, invokes the C++ core, reads its raw output, computes $P(\text{systemic})$ /
  bimodality / the width exponent, and makes every figure. `networkx` for *inspection only*, never as
  a data structure.
- **E1 — C++ ↔ Python boundary. ✅ DECIDED (D-003, 2026-06-03): (a) standalone C++ executable + file
  I/O.** Python writes a config / passes args, C++ writes raw per-realization outcomes to
  `results/raw/`, Python reads them back — chosen because it is dead simple, the languages stay
  decoupled and independently debuggable (standard C++ tooling, no Python in the loop), it maps
  trivially to PACE array jobs, and the data crossing is tiny so serialization cost is nil. *(b)*
  **pybind11** (compile the C++ as a Python extension and call it directly — cleaner, more
  résumé-impressive, but adds build complexity) is **deferred to the §6 stretch menu.** Build the C++
  core as a library (graph / rng / engine) with a **thin `main.cpp` CLI wrapper**, so a pybind11
  binding can be layered over the same core later without a rewrite.
- **Never** materialize a dense $n\times n$ float adjacency matrix, in either language.

### 5.2 Performance contract (from the feasibility analysis)
- Generate $G(n,p)$ **sparsely** (Batagelj–Brandes, $O(n + \text{edges})$).
- Maintain a **per-node failed-neighbor counter**, updated only when a neighbor fails.
- One cascade realization is **$O(\text{edges})$**. At $np\approx10$, $n=5000$ is milliseconds even in
  Python; the C++ core is what makes the $10^6$–$10^7$-run critical-window study comfortable.
- A coarse diagram ($r\in\{2,3,4\}$, ~30 $\mu$ points, ~500 realizations/cell) ≈ $10^5$–$10^6$
  cascades — minutes-to-overnight on a laptop. If a design implies more than that for the *core*
  diagram, something is wrong.
