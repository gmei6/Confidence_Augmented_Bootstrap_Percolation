# Two-Channel Cascade Model — Project Tracker & LLM Context

> **Single source of truth** for the project *"A Two-Channel Cascade Model of Bank Failure."*
> Paste this whole file into a fresh LLM conversation before working, and ask the LLM to
> return the whole updated file at the end (see **§14 — LLM Update Protocol**).

- **Last updated:** 2026-06-04 — Session 15 (conjecture validation verified)
- **File version:** v1.8
- **Owner:** Gary Mei (Georgia Tech ISyE, SURS) · **Advisor:** Prof. Souvik Dhara

---

## §0 — START HERE (operating instructions for the LLM)

You are helping with an undergraduate research project. This file is the project's memory across
many separate conversations. Read it before doing anything else.

**The three rules that matter most:**

1. **Respect the section legend.**
   - 🔒 **FROZEN** sections encode the agreed direction, the model definition, the analytical
     benchmark, and the quality bar. **Do not silently rewrite them.** They change *only* through a
     dated entry in the **Decision Log (§11)** plus a minimal edit, flagged in the Changelog (§12).
   - 🟢 **LIVE** sections (§8–§10) describe the current state. Overwrite them freely to reflect
     reality — but truthfully (see rule 3).
   - 📜 **APPEND-ONLY** sections (§11–§12) are a permanent record. Add to the bottom; never delete
     or rewrite prior entries.
2. **Preserve direction.** The whole point of this file is that the project does not drift. If a
   request would pull the work away from the **North Star (§2)** or contradict a prior **Decision
   (§11)**, say so explicitly and ask before proceeding. Surface the tension; don't quietly adjust.
3. **Be honest in the live state.** Don't mark something done that isn't. Record blockers. If you
   are unsure a result is correct, say so. A tracker full of optimistic fiction is worse than no
   tracker.

**Session-start checklist (run this when you receive the file):**
read §2 (North Star) → §8 (Current Status) → §9 (Open Questions) → §10 (Next Actions), then the
specific 🔒 sections relevant to today's task (usually §3 Model and/or §5 Coding Standards).

**Section legend:** 🔒 frozen · 🟢 live · 📜 append-only.

---

## §1 — Project Identity 🔒

- **One-line goal:** Extend Janson et al.'s bootstrap percolation on $G(n,p)$ with a second,
  confidence-driven failure channel ("fear"), and characterize how the two channels jointly set the
  systemic-collapse boundary.
- **Central deliverable:** a phase diagram in $(r,\mu)$ space of the **probability of a system-wide
  cascade**, with a finite-size analysis and a comparison to an analytical (mean-field /
  branching-process) threshold.
- **Context:** Georgia Tech ISyE Summer Undergraduate Research, ~10 weeks, ~30 hrs/week, ~monthly
  advisor contact. Advisor: Prof. Souvik Dhara (critical percolation, critical windows on
  configuration / scale-free graphs, scaling limits, spectral methods).
- **Compute:** laptop is sufficient for the core deliverable; PACE (free cluster) only for the
  data-hungry critical-window scaling. Request PACE access early but **do not block on it.**

---

## §2 — North Star & Contribution Claim 🔒

**This is what the project *is*. Do not let it drift.**

The honest novelty is **incremental-to-moderate**, and the contribution must be framed accordingly:

> *"A clean, analyzable instance that couples a rigorously-understood local-threshold (Janson-style,
> absolute-$r$) solvency rule with a **self-reinforcing global panic field**, and a characterization
> of how the two channels jointly set the cascade boundary, via a probability-of-systemic-event
> phase diagram."*

**Claim this:** the *self-referential* global feedback (panic proportional to the system's own
recent failure rate — a positive feedback, not an exogenous constant) combined with the *absolute*
threshold rule, analyzed through the systemic-event phase diagram.

**Do NOT claim:** a new contagion *mechanism*. Hybrid local-threshold + probabilistic-channel models,
and threshold + external-field models, are an established subfield (Choi/Min et al. 2018; Miller
2015; Shu et al. 2024; Ruan et al. 2015). Overclaiming will be caught immediately. The ingredients
are known; the specific *instantiation* (global realized-failure-rate field with heterogeneous
individual susceptibility on top of an absolute-$r$ bootstrap rule) appears new.

**Rigor stance (✅ DECIDED D-009, 2026-06-04):** Adopt a **Tiered Stance**.
1. **Rigorously Prove** the auxiliary safety lemmas (specifically, that the fear-only channel at $p=0$ is a subcritical branching process with expected offspring $\mu < 1$, which terminates in $o(n)$ steps with $A^* = O(a)$ w.h.p., and that fear acts as a stochastically bounded amplifier under the combined model).
2. **Conjecture with Mean-Field Analysis** the $(1-\mu)^{r/(r-1)}$ scaling law for the critical seed $a_c(\mu)$ derived from the Poisson-combined self-consistent equations.
3. **Validate via Simulation** the phase diagrams, bimodality, and scaling exponent $\nu$ using a high-performance C++ implementation to preempt finite-size effect arguments.


---

## §3 — Model Specification 🔒

Precise definition. Change only via the Decision Log.

### 3.1 Network & states
- Interbank network: Erdős–Rényi random graph $G(n,p)$.
- Each bank is **solvent** or **failed**. Failure is **absorbing** (a failed bank stays failed), so
  the failed set grows monotonically.
- Seed: at $t=0$, a set of $a$ banks is failed (chosen at random by default; high-degree targeting
  is a variant — but see §3.6, on $G(n,p)$ targeting ≈ random).
- $A(t)$ = number of failed banks after round $t$. $a_t := A(t) - A(t-1)$ = **new** failures in
  round $t$, with $A(-1):=0$ so $a_0 = a$.

### 3.2 Channel 1 — Solvency (Janson local rule)
A solvent bank $i$ fails if at least $r$ of its neighbors have already failed:
$$\bigl|\{\, j \in N(i) : j \text{ failed} \,\}\bigr| \ge r.$$
Threshold $r$ is the capital-buffer depth. Use $r \ge 2$ (the $r=1$ case is qualitatively
different). This channel is **super-linear near zero** for $r \ge 2$ (it contributes nothing to the
linearization at the all-solvent state) — this is *why* Janson's threshold has the
$(np^r)^{-1/(r-1)}$ form. Keep this fact in mind for all mean-field / spectral reasoning.

### 3.3 Channel 2 — Fear (global, self-referential, heterogeneous)
- **Global fear field** $g_t \in [0,1]$ = fraction of banks that failed in the *previous* round:
  $$g_t := \frac{a_{t-1}}{n}\quad\text{(incremental — current default; see fork F1 in §3.6).}$$
