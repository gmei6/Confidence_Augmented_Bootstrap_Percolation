# Q4 Scoping — Degree-Dependent Fear on a Power-Law Configuration Model

**Status:** design document only (no implementation). Produced for queue task J on 2026-07-04.
**Research question affected:** **Q4** (okf/open-questions.md; advisor directive D-028, 2026-07-01): *degree-dependent fear factor on a power-law configuration model — advisor explicitly requested this simulation.*
**Reader contract:** self-contained; §N labels refer to the migrated tracker sections (`okf/` bundle — §3 = `okf/model/`, §4 = `okf/benchmark.md`, etc.).

> **Notation guard** (same warning as `docs/research/other/souvik_dhara_papers_application.md`): $\alpha,\beta$ are overloaded across this project (Janson scaling $p_n=\beta_J n^{-\alpha_J}$; Beta$(\alpha_B,\beta_B)$ fear). This doc uses **$\tau$** for the power-law degree exponent, **$\gamma$** for the fear–degree tilt exponent (local to this doc), and never bare $\alpha/\beta$.

---

## 1. Graph model: erased configuration model with power-law degrees

**Replace** $G(n,p)$ **with** $\mathrm{CM}_n(\mathbf d)$, the configuration model on degree sequence $\mathbf d = (d_1,\dots,d_n)$, constructed by uniform half-edge pairing (each vertex $j$ gets $d_j$ stubs; repeatedly pair a stub with a uniformly chosen unpaired stub). This is the exact construction in the advisor's own papers (Bhamidi–Dhara–van der Hofstad–Sen, *EJP* 27:103, §1.1 — in-repo under `docs/souvik_dhara_markdown/`) and in van der Hofstad, *Random Graphs and Complex Networks* Vol. I ch. 7 (the book Prof. Dhara pointed to at the 2026-07-01 meeting, D-028/S-038).

**Degree distribution.** Draw $d_i$ i.i.d. from a discrete power law with hard minimum:
$$\mathbb P(D=k) = \frac{k^{-\tau}}{\zeta(\tau,d_{\min})},\qquad k\ge d_{\min},$$
with $\zeta(\tau,d_{\min})=\sum_{k\ge d_{\min}}k^{-\tau}$ the Hurwitz normalizer. If $\sum_i d_i$ is odd, add one stub to a uniformly chosen vertex (standard evenness fix; an $O(1/n)$ perturbation — document the fixed rule so runs are reproducible).

- **$d_{\min} = r$** (i.e. 2 for the working $r{=}2$). A node with $d_i<r$ can *never* fail through the solvency channel (it is solvency-immune, reachable only by fear); setting $d_{\min}=r$ keeps every node exposed to both channels and avoids an accidental "immune fringe" confound. If we later *want* an immune fringe (link to Ruan et al.'s blocked nodes, §13), lower $d_{\min}$ deliberately — as a variant, not a default.
- **Exponent regimes to cover, motivated by the advisor's own program:** $\tau\in(3,4)$ (finite variance, infinite third moment — the critical-window regime of Dhara–van der Hofstad–van Leeuwaarden–Sen 2017) and $\tau\in(2,3)$ (infinite variance — the scale-free/tiny-giant regime of Bhamidi–Dhara–van der Hofstad 2024). **Concrete contrast pair for the first sweep: $\tau=3.5$ vs $\tau=2.5$**, with $\tau=2.2$ as a stretch point (hub dominance strongest). The degree-tail axis is the whole point of Q4 — the motivating question from D-028 is precisely *"can a small failure set still cascade widely under a fat-tailed degree distribution?"*
- **Sparse, bounded mean degree.** $\mathbb E[D]$ is an $O(1)$ constant set by $(\tau, d_{\min})$ — e.g. $(\tau{=}2.5, d_{\min}{=}2)\Rightarrow \mathbb E[D]\approx 3.7$. There is deliberately **no** $p_n$-style density scaling knob (see §3 below for the head-on reconciliation with D-004).

**Simple-graph handling: erased configuration model.** After pairing, delete self-loops and collapse multi-edges. Rationale: (i) the cascade engine's adjacency-list contract (`adjacency[i]` = neighbor indices, one entry per neighbor) assumes simple graphs — multi-edges would silently double-count a single failed neighbor toward the $r$ threshold, which is a *modeling* change, not an implementation detail; (ii) erasure is the standard choice with clean theory (vdH Vol. I §7.5: the erased CM's degree distribution converges to the target law; for $\tau>2$ the erased fraction is $o(1)$ per node but concentrated at hubs). **Watch-out to measure, not assume:** at $\tau\in(2,3)$ hubs lose a non-trivial share of their stubs to erasure ($d_{\max}=\Theta(n^{1/(\tau-1)}) \gg \sqrt n$ forces multi-edges); every run must log realized-vs-target tail exponent and $d_{\max}$ before/after erasure. If erasure distortion turns out to matter, the fallback is a rank-1 inhomogeneous model (Norros–Reittu / Chung–Lu), which the advisor's 2024 paper uses natively — flag at pilot time, don't silently switch.

