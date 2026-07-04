# Task K Report: Q5 Scoping Doc — Panic-Field Locality on Geometric Graphs

**Date:** 2026-07-04 (fable overnight run) · **Research question affected:** Q5 (D-028) — new `docs/research/` document, nothing revised (stated per the AGENTS.md §III rule).

## What was produced

`docs/research/q5_geometric_graph_scoping.md`, covering all seven plan steps:

1. **Three graph stages per the advisor's directive:** hard RGG on the unit **torus** (choice justified: kills boundary contamination of the locality statistics) at mean degree $c\log n$, $c=2$ (connectivity regime — justified as the thinnest regime where "does it cross the domain" is well-posed); soft RGG with decay exponent $\alpha_g$ (isolates structural long-edge delocalization from behavioral fear delocalization); GIRG as a deliberate short forward-pointer to Task J's design (it nests both, and is Q6's home). The doc **explicitly refuses** to fabricate a Janson-window analog ($np^r\to0$) for RGGs and says why (cliquishness is the point of the geometry).
2. **Locality statistic defined exactly, not vaguely** — anchored on a structural fact that makes it rigorous on the hard RGG: solvency can only spread within $r_n$ of the failed set, so any farther failure is *provably* fear-caused. Committed trio: remote **nucleation** count (clusters of $\ge r$ coincident remote fear failures — the causal mechanism), grid coverage entropy (summary), and duration scaling $T_\theta(n)$ (position-free cross-$n$ discriminator: ballistic $\Theta(\sqrt{n/\log n})$ vs delocalized $O(\text{polylog})$). Supporting: remote-failure count, front-radius quantile. All computable from per-round new-failure lists + stored positions.
3. **Fear-field variants:** global $g_t$ kept as the control (zero engine change); local variant $g_t^{(i)}$ = realized failed fraction within fear radius $\ell$ (realized-count normalization keeps it in $[0,1]$; subcriticality $R_\text{fear}\approx\bar\mu$ shown preserved for every $\ell$; $\ell\to\infty$ recovers the frozen model — the backward-compatibility/validation identity). Explicitly flagged as a model-change *proposal* requiring a d-031+ decision if adopted.
4. **Falsifiable conjecture C-Q5** with a mechanism that makes it non-obvious: remote ignition needs $r$ coincident fear failures in one ball ⇒ nucleation rate $\propto (\bar\mu g_t)^r$ — a threshold, not a leak. Three clauses (log-log nucleation slope $\approx r$; duration-exponent dichotomy global-vs-local; entropy homogenization with pre-registered thresholds), each with a stated refutation. The $\mu=0$ arm is a built-in exact negative control ($N_\text{rem}\equiv0$ or it's a bug).
5. **Analytical angle honestly downgraded:** the doc states plainly that tree-likeness — and with it Janson's machinery, the Watts/Gleeson recursions, Task J's recursion, and D-025's decoupling — fails on RGGs (citing D-025's withdrawn-argument history as the cautionary precedent, per the task's watch-out). Replacement frames: lattice-bootstrap nucleation/metastability at $\mu=0$ ("critical seed" becomes a local-density condition, not a count) and a two-scale front-propagation + KJMA/Avrami nucleation heuristic for $\mu>0$, explicitly labeled heuristic; Tier-2/3 of D-009, not Tier-1.
6. **Implementation plan (§IV shape):** new `src/twocascade/geometry.py` (grid-bucket generator — the spatial data structure named per the watch-out, no dense matrix, no all-pairs; soft-RGG far-field via per-annulus Poisson sampling; fear-radius graph; a clearly-labeled variant engine `run_cascade_local_fear` mirroring the oracle's two-phase simultaneous update); **zero `reference.py` changes** (global arm reuses the oracle; local arm is a new module validated against the oracle in the $\ell\to\infty$ limit — exact at $\mu=0$, D-024 p-value statistics at $\mu>0$); additive runner config with byte-identical legacy path; position/history logging gated behind a flag (D-014 bloat lesson); C++ **explicitly flagged as not fitting the current Batagelj–Brandes/CSR path**, deferred to Phase 2 with PACE noted.
7. **Risks:** both trivial-outcome directions pre-committed as reportable negatives (with a 10-minute analytic pre-check on the nucleation barrier vs realistic $g_t$ before any sweep — the anti-parameter-fishing guard, citing the D-024 lesson); long-edge vs fear confound (controlled by the hard-RGG/soft-RGG split); disc-vs-uniform seeding sensitivity; the shifted meaning of "critical seed"; compute/storage; direction guard.

## Environment finding recorded in the doc

No internet in this container and no geometric/GIRG papers in `docs/souvik_dhara_markdown/` — per the task's instruction, the doc proceeds on the advisor's framing plus general knowledge and **marks every external citation [verify]** (Penrose; Bradonjić–Saniee; Aizenman–Lebowitz; Holroyd; Bringmann–Keusch–Lengler; Koch–Lengler; Candellero–Fountoulakis; Deijfen–vdH–Hooghiemstra; KJMA), with a top-of-file flag telling the human to confirm before onward citation.

## Definition of Done check

- [x] Doc exists, self-contained.
- [x] All three stages addressed (GIRG as the sanctioned forward-pointer to Task J).
- [x] Locality statistic precise and computable (five defined; committed trio named; the hard-RGG certification argument makes it exact, not heuristic).
- [x] Conjecture precise, refutable, and explicit that it concerns the **global** field breaking locality with the **local** field as the restoring treatment.
- [x] §2/§4 reconciliation explicit; the no-Janson-analog tension surfaced rather than smoothed (task watch-out honored).
- [x] No file outside `docs/research/` modified.

## Notes for the reviewer

- `/verify` gate unavailable in this sandbox; substituted a checklist self-audit (above) plus a consistency pass against the frozen decisions touched (D-002, D-005/D-006 kept; §3.3 locality variant explicitly gated behind a future decision).
- Git-dependent instructions in the task template don't apply; docs-only, edited in place per the task's own environment note.
