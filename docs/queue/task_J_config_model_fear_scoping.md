# Task J — Scoping doc: degree-dependent fear on a configuration-model graph (Q4)

**One-line task.** Produce a rigorous, implementation-ready design document for the advisor-directed Q4 extension (D-028): replace $G(n,p)$ with a power-law configuration-model graph, and make the fear channel degree-dependent, ending in a falsifiable conjecture ready to test.

**Touches:** new `docs/research/q4_config_model_scoping.md`. Read-only against everything else.

## Environment note (read first)

This container has no git access, on purpose — do not attempt `git commit`/`push`/`branch`/`worktree`. This task only writes one new file under `docs/research/`, so no isolation mechanism is needed; edit in place. **This is a design document, not an implementation task** — do not modify `src/`, `cpp/`, or any file under `results/`. A human (with git access) will read the doc and decide whether to turn it into an implementation task next.

## Why this is low-human-input

Purely a literature-grounded design exercise: read the frozen model spec, read the advisor's directive, read the cited references, and produce a spec. No simulation runs, no code, no ambiguous judgment calls that need a human mid-task — the human review happens once, at the end, reading the finished doc.

## Context to read first

- `docs/PROJECT_TRACKER.md` §2 (North Star), §3 (Model Specification — especially §3.2 solvency channel and §3.3 fear channel), §4 (Analytical Benchmark), §9 Q4, and D-028 in §11 (the advisor's exact directive).
- `docs/LESSONS_LEARNED.md` — all of it, but especially the "Mathematical & Simulation Pitfalls" section (Beta concentration, subcriticality of fear, Janson scaling regime).
- `docs/souvik_dhara_markdown/` — the papers already in the repo, particularly anything on configuration models and degree sequences (van der Hofstad's book is cited in §13 as the advisor's recommended reference for this exact extension; check `docs/research/` for any existing notes referencing it).
- If `okf/` exists by the time this task runs (Task I may have completed first), read `okf/model/` and `okf/model/forks.md` instead of the tracker sections above — same content, new location.

## Plan

1. **Define the graph model precisely.** Specify the power-law configuration model construction: degree distribution (e.g. $\mathbb{P}(D=k) \sim k^{-\tau}$ for some exponent range — ground the choice in van der Hofstad's book or the Dhara et al. critical-window papers already cited in §13), the degree-sequence sampling procedure, and how edges are generated from it (configuration-model pairing / erased configuration model — note the self-loop/multi-edge handling choice explicitly, since $G(n,p)$'s code assumed simple sparse graphs).
2. **Define the degree-dependent fear function precisely.** The current model has $f_i \sim \text{Beta}(\mu\kappa, (1-\mu)\kappa)$ drawn once, independent of degree (§3.3/§3.5). Propose a concrete functional form making individual fear $f_i$ depend on degree $d_i$ (e.g. $E[f_i] = \mu(d_i)$ for some monotone $\mu(\cdot)$, high-degree "hub" banks more/less fearful — motivate the direction from the financial-contagion framing in §2, not arbitrarily) while preserving the existing structural invariant that $R_{\text{fear}} < 1$ per-bank (subcriticality, §3.3's central risk).
3. **State what changes and what's preserved.** Explicitly list: which frozen model facts (§3.2 solvency rule, §3.4 dynamics/halting rule, the incremental fear field D-005/D-006) carry over unchanged, and which (§3.3's fear draw, §4's Janson benchmark which assumes $G(n,p)$) need a new derivation or a stated "benchmark doesn't apply here, here's why."
4. **Formulate the falsifiable conjecture**, per the advisor's adopted workflow (D-028): something in the shape of "low fear keeps cascades small regardless of degree-tail heaviness; high fear lets even a small failure set reach a large fraction, and the transition sharpens/shifts with the degree-dependence direction" — state it precisely enough that a simulation could confirm or refute it.
5. **Sketch the mean-field analysis**, mirroring §4's approach (tangency of a combined map at an interior unstable fixed point) but adapted to a configuration-model degree distribution instead of Poisson($c\varphi$) neighbor counts — this is the generating-function / Watts-style tree recursion the tracker's §4 "Machinery" note already points at (Watts 2002, Gleeson & Cahalane 2007, Amini–Cont–Minca 2016 — all cited in §13).
6. **Write the implementation plan** (in the same doc, or a linked section) in the shape of this project's own `implementation_plan.md` convention (per `AGENTS.md` Section IV): what changes in `src/twocascade/model.py`/`graph.py` generation code, whether the C++ engine needs a parallel change and why, and what the §5.4-style cross-validation check would look like for the new graph generator (same-graph exact-match test at a degenerate case, e.g. $\mu=0$, plus statistical agreement for $\mu>0$).
7. **Name the risks**, mirroring §7's style: what could make this extension a dead end (e.g., "if the degree-dependence direction is inert, this reduces to Task Q4 = Q1 restated"), and how the design would catch that early.

## Definition of Done

- [ ] `docs/research/q4_config_model_scoping.md` exists, self-contained (a reader who hasn't seen this task file can follow it).
- [ ] The graph model and degree-dependent fear function are both fully specified with concrete functional forms, not left as "TBD."
- [ ] The falsifiable conjecture is stated precisely enough to test.
- [ ] The doc explicitly reconciles with §2 (North Star) and §4 (existing benchmark) — flags, rather than silently ignores, any tension (per this project's own "guard the direction" rule, tracker §14 rule 5 / `AGENTS.md` Section II tracker-ownership rule).
- [ ] No file outside `docs/research/` is modified.

## Watch-outs

- Don't silently contradict a frozen decision (D-002 Beta distribution, D-005/D-006 incremental fear field, D-004 Janson $p$-scaling regime) — if the new graph model requires revisiting one of these, say so explicitly in the doc rather than quietly assuming a different rule.
- Per the "RNG Seeding" and "Adjacency Representation" lessons in `LESSONS_LEARNED.md`: don't propose a design that implies a dense $n \times n$ adjacency matrix or naive additive RNG seeding — configuration-model degree-sequence generation has its own correlated-stream pitfalls (repeated-node pairing), call this out in the implementation plan.
