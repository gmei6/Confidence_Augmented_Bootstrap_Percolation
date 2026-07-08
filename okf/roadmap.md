---
type: Concept
title: "§6 — Roadmap (≈10 weeks)"
description: "Frozen ~10-week roadmap; MVP is one (r,mu) phase diagram with verified bimodality; checkboxes ticked in place."
mutability: frozen
---

# §6 — Roadmap (≈10 weeks) 🔒 *(structure frozen; check items off in place)*

> The **MVP** alone is a complete, presentable result. Everything past it is stretch. Protect the MVP.

**MVP (guaranteeable):** a clean, documented simulator → **one $(r,\mu)$ phase diagram of
$\Pr(|A^*|/n \ge \theta)$ at a single $n$**, with **verified bimodality**, plus an **overlaid
heuristic mean-field threshold** showing qualitative agreement.

- [x] **Wk 1 — Python prototype + code validation.** Build the two-channel cascade on sparse
      $G(n,p)$ (counter-based) **in Python first** — iteration speed beats throughput here, the model
      still has open forks, and $n{=}1000$ at a few hundred realizations is fast enough. Reproduce
      *pure* bootstrap percolation at $\mu=0$ and check the empirical seed threshold against $a_c$.
      This prototype becomes the **reference oracle** (`reference.py`) for the C++ port.
- [x] **Wk 2 — GO/NO-GO week.** (i) 1-D $\mu$-sweep at near-critical $r$: *does $\mu$ have teeth?*
      (ii) Bimodality histograms of $|A^*|/n$ (justify $\theta$). (iii) **Decide F1** (incremental vs.
      cumulative) and **fix the $p_n$ scaling (F4)**. If $\mu$ is inert, pivot (§7) before building
      the pipeline.
- [x] **Wk 3–4 — Port the (now-locked) hot path to C++ + full $(r,\mu)$ diagram at one moderate $n$
      (e.g. 1000).** With the model decided (forks closed in Wk 2), port $G(n,p)$ generation + the
      cascade engine + the realization loop to C++ (CSR, `<random>`), wire it to Python via E1, and
      **validate it against the Python reference (§5.4)**. Then run the full diagram and solidify the
      pipeline / parallelization / plotting; draft the heuristic mean-field threshold curve. *(Want
      C++ exposure sooner? Build it in parallel during Wk 2 against the stabilizing spec — but keep
      the Python prototype as the tool that decides the forks.)*
- [x] **Wk 5 — Overlay mean-field on empirical; iterate the analytics where they disagree.**
      *(First/second advisor meeting ~here — bring the diagram + threshold comparison.)*
- [x] **Wk 6–7 — Finite-size analysis** across 5–6 values of $n$; estimate the **transition-width
      scaling exponent $\nu$** (width $\sim n^{-1/\nu}$). Put the realization budget **near the
      boundary**, not deep in either phase. *(Preliminary: n∈{1000,2000,5000}; ν≈8.39 at μ=0, ν≈5.33 at μ=0.3; pending advisor Q3 alignment.)*
- [ ] **Wk 8 — First stretch goal** (recommended: configuration-model variant; see §2/§7 and the
      advisor angles).
- [x] **Wk 9 — Robustness & consolidation:** [x] $\theta$ sensitivity, [x] $\sigma$-sweep ($\kappa$), [x] random vs.
      targeted seeding (confirmed near-null on $G(n,p)$: shift shrinks from 0.13%→0.08% of $n$ as $n$ doubles);
      [x] fear-persistence window ($X$) invariance check (D-006): max $|\Delta P|=0.0146\le0.03$ ✓; duration grows $X=1\to8.6,X=4\to13.2,X=8\to17.8$ rounds at $\mu=0.5$ ✓.
- [ ] **Wk 10 — Write-up, clean figures, reproducibility pass, final presentation.**

**Stretch menu (advisor-aligned, increasing ambition):**
- **Performance / engineering polish:** OpenMP-parallel realizations in the C++ core, and a
  **pybind11** binding (E1 option b) so Python calls C++ directly. Both are strong, *true* résumé
  points **if actually built**, and they make the $10^6$–$10^7$-run critical-window study comfortable.
- Finite-size **width exponent** $\nu$ (cheapest way to speak Dhara's "critical window" dialect —
  pure simulation + curve fitting).
- **Configuration model** (+ targeted seeding): makes heterogeneity/targeting meaningful, connects to
  Amini–Cont–Minca, opens a universality-class question. *Stretch-of-stretch:* probe whether the
  critical cascade shows $n^{2/3}$-type scaling or a heavy-tailed size distribution at the boundary.
- **Spectral interpretation of the panic channel:** fear is a **rank-one / mean-field** coupling (the
  $f$ vector); solvency spread is governed by the adjacency operator (leading eigenvalue $\approx np$
  for $G(n,p)$); cascade takeoff $\to$ a spectral-radius condition. **Pitch as "spectral interpretation
  of the panic channel and its interplay with network structure," NOT "spectral theory of bootstrap
  percolation"** (the latter is false for $r\ge2$, since solvency contributes nothing to the
  linearization). Cleanest on a degree-heterogeneous graph.
