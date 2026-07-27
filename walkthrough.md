# walkthrough.md — Q4: empirical P(systemic) cascade boundary τ_c(μ, n) at seed size a = 8

**Artifact under verification:** an *empirical, descriptive fit* of the P(systemic) = 0.5
contour on a finite (τ, μ, n) grid for the configuration-model graph family, at fixed
seed size a = 8.

**This is NOT a law, a theorem, or a universal scaling form.** It is a curve fitted to 27
interpolated boundary points drawn from a 196-cell grid. Everything below should be read
with that framing. The caveats in §7 are load-bearing, not boilerplate, and are stated
before the results are discussed further.

Prepared by the implementing worker. This document is self-contained: every number in it
was re-derived from the on-disk artifacts during the writing of this document, not copied
from the implementation session's console output.

---

## 0. TL;DR of what is and is not established

| Claim | Status |
| --- | --- |
| 98,000 Python-engine runs completed over the stated 196-cell grid | **Verified** (28 raws × 7 μ × 500 trials) |
| All raws carry a single, uniform `metadata.git_commit` = the real HEAD at run time | **Verified** |
| Realized seed size is exactly a = 8 in every raw, and matches an independent recomputation | **Verified** |
| Figures + processed JSON regenerate from a committed script (numerics byte-identical) | **Verified** |
| Full test suite green (`pytest tests/ -q`: 61 passed) | **Verified** |
| Configs and both scripts are committed | **Verified** |
| Raw outputs / figures / processed JSON are in git | **False, and deliberately so** — see §5 |
| §5.4 Python↔C++ cross-validation | **N/A** — the C++ engine cannot build this graph family; see §6 |
| τ_c(μ, n) = a₀ + c·log₂(n/2000) + D·μ² describes the boundary points well | **Supported** (R² = 0.970, RMSE = 0.047 in τ units, 27 points) |
| The single-argument logistic collapse describes the *full* surface | **Only partially** — χ²/dof ≈ 33.7; the constant-width assumption is wrong; see §7 |
| c = −0.096 is an asymptotic exponent | **Not established** — n spans a factor of 8 only; see §7 |
| This transfers to other seed sizes (e.g. a = 2) | **No** — see §7 |

---

## 1. What was run

### 1.1 Design (fixed in the 28 committed configs)

Graph family: **configuration model** with a power-law degree distribution,
`d_min = 2`, tail exponent τ. Everything else is pinned:

| Parameter | Value |
| --- | --- |
| `r` (bootstrap threshold) | 2 |
| `concentration` κ (Beta fear) | 50 |
| `theta` θ (systemic iff final failed fraction ≥ θ) | 0.5 |
| `window_len` | 5 |
| `weights` | [0.2, 0.2, 0.2, 0.2, 0.2] |
| `target_high_degree` | false |
| fear tilt `gamma` γ | 0.0 (no degree tilt) |
| scaling | `target_mean_degree` 4.0, `n_ref` 10000, `alpha` 0.6 |
| engine | `"python"` |
| `trials_per_cell` | 500 |
| `base_seed` | 42 |

I verified programmatically that **all 28 configs are byte-equivalent in these fields**,
differing only in `n`, `graph.tau`, `sweep.seed_multiples`, and `output.raw_filepath`.

### 1.2 Grid

- τ ∈ {2.3, 2.5, 2.7, 2.9, 3.1, 3.3, 3.5} — 7 values (one config file each, per n)
- μ ∈ {0.0, 0.15, 0.30, 0.45, 0.60, 0.75, 0.90} — 7 values (swept *inside* each config)
- n ∈ {2000, 4000, 8000, 16000} — 4 values

7 × 7 × 4 = **196 cells**, × 500 trials = **98,000 simulation runs**.
The processed JSON reports `grid.n_cells = 196` and a `p_surface` of length 196; I
confirmed both, and that every cell has `nt = 500`.

### 1.3 Provenance chain