## 2. Degree-dependent fear: mean-tilted Beta, population mean pinned

The current model (§3.3, D-002) draws $f_i\sim\mathrm{Beta}(\mu\kappa,(1-\mu)\kappa)$ once at $t=0$, i.i.d. and degree-independent, so $\mathbb E[f_i]=\mu$ exactly. **Q4 keeps the Beta shape and makes only the conditional mean degree-dependent:**

$$f_i \mid d_i \;\sim\; \mathrm{Beta}\!\big(\mu(d_i)\,\kappa,\;(1-\mu(d_i))\,\kappa\big),\qquad
\mu(d) \;=\; \min\!\Big\{\,\bar\mu\,\frac{(d/\langle D\rangle)^{\gamma}}{Z_n(\gamma)}\,,\; 1-\varepsilon\Big\},$$

where $\langle D\rangle = \frac1n\sum_i d_i$, $\varepsilon = 10^{-3}$ (cap guard; log cap-hit counts), and $Z_n(\gamma) = \frac1n\sum_i (d_i/\langle D\rangle)^{\gamma}$ is the **empirical normalizer that pins the population mean fear at $\bar\mu$ for every tilt $\gamma$** (computed on the realized degree sequence, so $\frac1n\sum_i \mu(d_i)=\bar\mu$ exactly up to cap events).

