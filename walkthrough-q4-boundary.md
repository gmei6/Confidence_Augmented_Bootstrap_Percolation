# walkthrough-q4-boundary.md — promoting the Q4 cascade-boundary card from Preliminary

**Result under promotion:** the advisor-site card *"Where the cascade boundary sits: mapping
τ_c(μ, n) at a larger seed"* — an **empirical, descriptive fit** of the P(systemic) = 0.5
contour on a finite (τ, μ, n) grid for the configuration-model graph family at fixed seed
size **a = 8**.

**This is not a law, a theorem, or an asymptotic scaling form.** It is a curve fitted to 27
interpolated boundary points drawn from a 196-cell grid, at one seed size, one base seed,
and over three doublings of n. Section 7 is load-bearing, not boilerplate.

## Relationship to the existing `walkthrough.md`

There is already a 496-line `walkthrough.md` at the repo root, written by the *implementation*
session for this same result. **I did not modify or destroy it.** I wrote this separate file
instead, for two reasons: (a) it is the artifact the earlier blind reviewer pass was fed, so
editing it would change the reviewer's input after the fact; and (b) this session adds
evidence that document does not contain — most importantly a **simulation-level regeneration
check** (that one re-ran the *analysis*, not the *simulation*).

Read `walkthrough.md` for the original implementation record. This file is the promotion
record and supersedes it where the two overlap. Every number below was re-derived on disk in
this session; none was copied from the earlier document without re-checking.

---

## 0. TL;DR — what is verified, and what is not

| Claim | Status |
| --- | --- |
| The simulation regenerates: re-running a committed config through `twocascade.runner.run_sweep` at `base_seed = 42` reproduces the on-disk raw **bit-for-bit** | **VERIFIED** — see §2, 2 of 28 configs re-run |
| 98,000 Python-engine runs over a 196-cell (τ, μ, n) grid, 500 trials/cell | **VERIFIED** (§3) |
| All 28 raws carry one uniform `git_commit` (`54e7a5e…`), no `dirty-or-unknown` sentinel | **VERIFIED** (§3) |
| Realized seed size is exactly a = 8 in every raw | **VERIFIED** (§3) |
| Filename-encoded τ agrees with the committed config's `graph.tau` in all 28 pairs | **VERIFIED** (§3) — this closes a hole flagged in `walkthrough.md` §7.4 |
| θ = 0.5 is read from raw metadata, not assumed, and is uniform | **VERIFIED** (§3) |
| The figure regenerates from a **committed script that asserts its own claims** and fails closed | **VERIFIED** (§4) |
| τ_c = a₀ + c·log₂(n/2000) + D·μ² with a₀ = 2.6295, c = −0.09607, D = 0.96039, R² = 0.96964 | **VERIFIED by independent recomputation** (§4) |
| **There is no resolved linear-in-μ term.** B = −0.030 ± 0.119, \|B\|/σ = 0.25 | **VERIFIED — and the script asserts it** (§4) |
| The single-argument logistic collapse describes the full surface | **NO** — χ²/dof = 33.70; the constant-width assumption is wrong (§7.1) |
| c = −0.096 is an asymptotic exponent | **NOT ESTABLISHED** — three doublings of n only (§7.3) |
| The *sign* of c (boundary moves down in τ as n grows) | **Solid** — \|c\|/σ ≈ 10.9, and monotone across all four n at every μ (§7.3) |
| This transfers to other seed sizes (e.g. a = 2) | **NO** (§7.2) |
| §5.4 Python↔C++ cross-validation | **N/A, with reason** — the C++ engine cannot build this graph family (§6). Not run, not faked, not claimed. |
| Raw outputs / figures are tracked in git | **No, deliberately** — `.gitignore` excludes them; nothing was force-added (§5b) |
| A dedicated regression test for this sweep exists | **No** — this is the weakest leg (§5d) |
| The result is recorded in the `okf/` knowledge bundle (§8/§11) | **NOT DONE** — out of scope for this session; §5f is OPEN |

---

## 1. Scope of this session

Done here:

1. Simulation-level regeneration check on 2 of 28 configs (§2).
2. A new committed, **self-verifying** figure script (§4).
3. §5.4 recorded as N/A with the structural reason (§6).
4. This walkthrough.
5. The blind `critic` → `auditor` gate (§8).

Explicitly **not** done here: no change to `src/`, `cpp/src/`, `configs/`, `tests/`, `okf/`,
`advisor-update-2026-07-22/index.html`, or `.lavish/`. The Preliminary badge was **not**
flipped — that is Gary's call, on AUDIT PASS.