- Configs: `configs/q4_psys_boundary_n{2000,4000,8000,16000}_tau{2p3,2p5,2p7,2p9,3p1,3p3,3p5}.json`
  — 28 files, committed in **`54e7a5e3412d07c339413b04bbb55efac116803a`**
  ("Q4: land 28 committed configs for the P(systemic) boundary sweep (a=8)", 2026-07-22 02:25:17 −0400).
- Driver: `scripts/run_q4_psys_boundary.py` — calls the sanctioned
  `twocascade.runner.run_sweep(cfg_path)` once per config. It does not write to
  `results/` itself; the runner owns all output and stamps it.
- Analysis: `scripts/analyze_q4_psys_boundary.py` — reads the raws, builds the P surface,
  locates the P = 0.5 contour, fits, and writes the figures + processed JSON.
- Both scripts committed in **`dce2bbbbcf2858da4fe0f9a8707b0f17c628e427`**
  ("Q4: runner driver and analysis script…", 2026-07-22 02:57:43 −0400). This is current HEAD.

**Note on commit ordering, stated plainly because it looks like a discrepancy and is not:**
the raws were produced *between* the two commits. The runner stamps whatever `git rev-parse HEAD`
returns at run time; at run time HEAD was `54e7a5e`, because the driver/analysis scripts
had not yet been committed. Timestamps confirm the ordering:

| Event | Time (2026-07-22, −0400) |
| --- | --- |
| `54e7a5e` (configs) committed | 02:25:17 |
| first raw written | 02:25:43 |
| last raw written | 02:49:32 |
| figures + processed JSON written | 02:51 |
| `105d5e3` (unrelated plotting scripts) committed | 02:52:51 |
| `dce2bbb` (this sweep's driver + analysis) committed | 02:57:43 |

So the stamp is *correct*, not stale — but it points at the configs commit, not at the
commit that contains the driver script. A re-run today would stamp `dce2bbb`. This is a
real (if minor) provenance weakness of committing the driver after the run, and it is
recorded here rather than smoothed over.

Also for the record: there is an intervening commit `105d5e3` ("Add committed plotting
scripts for the nu-scaling and size-biased-collapse figures") between the two commits
above. It touches only `scripts/plot_q3_nu_transition_width.py` and
`scripts/plot_q4_size_biased_collapse.py` and is unrelated to this result.

---

## 2. Git-stamp verification (all 28 raws)

I loaded **every one** of the 28 files matching `results/q4_psys_boundary_*_raw.json` and
read `metadata.git_commit`.

- Files found: **28** (matches the 28 configs, one raw each).
- Distinct `git_commit` values: **exactly one**.
- The value: **`54e7a5e3412d07c339413b04bbb55efac116803a`**, appearing in **28/28** files.
- `git rev-list` confirms this is a real commit in this repository, and it is the configs
  commit named in §1.3.
- No file carries the runner's fallback sentinel `"dirty-or-unknown"`.

**Result: the stamp is uniform and points at a real commit that was HEAD during the run.**

The analysis script independently re-derives this: its console output on re-run prints
`git_commit(s) in raws : ['54e7a5e3412d07c339413b04bbb55efac116803a']`, and the processed
JSON records `git_commits_in_raws` with that single entry.

---

## 3. Realized seed size — a = 8, checked two ways

The design intent is a **fixed absolute seed size a = 8**, identical at every n. The
configs express this indirectly: `sweep.seed_multiples = [8 / a_c0]`, where
`a_c0 = janson_a_c(n, p, r)` is the G(n,p) Janson critical seed size. The runner then
computes the realized seed as `a = max(r, round(mult * a_c0))`
(`src/twocascade/runner.py`, lines 272 and 282).

### 3.1 Direct read from the raws

`sweep_parameters.seed_size_grid` in all 28 raws: **`[8]`** — one distinct value across
all 28 files. The processed JSON likewise reports `seed_size_grid_values = [8]`.

### 3.2 Independent recomputation

I recomputed, from scratch, `beta = calculate_beta(4.0, 10000, 0.6)`,
`p = calculate_p_n(beta, n, 0.6)` and `a_c0 = janson_a_c(n, p, 2)` for each n
(functions from `src/twocascade/model.py`), and compared against the config's stored
multiple and the raw's stored `p`:

β = 0.10047545726038318

| n | recomputed p | p stored in raw | a_c0 | `seed_multiples[0]` from config | mult × a_c0 | round() | realized in raw |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2000 | 0.001050611122 | 0.001050611122 | 226.493645 | 0.03532107933340709 | 8.000000 | **8** | 8 |
| 4000 | 0.0006931448432 | 0.0006931448432 | 260.172877 | 0.03074878551 | 8.000000 | **8** | 8 |
| 8000 | 0.0004573050519 | 0.0004573050519 | 298.860156 | 0.02676837255 | 8.000000 | **8** | 8 |
| 16000 | 0.0003017088168 | 0.0003017088168 | 343.300170 | 0.0233032218 | 8.000000 | **8** | 8 |

`round(mult × a_c0) == 8` at every n, `max(r=2, 8) = 8`, and the recomputed p matches the
raw's stored p to full printed precision at every n.

**Result: the seed size actually simulated is a = 8 at every n. Confirmed.**

### 3.3 Why a = 8, and why a_c0 appears at all (lessons check)

`okf/lessons.md` records: *"Janson a_c Does Not Transfer to Heavy-Tailed Configuration
Models: seed grids built as multiples of the G(n,p) Janson a_c are entirely supercritical
on a τ = 2.5 CM — the real ignition transition sits near a ∈ [2, 32] at n = 4000, two
orders below."*

This design **complies with** that lesson rather than tripping it: a = 8 sits inside the
[2, 32] window the lesson identifies, and a_c0 is used here only as a *divisor* to express
that fixed absolute seed through the runner's multiple-based API. The realized seed grid is
`[8]`, not a multiple of a_c0 (a_c0 itself is 226–343). Nothing in this sweep is seeded at
O(a_c0).

---

## 4. Results read from `results/processed/q4_psys_boundary_analysis.json`

### 4.1 The P = 0.5 boundary points

For each (n, μ), P(systemic) is interpolated linearly in τ to find the crossing of 0.5.
**27 boundary points** were found, not 28:

| n | μ=0.00 | 0.15 | 0.30 | 0.45 | 0.60 | 0.75 | 0.90 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2000 | 2.549 | 2.641 | 2.714 | 2.822 | 2.989 | 3.212 | **—** |
| 4000 | 2.510 | 2.560 | 2.621 | 2.733 | 2.838 | 3.051 | 3.448 |
| 8000 | 2.421 | 2.477 | 2.580 | 2.618 | 2.752 | 2.923 | 3.251 |
| 16000 | 2.389 | 2.427 | 2.478 | 2.544 | 2.642 | 2.797 | 3.062 |

The missing cell is **(n = 2000, μ = 0.90)**: P never falls below 0.5 anywhere on the τ
grid there (P = 0.998 at τ = 2.3 falling only to 0.608 at τ = 3.5), so the crossing lies
**beyond τ = 3.5** and is censored by the grid edge. It is silently dropped by the fit —
the fit uses 27 points and reports `n_points = 27`. This is right-censoring at the corner
where the boundary is steepest in n, so the fit is being asked to extrapolate there.

### 4.2 Boundary fits

Full quadratic, `τ_c = a₀ + c·log₂(n/2000) + B·μ + D·μ²`, 27 points:

| coefficient | value | std. error |
| --- | --- | --- |
| a₀ | 2.6340 | 0.0265 |
| c | −0.09621 | 0.00903 |
| B | −0.02982 | 0.11906 |
| D | 0.99170 | 0.13038 |

R² = 0.96972, RMSE = 0.04732 (τ units).

**B is consistent with zero** (−0.030 ± 0.119; |B|/σ ≈ 0.25), so the reduced μ²-only form
is the one plotted and quoted:

`τ_c = a₀ + c·log₂(n/2000) + D·μ²`, 27 points:

| coefficient | value | std. error |
| --- | --- | --- |
| a₀ | 2.62946 | 0.01880 |
| c | −0.09607 | 0.00884 |
| D | 0.96039 | 0.03633 |

R² = 0.96964, RMSE = 0.04739. Dropping B costs essentially nothing in R² (0.96972 →
0.96964), which is the justification for the reduction. Note this makes B and D strongly
collinear over μ ∈ [0, 0.9] — the data do not cleanly separate a linear from a quadratic μ
dependence; they only say that *some* convex increasing function of μ fits, and μ² is the
simplest that does. Do not read D = 0.96 as evidence of a quadratic mechanism.

### 4.3 Full-surface logistic collapse

`P = 1 / (1 + exp((τ − (tc0 + D·μ² + c·log₂(n/2000))) / w))`, fitted to all 196 cells with
`sigma = max(binomial SE, 1e-3)` and `absolute_sigma=True`:

| coefficient | value | std. error |
| --- | --- | --- |
| tc0 | 2.51984 | 0.00234 |
| D | 1.06975 | 0.00486 |
| c | −0.06304 | 0.00113 |
| w | 0.105727 | 0.000682 |

R² = 0.92503, χ² = 6469.86, dof = 192, **χ²/dof = 33.70**.

**Read the standard errors here with suspicion.** They come from `curve_fit` with
`absolute_sigma=True` and are therefore *not* inflated by the χ²/dof ≈ 34 misfit. With the
model this badly misspecified, the quoted ±0.002 on tc0 measures curvature of a wrong
likelihood, not the uncertainty in tc0. Inflating naively by √33.7 ≈ 5.8 would give
tc0 ± 0.014, c ± 0.0066, w ± 0.0040 — still probably optimistic, since the residuals are
structured rather than random (§7.1).

Also note the two fits disagree on the same-named coefficients: the boundary fit gives
c = −0.096 ± 0.009, the collapse gives c = −0.063 ± 0.001. Those intervals do not overlap.
This is a direct symptom of the collapse's misspecification — it is trading n-dependence
against the width it cannot vary. **The boundary fit (§4.2) is the defensible number; the
collapse is a visualization, not an independent measurement.**

---

## 5. §5.6 Definition of Done — item by item, honestly

**(a) Committed config + logged seed — HOLDS.**
28 configs committed in `54e7a5e`. `base_seed = 42` is in every config and echoed into
every raw's `metadata.base_seed`. Seed derivation is `SeedSequence(42).spawn(196 × 500)`
consumed cell-major in the Python path (`runner.py` lines 318–327), so the run is
deterministic given (config, seed).

**(b) Raw outputs saved — HOLDS on disk; the outputs are NOT in git, by design.**
All 28 raws are present at `results/q4_psys_boundary_n{n}_tau{tag}_raw.json`, plus
`results/processed/q4_psys_boundary_analysis.json` and three PNGs under `results/figures/`.

**They are not tracked by git and cannot be without `git add -f`.** `.gitignore` lines
29–33 exclude `results/raw/*`, `results/figures/*`, `results/analysis/*`,
`results/processed/*`, `results/*.json`, and `results/*.csv`, with a comment stating the
policy explicitly: *"Results — all simulation outputs are large and regenerable from
(config, seed, commit). Keep the dir, ignore its contents."* `git check-ignore -v`
confirms each of the three artifact classes is matched by a specific rule.

This is the repository's **deliberate reproducibility model: scripts and configs are
committed; outputs are regenerated.** I am recording it plainly rather than presenting
untracked files as committed, and I did not force-add anything.

One honest wrinkle a verifier will find: `git ls-files results/` returns 20 tracked paths —
older figures and a few `results/processed/*_analysis.json` from earlier tasks that were
evidently force-added at some point in the past, before or despite this policy. **None of
them belong to this sweep**; `git ls-files results/ | grep q4_psys` returns nothing. So the
policy is applied consistently *to this result*, but the repo is not uniformly clean on
this point, and a verifier should not be surprised by those 20 files.

**(c) Figure regenerates from a committed script — HOLDS (numerics exactly; PNGs
semantically).**
I copied the pre-existing processed JSON and three PNGs aside, then re-ran the committed
`scripts/analyze_q4_psys_boundary.py` from a clean shell and compared.

- `results/processed/q4_psys_boundary_analysis.json`: **byte-identical after canonical
  JSON normalization** — every fitted coefficient, standard error, R², χ², the full
  196-cell `p_surface`, and all 27 boundary points reproduce exactly.
- The three PNGs are **not byte-identical**, and the pixel arrays are not identical either
  (1.8%–10.3% of pixels differ across the three). I inspected the before/after images
  side by side: they are visually the same figure with the same data, curves, ticks,
  labels, legend, and title text; the differences are sub-pixel text/line rasterization
  (matplotlib 3.10.8, Agg, font hinting). I am reporting this rather than claiming
  byte-reproducibility I did not observe. **Figures regenerate; they do not regenerate
  bit-for-bit.**

Also worth flagging, because it is exactly the failure mode `okf/lessons.md` warns about
("*'Done!' doesn't prove a file was written*"): every figure function in this script does
end with an explicit `savefig` + `close`, and I verified the regeneration by content
comparison and mtime, not by trusting the script's success message.

**(d) Validation — PARTIAL, and this is the weakest leg.**
There is **no test that exercises this specific sweep or its analysis script.** What does
exist and does pass:

- `tests/test_q4_config_model.py`, `tests/test_model.py`, `tests/test_analysis.py`: **22
  passed** in 1.68s. These cover the configuration-model degree sampler / pairing, the
  Janson scaling helpers (`calculate_beta`, `calculate_p_n`, `janson_a_c`) that §3.2
  depends on, and the analysis utilities.
- Full suite `python3 -m pytest tests/ -q`: **61 passed in 1647.48s (27m27s)**, zero
  failures, zero skips, run during the preparation of this document.

So the *components* this result stands on are tested; the *pipeline that produced this
particular number* is exercised only by the regeneration check in (c). A verifier should
weigh (d) accordingly: this is a data-analysis result validated by reproduction, not by a
dedicated regression test.

**(e) §5.4 C++ parity — N/A.** See §6.

**(f) Recorded in §8 / §11 of the knowledge bundle — NOT DONE in this session.**
I did not edit anything under `okf/`. The result is not yet recorded in the live-state or
decisions files. If the §5.6 checklist requires that entry before "Done", **this item is
open.**

---

## 6. §5.4 Python↔C++ cross-validation — N/A, with reason

**No parity check was run, and none is claimed.** The reason is structural, not a
shortcut: **the C++ engine cannot generate this graph family.**

Evidence, from reading the sources directly:

1. `cpp/src/main.cpp` accepts `--n --p --r --mu --kappa --seed-size --trials --base-seed
   --window-len --weights --graph-file --seed-file --output`. There is **no `--tau`, no
   `--d-min`, and no graph-type flag.** Its only two graph paths are (i) load a static CSR
   graph from `--graph-file`, or (ii) generate one internally.
2. The internal generator is `sample_gnp_adjacency(n, p, rng)` — the **only** graph
   sampler declared in `cpp/include/twocascade/graph.hpp`. There is no power-law degree
   sampler and no configuration-model pairing anywhere under `cpp/`.
3. Fear sampling in C++ is `sample_individual_fears(n, mean_fear, concentration, rng)`
   (`cpp/include/twocascade/rng.hpp`). It has **no degree argument and no γ tilt**. The
   Python path for this sweep uses `sample_degree_dependent_fears(degrees, mu, gamma,
   kappa, rng_fear)` (`runner.py` line 138). Even at γ = 0 these are different call paths
   over a different degree structure.
4. `runner.py`'s C++ dispatch (`run_single_cell_cpp`, lines 52–111, and the task
   construction at lines 287–300) **never passes `graph_cfg` or `fear_cfg` to the binary.**
   The configuration-model branch (line 131) exists solely in the Python single-trial path.

Consequence: setting `engine: "cpp"` on these configs would not raise an error — it would
**silently simulate G(n, p) instead of a τ-parameterized configuration model**, producing a
comparison that is not a parity test of anything. Running it and reporting agreement or
disagreement would be actively misleading.

Therefore §5.4 is recorded as **not applicable to this result**: the C++ engine does not
implement the graph family or the fear-sampling path under test. The configs pin
`engine: "python"` and every raw records `metadata.engine = "python"` (28/28), so no C++
result is being trusted here. (A C++ binary does exist at `cpp/build/twocascade_run`,
dated 2026-06-11, and was not invoked.)

**If the project wants a parity check for the configuration-model path, it requires new
C++ work — a power-law degree sampler, configuration-model pairing, and degree-dependent
fear — not a re-run of this sweep.**

---

## 7. Caveats — stated up front, not buried

### 7.1 The constant-width logistic collapse underfits. Badly.

χ²/dof = **33.70** (χ² = 6469.86 on 192 dof). For a well-specified model this should be
≈ 1. A value of 34 means the single-width assumption is **wrong**, not merely imprecise.

The mechanism is visible in the raw surface. The transition is a near-step at μ = 0 and
broad at high μ:

| n = 2000, μ = 0.00 | τ=2.3 | 2.5 | 2.7 | 2.9 | 3.1 | 3.3 | 3.5 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P(systemic) | 0.838 | 0.606 | 0.176 | 0.000 | 0.000 | 0.000 | 0.000 |

| n = 2000, μ = 0.90 | τ=2.3 | 2.5 | 2.7 | 2.9 | 3.1 | 3.3 | 3.5 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P(systemic) | 0.998 | 0.990 | 0.950 | 0.922 | 0.820 | 0.724 | 0.608 |

At μ = 0 the whole transition is over inside Δτ ≈ 0.4 and P is pinned at exactly 0.000 for
four consecutive τ values. At μ = 0.9 the same n has not even reached P = 0.5 across the
entire Δτ = 1.2 span of the grid. One constant w = 0.106 cannot describe both. Binning the
fit's χ² contribution by μ shows the misfit is concentrated in exactly those tails:

| μ | 0.00 | 0.15 | 0.30 | 0.45 | 0.60 | 0.75 | 0.90 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| mean χ² per cell | 42.4 | 20.9 | 24.0 | 18.3 | 21.4 | 42.1 | **61.9** |

Structured, U-shaped, sign-coherent residuals — not noise. **The collapse figure should be
presented as a qualitative visual summary, and its w and c should not be quoted as
measurements.** The μ = 0 column also has a second, mundane problem: cells with P = 0.000
have binomial SE = 0, floored to `1e-3` by the script, which manufactures very large
standardized residuals from zero-variance cells. Part of the 42.4 at μ = 0 is that flooring
artifact rather than physics.

### 7.2 This fit is specific to a = 8. It does not transfer to other seed sizes.

The entire result is conditioned on one fixed absolute seed size. At **a = 2 there is no
P = 0.5 boundary at all** in this regime — the surface does not cross 0.5, so there is
nothing to interpolate and the whole construction here is undefined. That is a separate
finding on a separate card and must not be conflated with this one. Nothing in this
document licenses a statement of the form "the cascade boundary is τ_c(μ, n) = …"
without the qualifier **at a = 8**.

### 7.3 n spans a factor of 8. c = −0.096 is a local slope, not an asymptotic exponent.

n ∈ {2000, 4000, 8000, 16000} is **three doublings** — the `log₂(n/2000)` regressor takes
only the four values {0, 1, 2, 3}. A linear-in-log₂n term fitted over three doublings is a
**local finite-size slope over that decade**. It is not evidence of a logarithmic
asymptotic form, and it cannot distinguish log n from a slowly-varying power of n or from
a drift that saturates beyond n = 16000. Extrapolating τ_c to n = 10⁵ or n → ∞ from
c = −0.096 is not supported by this data.

Related: the sign is at least stable and well-resolved (c/σ ≈ 10.9 in the boundary fit),
and the direction is consistent across all four n at every μ in the §4.1 table — the
boundary moves **down** in τ as n grows. That qualitative statement is solid. The numeric
coefficient is what should not be exported.

### 7.4 Other limitations a verifier should know

- **τ grid spacing is 0.2**, and boundary points are found by *linear* interpolation of P
  in τ. Where the transition is a near-step (low μ), a linear interpolant between two grid
  points is a crude locator, and the interpolation error there is a meaningful fraction of
  the 0.047 fit RMSE. The reported τ_c values are quoted to three decimals; they are not
  good to three decimals.
- **One boundary point is censored** (n = 2000, μ = 0.90, §4.1) and silently dropped. The
  fit is therefore not on a balanced 28-point design.
- **500 trials/cell** gives binomial SE ≈ 0.022 at P = 0.5. Fine for locating a contour;
  not fine for the χ²-weighted collapse to be taken at face value.
- **Single base seed (42).** There is no seed-to-seed replication of the whole sweep, so
  there is no empirical estimate of run-to-run variability in the fitted coefficients. The
  quoted standard errors are conditional on this one realization of the RNG stream.
- **γ = 0 only.** No degree–fear tilt is explored; this is the untilted slice.
- `THETA = 0.5` is **hardcoded** in `scripts/analyze_q4_psys_boundary.py` (line 43) rather
  than read from `metadata.theta`. It happens to match the configs (verified: `theta = 0.5`
  in all 28 configs and all 28 raws), so this result is correct — but the coupling is by
  convention, not enforced.
- τ is recovered by the analysis script by **parsing the raw's filename**
  (`..._tau2p3_raw.json` → 2.3), because τ is a graph parameter the runner does not copy
  into `metadata`. Correct here (filenames and configs were verified consistent), but it
  is a filename-as-database dependency worth knowing about.

---

## 8. How to reproduce from scratch

```bash
# from repo root, at commit dce2bbb (or later)
python scripts/run_q4_psys_boundary.py        # 28 configs -> 28 raws, ~24 min wall
python scripts/analyze_q4_psys_boundary.py    # -> 3 PNGs + processed JSON
```

The run is deterministic given (config, `base_seed = 42`). Note that the raws produced by
a re-run today will carry `git_commit = dce2bbb…` rather than `54e7a5e…`, for the reason
given in §1.3.

---

## 9. Files

**Committed:**
- `configs/q4_psys_boundary_n{2000,4000,8000,16000}_tau{2p3,2p5,2p7,2p9,3p1,3p3,3p5}.json` (28) — `54e7a5e`
- `scripts/run_q4_psys_boundary.py` — `dce2bbb`
- `scripts/analyze_q4_psys_boundary.py` — `dce2bbb`

**On disk, intentionally untracked per `.gitignore` (§5b):**
- `results/q4_psys_boundary_n{n}_tau{tag}_raw.json` (28)
- `results/processed/q4_psys_boundary_analysis.json`
- `results/figures/q4_psys_boundary_{fitted,collapse,heatmap}.png`

**Unmodified during this verification:** `src/` (including the oracle
`src/twocascade/reference.py`), `cpp/`, `okf/`, `configs/`, `tests/`,
`advisor-update-2026-07-22/index.html`. The only writes were the regeneration of the three
PNGs and the processed JSON by the committed analysis script (content-identical for the
JSON), plus this file.

---

**[Files Changed: `walkthrough.md` (new, uncommitted); `results/figures/q4_psys_boundary_*.png`
and `results/processed/q4_psys_boundary_analysis.json` regenerated by the committed
analysis script · Validation Status: §5.6 (a) HOLDS, (b) HOLDS on disk / intentionally
untracked, (c) HOLDS (numerics exact, PNG semantic), (d) PARTIAL — components tested, no
sweep-specific regression test, (e) §5.4 N/A with documented reason, (f) OPEN — not
recorded in `okf/` · New Decisions: none — no decision was taken in this session]**