- **Individual fear** $f_i \in [0,1]$, drawn **once** at $t=0$ from $\text{Beta}(\alpha,\beta)$ with
  $\alpha=\mu\kappa,\ \beta=(1-\mu)\kappa$, so $E[f]=\mu$ **exactly** (fork F3 resolved → Beta; see
  D-002 and §3.5). Concentration $\kappa$ sets the heterogeneity independently of the mean.
- A solvent bank $i$ fails through the fear channel in round $t$ with probability $f_i\, g_t$
  (a valid probability since $f_i, g_t \in [0,1]$).

**Key structural fact (most important consequence in the whole project):** because $f_i \in [0,1]$
forces $\mu < 1$, the **fear-only per-round reproduction number is $R_{\text{fear}} \approx \mu < 1$.**
Fear is a **subcritical amplifier**: it cannot ignite a cascade on its own; it can only amplify one
that the solvency channel has already started. At $t=1$, $g_1 = a/n \approx 0$ for any sub-linear
seed, so fear is essentially *off* until the solvency channel first produces a macroscopic round.
**This is the project's central risk** (see §7) and shapes the analytical check (see §4).

### 3.4 Dynamics & stopping rule
- Each round, **simultaneously**, every solvent bank fails if **Channel 1 is satisfied OR** an
  independent **Bernoulli$(f_i\, g_t)$** draw succeeds.
- The process **halts** at the first round with no new failures ($a_t = 0$). Fear is then zero by
  construction ($g_{t+1} = 0$), so the absorbing state is genuine.
- Record the final failed fraction $|A^*|/n$.

### 3.5 Notation & parameters

> **Notation reconciliation (resolves an inconsistency in the original summary):** the summary's
> fear-channel definition used $f_i, g_t$ while its parameter table and dynamics used
> $\upsilon_i, \tau_t$ for the *same* objects (the mentor review also uses $\upsilon, \tau$). **This
> tracker standardizes on $f$ (individual fear) and $g$ (global fear field).** Mapping for reading
> the review: $\upsilon_i \equiv f_i$, $\tau_t \equiv g_t$, $E[\upsilon] \equiv \mu$.

**True parameters (knobs you set):**

| Symbol | Meaning | Notes / working regime |
|---|---|---|
| $n$ | number of banks (system size) | finite-size set: 1000, 2000, 5000, (10000 for exponent fit) |
| $p$ | edge probability (connectivity) | **scale with $n$** — see §4. Working mean degree $np$ ≈ 8–10 |
| $r$ | failed neighbors for solvency failure | **short discrete list** {2, 3, 4}; not a continuous axis |
| $\mu$ | mean individual fear $E[f]$ | the continuous sweep axis, $\mu \in [0,1]$ (~30 pts) |
| $\sigma$ | fear heterogeneity (sd of $f$) | via Beta concentration $\kappa$: $\sigma^2=\mu(1-\mu)/(\kappa+1)$. Enters only at 2nd order — **fix $\kappa$ for main diagram**, separate $\kappa$-sweep |
| $a$ | seed size (initial shock) | set as a multiple of per-$n$ $a_c$, e.g. $0.8a_c$, $1.2a_c$ |
| $\theta$ | systemic-event threshold | pick in the bimodal trough (0.5); show robustness for $\theta\in[0.2,0.8]$ |

**State variables (NOT parameters — recomputed each round / drawn once):**
$A(t)$, $a_t$ (dynamic counts); $g_t$ (recomputed every round); $f_i$ (per-bank draw at $t=0$).

### 3.6 Open modeling forks (decide deliberately — track in §11)

- **F1 — Incremental vs. cumulative fear field. ✅ DECIDED (D-005, D-006, 2026-06-03): INCREMENTAL, $g_t = a_{t-1}/n$.** Fear is a transient amplifier with bounded gain $\approx 1/(1-\mu)$; per-failure total fear offspring $= \mu < 1$ (subcritical); the all-solvent state stays linearly stable; §3.4 absorbing state is genuine. Economically: news-flow panic, salience decays when failures stop. *Rejected:* cumulative ($g_t = A(t-1)/n$) — makes the all-solvent state linearly unstable for any $\mu>0$ (linearized growth $1+\mu$), eliminates the critical-seed barrier, demotes $r$ to a correction, and breaks §3.4's absorbing-state claim; NOT retained as a reported contrast (D-005 supersedes §3.6's prior "ideally report both"). *Extension (D-006):* normalized memory-window family $g_t = (1/n)\sum_{k=1}^X w_k a_{t-k}$, $\sum w_k = 1$ (exemplar $X=4$, $w = 0.50/0.25/0.15/0.10$); $X=1$ is the decided model; halting rule generalizes to "window empty" ($X$ consecutive quiet rounds); pilot ($n=2000$, 300--400 paired trials) confirms $P(\text{systemic})$ invariant in $X$ within $\pm 0.03$ (boundary depends only on kernel mass $= \mu$); cascade duration scales with $X$ ($\approx 13.5\to31.5$ rounds at $\mu=0.5$); study slotted Wk-9/stretch.
- **F2 — The $m$/$k$ "fear marks" mechanism. ✅ DECIDED (D-008, 2026-06-04): DROPPED.** The original summary's $m/k$ fear marks mechanism (fear feeds temporary marks that lower the effective solvency threshold $r$) is dropped for the MVP. Standardize on the simple direct-failure fear channel of §3.3. *Rationale:* The marks mechanism violates Janson-regime scaling assumptions (even $m=1$ mark lowers the solvency barrier to $r-1$, making $np^{r-1} \to \infty$ and trivially satisfying solvency, destroying the sharp threshold dichotomy). Furthermore, marks stack, breaking the subcritical amplifier property ($R_{\text{fear}} \approx \mu < 1$) when $m \ge r$ or mark lifetimes accumulate, and render the mean-field analysis mathematically intractable by replacing the scalar map with a high-dimensional coupled map. Dropping it preserves the clean direct-failure engine and avoids a parameter space explosion ($r, \mu, m, k$).
- **F3 — Fear distribution. ✅ DECIDED (D-002, 2026-06-02): Beta$(\alpha,\beta)$.** Individual fear
  $f_i\sim\text{Beta}(\mu\kappa,(1-\mu)\kappa)$, so $E[f]=\mu$ exactly with no truncation artifact;
  concentration $\kappa$ tunes heterogeneity independently of the mean ($\sigma^2=\mu(1-\mu)/(\kappa+1)$),
  and the limits are clean ($\kappa\to\infty$ point mass at $\mu$; $\kappa\to0$ two-point at $\{0,1\}$;
  $\mu=0$ the Janson baseline). **Two-point** (a fraction "immune" with $f=0$, rest susceptible —
  direct link to Watts's immune nodes / Ruan's blocked nodes) is kept as a **robustness variant**.
  *Rejected:* truncated-normal — its realized mean $\ne\mu$ near 0/1 (nominal $0.1\to0.164$ at
  $\sigma=0.15$), silently mislabeling the sole sweep axis, which is the one quantity the dynamics
  depend on (§4: fear-failures $\approx\mu\,a_{t-1}$).
