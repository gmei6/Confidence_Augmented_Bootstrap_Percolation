# Q5 Scoping — Panic-Field Locality on Geometric Graphs (RGG → soft RGG → GIRG)

**Status:** design document only (no implementation). Produced for queue task K on 2026-07-04.
**Research question affected:** **Q5** (okf/open-questions.md; advisor directive D-028, 2026-07-01): *geometric effects on cascade locality — random geometric graphs first, then geometric inhomogeneous random graphs; does the panic field stay spatially local, or does the cascade still percolate across "continents"?*
**Reader contract:** self-contained; §N labels refer to the migrated tracker sections in `okf/` (§3 = `okf/model/`, §4 = `okf/benchmark.md`). Companion doc: `q4_config_model_scoping.md` (Task J — degree axis; stage (c) below points there).

> **Offline-citation flag:** this container has no internet access and `docs/souvik_dhara_markdown/` contains no geometric/GIRG papers. The GIRG/RGG citations in §8 are from memory and marked **[verify]** — a human with paper access should confirm authors/years/IDs before this doc is cited onward.

---

## 1. Graph model, in the advisor's three stages

### (a) Hard random geometric graph (RGG) — the first experiment

$n$ points $x_1,\dots,x_n$ i.i.d. uniform on the **unit torus** $\mathbb T^2 = [0,1)^2$ (torus, not box: kills boundary effects that would otherwise contaminate the locality statistics near walls — a cascade front hitting a wall slows down for reasons that have nothing to do with the physics under study; state-of-the-art RGG results are typically proved on the torus for the same reason). Edge $i\sim j$ iff $\|x_i - x_j\|_{\mathbb T} < r_n$ (Euclidean torus metric, hard cutoff).

**Radius scaling.** Choose $r_n$ by pinning the mean degree:
$$\bar D = n\pi r_n^2 = c\,\log n,\qquad c > c_0 \approx 1\ \text{(connectivity regime)},\ \text{working value } c = 2.$$
Rationale, stated against §4's regime discipline rather than borrowed from it: the RGG is connected w.h.p. iff $n\pi r_n^2 \gtrsim \log n$ (Penrose **[verify]**; Gupta–Kumar), so $c\log n$ is the thinnest regime where "does the cascade cross the whole domain" is even well-posed (below it, disconnected islands trivially answer "no"). **There is no honest analog of the Janson window $np\to\infty,\ np^r\to0$ here** — that window exists to keep the *tree-like branching* solvency channel non-degenerate, and an RGG is the opposite of tree-like: neighborhoods are cliquish (two banks within $r_n$ of bank $i$ are themselves likely within $r_n$ of each other — constant local clustering $\approx 0.5865$ in 2D). Forcing a "$np^r\to0$ analog" would be exactly the unfounded-analogy mistake the D-025 withdrawal taught us to avoid; §5 states what replaces it.

### (b) Soft RGG (distance-decaying connection probability)

$\mathbb P(i\sim j) = \min\{1, (\|x_i-x_j\|_{\mathbb T}/r_n)^{-\alpha_g}\}$ conditionally independently over pairs, with decay exponent $\alpha_g > 2$ (= dimension; ensures finite mean degree) and the same mean-degree pinning (calibrate the prefactor numerically to hold $\bar D = c\log n$). This adds *occasional long-range edges* — the knob that interpolates between pure geometry ($\alpha_g\to\infty$ recovers the hard RGG) and mean-field ($\alpha_g\downarrow 2$ approaches degree-driven long-range percolation). Long edges are the solvency channel's own way to jump continents, so sweeping $\alpha_g$ separates *structural* locality breaking (long edges) from *behavioral* locality breaking (global fear) — the confound the design must be able to tell apart.

### (c) GIRG — forward-pointer to Task J

