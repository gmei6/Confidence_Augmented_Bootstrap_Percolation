# F2 Adversary Report — Fear Marks (m/k) Mechanism

> **Status:** Advisory assessment — no source or test files modified.
> **Date:** 2026-06-04
> **Author:** Adversary Agent
> **Scope:** Fork F2 as described in §3.6 of PROJECT_TRACKER.md

---

## Reporting Contract

| Category | Details |
|---|---|
| **Tests Added/Modified** | 0 — advisory only. 14 concrete test cases proposed (see §9). |
| **Validation Pass/Fail** | Existing `test_mu0_bootstrap_threshold.py` passes 4/4 under the CURRENT engine. F2 implementation risks breaking this — conditions enumerated below. |
| **Edge Cases Discovered** | 12 distinct edge cases / failure modes identified across 9 analysis sections. |

---

## Table of Contents

1. [Critical Invariant: μ=0 Equivalence](#1-critical-invariant-μ0-equivalence)
2. [Effective Threshold Reduction](#2-effective-threshold-reduction)
3. [Mark Accumulation and Supercriticality](#3-mark-accumulation-and-supercriticality)
4. [Simultaneous Update Rule (§3.4)](#4-simultaneous-update-rule-§34)
5. [Interaction with D-006 Window-Length](#5-interaction-with-d-006-window-length)
6. [Halting Condition](#6-halting-condition)
7. [Degenerate Parameter Values](#7-degenerate-parameter-values)
8. [Cross-Language Validation Impact (§5.4)](#8-cross-language-validation-impact-§54)
9. [Proposed Test Cases](#9-proposed-test-cases)

---

## 1. Critical Invariant: μ=0 Equivalence

### The requirement

At μ=0, `sample_individual_fears` returns an all-zero vector ([reference.py:269–270](file:///Users/garymei/Downloads/CABP_copy_for_antigravity/src/twocascade/reference.py#L269-L270)). Since every `f_i = 0`, the fear probability `f_i · g_t = 0` for all nodes in all rounds. Therefore:

- No Bernoulli draw ever succeeds → **no fear activations occur** → **no marks are ever generated**.
- The solvency channel check `(failed_neighbor_count + active_marks) >= r` reduces to `failed_neighbor_count >= r` because `active_marks = 0` always.
- **The F2 model MUST be identical to pure Janson bootstrap percolation at μ=0.**

### The test

[test_mu0_bootstrap_threshold.py](file:///Users/garymei/Downloads/CABP_copy_for_antigravity/tests/test_mu0_bootstrap_threshold.py) must pass with **zero code changes** after F2 is implemented. All four tests (`test_mu0_run_is_reproducible`, `test_deep_subcritical_stays_small`, `test_deep_supercritical_percolates`, `test_empirical_threshold_matches_a_c`) depend exclusively on the solvency channel at μ=0.

### What could go wrong

| Risk | Mechanism | Likelihood |
|---|---|---|
| **Default marks ≠ 0** | If `Node` gains a `marks` field initialized to a nonzero default (e.g., `marks: int = 1` by typo), the solvency check is corrupted for ALL nodes at ALL μ values, including μ=0. | Medium — dataclass default errors are common. |
| **Off-by-one in mark lifetime** | If marks are initialized with lifetime `k` but the decay logic uses `> 0` instead of `>= 0` (or vice versa), a mark could persist one round too long or vanish one round too early. At μ=0 this is harmless (no marks), but it could mask bugs that only appear at μ>0. | Low at μ=0; high at μ>0. |
| **RNG stream divergence** | If the F2 engine draws random numbers for mark generation even when `f_i = 0` (i.e., it calls `rng.random()` unconditionally and then checks whether to apply marks), the RNG stream shifts relative to the current engine. The current engine has a guard: `fear_failure_probability > 0.0 and rng.random() < fear_failure_probability` ([reference.py:114](file:///Users/garymei/Downloads/CABP_copy_for_antigravity/src/twocascade/reference.py#L114)). At μ=0, `fear_failure_probability = 0.0`, so `rng.random()` is never called. If F2 removes this guard, the graph generation and seed selection RNG draws are identical, but any subsequent Bernoulli draws for fear shift the RNG state, changing subsequent graph generations within multi-trial runs. `test_mu0_run_is_reproducible` would still pass (same seed → same stream), but statistical tests could shift. | Medium — subtle and hard to detect. |
| **Solvency check refactored incorrectly** | If the implementer changes the solvency check to `failed_neighbor_count + active_marks >= r` but introduces a bug where `active_marks` is read from uninitialized memory or a stale round's state, the μ=0 behavior could break. | Low. |

> [!IMPORTANT]
> **Guard required:** The F2 implementation MUST preserve the `fear_failure_probability > 0.0` short-circuit in [reference.py:114](file:///Users/garymei/Downloads/CABP_copy_for_antigravity/src/twocascade/reference.py#L114). Removing it would change the RNG stream for all μ=0 tests, even though the marks mechanism itself is dormant.

---

## 2. Effective Threshold Reduction

### The core issue

Under F2, the solvency check becomes:

```
(failed_neighbor_count + active_marks) >= r
```

This means a node can fail with **fewer** failed neighbors than the current model requires. The effective threshold becomes `r_eff = r - active_marks`. This is a fundamental change to the cascade dynamics.

### Case analysis: m ≥ r

If `m ≥ r`, a single fear activation on a node with **zero** failed neighbors immediately satisfies the solvency check:

```
0 + m >= r  →  True (when m >= r)
```

**This is functionally equivalent to direct fear failure** (the current §3.3 model), but routed through the solvency channel with a one-round delay (marks generated in round t are visible in round t+1 under the frozen-snapshot rule — see §4 below).

| Property | Current §3.3 (direct) | F2 with m ≥ r |
|---|---|---|
| **Timing** | Fails in the same round as the fear draw | Fails one round AFTER the fear draw (if marks are t+1 visible) |
| **Can chain further failures?** | Yes, immediately (the failed node's neighbors see it this round) | Yes, but delayed by one round |
| **R_fear** | ≈ μ (subcritical) | Depends on mark accumulation — see §3 |
| **Reversion possible?** | No (failure is absorbing) | No (once the solvency check fires, failure is still absorbing) |

> [!WARNING]
> **m ≥ r is a degenerate case that eliminates the "subcritical amplifier" framing.** In this regime, a single fear activation is sufficient to fail a node regardless of its network neighborhood. Fear becomes an autonomous failure channel again, just with a one-round lag. The project's central claim (§3.3: "fear is a subcritical amplifier that cannot ignite a cascade on its own") survives only if the m/k mechanism is **carefully parameterized** with m < r.

### Case analysis: m = 1, r = 2

A node needs `failed_neighbors + marks >= 2`. With 1 active mark, the node fails with just **1** failed neighbor instead of the usual 2. This:

- **Halves the effective solvency barrier** for marked nodes.
- Changes the cascade geometry: in the Janson regime, a node with degree ~np ≈ 10 has ~`np · φ` failed neighbors at failed fraction φ. The solvency probability per node goes from `~(npφ)^r / r!` to a mixture: nodes with active marks contribute `~(npφ)^1 / 1!` (effectively an r=1 rule), while unmarked nodes contribute `~(npφ)^2 / 2!`.
- **r=1 bootstrap percolation is qualitatively different** from r≥2 (§3.2 notes this explicitly). Marked nodes temporarily behave as r=1 nodes — this creates a heterogeneous-threshold network where the threshold depends on recent fear history.

> [!CAUTION]
> The Janson threshold formula $a_c = (1-1/r) \cdot t_c$ with $t_c = ((r-1)!/np^r)^{1/(r-1)}$ assumes a **uniform** threshold r. F2 with m=1, r=2 creates a time-varying mixture of r=1 and r=2 nodes. The analytical benchmark (§4) is no longer directly applicable for μ>0, and a new mean-field analysis would be needed.

---

## 3. Mark Accumulation and Supercriticality

### Can marks accumulate?

The original summary says "m fear marks are added" per activation. If fear activates on the same node in round t and round t+1 (and marks from round t haven't yet expired), the node would have **2m** active marks. This must be specified:

**Option A — Marks stack additively.** Each fear activation adds m marks with independent k-round lifetimes. A node can accumulate arbitrarily many marks over multiple rounds of fear activation.

**Option B — Marks cap at m.** Each fear activation refreshes the mark count to m and resets the decay timer. Multiple activations don't compound.

**Option C — Marks cap at r.** Marks are capped at the solvency threshold, since exceeding r has no additional effect (the node fails at r).

### Supercriticality analysis (Option A — additive stacking)

Under additive stacking, consider a node experiencing fear activation in consecutive rounds. After round t, it has m marks (decaying over k rounds). After round t+1, it has 2m marks (the first batch partially decayed, plus m new). The maximum possible marks on a single node is `m · min(k, cascade_duration)`.

The feared reproduction number under marks is **not** simply μ. Consider:

1. A fear activation at round t adds m marks to a node.
2. Those marks persist for k rounds, making that node easier to fail during all k rounds.
3. If the node fails at round t+j (j < k) due to the lowered threshold, that failure propagates to its neighbors via the solvency channel.

The **effective fear reproduction number** becomes:

```
R_fear_marks ≈ μ · (probability that marks cause an additional failure 
                     that wouldn't have occurred without marks)
```

This is **larger** than μ when marks are bridging the gap between `failed_neighbors` and `r`, because each marked node has a k-round window to be "pushed over" by solvency.

### Conditions for breaking subcriticality

Mark accumulation breaks the subcritical amplifier property when:

1. **k is large** (marks persist for many rounds) — more nodes carry active marks at any time.
2. **m is close to r** — fewer additional failed neighbors needed.
3. **μ is moderately large** (but still < 1) — more nodes receive marks per round.
4. **The network is dense** (high np) — more neighbors to interact with marked nodes.

The critical question: **can marks create a self-sustaining cascade even without the solvency channel?** If a fear activation marks node A, and that mark causes A to fail (by bridging the gap), and A's failure increases g_t, which causes more fear activations, which mark more nodes... this is a feedback loop that could make fear self-sustaining.

> [!WARNING]
> **If m · k is large enough relative to r, the marks mechanism can make fear effectively supercritical**, breaking the project's central structural property (§3.3: R_fear ≈ μ < 1). The subcritical amplifier claim requires either (a) m < r strictly, AND k is bounded, or (b) a proof that the indirect effect through marks preserves subcriticality. Neither is currently established.

---

## 4. Simultaneous Update Rule (§3.4)

### The timing ambiguity

The current engine ([reference.py:97–128](file:///Users/garymei/Downloads/CABP_copy_for_antigravity/src/twocascade/reference.py#L97-L128)) uses a frozen-snapshot evaluation:

1. **STEP 1 (evaluate):** Read the start-of-round state. Determine which nodes fail.
2. **STEP 2 (apply):** Apply all failures simultaneously. Update neighbor counters.

With marks, two timing questions arise:

### Question 1: When are newly generated marks visible?

**Option A — Same-round visibility (violates frozen snapshot):**
- Round t: fear activates on node X → m marks added to X → solvency check sees the marks → X could fail this round.
- **Problem:** This violates the frozen-snapshot rule. A node's marks are generated by a fear draw in this round, but the fear draw result is "new information" from this round. If marks are visible immediately, then evaluation order matters (nodes checked before X don't see X's marks, but X sees its own marks).

**Option B — Next-round visibility (preserves frozen snapshot):**
- Round t: fear activates on node X → m marks are *queued* for X.
- Round t+1: X's marks become active. Solvency check sees `failed_neighbors + marks >= r`.
- **This is the only option consistent with §3.4's design.** It means fear has a **two-round delay**: round t's failures → round t+1's fear probability → marks generated in round t+1 → visible in round t+2.

### Question 2: Mark decay timing

If marks last k rounds, when do they expire?

**Option A — Marks from round t expire at the START of round t+k:**
- A mark generated in round t is active during rounds t+1, t+2, ..., t+k-1 (k-1 rounds of activity if next-round visibility).

**Option B — Marks from round t expire at the END of round t+k:**
- A mark generated in round t is active during rounds t+1, t+2, ..., t+k (k rounds of activity if next-round visibility).

**Option C — Marks from round t expire at the START of round t+k+1:**
- Equivalent to Option B.

### Proposed precise timing specification

```
PROPOSED RULE (consistent with §3.4 frozen-snapshot):

1. At the START of round t, for each solvent node i:
   a. Decay: remove all marks whose creation_round <= t - k.
   b. Evaluate solvency: fails if (failed_neighbor_count + active_marks) >= r.
   c. Evaluate fear: if Bernoulli(f_i · g_t) succeeds, QUEUE m new marks 
      for node i with creation_round = t.
      (These marks are NOT visible until round t+1.)

2. At the END of round t:
   a. Apply all solvency failures simultaneously.
   b. Activate all queued marks (they become visible next round).
   c. Update neighbor counters for newly failed nodes.

Effect: a mark created in round t is active in rounds t+1 through t+k-1 
        (k-1 rounds of activity). For k=1: the mark is active only in 
        round t+1 (a one-round pulse). For k=0: the mark is never active 
        (no-op).
```

> [!IMPORTANT]
> The timing specification MUST be nailed down before implementation. An off-by-one here changes the effective duration of marks by one full round and can shift cascade dynamics.

---

## 5. Interaction with D-006 Window-Length

### Double persistence

The D-006 window-length parameter already provides fear persistence through the global fear field:

```
g_t = (1/n) · Σ_{k=1}^{X} w_k · a_{t-k}
```

With X > 1, fear "remembers" multiple past rounds. Marks add a **second** persistence mechanism: even after g_t drops to zero, marks placed in earlier rounds remain active for k rounds.

### The interaction matrix

| Scenario | g_t behavior | Mark behavior | Combined effect |
|---|---|---|---|
| X=1, k=1 | One-round memory | One-round pulse | Minimal persistence: fear activation in round t generates marks active only in round t+1. If no new failures in t, g_{t+1}=0 and no new marks. |
| X=4, k=1 | Four-round memory | One-round pulse | g_t stays nonzero for 4 quiet rounds, generating marks each round. But each batch of marks lasts only 1 round. |
| X=1, k=4 | One-round memory | Four-round persistence | g_t drops to 0 after one quiet round, but marks from the last active round persist for 4 rounds, potentially causing delayed failures. |
| X=4, k=4 | Four-round memory | Four-round persistence | **Maximum persistence.** g_t has a 4-round tail, each round potentially generating marks that persist 4 more rounds. Effective fear persistence window = X + k - 1 = 7 rounds. |

### Risk: Double-counting fear persistence

D-006's pilot showed that P(systemic) is invariant in X (within ±0.03) because the kernel mass (= μ) is preserved. But marks add a persistence channel **outside** the kernel normalization. The total fear "energy" over time is no longer bounded by μ alone — it's μ (from the kernel) plus the additional solvency-lowering effect of accumulated marks.

> [!WARNING]
> **The D-006 invariance result (P(systemic) is independent of X) may NOT hold when marks are present.** With marks, increasing X means more rounds of mark generation → more active marks at any given time → more nodes with lowered effective threshold. This breaks the "only kernel mass matters" argument that underpins D-006.

### Recommendation

If F2 is implemented, the D-006 window-length study (Wk-9) must be **re-run** with marks enabled to verify whether the invariance holds. If it doesn't, the interaction between X and k must be characterized as a 2D parameter space, which significantly increases the study's scope.

---

## 6. Halting Condition

### Current halting rule

The engine halts when `new_failed_last_round = 0` (i.e., `a_t = 0`). At that point, `g_{t+1} = a_t / n = 0`, so no new fear activations occur, and no new solvency failures occur (because no new neighbor failures). The absorbing state is genuine ([reference.py:94](file:///Users/garymei/Downloads/CABP_copy_for_antigravity/src/twocascade/reference.py#L94), §3.4).

### With marks: the halting problem

Consider this scenario:

1. Round t: 5 new failures occur. g_{t+1} = 5/n.
2. Round t+1: Fear activates on several nodes, placing marks. But 0 new solvency failures occur. `a_{t+1} = 0`.
3. Under the current halting rule, the cascade stops here.
4. **But:** marks placed in round t+1 are still active. In round t+2, some nodes have `failed_neighbors + marks >= r` and SHOULD fail.

**The current halting rule is INCORRECT for the marks model.** A round with zero new failures but active marks on nodes is not a genuine absorbing state — it's a "quiet" round that could be followed by mark-triggered failures.

### Can a quiet round be followed by failures?

Yes, under this sequence:
1. Round t: node A fails (by solvency), incrementing neighbors' counters.
2. Round t+1: g_t = 1/n. Fear activates on node B (which has, say, r-1 failed neighbors). m marks are added to B. But no node has enough failed neighbors to fail yet (B has r-1 + 0 marks currently visible = r-1 < r). So `a_{t+1} = 0`.
3. Round t+2: B's marks become active (next-round visibility). Now B has `r-1 + m >= r` (if m >= 1). B fails.

Under the current halting rule, the cascade would have stopped at the end of round t+1, **missing B's failure in round t+2**.

### Proposed fix

The halting condition must be generalized:

```
PROPOSED HALTING RULE (with marks):

The cascade halts at the end of round t if ALL of:
  (a) a_t = 0  (no new failures this round)
  (b) No solvent node has active_marks > 0  (no pending mark effects)
  (c) g_{t+1} = 0  (no fear activations will occur next round)

Equivalently: halt when there is no mechanism that could produce a 
new failure in any future round.

With D-006 window length X: condition (c) becomes "the fear window 
is empty" (X consecutive quiet rounds), as per D-006's generalized halt.
Combined with marks: halt when the fear window is empty AND no solvent 
node has active marks.
```

> [!CAUTION]
> **Failure to update the halting rule will cause the F2 engine to produce systematically smaller cascades than the true model.** This is a silent correctness bug — tests will pass (cascades are strictly smaller, not larger, than the correct answer), but the results will undercount systemic events. This is the single most likely implementation bug for F2.

---

## 7. Degenerate Parameter Values

### k = 0 (marks vanish instantly)

If marks have a lifetime of 0 rounds, they are never active (created in round t, expired before round t+1 under next-round visibility). **Fear has no effect whatsoever.** This is strictly weaker than the current §3.3 model (where fear causes direct failure). The model reduces to pure bootstrap percolation at **all** μ, not just μ=0.

**Test assertion:** For any μ ∈ [0,1], the final failed fraction distribution should be statistically indistinguishable from the μ=0 baseline when k=0.

### k = 1 (one-round pulse)

Marks are active for exactly one round (created in round t, active in round t+1, expired in round t+2). This is the minimal non-trivial duration. Fear's solvency contribution is a single-round opportunity: if the lowered threshold doesn't trigger failure in that one round, the marks vanish.

**Key property:** Because marks last only one round, accumulation is impossible (a node can have at most m marks at any time, from at most one fear activation). This makes k=1 the safest parameter choice for preserving the subcritical amplifier property.

### k → ∞ (permanent marks)

Marks never decay. Every fear activation permanently lowers a node's effective threshold by m. After enough activations, any node's threshold is effectively 0 (it will fail even with no failed neighbors, if marks ≥ r).

**This echoes the rejected cumulative fear field (D-005).** The cumulative field was rejected because it makes the all-solvent state linearly unstable for any μ>0. Permanent marks have a similar effect: once enough nodes accumulate marks ≥ r, they fail unconditionally, driving g_t higher, causing more marks, creating a runaway feedback loop.

> [!WARNING]
> **k → ∞ with additive mark stacking is functionally equivalent to the cumulative fear model rejected in D-005.** If F2 is implemented, k MUST be bounded and the specification should explicitly disallow k = ∞.

### m = 0 (fear generates no marks)

Fear activates (the Bernoulli draw succeeds) but adds 0 marks. **Fear is a complete no-op.** The model reduces to pure bootstrap percolation at all μ, identical to k=0.

**Test assertion:** For any μ, k, the model with m=0 should be indistinguishable from pure Janson bootstrap percolation.

### m = r (one activation = failure)

A single fear activation places r marks on a node. If the node has 0 failed neighbors, it has `0 + r >= r` → fails (in the next round under frozen-snapshot timing). This makes fear a delayed-direct-failure channel: functionally identical to §3.3 but with a one-round lag.

**Key difference from §3.3:** the one-round delay means that R_fear might be slightly different (because the node survives one extra round before failing, and g_t may change in that round). But the overall dynamics should be very similar to direct fear failure.

### m > r (marks exceed threshold)

A fear activation places m > r marks. The excess marks (beyond r) have no additional effect — the node fails when `marks >= r`, and having `marks = m > r` doesn't fail it "more." Failure is still absorbing.

**However,** if marks stack additively and the node doesn't fail in the round the marks become active (because it wasn't checked yet — impossible under simultaneous update), the excess marks are wasted. Under simultaneous update, all nodes are checked each round, so m > r is functionally identical to m = r. **m should be capped at r in the implementation** to avoid confusion, or at minimum documented as equivalent.

### Summary table

| Parameters | Behavior | Reduces to | Notes |
|---|---|---|---|
| m=0, any k | No-op | Pure Janson | Fear draws consume RNG but have no effect |
| any m, k=0 | No-op | Pure Janson | Marks never visible |
| m≥r, k≥1 | Delayed direct failure | ~§3.3 with 1-round lag | Breaks subcritical amplifier framing |
| m=1, r=2, k=1 | One-round threshold reduction | Heterogeneous r ∈ {1,2} network | Minimal non-trivial case |
| m=1, r=2, k→∞ | Permanent threshold reduction | Approaching cumulative D-005 | Subcriticality at risk |
| m<r, k=1 | One-round partial threshold reduction | Novel | Sweet spot for the mechanism |

---

## 8. Cross-Language Validation Impact (§5.4)

### μ=0 same-graph check: UNAFFECTED

At μ=0, no marks are generated. The cascade is deterministic given the graph. The §5.4 same-graph check (dump graph from Python, load in C++, confirm identical final failed set) is **unaffected** by F2 — the same test works.

### μ>0 statistical check: NEW CONSIDERATIONS

The statistical agreement check (C++ and Python P(systemic) and |A*|/n histograms agree within Monte Carlo error) is affected:

1. **Mark state adds implementation surface area.** The C++ port must replicate the exact mark semantics: when marks are generated, how they accumulate, when they decay, how they interact with the solvency check. Any divergence in mark timing produces systematically different cascade sizes.

2. **Additional validation needed for mark mechanics.** Beyond the existing μ>0 statistical check, the C++ port needs:
   - A **deterministic mark-counting check:** construct a small graph (e.g., 10 nodes), force specific fear activations (by setting f_i = 1.0 for target nodes and engineering g_t), and verify that the C++ and Python engines produce the same mark state at each round.
   - A **mark-decay check:** verify that marks expire at exactly the correct round in both languages.
   - A **mark-accumulation check:** if marks stack, verify that multiple activations produce the correct total mark count.

3. **Timing semantics must be byte-identical.** The mark visibility rule (same-round vs. next-round) and decay rule (start-of-round vs. end-of-round) must be implemented identically. Even a one-round difference in mark timing will produce different cascade dynamics.

### Proposed validation strategy addition

```
PROPOSED ADDITIONAL CROSS-LANGUAGE CHECK (for F2):

(3) Mark-mechanics check: construct a small fixed graph (n ≤ 20) with 
    known topology. Set μ high (e.g., all f_i = 0.9) and a specific seed. 
    Run one cascade and dump the FULL per-round state (failed set, mark 
    counts per node, g_t) from both Python and C++. Verify that the mark 
    state is identical at every round.

    NOTE: This requires both engines to use the same RNG stream, which is 
    generally NOT possible across languages (§5.4). Workaround: at μ=1.0 
    and f_i = 1.0, fear ALWAYS activates (probability = 1.0 · g_t, which 
    equals 1.0 when g_t = 1.0 — but g_t < 1 in general). Better workaround: 
    engineer a test where fear activation is deterministic by construction 
    (e.g., only one solvent node with f_i = 1.0, seeded with g_t = 1.0).
```

---

## 9. Proposed Test Cases

The following pytest test functions should exist before F2 can be marked as validated. They are grouped by the property they test.

### Group A: μ=0 invariant preservation

#### `test_f2_mu0_matches_janson_threshold`
**Description:** Run the full `test_mu0_bootstrap_threshold.py` suite with the F2 engine (m=1, k=1 and m=2, k=3) at μ=0. All four tests must pass with identical outcomes to the current engine.

**Assertion:** Final failed fractions are bitwise identical to the non-F2 engine at μ=0, because no marks are generated.

#### `test_f2_m0_is_pure_janson`
**Description:** With m=0 (marks generate nothing), run cascades at μ=0.5 and compare the final failed fraction distribution to μ=0 (pure Janson). They should be statistically indistinguishable.

**Assertion:** Two-sample KS test p-value > 0.05 between m=0, μ=0.5 cascades and μ=0 cascades.

#### `test_f2_k0_is_pure_janson`
**Description:** With k=0 (marks vanish instantly), run cascades at μ=0.5. Compare to μ=0. They should be statistically indistinguishable.

**Assertion:** Two-sample KS test p-value > 0.05 between k=0, μ=0.5 cascades and μ=0 cascades.

### Group B: Mark mechanics

#### `test_f2_mark_generation_on_fear_activation`
**Description:** Construct a small graph (n=10, known topology). Set f_i = 1.0 for one specific node, all others f_i = 0. Trigger one failure to create g_t > 0. Verify that exactly m marks are placed on the target node and 0 marks on all others.

**Assertion:** After the fear activation round, `target_node.active_marks == m` and all other nodes have 0 marks.

#### `test_f2_mark_decay_after_k_rounds`
**Description:** Same setup as above. After marks are placed, run k additional rounds with no new fear activations (g_t = 0 or f_i = 0 for all). Verify marks decay to 0 after exactly k rounds.

**Assertion:** At round `t + k`, `target_node.active_marks == 0`.

#### `test_f2_mark_visibility_respects_frozen_snapshot`
**Description:** Place marks on a node in round t. Verify they are NOT visible in the solvency check of round t (same round), but ARE visible in round t+1.

**Assertion:** Node does not fail in round t (despite having marks + failed_neighbors >= r, if marks were visible). Node DOES fail in round t+1 (marks now visible).

### Group C: Threshold reduction

#### `test_f2_marks_lower_effective_threshold`
**Description:** Construct a graph where a node has exactly r-1 failed neighbors. Without marks, it should NOT fail. Place m=1 mark on it. It should fail in the next round.

**Assertion:** Without marks: node survives. With 1 mark: node fails.

#### `test_f2_m_geq_r_immediate_failure`
**Description:** Set m=r. A single fear activation on a node with 0 failed neighbors should cause it to fail in the next round (marks = r >= r).

**Assertion:** Node with 0 failed neighbors and m=r marks fails in one round after mark activation.

### Group D: Accumulation and supercriticality

#### `test_f2_marks_accumulate_additively`
**Description:** (If additive stacking is the chosen semantics.) Activate fear on the same node in two consecutive rounds. Verify the node has 2m marks (not m).

**Assertion:** After two consecutive fear activations, `node.active_marks == 2 * m`.

#### `test_f2_subcritical_amplifier_preserved`
**Description:** At μ = 0.3 (well below 1), m=1, r=2, k=1, run 500 cascades with seed size a = 0 (no initial shock). Verify that NO cascade produces systemic failure — fear alone cannot ignite.

**Assertion:** With a=0, P(systemic) = 0.0 for all μ < 1.

### Group E: Halting condition

#### `test_f2_halting_waits_for_mark_expiry`
**Description:** Engineer a scenario where round t has 0 new failures but active marks exist on nodes. Verify the cascade does NOT halt and continues to round t+1, where mark-triggered failures may occur.

**Assertion:** Cascade continues past a quiet round when marks are active. Final failed count is larger than what premature halting would produce.

#### `test_f2_halting_after_marks_expire`
**Description:** Engineer a scenario where marks expire without triggering any failures. After marks expire and g_t = 0, the cascade should halt.

**Assertion:** Cascade halts exactly when all marks have expired and no new failures occurred.

### Group F: Interaction with D-006

#### `test_f2_window_invariance_with_marks`
**Description:** Re-run the D-006 invariance pilot with F2 marks enabled (m=1, r=2, k=2). Compare P(systemic) across X ∈ {1, 4, 8}. Check if invariance (within ±0.03) still holds.

**Assertion:** If invariance breaks, flag as a known interaction effect. If it holds, confirm the D-006 result extends to F2.

---

## Summary of Critical Risks

| Risk | Severity | Likelihood | Mitigation |
|---|---|---|---|
| μ=0 invariant broken by RNG stream shift | **High** | Medium | Preserve the `f_i·g_t > 0` guard before `rng.random()` |
| Halting rule misses mark-triggered failures | **Critical** | High | Generalize halt to require `a_t = 0 AND active_marks = 0 AND g_{t+1} = 0` |
| Mark timing off-by-one (same-round vs next-round) | **High** | High | Write explicit timing spec before coding; dedicated test |
| m ≥ r breaks subcritical amplifier claim | **High** | Low (parameter choice) | Document m < r as a requirement; test the boundary |
| Mark accumulation creates supercritical fear | **Medium** | Medium | Bound k; choose between additive/capped stacking; analyze R_fear with marks |
| D-006 invariance breaks with marks | **Medium** | Medium | Re-run the invariance pilot with marks enabled |
| k → ∞ reproduces rejected cumulative model D-005 | **High** | Low (parameter choice) | Explicitly disallow k = ∞ in the spec |
| Cross-language mark divergence | **Medium** | Medium | Add mark-mechanics cross-language check |

---

## Recommendation

> [!TIP]
> **The safest path for MVP is to DROP F2 (option (a) in §3.6), as already recommended by the tracker.** The D-006 window-length parameter provides a cleaner fear-persistence mechanism without touching the solvency threshold — and it preserves the subcritical amplifier property, the Janson μ=0 limit, and the analytical tractability of the mean-field threshold.
>
> If F2 is pursued as a separate model variant (option (b)), the implementer must:
> 1. Write the precise timing spec (§4 of this report) and get it reviewed BEFORE coding.
> 2. Fix the halting condition (§6).
> 3. Restrict parameters to m < r, finite k, to preserve the subcritical amplifier framing.
> 4. Re-derive the mean-field threshold with a heterogeneous effective-r distribution.
> 5. Pass all 14 proposed tests (§9).
> 6. Re-run the D-006 invariance pilot to check for interaction effects.