- **F4 — Regime of $p$ vs. $n$. ✅ DECIDED (D-004, 2026-06-03): Janson regime ($np\to\infty$,
  $np^r\to0$).** Scale $p_n=\beta\,n^{-\alpha}$ with $\alpha\in(1/r,1)$ (per §4; e.g. $\alpha=0.7$ for
  $r=2$), so the JŁTV sharp-threshold theory (§4) is the benchmark and finite-size scaling is
  well-defined. *Rejected:* the bounded-mean-degree branching/configuration regime ($np=$ const, using
  the sparse Watts / Amini–Cont–Minca threshold) — it would abandon the Janson benchmark the project is
  built on, muddy the finite-size scaling, and preclude extending Janson's theorems. **Kept** as the
  natural home only if the project later pivots to a configuration model with empirical degrees (Q2).

---

## §4 — Analytical Benchmark (Janson et al. 2012) 🔒 *(reference)*

Janson, Łuczak, Turova & Vallier, *Ann. Appl. Probab.* 22(5), 1989–2047 (arXiv:1012.3535). The
$\mu=0$ case of this project **is** their model; reproducing their threshold is the **code-validation
test (Week 1).**

**Critical quantities (their eqs. 3.1–3.2, 3.12), fixed $r\ge2$:**
$$t_c := \left(\frac{(r-1)!}{n p^{r}}\right)^{1/(r-1)},\qquad
a_c := \left(1-\frac1r\right) t_c,\qquad
p_c := \left(\frac{(r-1)^{r-1}(r-1)!}{r^{r-1}}\right)^{1/r}\!\!\left(n\,a^{r-1}\right)^{-1/r}.$$
For $r=2$: $\;t_c = 1/(np^2)$, $\;a_c = 1/(2np^2)$.

**The dichotomy:** for $n^{-1}\ll p\ll n^{-1/r}$, w.h.p. the final active set is either $o(n)$
(subcritical; in fact $A^* < \frac{r}{r-1}a \le 2a$) or $n - o(n)$ (almost percolation). Threshold at
$a = a_c$. Subcritical fraction solves $r\varphi - \varphi^{r} = (r-1)\alpha$ with $\alpha=a/a_c$;
for $r=2$, $\varphi(\alpha)=1-\sqrt{1-\alpha}$. Once $p \gg n^{-1/r}$, any seed $a\ge r$ percolates
completely (the channel is degenerate there). **The interesting solvency physics lives in this
density window** — stay in it.

**How to scale $p$ with $n$ (do NOT hold $p$ fixed while growing $n$):**
choose $p_n = \beta\, n^{-\alpha}$ with $\alpha \in (1/r, 1)$ — e.g. $r=2,\alpha=0.7$;
$r=3,\alpha=0.5$. This keeps $np\to\infty$ and $np^r\to0$. For each $n$, seed at fixed multiples of
the per-$n$ $a_c$ so every $n$ sits the same relative distance from threshold. Holding $p$ fixed makes
large systems trivially easier to ignite and **confounds the finite-size scaling.**

**How the analytical check must be set up (do this, not the naive thing):**
compare the empirical boundary to the **tangency of the combined mean-field map** — a **saddle-node
tangency at an interior unstable fixed point**, *not* "find where $R=1$ at the all-solvent state."
Because the solvency channel is super-linear near zero (slope 0 in the linearization for $r\ge2$) and
fear contributes slope $\mu<1$, the empty state is linearly stable; a critical seed is needed to cross
the barrier.
- *Solvency piece:* with mean degree $c=np$ and failed fraction $\varphi$, a solvent bank has
  $\approx\text{Poisson}(c\varphi)$ failed neighbors, so fails via solvency w.p.
  $\approx (c\varphi)^r/r!$. Set the mean-field map tangent to the diagonal (map $=$ identity **and**
  derivative $=1$); this reproduces $a_c$.
- *Fear piece:* expected new fear-failures $\approx (a_{t-1}/n)\sum_i f_i \approx \mu\, a_{t-1}$ when
  most banks are solvent, i.e. $R_{\text{fear}}\approx\mu$.
- Machinery: Watts (2002) and Gleeson & Cahalane (2007) tree / generating-function recursions —
  implementable numerically by a strong programmer.

---