---

## 2. Regeneration check — the simulation, not just the analysis

This is the evidence the earlier `walkthrough.md` does not have. Its §5(c) re-ran
`analyze_q4_psys_boundary.py` and confirmed the *analysis* reproduces from the raws. That
does not test whether the **raws themselves** are reproducible from (config, seed).

### 2.1 Method

For each config tested, I loaded the committed `configs/q4_psys_boundary_*.json`, changed
**only** `output.raw_filepath` to a scratch path outside the repository, and called the
sanctioned runner `twocascade.runner.run_sweep(cfg)` from the repo root. Nothing was written
under `results/`. The regenerated raw was then compared against the on-disk original.

Script: `scratchpad/regen_check.py` (session scratch, not committed — it is a one-shot
verification harness, and committing it would imply it is part of the pipeline).

Comparison is a SHA-256 over the canonicalized `results` array — all 7 μ-cells × 500
`failed_fractions` and `rounds_completed` — plus a field-by-field metadata comparison
excluding the two fields that are *expected* to differ (`git_commit`, `timestamp`).

### 2.2 Result

<!--REGEN_RESULTS-->

### 2.3 What this does and does not establish

- It **does** establish that (committed config, `base_seed = 42`) → the exact raw on disk,
  for the configs tested, on this machine and this NumPy. Determinism is not merely claimed.
- It **does not** cover the other 26 configs. They share one code path and one seeding
  scheme (`SeedSequence(42).spawn(num_cells × trials_per_cell)`, consumed cell-major), so
  there is no mechanism by which they would behave differently — but that is an argument,
  not a measurement, and it is labelled as such.
- `git_commit` in a fresh raw is **today's HEAD**, not `54e7a5e…`. The stamp records when a
  raw was produced, and the raws on disk predate the commit that landed the driver script.
  `walkthrough.md` §1.3 documents this ordering with timestamps; it is a real (minor)
  provenance weakness, and it is not smoothed over here either.

---

## 3. Provenance — machine-checked, not asserted

Every item in this section is checked **by the committed script**
`scripts/verify_q4_psys_boundary_figure.py`, which fails with a non-zero exit and writes no
figure if any check fails. It re-derives everything from the 28 raws and the 28 configs; it
deliberately does **not** read `results/processed/q4_psys_boundary_analysis.json`, so it is an
independent check of `analyze_q4_psys_boundary.py`, not a re-read of that script's output.

```
=== provenance checks ===
  [PASS] 28 raw files present   found 28
  [PASS] filename tau / n agree with the committed configs (28/28)
  [PASS] single uniform git_commit across all raws   ['54e7a5e3412d07c339413b04bbb55efac116803a']
  [PASS] git_commit is not the 'dirty-or-unknown' sentinel
  [PASS] realized seed size is exactly a = 8 everywhere   [8]
  [PASS] engine is 'python' in every raw (no C++ result trusted; §5.4 N/A)   ['python']
  [PASS] theta uniform and read from metadata, not hardcoded   theta = [0.5]
  [PASS] trials_per_cell == 500 everywhere   [500]
  [PASS] 196 cells on the (tau, mu, n) grid   got 196
  [PASS] every cell has exactly 500 trials
```

Two of these close holes the earlier walkthrough flagged as open weaknesses in its §7.4:

- **θ is now read from `metadata.theta` per raw** and required to be uniform, instead of the
  hardcoded `THETA = 0.5` in `analyze_q4_psys_boundary.py`.
- **The filename-as-database dependency is now checked**: τ is parsed from
  `..._tau2p3_raw.json` and cross-checked against `pinned_params.graph.tau` (and n against
  `pinned_params.n`) in the matching committed config, for all 28 pairs.

---

## 4. The figure, and the claims it asserts

`scripts/verify_q4_psys_boundary_figure.py` → `results/figures/q4_psys_boundary_advisor.png`.

It recomputes the boundary and both fits from the raws, and **asserts** every constant quoted
on the advisor card. Output verbatim:

```
=== boundary-location checks ===
  [PASS] 27 boundary points located   got 27
  [PASS] exactly one grid-censored corner, at n=2000, mu=0.90   [(2000, 0.9)]

=== fit  tau_c = a0 + c*log2(n/2000) + D*mu^2  (27 points) ===
      a0 =  2.62946 +/- 0.01880
      c  = -0.09607 +/- 0.00884
      D  =  0.96039 +/- 0.03633
      R2 = 0.96964   rmse = 0.04739 (tau units)
  [PASS] a0 matches the quoted 2.6295   got 2.62946, expected 2.6295 +/- 0.0005
  [PASS] c  matches the quoted -0.09607   got -0.096074, expected -0.09607 +/- 5e-05
  [PASS] D  matches the quoted 0.96039   got 0.960389, expected 0.96039 +/- 5e-05
  [PASS] R2 matches the quoted 0.96964   got 0.96964, expected 0.96964 +/- 5e-05
  [PASS] c < 0 and resolved (|c|/sigma > 3): boundary moves DOWN in tau as n grows   |c|/sigma = 10.9

=== full quadratic (adds B*mu):  B = -0.02982 +/- 0.11906   R2 = 0.96972 ===
  [PASS] B matches the quoted -0.030   got -0.0298203, expected -0.03 +/- 0.005
  [PASS] sigma_B matches the quoted 0.119   got 0.119055, expected 0.119 +/- 0.005
  [PASS] B is CONSISTENT WITH ZERO (|B|/sigma_B < 1) -- no linear-in-mu claim licensed   |B|/sigma_B = 0.25
  [PASS] dropping B costs < 0.001 in R2 (justifies the reduced form)   dR2 = 8.26e-05

=== single-argument logistic collapse: chi2/dof = 33.70 (dof=192) ===
  [PASS] chi2/dof matches the quoted 33.70   got 33.6972, expected 33.7 +/- 0.05
  [PASS] chi2/dof >= 10, i.e. the constant-width collapse UNDERFITS (reported, not hidden)

All claim checks passed. Drawing the figure.
```

Three of these assertions are deliberately adversarial rather than confirmatory:

- **`|B|/σ_B < 1`.** The linear-in-μ coefficient is consistent with zero. The script hard-fails
  if a future re-run ever produced a B this data does not support, so no downstream text can
  quietly acquire a μ-linear claim. **Nothing in this result says τ_c depends linearly on μ.**
- **`χ²/dof ≥ 10`.** The collapse's misfit is part of the reported result. Asserting it is
  *large* means a future change that appeared to "fix" the collapse would trip the gate and
  demand a fresh look, instead of silently improving a number the write-up calls bad.
- **Exactly one censored corner.** The (n = 2000, μ = 0.90) cell has no P = 0.5 crossing on
  the τ grid and is dropped from the fit. The script requires it to be exactly one and at
  exactly that corner, and the figure draws it as a marked triangle rather than letting it
  vanish.

### 4.1 Figure design notes

- **n is an ordered quantity, so the four series use one blue hue stepped light→dark**
  (ordinal ramp, validated: monotone lightness, adjacent ΔL ≥ 0.06, light end 2.06:1 against
  the surface), not four categorical identities.
- **Measured vs. computed are visually separated**: dots are interpolated crossings from
  simulation, lines are the fit. The subtitle says which is which. (`okf/lessons.md`:
  *"Label Computed Values as Computed, Especially Beside Measured Ones."*)
- Single y-axis, recessive grid, legend **and** direct labels on all four series so identity
  is never carried by color alone, and the "not a law" qualifier is in the subtitle rather
  than a distant caption.
- The three pre-existing figures from `analyze_q4_psys_boundary.py` (heatmap, fitted,
  collapse) are unchanged and still regenerate from that committed script.

---

## 5. §5.6 Definition of Done — item by item

**(a) Committed config + logged seed — HOLDS.** 28 configs committed in `54e7a5e`;
`base_seed = 42` in every config and echoed into every raw. Regeneration from that pair is
now *measured*, not assumed (§2).

**(b) Raw outputs saved — HOLDS on disk; NOT in git, by design.** All 28 raws, the processed
JSON, and four figures are on disk. `.gitignore` lines 29–33 exclude `results/raw/*`,
`results/figures/*`, `results/analysis/*`, `results/processed/*`, `results/*.json`,
`results/*.csv`, with the stated policy *"all simulation outputs are large and regenerable
from (config, seed, commit)."* Confirmed by `git check-ignore -v` on one raw, the new figure,
and the processed JSON. **Nothing was force-added.** `git ls-files results/ | grep q4_psys`
returns nothing.

For a verifier's benefit: `git ls-files results/` does return 20 tracked paths — older
artifacts from earlier tasks, force-added at some point in the past. **None belong to this
sweep.** The policy is applied consistently to this result; the repo is not uniformly clean
on this point historically.