- $\gamma = 0$ **recovers the current model exactly** ($\mu(d)\equiv\bar\mu$): the frozen $G(n,p)$-baseline fear draw is the degenerate limit, which is both the backward-compatibility invariant for code and the control arm for experiments.
- $\gamma > 0$: **hubs more fearful** — financial reading: highly connected banks see more counterparty stress and news flow first; interconnectedness makes distress *salient* to them (herding/exposure-visibility channel).
- $\gamma < 0$: **hubs less fearful** — financial reading: too-big-to-fail confidence, diversification, implicit guarantees. Both directions are economically defensible, which is exactly why the tilt is a *parameter*, swept over $\gamma\in\{-1,0,+1\}$ first (extremes $\pm2$ in the pilot's inertness check, §7).

**Why pin the population mean.** The subcritical-amplifier invariant (§3.3's central structural fact) survives *by construction*: expected fear failures in round $t$ are $\sum_i f_i g_t \approx g_t \sum_i \mu(d_i) = \bar\mu\, a_{t-1}$, so the fear-only per-failure reproduction number stays $R_{\text{fear}} \approx \bar\mu < 1$ **for every $\gamma$ and every degree sequence**. Fear remains an amplifier that cannot ignite alone; the $\bar\mu$ sweep axis stays directly comparable to the baseline; and the *only* thing $\gamma$ changes is **where in the degree distribution the fear mass sits** — i.e. the experiment isolates the fear–degree covariance, not total fear.

**The quantity $\gamma$ actually moves** (this drives §4–§5): the **size-biased mean fear**
$$\mu^\star(\gamma) \;=\; \frac{\mathbb E[\mu(D)\,D]}{\mathbb E[D]},$$
the mean fear of the bank *at the end of a uniformly random edge*. A fear-failed bank contributes $d_i$ failed-neighbor increments to the solvency channel, so fear→solvency coupling is governed by $\mu^\star$, not $\bar\mu$. $\mu^\star$ is increasing in $\gamma$, equals $\bar\mu$ at $\gamma=0$, and — the heavy-tail punchline — for $\tau\in(2,3)$ the size-biased degree law has tail exponent $\tau-1\in(1,2)$ (infinite mean), so even moderate $\gamma>0$ concentrates enormous fear mass on exactly the nodes whose failure is structurally catastrophic.

**Frozen-decision reconciliation (explicit, per the direction-guard rule):** D-002's *Beta family and exact-mean property* are preserved (mean exact conditionally on $d_i$; population mean exact by $Z_n$); what changes is i.i.d.-ness across nodes ($f_i$ becomes i.i.d. *conditional on degree*). D-005/D-006 (incremental field $g_t=a_{t-1}/n$, window family) carry over **unchanged** — the field stays global and degree-blind; only susceptibility is degree-aware. Neither decision is contradicted, but adopting Q4 into the model spec would *extend* §3.3/§3.5 and therefore requires its own decision entry (d-031+) if/when promoted from scoping to model — this doc deliberately does not make that edit.

## 3. What carries over, what breaks

| Model element | Status under Q4 |
|---|---|
| Absorbing failure, absolute-$r$ solvency rule (§3.2) | **Unchanged.** |
| Simultaneous rounds + halting on quiet window (§3.4) | **Unchanged** (engine is graph-agnostic). |
| Incremental global fear field $g_t = a_{t-1}/n$, window family (D-005/D-006) | **Unchanged.** |
| Beta fear with exact mean (D-002) | **Extended** — conditional mean $\mu(d_i)$; $\gamma=0$ is the old model. |
| Systemic-event threshold $\theta$, bimodality framing (§3.5) | **Unchanged** (re-verify bimodality holds on CM before trusting $\theta=0.5$; heavy tails can distort the trough). |
| Graph law $G(n,p)$ (§3.1) | **Replaced** by erased $\mathrm{CM}_n(\mathbf d)$, power-law degrees. |
| Janson benchmark & regime (§4, D-004): $p_n=\beta_J n^{-\alpha_J}$, $np\to\infty$, $np^r\to0$; closed-form $a_c,t_c$ | **Does not apply — stated, not ignored.** The CM here is the *bounded-mean-degree* regime D-004 explicitly rejected *for the baseline* and explicitly reserved "as the natural home only if the project later pivots to a configuration model (Q2)." D-028 resolved Q2 exactly that way, so entering this regime on the Q4 *track* is the sanctioned path, not a silent contradiction. Consequences: no closed-form $a_c$; the analytical anchor becomes the sparse-regime cascade theory — Watts (2002), Gleeson–Cahalane (2007), Amini–Cont–Minca (2016), all already in §13 — via the recursion in §5. The $\mu=0$ code-validation test must be re-anchored to a *numerical* fixed-point benchmark (§6) instead of $a_c=(1-1/r)\,t_c$. |
| Finite-size scaling protocol (§4: scale $p$ with $n$, seed at multiples of per-$n$ $a_c$) | **Replaced**: on CM, $n$ grows at *fixed* $(\tau,d_{\min})$ (degree law is $n$-free); seeds set as multiples of the *numerical* critical seed per $(n,\tau,\gamma,\bar\mu)$. |
| North Star (§2) | **Consistent with the D-028-amended direction**: the claim stays "self-referential global panic field × absolute-$r$ rule, characterized by a systemic-event phase diagram" — now with the degree axis the advisor asked for. The $G(n,p)$ results remain the paper's validated core; Q4 is additive, not a rewrite. Tension to keep visible: Q4 leaves the regime where "extending Janson's theorems" (D-004's rationale) is available; the theory target shifts to the ACM/branching-process lineage. That trade was made consciously by the advisor (D-028). |

## 4. The falsifiable conjecture (C-Q4)

Per the D-028 workflow (model → simulate → falsifiable conjecture → test → attempt proof), state it sharply enough to be killed by simulation:

> **C-Q4 (fear–degree covariance controls ignition; tail heaviness gates it).**
> Fix $r=2$, $\kappa=50$, $\theta=0.5$, seed $a$ uniformly random with $a = o(n)$ (working point: $a \le 10$ absolute). Let $a_c^{\mathrm{emp}}(\bar\mu,\gamma,\tau;n)$ be the empirical critical seed (the $P(\text{systemic})=\tfrac12$ crossing).
> **(i) Tilt monotonicity.** At fixed $\bar\mu\in(0,1)$ and fixed $\tau$, $a_c^{\mathrm{emp}}$ is strictly decreasing in $\gamma$: putting the *same total fear* on higher-degree banks strictly enlarges the systemic region.
> **(ii) Size-biased collapse.** The tilt acts through the size-biased mean: cells with equal $\mu^\star$ (different $(\bar\mu,\gamma)$ combinations, same $\tau$) have equal $a_c^{\mathrm{emp}}$ within Monte-Carlo error — i.e. plotted against $\mu^\star$ instead of $\bar\mu$, the boundary curves for different $\gamma$ collapse onto one curve.
> **(iii) Tail-gated small-seed collapse.** For $\tau\in(2,3)$ and $\gamma\ge0$ there is a threshold $\mu_c(\tau,\gamma)<1$ such that for $\bar\mu>\mu_c$ a *bounded* seed ($a=r$, independent of $n$) produces $P(|A^*|/n\ge\theta)$ bounded away from 0 as $n\to\infty$; for $\tau>3$ (finite variance) with the same $(\bar\mu,\gamma)$, $P(\text{systemic}\mid a=r)\to0$. In words: **low fear keeps cascades small regardless of the degree tail; high fear on a fat tail lets even a minimal shock go systemic — and the fat tail is necessary, not just helpful.**

Operational refutation tests: (i) fails if any $\gamma$-monotonicity violation exceeds MC error across the grid; (ii) fails if matched-$\mu^\star$ cells differ by more than the paired-trial confidence band (this is the strongest, most informative part — it would say the mechanism is *not* summarized by one scalar); (iii) fails if the $a=r$ ignition probability at $\tau=2.5$ decays with $n$, or if $\tau=3.5$ ignites too. Each clause is a plain grid readout of $P(\text{systemic})$ — no new estimator theory needed beyond the existing `analysis.py` crossing interpolation (with the D-021 empirical clamping filter).

## 5. Mean-field sketch (heterogeneous tree recursion replacing §4's Poisson map)

Mirror §4's structure — a self-consistent map whose **saddle-node tangency at an interior unstable fixed point** locates the critical seed — but on the CM's local-tree limit (unimodular Galton–Watson tree, size-biased offspring; vdH Vol. II, and precisely the local-limit machinery of the advisor's lineage), replacing Poisson$(c\varphi)$ neighbor counts:

- Let $p_k$ be the degree law, $q_k = (k+1)p_{k+1}/\mathbb E[D]$ the size-biased offspring law, $\varphi$ the failed fraction, and $\rho$ the probability that a uniformly random *edge* points to a failed bank (on CM these differ; $G(n,p)$'s $\rho=\varphi$ shortcut is what breaks).
- **Fear exposure telescopes** (the incremental field's gift): a bank alive through the whole cascade sees total fear hazard $\sum_t f_i g_t = f_i A^{*}/n$, so its fear-failure probability is $\approx 1-e^{-f_i\varphi} \approx f_i\varphi$ (small-$\varphi$), preserving the amplifier structure exactly as in §4's "fear piece."
- **Node map:** $\varphi' = F(\varphi,\rho) = \frac{a}{n} + \mathbb E_{D}\Big[\big(1-\tfrac{a}{n}\big)\Big( \underbrace{\mathbb P\big(\mathrm{Bin}(D,\rho)\ge r\big)}_{\text{solvency}} + \underbrace{\mu(D)\,\varphi}_{\text{fear}} - \text{overlap}\Big)\Big]$,
  **edge map:** $\rho' = G(\varphi,\rho)$ = the same expression under the size-biased law $q$ with $\mathrm{Bin}(D^\star-1,\rho)$ (exclude the parent edge). The **fear term under the edge map carries $\mathbb E_{q}[\mu(D^\star)] = \mu^\star$** — this is where the size-biased mean of §2 enters the analytics and why clause (ii) of C-Q4 is the natural conjecture.
- **Critical seed:** smallest $a$ for which the iterated pair map escapes the basin of the near-zero stable fixed point — numerically, the tangency $\det(J - I) = 0$ of the 2-D map's Jacobian at the interior fixed point. For $\tau\in(2,3)$, $\mathbb E[D^\star]=\infty$: the linearized solvency term at 0 is still super-linear (nothing fails via solvency with $<r$ failed neighbors — the §3.2 super-linearity survives on any graph), but the *second* iterate through a hub is unbounded, which is the analytic shadow of clause (iii).
- **Known honesty caveats,** carried over from §4's own: the map is round-free (equilibrium counting) while the simulation is round-structured; the leave-m-out/decoupling machinery (D-025) was proven on $G(n,p)$ and does *not* transfer automatically — on CM the fear field is still global (helpful) but neighbor counts are degree-correlated (harmful). Rigor target here is Tier-2/Tier-3 of D-009 (conjecture + simulate), not Tier-1.

## 6. Implementation plan (per `AGENTS.md` §IV `implementation_plan.md` convention)

**Oracle-protection first (the load-bearing design choice):** `run_cascade` in `src/twocascade/reference.py` is **graph-agnostic** — it consumes an adjacency list and per-node fears. Therefore Q4 needs **zero changes to the oracle**: no edit to `reference.py` is proposed, requested, or permitted here (D-026 precedent: even additive oracle changes need a standalone approved instruction). New code goes in a **new module**:

- `src/twocascade/graphs.py` (new):
  - `sample_powerlaw_degrees(n, tau, d_min, rng) -> list[int]` — inverse-CDF sampling of the Hurwitz-normalized law + the documented evenness fix.
  - `sample_configuration_model(degrees, rng) -> list[list[int]]` — half-edge pairing via one `rng.permutation` of the stub array (pairing adjacent entries), then erase self-loops/multi-edges. $O(\sum d_i)$ time and memory; **no dense matrix at any point** (LESSONS §2). Returns simple adjacency lists matching `sample_gnp_adjacency`'s contract.
  - `sample_degree_dependent_fears(degrees, mu_bar, gamma, kappa, rng) -> list[float]` — computes $Z_n(\gamma)$ on the realized sequence, then per-node Beta draws; logs cap-hit count and realized $\bar\mu,\mu^\star$.
- `src/twocascade/runner.py`: additive config branch — `"graph": {"type": "configuration_model", "tau": ..., "d_min": ...}` and `"fear": {"gamma": ...}`; absent keys → existing $G(n,p)$ path byte-identical (the $\gamma=0$/no-key regression guard). Metadata block gains realized-degree diagnostics (tail fit, $d_{\max}$, erased fraction, realized $\mu^\star$).
- **RNG discipline (LESSONS §1):** spawn *separate* `SeedSequence` children for (degree sequence, pairing permutation, fear draws, cascade Bernoullis) per trial — never share one stream across stages, never additive seed offsets. Degree sampling and pairing sharing a stream is this design's specific correlated-stream trap (repeated-node pairing correlates with degree ranks).
- **C++ parity (explicit scope statement, per §IV):** **out of scope for the pilot; required for production.** Phase 1 runs Python-only at $n\le 2\times10^4$, feasible because one cascade is $O(\text{edges})$ and $\mathbb E[D]=O(1)$. Phase 2 (only if the pilot shows a live effect, §7) ports `graphs.py`'s two samplers + degree-dependent fear into `cpp/include/twocascade/graph.hpp`/`engine.hpp` (`main.cpp` gains `--graph cm --tau --dmin --gamma`); the Beta-via-Gamma guard in LESSONS §2 already covers the $\mu(d)\in\{0,1\}$ cap edge. Python remains the oracle throughout.
- **§5.4-style cross-validation for the new pieces:**
  - *Generator prong (new, Python-internal):* realized degree moments and tail exponent vs. target law; erased fraction vs. vdH §7.5 asymptotics; size-biased neighbor-degree mean $\mathbb E[D^\star]$ vs. $\mathbb E[D^2]/\mathbb E[D]$ (finite-$\tau>3$ case) on $10^3$ graphs.
  - *Engine prong A (exact, $\mu=0$):* dump one erased-CM graph + seed set from Python, load the same graph in C++, require identical final failed sets (the cascade is deterministic at $\mu=0$ given the graph — unchanged from §5.4).
  - *Engine prong B (statistical, $\mu>0$):* $P(\text{systemic})$ and $|A^*|/n$ agreement on matched $(\tau,\gamma,\bar\mu)$ cells, thresholded by p-value per D-024 (never a fixed KS distance), single documented seed both sides.
  - *$\mu=0$ benchmark re-anchor:* replace the $a_c$ closed form with the §5 numerical fixed-point solution; the validation test becomes "empirical threshold within the finite-$n$ band of the numerical tangency point," with the band estimated the same way the $G(n,p)$ tests handled the finite-$np$ offset (S-006/S-007 lesson: don't mistake finite-size offset for regime error).
- **Config/sweep shape for the first real run (Phase 1):** $n\in\{4000, 10000, 20000\}$, $\tau\in\{2.5, 3.5\}$, $\gamma\in\{-1,0,1\}$, $\bar\mu\in\{0,0.1,\dots,0.7\}$, seed multiples over the numerical $a_c$, $\ge500$ trials/cell, plus the C-Q4(iii) bounded-seed cells ($a=r$) at the extreme corners. Raw outputs through the runner only (stamped config+seed+commit), per the results-integrity rule.

## 7. Risks (mirroring §7's style) and early kill-switches

- **Inertness of the tilt (the Q4-specific "μ has no teeth").** At fixed $\bar\mu$, $\gamma$ might move the boundary by less than MC error — then Q4 collapses to "Q2 with plain CM," the covariance story dies, and only the tail axis remains. **Catch it first:** pilot at $n=10^4$, $\tau=2.5$, extreme tilts $\gamma=\pm2$, one $\bar\mu$ column (0.4), paired trials on shared graphs. If $\Delta P(\text{systemic})$ between $\gamma=+2$ and $-2$ is within the paired confidence band everywhere, stop and report a (publishable, honest) negative before building anything else. Analytic early-warning of the same failure: compute $\mu^\star(\pm2)$ on sampled sequences first — if the cap at $1-\varepsilon$ compresses $\mu^\star$'s range at the chosen $(\tau,\bar\mu)$, widen $\varepsilon$ headroom or lower $\bar\mu$ *before* burning trials.
- **Erased-CM distortion at $\tau\in(2,3)$** (hub stub loss biases exactly the objects the conjecture is about). Mitigation: the §6 generator prong measures it; fallback is Norros–Reittu (advisor-native). Decide on data, not taste.
- **Loss of the closed-form benchmark** weakens the "validated against theory" story that anchored Weeks 1–5. Mitigation: the numerical tangency benchmark + the ACM threshold as an independent cross-check at $\mu=0$; and the $G(n,p)$ baseline remains fully intact as the validated core (§3 of this doc).
- **Compute discipline.** Heavy tails self-average slowly (one $d_{\max}$ hub dominates realizations): expect noisier $P(\text{systemic})$ per trial count than $G(n,p)$; graph-resampling *between* trials is mandatory (quenched-vs-annealed distinction — averaging over graphs is the object of study), and PACE only enters at Phase 2 scale. Trial budgets per cell should be set from a pilot variance estimate, not copied from $G(n,p)$ configs.
- **Direction guard.** Q4 must not silently *become* the model: §3 stays frozen $G(n,p)$ until an explicit decision (d-031+) adopts the CM track into the spec. This doc is input to that decision, not the decision.

## 8. References (all already in `okf/references/` / §13 unless noted)

- Janson, Łuczak, Turova & Vallier (2012) — the retiring benchmark, §4.
- van der Hofstad, *RGCN* Vol. I — CM construction, erased CM (§7.5); the advisor's named reference (D-028, S-038).
- Bhamidi, Dhara, van der Hofstad & Sen (EJP 2022); Dhara, van der Hofstad, van Leeuwaarden & Sen (2017); Bhamidi, Dhara & van der Hofstad (2024, "tiny giant," in-repo) — the advisor's critical-CM program; regime choices in §1 and the $\tau\in(2,3)$ intuition in §5 lean on these.
- Watts (2002); Gleeson & Cahalane (2007); Amini, Cont & Minca (2016) — the sparse-regime cascade recursion machinery for §5.
- `docs/research/other/souvik_dhara_papers_application.md` — prior in-repo analysis; §5's size-biased fear term sharpens its closing observation that *in a bounded-mean-degree CM, fear heterogeneity enters the takeoff boundary at first order* (unlike the Janson regime, where it is second-order) — Q4's tilt is precisely a first-order probe of that claim.