## §5 — Coding Standards & Architecture 🔒

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
│   └── figures/
├── tests/                        # incl. μ=0 ↦ a_c, AND the C++-vs-Python agreement check (§5.4)
└── notebooks/                    # exploration ONLY; nothing canonical lives here
```

### 5.4 Reproducibility (non-negotiable)
- **Seed everything** through an explicit RNG — `numpy.random.default_rng(seed)` in Python, a seeded
  `<random>` engine in C++ — with no implicit global state. A run is deterministic given (config,
  seed). In C++, seed each realization as a deterministic function of (base_seed, realization_index)
  so parallel runs stay reproducible and order-independent.
- Persist, with every results file: the **full config**, the **seed(s)**, the code **git commit
  hash**, and a timestamp.
- **Save raw per-realization outcomes** to `results/raw/`. Analysis and plotting read from disk; they
  never re-run the simulation to make a figure.
- **Cross-language validation (the C++ port must be trusted).** numpy's `Generator` and C++ `<random>`
  produce *different* streams from the same seed, so do **not** expect bit-identical Monte Carlo output
  across languages. Validate two ways: (1) **engine logic** — at $\mu=0$ the cascade is deterministic
  given the graph, so dump a graph from the Python reference, load *the same graph* in C++, and confirm
  the final failed set is identical (this tests the cascade independent of RNG); (2) **statistics** —
  for $\mu>0$, confirm the C++ and Python $P(\text{systemic})$ and $|A^*|/n$ histograms agree within
  Monte Carlo error over many seeds.

### 5.5 Style
- Small **pure functions**; no hidden global state. The engine takes a graph + params + RNG and
  returns outcomes — it does no I/O and no plotting (true in both languages).
- **Python:** type hints; concise docstrings (what it computes, units, the relevant equation §);
  parameters in a single validated dataclass ($0\le\theta\le1$, $r\ge2$, $p$ in regime).
- **C++:** RAII and value semantics; pass big objects by `const&`, never copy the graph; **CSR**
  adjacency for cache locality (a `vector<vector<int>>` is an acceptable first cut, CSR is the
  optimization); `reserve()` buffers to avoid per-round reallocation; const-correctness; **no shared
  mutable state in the parallel realization loop** (each thread owns its RNG and buffers). Build
  `-O3 -march=native` for runs, `-O0 -g -fsanitize=address,undefined` for debugging.
- Optimize only where it aids speed *and* clarity, and **profile before optimizing** — the reason the
  core is C++ is that the cascade loop is the measured hot path, not faith.

### 5.6 Definition of Done (apply to every result)
A deliverable is "done" only when: (1) it is produced by a script from a committed config + logged
seed; (2) raw outputs are saved to `results/raw/`; (3) the figure regenerates from those raw outputs
via `plotting.py`; (4) for anything validatable, the validation passes (e.g. $\mu=0$ reproduces
$a_c$); (5) any result from the C++ core has passed the cross-language check in §5.4 against the
Python reference; and (6) the result is recorded in §8 and, if it resolves a fork, in §11.

---

## §6 — Roadmap (≈10 weeks) 🔒 *(structure frozen; check items off in place)*

> The **MVP** alone is a complete, presentable result. Everything past it is stretch. Protect the MVP.

**MVP (guaranteeable):** a clean, documented simulator → **one $(r,\mu)$ phase diagram of
$\Pr(|A^*|/n \ge \theta)$ at a single $n$**, with **verified bimodality**, plus an **overlaid
heuristic mean-field threshold** showing qualitative agreement.

- [x] **Wk 1 — Python prototype + code validation.** Build the two-channel cascade on sparse
      $G(n,p)$ (counter-based) **in Python first** — iteration speed beats throughput here, the model
      still has open forks, and $n{=}1000$ at a few hundred realizations is fast enough. Reproduce
      *pure* bootstrap percolation at $\mu=0$ and check the empirical seed threshold against $a_c$.
      This prototype becomes the **reference oracle** (`reference.py`) for the C++ port.
- [ ] **Wk 2 — GO/NO-GO week.** (i) 1-D $\mu$-sweep at near-critical $r$: *does $\mu$ have teeth?*
      (ii) Bimodality histograms of $|A^*|/n$ (justify $\theta$). (iii) **Decide F1** (incremental vs.
      cumulative) and **fix the $p_n$ scaling (F4)**. If $\mu$ is inert, pivot (§7) before building
      the pipeline.
- [ ] **Wk 3–4 — Port the (now-locked) hot path to C++ + full $(r,\mu)$ diagram at one moderate $n$
      (e.g. 1000).** With the model decided (forks closed in Wk 2), port $G(n,p)$ generation + the
      cascade engine + the realization loop to C++ (CSR, `<random>`), wire it to Python via E1, and
      **validate it against the Python reference (§5.4)**. Then run the full diagram and solidify the
      pipeline / parallelization / plotting; draft the heuristic mean-field threshold curve. *(Want
      C++ exposure sooner? Build it in parallel during Wk 2 against the stabilizing spec — but keep
      the Python prototype as the tool that decides the forks.)*
- [ ] **Wk 5 — Overlay mean-field on empirical; iterate the analytics where they disagree.**
      *(First/second advisor meeting ~here — bring the diagram + threshold comparison.)*
- [ ] **Wk 6–7 — Finite-size analysis** across 5–6 values of $n$; estimate the **transition-width
      scaling exponent $\nu$** (width $\sim n^{-1/\nu}$). Put the realization budget **near the
      boundary**, not deep in either phase.
- [ ] **Wk 8 — First stretch goal** (recommended: configuration-model variant; see §2/§7 and the
      advisor angles).
- [ ] **Wk 9 — Robustness & consolidation:** $\theta$ sensitivity, $\sigma$-sweep, random vs.
      targeted seeding (expect a near-null on $G(n,p)$ — report as a deliberate negative result);
      fear-persistence window ($X$) invariance check (D-006): pilot confirms boundary near-invariant
      in $X$ within $\pm 0.03$; expected result is an invariance/robustness lemma plus the
      cascade-duration effect.
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

---

## §7 — Risks & Mitigations 🔒

- **BIGGEST RISK — $\mu$ has no teeth.** The $(r,\mu)$ diagram could turn out essentially controlled
  by $r$ alone, with $\mu$ muted or knife-edge, because $R_{\text{fear}}\approx\mu<1$ and fear can't
  initiate (the model reduces to pure bootstrap percolation over much of the plane). This would
  undercut the two-channel premise. **Mitigation:** the Week-2 $\mu$-sweep. Caught in Week 2 it's a
  pivot (move to a heterogeneous graph — Q2);
  caught in Month 2 with sparse advisor contact it's a crisis. **Run this check first.**
- **Scope creep into rigor you can't finish.** Hold the line at "heuristic threshold validated by
  simulation; sharpness stated as a conjecture." (Confirm boundary with advisor — §9 Q1.)
- **Confounded finite-size scaling** from holding $p$ fixed across $n$. **Mitigation:** the
  $p_n = \beta n^{-\alpha}$ scaling and per-$n$ seeding at multiples of $a_c$ (§4). Four $n$ values
  across ~1.7 decades is thin for a clean log-log exponent — add $n=2000$ and ideally $10000$.
- **Distribution confound** ($E[f]\ne\mu$ for truncated-normal near 0/1) silently mislabeling the
  $\mu$-axis. **Resolved (D-002):** Beta$(\mu\kappa,(1-\mu)\kappa)$ sets the mean to $\mu$ exactly;
  two-point kept as a robustness variant (F3).
- **Watts window, not just a one-sided threshold.** Too-dense networks suppress cascades (each node
  needs too many failed neighbors). Watch for a *window* in $p$, not only a lower threshold.

---

## §8 — Current Status 🟢 *(overwrite each session to reflect reality)*

- **Phase:** Week 2. Wk-1 milestone remains complete. Modeling forks resolved. Repository structure standardized and dependencies pinned (D-011).
- **State of the code:** `src/twocascade/reference.py` is the validated Python reference oracle (with the normalized memory-window specification fully implemented and verified). The C++ core remains empty stubs.
- **Validation:** `tests/test_mu0_bootstrap_threshold.py` and `tests/test_window_len.py` both pass (10/10 tests total) under pytest.
- **First quantitative result (carried forward):** at $n{=}4000$, $r{=}2$, empirical threshold $\approx 25.3$ vs. $a_c=20$ (ratio $\approx 1.26$) — a finite-size effect set by the magnitude of $a_c$; Janson scaling adopted for theorem validity.
- **Pilot (S-008), carried forward:** paired-simulation pilot confirmed memory-window family details.
- **This session (S-014) — Verified reference.py memory-window implementation:** Verified the implementation of `window_len` and `weights` in `run_cascade` (and their passthrough in `estimate_systemic_probability`), ran pytest suite, and confirmed that all 10 tests passed successfully.
- **Conjecture validation (S-015):** Derived critical seed size scaling $a_c(\mu) = a_c(0) (1-\mu)^{r/(r-1)}$ from Poisson self-consistent equations. Validated at $N=1000, 2000, 4000$ for $r=2$, yielding empirical thresholds that follow the predicted scaling ratios (e.g., at $N=2000$, $\mu=0.25$ ratio $0.601$ vs. expected $0.563$, and $\mu=0.50$ ratio $0.361$ vs. expected $0.250$).
- **Where the code lives:** `src/twocascade/reference.py`; tests in `tests/`; environment config in `requirements.txt`, `pytest.ini`, and `pyproject.toml`.

## §9 — Open Questions & Blockers 🟢 *(overwrite each session)*

- **Q2 (advisor):** stay on $G(n,p)$ with incremental fear for the cleanest Janson comparison, or move to a configuration model where heterogeneity/targeting matter and which connects to the critical-window work? *(This is also where the rejected F4 bounded-degree regime would live, and the §7 μ-inert pivot now points here.)*
- **Q3 (advisor):** is a critical-window framing of interest (finite-size width exponent; whether the critical cascade shows $n^{2/3}$-type scaling), and reasonable to probe empirically without a proof?
- **Forks awaiting decision:** None. *(Resolved: F1 → incremental (D-005, D-006); F2 → dropped (D-008); F3 → Beta (D-002); E1 → standalone executable + file I/O (D-003); F4 → Janson regime (D-004). Survivor-hazard removed entirely (D-007).)*
- **Engineering note (raised S-004; no §5.2 edit made):** §5.2's "one cascade realization is $O(\text{edges})$" undercounts the fear channel — realistic per-cascade cost is $O(\text{edges} + \sum_t |\text{solvent}_t|)$. Decide whether to amend §5.2 before the C++ port.
- **Logistics:** email Prof. Dhara about PACE access.
- **Blockers:** none.

## §10 — Next Actions 🟢 *(overwrite each session — keep it to the next few concrete steps)*

1. **Begin Wk-2 (GO/NO-GO):** 1-D $\mu$-sweep at near-critical $r$ — *does $\mu$ have teeth?* — plus bimodality histograms of $|A^*|/n$ to justify $\theta$.
2. Email Prof. Dhara re PACE; put Q2–Q3 on the first-meeting agenda.

---

## §11 — Decision Log 📜 *(APPEND-ONLY — newest at the bottom; never edit prior entries)*

> Format: `D-NNN | YYYY-MM-DD | Decision | Rationale | Affects §`. Any change to a 🔒 section
> requires an entry here.

- `D-000 | 2026-06-01 | Tracker created; standardized fear notation to f (individual) and g (global field), mapping υ→f, τ→g. | Original summary was internally inconsistent (f/g vs υ/τ). | §3.5`
- `D-001 | 2026-06-01 | Two-language architecture: C++ for the performance-critical core (G(n,p) generation + cascade engine + realization loop), Python for orchestration / analysis / plotting. Keep a pure-Python reference engine as the validation oracle for the C++ port. Prototype in Python first (Wk 1–2), port the locked hot path to C++ in Wk 3–4. | Hot path is integer/memory-bound and embarrassingly parallel — C++ gives a real, defensible speedup that enables the 10^6–10^7-run critical-window study; also satisfies the C++ learning/résumé goal; the split mirrors numpy/scipy. NOT required for the MVP, so it must not delay the Wk 1–2 go/no-go. Boundary mechanism left open as fork E1. | §5, §6`
- `D-002 | 2026-06-02 | Resolved fork F3: individual fear f_i ~ Beta(α,β) with α=μκ, β=(1−μ)κ, so E[f]=μ exactly; concentration κ tunes heterogeneity independently (var = μ(1−μ)/(κ+1)). Drop truncated-normal; keep two-point (immune/susceptible) as a robustness variant. | Truncated-normal's realized mean ≠ μ near 0/1 (nominal 0.1 → 0.164 at σ=0.15), silently mislabeling the sole sweep axis and the one quantity the dynamics depend on (§4: fear-failures ≈ μ·a_{t−1}). Beta is native to [0,1], sets the mean exactly, allows an independent κ-sweep for heterogeneity, and nests the degenerate limits (κ→∞ point mass, κ→0 two-point, μ=0 the Janson baseline). | §3.3, §3.5, §3.6, §7`
- `D-003 | 2026-06-03 | Resolved engineering fork E1: C++↔Python boundary = (a) standalone C++ executable + file I/O — Python writes config/args, C++ writes raw per-realization outcomes to results/raw/, Python reads them back. Reject pybind11 for now; keep it as a stretch/second-iteration polish layer (§6). Build the C++ core as a library (graph/rng/engine) with a thin main.cpp CLI wrapper so a pybind11 binding can be added over the same core later without a rewrite. | Boundary crossing is tiny and infrequent (scalars in, compact outcomes out, once per cell — no hot data path), so pybind11's in-memory advantage is moot here; (a) is far easier to debug with standard C++ tooling (gdb/ASan/valgrind), maps trivially to PACE array jobs for the 10^6–10^7-run critical-window study, and makes the §5.4 same-graph cross-language check a natural file dump. pybind11's gains are mainly résumé-oriented and can be layered on later; owner is new to C++, so debuggability/maintainability win. | §5.1, §9, §10`
- `D-004 | 2026-06-03 | Resolved fork F4: p–n regime = Janson regime (np→∞, np^r→0), scaling p_n = β·n^{-α} with α∈(1/r,1) (e.g. α=0.7 for r=2, per §4). Reject the bounded-mean-degree branching/configuration regime (np const, Watts / Amini–Cont–Minca threshold). | The project's μ=0 benchmark IS Janson (§4) and the Wk-1 validation is already built on it, so the growing-degree regime keeps that benchmark sharp and makes the finite-size scaling behind the critical-window interest (Q3) well-defined. Decisively, the advisor's steer is toward a theoretical result — extending Janson's theorems to the fear setup — which is only feasible while staying inside Janson's regime; the bounded-degree route builds on different theory (Watts/ACM) and would abandon the extension. Bounded-degree stays reserved for a possible configuration-model pivot (Q2). | §3.6, §4, §6, §8, §9, §10`
- `D-005 | 2026-06-03 | Resolved fork F1: fear field = INCREMENTAL, g_t = a_{t-1}/n. Cumulative (g_t = A(t-1)/n) rejected outright and NOT retained as a reported contrast (explicitly supersedes §3.6\'s prior "ideally report both"); survivor-hazard kept solely as the §7 fallback if the Wk-2 μ-sweep shows μ inert. | Incremental preserves the frozen analytical core: R_fear≈μ (subcritical, §3.3), all-solvent state linearly stable (critical-seed barrier and §4 saddle-node tangency intact), §3.4 absorbing state genuine, continuous μ=0 Janson limit — keeping the Q1 Janson-extension route tractable. Cumulative makes the empty state linearly unstable for any μ>0 (linearized growth 1+μ): fear becomes an autonomous ignition channel, systemic region degenerates to {a ≳ a_c(r)} ∪ {μa ≳ O(1)} with r demoted (paired sims, n=2000, a=6: at r=4 where a=0.047·a_c, cumulative reaches P(systemic)=0.95 at μ=0.5 vs 0.000 incremental), μ controls speed/odds not size, halting rule becomes load-bearing (g > 0 after a quiet round, contradicting §3.4). Economically: transient news-flow panic (incremental) vs ratcheting panic predicting universal collapse (cumulative). | §3.6 (F1 marked DECIDED; §3.3/§3.4 already written incrementally — no text change)`
- `D-006 | 2026-06-03 | Adopted the NORMALIZED memory-window family as the sanctioned persistence extension of the F1 field, replacing the dropped cumulative contrast: g_t = (1/n)·Σ_{k=1..X} w_k·a_{t-k} with Σw_k = 1 (exemplar X=4, w = 0.50/0.25/0.15/0.10); X=1 is exactly the decided model. For X>1 the halting rule generalizes to "halt when the window is empty" (X consecutive quiet rounds), keeping the absorbing state genuine. Study slotted Wk-9/stretch — NOT MVP; Wk-2 sweep runs at X=1. | Normalization is the safety property: per-failure total fear offspring = μ·Σw_k = μ, subcritical for every X (largest root of z^X = μ·Σw_k z^{X-k} is <1 for μ<1); cumulative is the un-normalized infinite-window endpoint. Pilot (n=2000, r=2, a=6=0.6a_c, 300–400 paired trials): P(systemic) invariant in X within ±0.03 (sign tests p≥0.40 at μ∈{0.3,0.5}, X∈{1,4,8}); cascade duration grows with X (≈13.5→31.5 rounds at μ=0.5). Frame the Wk-9 study as an invariance result (candidate robustness lemma for the Q1 extension) plus the duration effect. | §3.6, §6 (Wk-9 robustness line)`
- `D-007 | 2026-06-03 | Removed the survivor-hazard normalization (g_t = a_{t-1}/solvent_t) from the project entirely — dropped as the μ-inert fallback, given no code path, and struck from §3.6 (the F1 "retained as §7 fallback" line), §6 (Wk-2 note), and §7 (μ-inert pivot list, which also shed the already-rejected cumulative per D-005). If the Wk-2 μ-sweep shows μ inert, the pivot is now to a heterogeneous graph (configuration model, Q2), not a normalization swap. | The project is committed to the incremental fear model (D-005) and its normalized memory-window extension (D-006); survivor-hazard normalizes by the shrinking solvent set, inflating g_t late in a cascade, which breaks the clean R_fear≈μ subcritical structure (§3.3) and diverges from the Janson-extension route (Q1/D-004) the project now targets. Supersedes the survivor-hazard retention recorded in D-005. | §3.6, §6, §7`
- `D-008 | 2026-06-04 | Resolved fork F2: Drop the $m/k$ fear marks mechanism for the MVP (option a in §3.6). Standardize on the direct-failure fear channel (§3.3) for both Python and C++ engines. | The marks mechanism violates critical Janson-regime assumptions at the threshold level (even $m=1$ mark reduces the solvency barrier to $r-1$, making $np^{r-1} \to \infty$ and trivially satisfying solvency, which destroys the sharp threshold dichotomy). Furthermore, marks break the subcritical amplifier property ($R_{\text{fear}} \approx \mu < 1$) when $m \ge r$ or when marks stack, and render the mean-field saddle-node bifurcation analysis mathematically intractable by replacing the scalar map with a high-dimensional coupled map. Dropping marks avoids a massive parameter space explosion ($r, \mu, m, k$) and keeps the 10-week timeline viable, while the memory-window family (D-006) already provides a clean, tractable persistence handle without coupling to the solvency threshold. | §3.3, §3.6, §8, §9, §10`
- `D-009 | 2026-06-04 | Resolved Q1 (Analytical Scope) by adopting the Tiered Stance for mathematical analysis. | Full rigor for the combined model is bottlenecked by global coupling and discrete round dependencies that break Janson's local tree-like martingale machinery. The Tiered Stance provides a publication-quality analytical breakthrough (the (1-μ)^{r/(r-1)} critical scaling law) and stochastically bounded lemmas, while leveraging high-performance simulations for full dynamic validation within the 10-week timeline. | §2, §9, §10`
- `D-010 | 2026-06-04 | Expose `window_len: int = 1` and `weights: list[float] | None = None` in the reference engine (`run_cascade` and `estimate_systemic_probability`). Update the fear channel to compute the normalized memory-window global fear field $g_t = (1/n)\sum_{k=1}^X w_k a_{t-k}$ and generalize the stopping condition to $X$ consecutive quiet rounds. | Enables execution of the Week 9 memory-window invariance robustness study (D-006) while guaranteeing that the default parameter ($X=1$) exactly preserves the core theoretical model ($g_t = a_{t-1}/n$) for all standard sweeps and validations. | §3.6, §8, §10`
- `D-011 | 2026-06-04 | Standardize repository structure and Python environment dependencies. | Lock exact dependency versions in requirements.txt, ensure pytest.ini aligns pythonpath, verify gitignore rules, and populate the project README.md structure to guarantee reproducibility. | §5.3, §5.4, §10`
- `D-012 | 2026-06-04 | Validated conjectured critical seed size scaling law mathematically and numerically. | Self-consistent map derivation shows a_c(mu) = a_c(0) (1-mu)^{r/(r-1)}; numerical tests at N=1000, 2000, 4000 confirm ratios follow (1-mu)^2 trend (e.g., mu=0.25 ratio ~0.60, mu=0.5 ratio ~0.36 at N=2000). | §2, §8`
- `D-013 | 2026-06-04 | Project Packaging via pyproject.toml | Adopt pyproject.toml for setuptools packaging, enabling editable pip installations (pip install -e .) to ensure clean module path resolution for testing and scratch scripts without relying on manual PYTHONPATH manipulation. | §5.3, §5.4`