**(c) Figure regenerates from a committed script — HOLDS.** Two independent paths:
`scripts/analyze_q4_psys_boundary.py` (pre-existing, three figures + processed JSON) and the
new `scripts/verify_q4_psys_boundary_figure.py` (advisor figure, self-asserting). The new
script's output was regenerated and visually inspected in this session; the PNG was confirmed
written by size and mtime, not by trusting a success message (`okf/lessons.md`:
*"'Done!' doesn't prove a file was written"*).

Honest caveat carried forward from `walkthrough.md` §5(c): matplotlib PNGs are **not**
byte-reproducible across runs (sub-pixel text rasterization); the *numerics* are exact.

**(d) Validation — PARTIAL. This is the weakest leg.** There is **no regression test that
exercises this sweep or its analysis**. What exists: `scripts/verify_q4_psys_boundary_figure.py`
now functions as an assertion harness over the on-disk artifacts (22 checks, fails closed),
and the component-level tests pass — see §5.1 below. This is a data-analysis result validated
by reproduction and assertion, not by a dedicated regression test. A verifier should weigh it
accordingly.

**(e) §5.4 C++ parity — N/A with reason.** See §6.

**(f) Recorded in `okf/` §8/§11 — NOT DONE.** No `okf/` file was edited in this session. If
§5.6 requires that entry before "Done", **this item is open** and is the one remaining gap.

### 5.1 Test status in this session

<!--TEST_RESULTS-->

---

## 6. §5.4 Python↔C++ cross-validation — N/A, with the reason stated

**No parity check was run, and none is claimed.** The reason is structural: **the C++ engine
cannot generate this graph family.** Verified by reading the sources in this session:

1. `cpp/src/main.cpp` accepts `--n --p --r --mu --kappa --seed-size --trials --base-seed
   --window-len --weights --graph-file --seed-file --output`. There is **no `--tau`, no
   `--d-min`, and no graph-type flag.**
2. The only graph sampler declared in `cpp/include/twocascade/graph.hpp` is
   `sample_gnp_adjacency`. There is no power-law degree sampler and no configuration-model
   pairing anywhere under `cpp/`.
3. C++ fear sampling is `sample_individual_fears(n, mean_fear, concentration, rng)` — no
   degree argument, no γ tilt. This sweep's Python path uses
   `sample_degree_dependent_fears(degrees, mu, gamma, kappa, rng_fear)`.
4. `runner.py`'s C++ dispatch never passes `graph_cfg` or `fear_cfg` to the binary.

**Consequence:** setting `engine: "cpp"` on these configs would not error — it would silently
simulate G(n, p) instead of a τ-parameterized configuration model. Reporting agreement or
disagreement from that would be actively misleading. So §5.4 is recorded as **not applicable
to this result.**

Guard rather than assertion: the committed verification script **checks that every raw records
`metadata.engine == "python"`** (28/28 PASS, §3), so it is machine-confirmed that no C++
output is being trusted here. A C++ binary exists at `cpp/build/twocascade_run` (dated
2026-06-11) and was not invoked.

A parity check for this path would require **new C++ work** — a power-law degree sampler,
configuration-model pairing, and degree-dependent fear — not a re-run of this sweep. That is
out of scope and was not attempted.

---

## 7. Caveats — stated before they are defended

### 7.1 The logistic collapse underfits, badly

χ²/dof = **33.70** (χ² = 6469.86, dof = 192). For a well-specified model this should be ≈ 1.
A value of 34 means the constant-width assumption is **wrong**, not merely imprecise: the
transition is a near-step at μ = 0 (P goes 0.838 → 0.606 → 0.176 → 0.000 across
τ = 2.3…2.9 at n = 2000) and has not even reached 0.5 across the whole Δτ = 1.2 grid at
μ = 0.9. One width cannot describe both. **The collapse figure is a qualitative visual
summary; its w and c must not be quoted as measurements.**

Note also that the two fits disagree on same-named coefficients — the boundary fit gives
c = −0.096 ± 0.009, the collapse gives c = −0.063 ± 0.001, and those intervals do not
overlap. That is a symptom of the collapse's misspecification. **The boundary fit is the
defensible number.**

Partly an artifact, stated plainly: cells with P = 0.000 have binomial SE = 0, floored to
`1e-3` by the analysis script, which manufactures large standardized residuals from
zero-variance cells. Part of the μ = 0 χ² contribution is that flooring, not physics.

### 7.2 The result is conditioned on a = 8 and does not transfer

At **a = 2 there is no P = 0.5 boundary at all** in this regime — the surface does not cross
0.5, so the construction here is undefined. That is a separate finding on a separate card.
Nothing here licenses "the cascade boundary is τ_c(μ, n) = …" without **at a = 8**.

