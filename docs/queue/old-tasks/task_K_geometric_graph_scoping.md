# Task K — Scoping doc: panic-field locality on geometric graphs (Q5)

**One-line task.** Produce a rigorous, implementation-ready design document for the advisor-directed Q5 extension (D-028): move from $G(n,p)$ to random geometric graphs (and, as a generalization, geometric inhomogeneous random graphs / GIRGs), and design a concrete test of whether the panic field stays spatially local or the cascade still percolates globally.

**Touches:** new `docs/research/q5_geometric_graph_scoping.md`. Read-only against everything else.

## Environment note (read first)

This container has no git access, on purpose — do not attempt `git commit`/`push`/`branch`/`worktree`. This task only writes one new file under `docs/research/`, so no isolation mechanism is needed; edit in place. **This is a design document, not an implementation task** — do not modify `src/`, `cpp/`, or any file under `results/`. A human (with git access) will read the doc and decide whether to turn it into an implementation task next.

## Why this is low-human-input

Same shape as Task J: a literature-grounded design exercise ending in a spec and a falsifiable conjecture, no simulation runs, no code, no mid-task human judgment calls needed.

## Context to read first

- `docs/PROJECT_TRACKER.md` §2 (North Star), §3 (Model Specification), §4 (Analytical Benchmark), §9 Q5, and D-028 in §11 (the advisor's exact directive: random geometric graphs first, generalizing to distance-decaying connection probability, then GIRGs).
- `docs/LESSONS_LEARNED.md` in full.
- `docs/souvik_dhara_markdown/` — check for any papers already in the repo on geometric random graphs or GIRGs; if none, the design doc should still proceed using the advisor's framing plus general knowledge of the GIRG literature, and should flag which specific citations are still needed (to hand to the human, since this container may not have live internet/paper access — check first whether it does, and if so, look up the canonical GIRG references, e.g. Bringmann–Keusch–Lengler, to cite properly).
- If `okf/` exists by the time this task runs (Task I may have completed first), read `okf/model/` instead of the tracker sections above — same content, new location.

## Plan

1. **Define the graph model precisely, in stages matching the advisor's directive:**
   (a) random geometric graph: $n$ points in $[0,1]^2$ (or a torus, to avoid boundary effects — state the choice and why), edge iff distance $< r_n$ for some connectivity radius $r_n(n)$ chosen to land in an analogous "Janson regime" (specify the scaling analog of $np^r \to 0$, $np \to \infty$ for this geometry);
   (b) generalize to a distance-decaying connection *probability* (soft geometric graph) rather than a hard cutoff;
   (c) generalize further to a GIRG (combining degree heterogeneity from Task J with geometry) — this stage can be a shorter forward-pointer to Task J's design rather than fully repeated.
2. **Design the locality measurement.** This is the crux of Q5: define a concrete, computable statistic for "does the panic field stay spatially local." Candidates to consider and choose from (justify the choice): the geodesic/Euclidean spread of the failed set over time, a spatial autocorrelation of per-round new failures, or a comparison of cascade radius growth rate vs. $\sqrt{t}$ (diffusive) vs. linear-in-$t$ (ballistic/percolating). State it precisely enough to compute from a single simulation run's history.
3. **Reconcile with the existing fear channel (§3.3).** The current fear field $g_t$ is a *global* scalar (fraction of the whole system that failed last round) — on a geometric graph this is the natural first thing to question. Propose both: (i) keep $g_t$ global as a baseline/control, and (ii) a spatially-local variant (e.g. fear computed from failures within a neighborhood radius) as the actual test of the locality question, and be explicit about which one the falsifiable conjecture in step 4 is actually about.
4. **Formulate the falsifiable conjecture**, per the advisor's adopted workflow (D-028): e.g. "with a global fear field, the cascade percolates across the whole spatial domain once systemic, regardless of geometry (fear breaks locality); with a spatially-local fear field, the cascade stays geographically confined even when systemic." State it precisely enough that a simulation could confirm or refute it.
5. **Sketch the analytical angle**, mirroring §4's approach but flag honestly if a clean mean-field/generating-function analysis is much harder here than for $G(n,p)$ or the configuration model (geometric graphs break the local tree-likeness that Janson's machinery and Watts/Gleeson–Cahalane recursions rely on — say so explicitly rather than forcing an analogy that doesn't hold; this is exactly the kind of tension §14 rule 5 / the tracker's "guard the direction" rule wants surfaced, not silently smoothed over).
6. **Write the implementation plan** in the shape of this project's `implementation_plan.md` convention (`AGENTS.md` Section IV): what new graph-generation code is needed in `src/twocascade/`, whether the C++ engine needs a parallel implementation (geometric graphs may not fit the current CSR-adjacency-from-Batagelj–Brandes generation path — flag this explicitly), and what the §5.4-style cross-validation check would look like.
7. **Name the risks**, mirroring §7's style, e.g.: "if the locality effect is trivial (fear always breaks locality, or never does, regardless of parameters), the result may be a clean negative result rather than a phase transition — that's still publishable per §2's honest-novelty framing, but say so up front rather than assuming a positive result."

## Definition of Done

- [ ] `docs/research/q5_geometric_graph_scoping.md` exists, self-contained.
- [ ] All three stages (hard RGG, soft/distance-decaying, GIRG) are addressed, with the GIRG stage allowed to be a shorter forward-pointer to Task J's design doc if that task has also run.
- [ ] The locality statistic is defined precisely enough to compute from simulation output, not left vague.
- [ ] The falsifiable conjecture is stated precisely enough to test, and specifies which fear-field variant (global vs. local) it's about.
- [ ] The doc explicitly reconciles with §2 (North Star) and §4 (existing benchmark), flagging tension rather than silently resolving it.
- [ ] No file outside `docs/research/` is modified.

## Watch-outs

- Don't assume the Janson-regime machinery (§4) transfers to geometric graphs without checking — local tree-likeness is exactly what geometric graphs violate, and forcing the analogy would repeat the kind of unproven-claim mistake flagged in D-025 (the discrepancy-bound argument that was found false and withdrawn) and the general "confirm, don't assume" ethos the auditor/critic/reviewer pipeline in this repo exists to enforce.
- Per `LESSONS_LEARNED.md`'s "Adjacency Representation" pitfall: a geometric graph generator must still avoid a dense $n \times n$ representation — call out the spatial data structure (grid buckets / k-d tree for neighbor queries) in the implementation plan rather than leaving it implicit.