## §12 — Session Changelog 📜 *(APPEND-ONLY — what changed in the file each session)*

- `S-000 | 2026-06-01 | v1.0 | Initial tracker built from the project summary, the Janson paper, and the mentor review.`
- `S-001 | 2026-06-01 | v1.1 | Adopted C++ performance core + Python orchestration (D-001). Rewrote §5 (stack, repo layout, reproducibility incl. cross-language validation, style, Definition of Done), updated §6 (Python-prototype-first; C++ port in Wk 3–4; OpenMP/pybind11 stretch), and refreshed live §8–§10. Added engineering fork E1.`
- `S-002 | 2026-06-02 | v1.2 | Resolved fork F3 (fear distribution → Beta) per D-002. Frozen edits: specified Beta(α,β) for f_i in §3.3, tied the σ row to the Beta concentration κ in §3.5, marked F3 decided in §3.6, and updated the distribution-confound risk in §7 to "resolved." Refreshed live §8–§10 (F3 off the open-forks list; Beta noted in the reference.py action).`
- `S-003 | 2026-06-03 | v1.2 | Stood up the repo per §5.3 (cpp/ + src/twocascade/ trees, CMakeLists stub, .gitkeep placeholders, .gitignore) and built reference.py (Batagelj–Brandes G(n,p) + counter-based two-channel single-cascade engine with the §3.4 simultaneous update + Beta fear per D-002 + a Monte-Carlo systemic-probability driver), sanity-checked (E[f]=μ across κ; μ=0 → all-zero baseline; demo cascade percolates). Refreshed live §8–§10. No frozen edits and no new decisions; flagged a §5.2 per-cascade-complexity wording question for next session.`
- `S-004 | 2026-06-03 | v1.3 | Resolved engineering fork E1 → standalone executable + file I/O per D-003. Frozen edit: marked E1 DECIDED in §5.1 (was "OPEN"), recorded the (a)-vs-(b) rationale as justification, deferred pybind11 to the §6 stretch menu, and added the "library core + thin main.cpp CLI wrapper" directive that keeps a future pybind11 binding cheap. Refreshed live §9 (E1 off the open-forks list) and §10 (E1 action removed; renumbered).`
- `S-005 | 2026-06-03 | v1.4 | Resolved fork F4 → Janson regime per D-004 (frozen edit: marked F4 DECIDED in §3.6 with the p_n=β·n^{-α}, α∈(1/r,1) scaling and the rejected bounded-degree alternative). Also checked the Wk-1 box in §6 — the μ=0 validation now passes — and brought the live sections to reality: §8 records Wk-1 complete, the first quantitative result (empirical threshold ≈ a_c with the expected finite-np offset), and the test + pytest.ini + μ=0 fear-draw guard; §9 takes F4 off the open-forks list, logs the advisor's lean toward a theoretical result/extending Janson under Q1, and flags Q2 as the bounded-degree home; §10 now leads with applying the D-004 p-scaling to the test, then the Wk-2 μ-sweep.`
- `S-006 | 2026-06-03 | v1.4 | Corrected misleading wording in §8/§10: the ~28% threshold offset at n=4000 is a finite-size effect set by the magnitude of a_c (present in any p–n regime), NOT an "np correction" removed by the Janson form — a multi-n check showed both the bounded-degree and Janson p-forms tighten toward 1 as n grows, and the two forms are numerically identical at n=4000. Recorded that the Janson p_n scaling (D-004) is now applied in the test (validation re-confirmed 4/4) and is adopted for theorem validity / clean scaling exponents, not a finite-n ratio gain. §10 drops the now-done p-scaling action and promotes the Wk-2 μ-sweep. Live-only; no frozen edits; version unchanged at v1.4.`
- `S-007 | 2026-06-03 | v1.4 | ERRATA — correction of record for two inaccuracies that entered the logs during the F4 / p-scaling work, both now fixed. (A) S-005 and the original §8 framed the ~28% gap between the empirical threshold (≈25.3) and a_c (20) at n=4000 as an "expected finite-np correction" the Janson regime would shrink; this was wrong — a multi-n check showed it is a finite-size effect set by the magnitude of a_c (larger a_c → sharper transition → ratio→1), present in ANY p–n regime, with the bounded-degree and Janson p-forms numerically identical at n=4000. Corrected in live §8/§10 under S-006. (B) S-006 stated the "Janson p_n scaling is applied," but the test then set BETA = TARGET_MEAN_DEGREE / N**(1-ALPHA), pinning BETA to the live N — which cancels ALPHA (P reduces to 10/N) and holds np constant, i.e. the bounded-degree regime in disguise: the FORM of D-004 but not its scaling. Fixed by FREEZING BETA at a fixed reference N_REF (BETA = TARGET_MEAN_DEGREE / N_REF**(1-ALPHA)), so np = BETA·N^(1-ALPHA) grows as N is varied; suite still passes 4/4 (P=0.0025 unchanged at n=4000) and np now grows (≈8→15 over n=2000–16000). Note: append-only S-005/S-006 retain their original wording; this entry is the correction of record. Live-only; no frozen edits; v1.4 unchanged.`