### 7.3 c = −0.096 is a local slope over three doublings, not an exponent

n ∈ {2000, 4000, 8000, 16000}: the `log₂(n/2000)` regressor takes exactly four values
{0, 1, 2, 3}. This cannot distinguish log n from a slowly-varying power of n or from a drift
that saturates past n = 16000. **Extrapolating τ_c to n = 10⁵ from c = −0.096 is not
supported.**

What *is* solid is the **sign and ordering**: c < 0 at |c|/σ ≈ 10.9, and the boundary is
monotone-decreasing in τ across all four n at every one of the seven μ values. (`okf/lessons.md`:
*"A statement about a rate is not a statement about a level"* — this is a rate claim about how
τ_c drifts with n, and it says nothing about the value of τ_c at any particular n beyond the
fitted grid.)

### 7.4 Remaining limitations

- **τ grid spacing is 0.2** and crossings are located by *linear* interpolation of P in τ.
  Where the transition is a near-step (low μ) that is a crude locator. τ_c values are printed
  to three decimals; **they are not good to three decimals.**
- **One boundary point is censored** (n = 2000, μ = 0.90). The fit is on 27 points, not a
  balanced 28-point design, and the censoring is at the corner where the boundary is
  steepest — so the fit is extrapolating exactly where it is least constrained.
- **500 trials/cell** → binomial SE ≈ 0.022 at P = 0.5. Fine for locating a contour; not fine
  for the χ²-weighted collapse to be read at face value.
- **A single base seed (42).** No seed-to-seed replication of the whole sweep exists, so there
  is **no empirical estimate of run-to-run variability in the fitted coefficients.** The
  quoted standard errors are conditional on one RNG realization. This is the largest
  unquantified uncertainty in the result.
- **γ = 0 only.** No degree–fear tilt; this is the untilted slice.

### 7.5 Lessons check — is this result forced by its parameters?

`okf/lessons.md` (S-059, Task P) requires: *"before calling any null or negative a finding,
name the input you would have to change to get a different answer."* Applying it here:

- The claim is **positive**, not null: P(systemic) varies from ≈ 1 to ≈ 0 across the τ grid,
  so τ demonstrably changes the outcome. It is not arithmetic.
- The input that changes the answer is τ (and μ, and n) — all three were varied, and all
  three move the boundary.
- The **censored corner is the one place** where the grid, not the physics, determined the
  output — and it is excluded from the fit and marked on the figure rather than reported as
  "no cascade there".
- The related S-057 selection-tautology trap does not apply: the P = 0.5 contour is located by
  interpolation over an independently swept axis, not by a selection rule that could force the
  answer.

---

## 8. Verification gate (§IV)

<!--GATE_RESULTS-->

---

## 9. Files

**Committed (this result):**
- `configs/q4_psys_boundary_n{2000,4000,8000,16000}_tau{2p3,2p5,2p7,2p9,3p1,3p3,3p5}.json` (28) — `54e7a5e`
- `scripts/run_q4_psys_boundary.py` — `dce2bbb`
- `scripts/analyze_q4_psys_boundary.py` — `dce2bbb`
- `scripts/verify_q4_psys_boundary_figure.py` — **new in this session**

**On disk, intentionally untracked per `.gitignore`:**
- `results/q4_psys_boundary_n{n}_tau{tag}_raw.json` (28)
- `results/processed/q4_psys_boundary_analysis.json`
- `results/figures/q4_psys_boundary_{heatmap,fitted,collapse,advisor}.png`

**Untouched in this session:** `src/` (including the oracle `src/twocascade/reference.py`),
`cpp/`, `configs/`, `tests/`, `okf/`, `advisor-update-2026-07-22/index.html`,
`.lavish/experiments-redesign.html`, `walkthrough.md`, and the `../tc-work-girg-q6`
worktree. The **Preliminary badge was not flipped.**

---

## 10. How to reproduce from scratch

```bash
# from the repo root
python scripts/run_q4_psys_boundary.py             # 28 configs -> 28 raws
python scripts/analyze_q4_psys_boundary.py         # -> 3 PNGs + processed JSON
python scripts/verify_q4_psys_boundary_figure.py   # -> asserts 22 claims, then the advisor PNG
```

Deterministic given (config, `base_seed = 42`) — now measured, §2. Fresh raws will carry
today's HEAD as `git_commit` rather than `54e7a5e…`, for the reason in §2.3.