GIRGs (Bringmann–Keusch–Lengler **[verify]**) attach to each node a weight $w_i$ (power-law, exponent $\tau$ — exactly Task J's degree axis) *and* a position, with $\mathbb P(i\sim j)\approx\min\{1,(w_iw_j/(n\|x_i-x_j\|^2))^{\alpha_g}\}$. It nests (a)/(b) (constant weights) and Task J's regime (geometry ignored). Everything in `q4_config_model_scoping.md` §2 (degree-dependent fear, size-biased mean $\mu^\star$, pinned population mean) carries over verbatim; the only new interaction is hub *placement* (a fearful hub is now a *located* super-spreader). This stage is Q6's home (D-028 track 3) and is deliberately left as this pointer — do not fully spec it until (a)/(b) results exist.

## 2. The locality measurement (the crux)

The hard RGG gives us one **exact structural fact that makes locality measurable without heuristics**: a solvency failure requires $\ge r$ failed neighbors, and neighbors are within $r_n$ — so **any node that fails at distance $> r_n$ from the previously-failed set can only have failed through fear.** Solvency spreads as a contact process (front); only fear can act at a distance. The statistics below exploit this dichotomy; all are computable from one trial's recorded history (per-round new-failure index lists + the stored positions).

Primary statistics (per round $t$, per trial):

1. **Remote-failure count** $N_{\mathrm{rem}}(t) = \#\{i \text{ newly failed at } t:\ \mathrm{dist}(x_i, F_{t-1}) > r_n\}$, where $F_{t-1}$ is the failed set (distance via the same grid-bucket index used for graph generation — no $O(n^2)$ pass). On the hard RGG these are *certified* fear failures. Also record its normalized rate $N_{\mathrm{rem}}(t)/a_t$.
2. **Remote nucleation count** $N_{\mathrm{nuc}}(t)$: cluster the remote failures of round $t$ (single-linkage with linking radius $2r_n$, grid-assisted); a cluster is a *nucleus* if it contains $\ge r$ nodes pairwise within $r_n$ (i.e. it can seed autonomous solvency growth next round). This is the quantity the mechanism in §4 predicts scales like $g_t^{\,r}$ — remote *ignition* needs $r$ coincident fear failures in one ball, so single stray fear failures ($N_{\mathrm{rem}}$ high, $N_{\mathrm{nuc}}\approx0$) do **not** break locality for $r\ge2$.
3. **Front radius** $R_q(t)$: the $q{=}0.9$ quantile of torus distance from the seed centroid to round-$t$ new failures (quantile, not max — max is one stray fear failure away from meaningless). Growth diagnostic: fit $R_q(t)\sim t^{\zeta}$; $\zeta\approx1$ = ballistic front (local growth), $R_q$ jumping to the torus diameter $\approx$ saturation = delocalized.
4. **Coverage entropy** $H(t)$: partition $\mathbb T^2$ into a $16\times16$ grid; $H(t)$ = Shannon entropy of the distribution of round-$t$ new failures over cells, normalized by $\log 256$. Pure front growth keeps $H$ low (failures concentrated on an annulus); global-field secondary nucleation drives $H\to1$ (spatially homogeneous rain). This is the "one number per round" summary for figures.
5. **Duration scaling** $T_\theta(n)$: rounds to reach $|A_t|/n \ge \theta$, conditioned on systemic. The cheapest cross-$n$ discriminator (needs no positions at all): a confined ballistic cascade must cross the domain, so $T_\theta = \Theta(1/r_n) = \Theta(\sqrt{n/\log n})$; a fear-delocalized cascade multiplies everywhere at rate $\propto \bar\mu g_t$ once $g_t$ is macroscopic, giving $T_\theta = O(\mathrm{polylog}\ n)$ tail behavior. Fitting the $T_\theta$-vs-$n$ exponent across $n\in\{10^4,\dots\}$ distinguishes the two phases even where position logging is too heavy.

**Decision: statistics 2 (mechanism-certifying), 4 (summary), and 5 (cross-$n$) are the committed trio**; 1 and 3 are recorded but supporting. Justification: 2 is the only one that measures the *causal* mechanism (fear-created autonomous growth nuclei) rather than a symptom; 4 is robust and figure-friendly; 5 survives at scales where storing positions/history is expensive.

## 3. Fear-field variants: global (control) vs local (treatment)

The current field $g_t = a_{t-1}/n$ (§3.3, D-005) is a **global scalar** — economically, planet-wide news flow. On a geometric substrate that is a *modeling choice*, not a given, and it is the choice Q5 interrogates. The design runs both:

- **(i) Global field (baseline/control):** exactly the frozen model on the new graph. Zero engine change; `run_cascade` is graph-agnostic. All frozen dynamics (D-005/D-006 incremental field, §3.4 halting) carry over unchanged.
- **(ii) Local field (treatment):** each bank hears only failures within fear radius $\ell$:
  $$g_t^{(i)} \;=\; \frac{\#\{j \in B(x_i,\ell) : j \text{ failed in round } t-1\}}{\#\{j \in B(x_i,\ell)\}},$$
  realized-count normalization (denominator = actual banks in the ball, not $n\pi\ell^2$) so $g_t^{(i)}\in[0,1]$ exactly and density fluctuations don't manufacture fear. Bank $i$'s fear-failure probability in round $t$ is $f_i\,g_t^{(i)}$; everything else (Beta draw D-002, simultaneous update §3.4) is unchanged. **Subcriticality survives:** one failed bank $j$ contributes next round $\sum_{i\in B(x_j,\ell)} f_i/|B(x_i,\ell)| \approx \bar\mu$ expected fear failures (ball sizes concentrate at $n\pi\ell^2 \gg 1$), so per-failure fear offspring $\approx \bar\mu < 1$ for every $\ell$ — the amplifier invariant (§3.3) is preserved, and $\ell \to$ torus diameter recovers (i) exactly (the $\gamma{=}0$-style backward-compatibility limit; also the natural cross-validation identity, §6).
  - $\ell$ is swept on $\ell/r_n \in \{1, 4, 16, \infty\}$: fear as local gossip, regional news, national news, global panic.
  - **Halting rule unchanged** ("no new failures anywhere") — with a local field, a quiet round still zeroes every $g_t^{(i)}$ simultaneously, so §3.4's absorbing-state argument goes through verbatim.

**Frozen-decision reconciliation (explicit):** variant (ii) *modifies the §3.3 field definition* — it is not deducible from the frozen model, and this doc does not adopt it; it specifies the experiment that would justify (or kill) adopting it via a d-031+ decision. D-005's incremental (last-round) structure and D-006's window generalization are orthogonal to the locality axis and are kept as-is (window sweeps on geometric graphs are out of scope here).

## 4. The falsifiable conjecture (C-Q5)

Mechanism the conjecture is built on (and which makes it non-obvious): with a **global** field, remote fear failures rain uniformly at per-ball rate $\propto \bar\mu\,g_t$, but for $r\ge2$ a *single* remote failure is inert — remote **ignition** needs $\ge r$ fear failures coincident in one $r_n$-ball, so the remote nucleation rate scales like $(\bar\mu\, g_t)^{r}\cdot n\pi r_n^2$ per round: **quadratically suppressed (at $r{=}2$) until $g_t$ is large, then explosive.** Locality breaking should therefore be a *threshold in $g_t$*, not a constant leak.

> **C-Q5 (global fear breaks locality via delayed secondary nucleation; local fear preserves it).** Fix $r=2$, $\kappa=50$, $\theta=0.5$, hard RGG at $\bar D = 2\log n$, macroscopic-enough seed to go systemic, $\bar\mu \in (0,1)$ fixed.
> **(i) Nucleation law (global field).** Conditioned on systemic cascades, $\mathbb E[N_{\mathrm{nuc}}(t)]$ is $\approx 0$ while $g_t \le g^\ast$ and grows $\propto g_t^{\,r}$ beyond — on a log-log plot of $N_{\mathrm{nuc}}(t)$ vs $g_t$, slope $\approx r = 2$. Refuted if the fitted slope is $\approx 1$ (constant leak, no threshold) or nucleation never occurs even at $g_t$ near its systemic peak.
> **(ii) Phase dichotomy in duration.** With the global field, $T_\theta(n)$ grows strictly slower than the ballistic bound: $T_\theta(n)/\sqrt{n/\log n} \to 0$ (secondary nucleation short-circuits the front). With the local field at any fixed $\ell/r_n$, $T_\theta(n) = \Theta(\sqrt{n/\log n})$ (ballistic restored, prefactor decreasing in $\bar\mu$ and $\ell$ — fear accelerates the front but cannot jump). Refuted by matching duration exponents between the two field types, or a global-field exponent equal to the ballistic one.
> **(iii) Homogenization.** With the global field, coverage entropy $H(t) \to 1$ before the cascade completes ($\ge0.9$ by the time $|A_t|/n = \theta$); with the local field at $\ell/r_n \le 4$, $H(t)$ stays $\le 0.6$ throughout. (Numbers are pre-registered working thresholds, to be sanity-tuned on the $\mu=0$ control where $H$ must stay low by construction.)
>
> In advisor-directive terms: *with global panic, a local power-grid failure **does** cascade to another continent — but only after a delay set by the $g^{r}$ nucleation barrier; making panic local by any finite radius restores continental confinement.*

All three clauses are single-figure readouts of the §2 statistics; no new estimator theory. The $\mu=0$ arm is the built-in negative control (no fear ⇒ $N_{\mathrm{rem}} \equiv 0$ identically on the hard RGG — any violation is a bug, which makes it a free engine test).

## 5. Analytical angle — honestly harder, and what replaces the §4 machinery

**What breaks (said plainly, per the direction-guard rule):** every analytic tool this project has used assumes local tree-likeness — Janson's martingale/branching structure (§4), the Watts/Gleeson–Cahalane recursions, Task J's size-biased tree recursion, and the D-025 leave-m-out decoupling all fail on RGGs, whose clustering is $\Theta(1)$ and whose short cycles are the *point* of the geometry. There is no honest generating-function shortcut; forcing one would repeat the withdrawn-discrepancy-bound mistake (D-025's history). Tier-1 rigor (D-009) is out of reach here for now; the target is Tier-2/3.

**What replaces it (the right classical frames):**
- $\mu=0$ anchor: bootstrap percolation on geometric/lattice-like structures — nucleation-and-growth metastability (Aizenman–Lebowitz; Holroyd's sharp 2D threshold **[verify]**; RGG-specific: Bradonjić–Saniee **[verify]**). Key qualitative import: on geometric substrates the "critical seed" is not a global count (Janson's $a_c$) but a **local density condition** — one supercritical droplet anywhere grows ballistically forever. The §4 tangency-of-a-scalar-map picture is replaced by *droplet criticality + front velocity*. This changes what "critical seed size" even means and must be respected in experiment design (seed the trials as a localized disc vs scattered uniform — run both, they are different experiments; the locality question wants the localized disc).
- $\mu>0$, global field: **two-scale heuristic = front propagation + KJMA/Avrami nucleation theory [verify]**: a deterministic front of velocity $v(\bar\mu)$ (local growth, fear-accelerated) plus a spatial Poisson rain of secondary nuclei with intensity $\lambda(t) \propto n\pi r_n^2\,(\bar\mu g_t)^r$ per ball per round; Avrami-type coverage integrals give $\varphi(t)$ and predict the §4-style knee in $T_\theta$. This yields C-Q5's exponents and is presented as an explicitly heuristic mean-field-in-time (not in space) calculation.
- Soft RGG / GIRG stage: long-range percolation and GIRG bootstrap results (Koch–Lengler; Candellero–Fountoulakis on hyperbolic models **[verify]**) become the anchors; these actually *do* restore some tree-like machinery at $\alpha_g$ near 2 — worth flagging as the one place a rigorous foothold may reopen.

## 6. Implementation plan (per `AGENTS.md` §IV convention)

**Oracle protection (the governing constraint):** the **global-field arm needs zero engine changes** — `reference.py::run_cascade` takes any adjacency list. The **local-field arm cannot be expressed through the current engine** (per-node fear probability depends on a second, fear-radius neighborhood), so it needs new engine code — which will **not** touch `reference.py` (D-026 precedent: oracle changes need a standalone approved instruction; none is requested here).

- `src/twocascade/geometry.py` (new):
  - `sample_torus_points(n, rng) -> ndarray (n,2)`.
  - `build_rgg_adjacency(points, radius) -> list[list[int]]` — **grid-bucket spatial index** (cell size $r_n$, scan 3×3 neighboring cells): expected $O(n\bar D)$ time, list-of-lists output matching the existing adjacency contract; **no dense structure, no k-d tree needed** (buckets beat trees at fixed radius; this satisfies the LESSONS "Adjacency Representation" pitfall explicitly).
  - `build_soft_rgg_adjacency(points, r_n, alpha_g, rng)` — same buckets for the near field plus explicit rejection sampling for the heavy far-field tail (document the truncation/normalization choice; far-field pair candidates via per-annulus Poisson counts, never all pairs).
  - `build_fear_adjacency(points, ell)` — the fear-radius graph for the local field (same bucket machinery).
  - `run_cascade_local_fear(adjacency, fear_adjacency, nodes, r, seeds, rng, ...)` — a **variant engine, clearly labeled experimental**, mirroring `run_cascade`'s two-phase simultaneous-update structure (evaluate frozen snapshot → apply; LESSONS §2 "Simultaneous Update Parity") with per-node $g_t^{(i)}$ from the fear graph. Validation identity: with `fear_adjacency` = complete graph (or $\ell \ge$ torus diameter), it must reproduce the *statistics* of `run_cascade` (per-round draw order differs, so demand distributional agreement per D-024's p-value discipline, plus an exact-match mode at $\mu=0$ where fear draws are never taken and the trajectory is deterministic given the graph — that prong is exact).
  - Locality statistics (§2) as pure post-processing functions reading (positions, per-round new-failure lists): `remote_failures`, `nucleation_clusters`, `coverage_entropy`, `front_radius`.
- `runner.py`: additive config branch `"graph": {"type": "rgg"|"soft_rgg", "mean_degree_c": ..., "alpha_g": ...}`, `"fear_field": {"type": "global"|"local", "ell_over_rn": ...}`, `"seed_layout": "disc"|"uniform"`; absent keys → existing path byte-identical. Raw output gains optional per-round new-failure index lists + positions (gate behind an output flag — same JSON-bloat concern as D-014; positions are $2n$ floats/trial, so default off above $n=10^4$ and rely on statistic 5).
- **RNG discipline:** separate `SeedSequence` children for (positions, soft-edge coin flips, fears, cascade Bernoullis); never additive offsets (LESSONS §1).
- **C++ parity — flagged, not assumed:** the current C++ core generates $G(n,p)$ via Batagelj–Brandes into CSR; **an RGG generator does not fit that path** (needs point storage + bucket index) and the local-fear engine needs the second CSR graph. Phase 1 is Python-only ($n \le 3\times10^4$: one cascade is $O(\text{edges} + n\cdot\text{rounds})$, and ballistic durations $\sim\sqrt n$ keep this minutes-scale). Phase 2 ports generator + local-field engine to `cpp/` only if Phase 1 shows the C-Q5 dichotomy is real and the $T_\theta(n)$ exponent needs $n \ge 10^5$ for a clean fit (likely — flag PACE here). §5.4-style prongs: (A) exact same-graph $\mu=0$ failed-set match (both engines, both field types — at $\mu=0$ the field type is irrelevant, which is itself the test); (B) statistical $P(\text{systemic})$/$|A^*|/n$ agreement at matched cells, p-value thresholds per D-024.

## 7. Risks (mirroring §7's style)

- **Trivial-outcome risk, both directions.** (a) Fear may *always* break locality at any $\bar\mu>0$ (if $N_{\mathrm{nuc}}$ has no threshold — slope 1, constant leak), or (b) *never* (if the $g^r$ barrier sits above the $g_t$ a systemic cascade ever reaches — nucleation needs $g_t \gtrsim (n\pi r_n^2)^{-1/r}/\bar\mu$, which shrinks with $n$; do this arithmetic against pilot $g_t$ trajectories *first*, it is a 10-minute pre-check that can kill or retune the design before any sweep). Either flat outcome is still a clean, publishable negative under §2's honest-novelty framing — *pre-commit to reporting it as such* rather than parameter-fishing for a transition (the D-024 lesson: recalibrate the test, never hunt for a passing seed).
- **Confound: long edges vs global fear** both delocalize. Controlled by design: hard RGG has no long edges (fear is the only remote channel — certified by the $>r_n$ argument), and the soft-RGG $\alpha_g$ sweep measures the structural channel separately at $\bar\mu=0$ before the two are combined.
- **Seed-layout sensitivity.** Disc vs uniform seeding are different physics on geometric graphs (droplet vs multi-nucleus start). Both are specified in the config; the conjecture is about disc seeding; uniform is the robustness arm.
- **The "critical seed" concept shifts** (local density, not global count — §5): naive reuse of `analysis.py`'s $a_c$-crossing machinery on seed *count* may produce smooth, non-sharp curves and tempt misreading. Expect and document a rounded transition; the sharp objects here are the duration/entropy dichotomies, not $a_c$.
- **Compute/storage.** Position + history logging at $n>10^4$ is the JSON-bloat trap (D-014) — statistic 5 (durations only) is the designed cheap fallback; keep full-position logging to a small designated subset of cells.
- **Direction guard.** Like Q4: this track leaves the Janson benchmark (§4) — sanctioned by D-028, but §3 stays the frozen model until a dedicated decision adopts any geometric variant. The local-fear field (§3(ii)) in particular is a *model change proposal*, not a model change.

## 8. References (to add to `okf/references/` when verified — see offline flag at top)

- Penrose, *Random Geometric Graphs*, OUP 2003 **[verify]** — RGG connectivity regime.
- Bradonjić & Saniee, bootstrap percolation on RGGs **[verify — arXiv:1201.2953?]**.
- Aizenman & Lebowitz (1988); Holroyd (2003) — lattice bootstrap nucleation/metastability, the $\mu=0$ conceptual anchor **[verify]**.
- Bringmann, Keusch & Lengler, "Geometric inhomogeneous random graphs" **[verify — arXiv:1511.00576]**; also their expected-linear-time GIRG sampling paper **[verify]** — stage (c).
- Koch & Lengler, bootstrap percolation on GIRGs **[verify — ICALP 2016?]**; Candellero & Fountoulakis, bootstrap percolation on hyperbolic random graphs **[verify]**.
- Deijfen, van der Hofstad & Hooghiemstra, scale-free percolation **[verify]** — the long-range/heavy-tail bridge relevant to stage (b)→(c).
- Kolmogorov / Johnson–Mehl / Avrami nucleation-growth theory (any standard statistical-physics treatment) **[verify]** — §5's two-scale heuristic.
- In-repo: Janson et al. (§4, what does *not* transfer); `q4_config_model_scoping.md` (Task J, stage (c) and the degree-dependent fear it inherits); Dhara et al. critical-window papers (the advisor-program context motivating D-028's geometric track).