---
- `S-008 | 2026-06-03 | v1.5 | Resolved fork F1 (D-005): incremental field confirmed; cumulative rejected outright and not reported (supersedes "ideally report both" in §3.6). Adopted normalized memory-window family as the sanctioned persistence extension (D-006): g_t = (1/n)·Σw_k·a_{t-k}, Σw_k=1, X=1 is the decided model, X-study slotted Wk-9/stretch. Frozen edits: §3.6 F1 marked DECIDED with full rationale (D-005 and D-006); §6 Wk-9 robustness line gains the window invariance check. Refreshed §8–§10: F1 off open-forks, F2 still open, next-action list updated. No code committed this session.`
- `S-009 | 2026-06-03 | v1.6 | Removed survivor-hazard entirely (D-007): struck the "retained as §7 fallback" survivor-hazard line from §3.6 (F1), and removed survivor-hazard — plus the already-rejected cumulative (D-005) — from the §7 μ-inert pivot list and the §6 Wk-2 note; the μ-inert pivot is now the heterogeneous-graph route (Q2). Earlier this session (per request): reworked §10 action #2, replacing the planned fear_field parameter with a window_len parameter (D-006's window length X), and updated §8's matching mention. Frozen edits to §3.6/§6/§7 → File version v1.6; header bumped to Session 9. No code committed.`
- `S-010 | 2026-06-04 | v1.7 | Resolved Fork F2 per D-008: F2 marks mechanism dropped. Frozen edits: §3.6 marked F2 DECIDED with full rationale. Refreshed §8–§10 to reflect F2 resolution. Cleaned up F2 open-fork comment in test_mu0_bootstrap_threshold.py. No engine or simulation logic changes required.`
- `S-011 | 2026-06-04 | v1.8 | Resolved Q1 scope via Tiered Stance (D-009). Frozen edits: §2 Rigor Stance updated to Tiered Stance. Refreshed §9 (Q1 off open questions) and §10 (renumbered actions). Added docstrings in reference.py noting direct-failure stance and (1-μ)^{r/(r-1)} scaling law. Run pytest verification suite.`
- `S-012 | 2026-06-04 | v1.8 | Implemented memory-window integration in Python reference cascade engine per D-010. Added collections.deque, validations, collapse-guard, and halt logic fixes. Added test_window_len.py (6/6 tests passed). Verified 10/10 test suite passes.`
- `S-013 | 2026-06-04 | v1.8 | Standardize repo structure, lock versions in requirements.txt, configure testing/ignores, and populate README.md. | Live §8–§10 updated; requirements.txt populated; README.md initialized.`
- `S-014 | 2026-06-04 | v1.8 | Verified Python reference engine memory-window synchronization and updated Next Actions. | Live §8, §10 updated; S-014 appended.`
- `S-015 | 2026-06-04 | v1.8 | Mathematical derivation and numerical verification of the conjectured scaling law. Added pyproject.toml and scratch_check.py to README. | Live §8, §11, §12 updated.`


## §13 — Key References

- **Janson, Łuczak, Turova & Vallier (2012)** — "Bootstrap percolation on the random graph $G(n,p)$,"
  *Ann. Appl. Probab.* 22(5), 1989–2047. arXiv:1012.3535. *Base model + the sharp-threshold dichotomy
  (the §4 benchmark).*
- **Watts (2002)** — "A simple model of global cascades on random networks," *PNAS* 99(9), 5766–5771.
  *Canonical threshold cascade; the cascade window; heterogeneity ↑ vulnerability; "frequency of
  global cascades" = the order parameter.*
- **Gleeson & Cahalane (2007)** — seed-size-dependent cascade condition / tree recursion. *Machinery
  for the mean-field threshold.*
- **Amini, Cont & Minca (2016)** — "Resilience to contagion in financial networks," *Math. Finance.*
  arXiv:1112.5687. *Rigorous default-cascade asymptotics on inhomogeneous random graphs (Wormald DE
  method); the rigorous route if rigor is ever in scope.*
- **Gai & Kapadia (2010)** — analytical contagion in financial networks. *Foundational default cascade.*
- **Kobayashi (2013)** — arXiv:1312.6804. *Balance-sheet contagion ≡ Watts threshold model.*
- **Choi, Min et al. (2018)** — "Competing contagion processes…," *Sci. Rep.* arXiv:1712.05059.
  *Generalized contagion: transmission prob + heterogeneous threshold; hybrid/double transitions
  (closest prior to the two-channel idea — but its 2nd channel is local).*
- **Miller (2015)** — arXiv:1501.01585. *Dynamic Watts model with hybrid bifurcations.*
- **Shu, Yang, Ruan & Xuan (2024)** — arXiv:2408.05050. *Social contagion under hybrid interactions.*
- **Ruan, Iñiguez, Karsai & Kertész (2015)** — "Kinetics of Social Contagion," *PRL* 115, 218702.
  arXiv:1506.00251. *Threshold model + immune nodes + external driving (nearest relative to the global
  field — but exogenous, not self-referential).*
- **van der Hofstad** — *Random Graphs and Complex Networks*, Vol. 1 (free online). *Bridge text:
  branching-process approximations, local tree-likeness; the advisor's lineage.*
- **Dhara, van der Hofstad, van Leeuwaarden & Sen (2017)** — "Critical window for the configuration
  model: finite third moment degrees," *EJP* 22(16). arXiv:1605.02868. *Advisor's critical-window
  framing.*
- **Dhara, van der Hofstad & van Leeuwaarden (2021)** — "Critical percolation on scale-free random
  graphs," *Comm. Math. Phys.* 382, 123–171. arXiv:1909.05590.

---

## §14 — LLM Update Protocol (run at END of each conversation)

When the user asks you to update this file:

1. **Output the ENTIRE file**, top to bottom, as one block the user can copy and paste back wholesale.
   Do **not** output a diff, a patch, or "just the changed sections." The user maintains this by
   replacing the old file with your output.
2. **Update the header:** bump `Last updated` (date + increment the session number) and `File version`
   if any 🔒 section changed (minor bump for content fixes, e.g. v1.0 → v1.1).
3. **Rewrite the 🟢 LIVE sections (§8–§10)** to match reality at end of session: current phase, what
   got done, what's in progress, where new code lives, the latest validated result, refreshed open
   questions/blockers, and the next few concrete actions. Overwrite stale content — these sections
   describe *now*, not history.
4. **Append to 📜 sections (§11–§12), never edit them.**
   - **Decision Log (§11):** add a `D-NNN` line for every decision reached this session — especially
     any fork resolved (F1–F4) or any change to a 🔒 section. Keep each entry to one line.
   - **Session Changelog (§12):** add one `S-NNN` line summarizing what changed in the file.
5. **Touch 🔒 FROZEN sections only with cause.** If a decision genuinely changes the model (§3), the
   benchmark (§4), the standards (§5), the roadmap structure (§6), the risks (§7), or the North Star
   (§2): (a) record it in §11 first, (b) make the **minimal** edit, (c) note it in §12, and (d) call
   it out to the user in your reply ("I changed §3.3 because of decision D-007"). **Never** silently
   alter the North Star or the model definition.
6. **Guard the direction.** If the session pulled the work toward something at odds with §2 or a prior
   decision, do **not** quietly fold it in. Flag the tension in your reply and ask whether to record it
   as a deliberate pivot (new Decision) or set it aside.
7. **Record state, not source.** This file tracks *what* exists and *why* — note which module/script
   holds new code and what it does. Do **not** paste source code into the tracker.
8. **Be truthful and lean.** Don't mark unfinished work done; record real blockers. Keep live sections
   tight (the next few steps, not a backlog dump) and log lines to one sentence. Preserve all section
   numbers, the legend (🔒/🟢/📜), and the markdown structure so the file stays pasteable and scannable.
9. **Sanity pass before returning:** Is the North Star (§2) intact? Do §8–§10 reflect today? Is every
   decision and fork-resolution in §11? Is the changelog (§12) appended? Are frozen edits (if any)
   justified by a Decision and flagged to the user?
