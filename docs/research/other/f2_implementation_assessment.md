# F2 Implementation Assessment — Fear Marks Mechanism (m/k)

> **Author:** Python Simulation Agent (advisory assessment)
> **Date:** 2026-06-04
> **Status:** Advisory only — NO source files modified.
> **Context:** Fork F2 (§3.6 of PROJECT_TRACKER.md) proposes replacing direct fear failure with a "fear marks" mechanism.

---

## 1. Summary of the F2 Mechanism

Under the current §3.3 model, when a solvent bank's fear Bernoulli draw succeeds (`rng.random() < f_i * g_t`), the bank **fails immediately**. Under F2:

- Fear activation does **not** fail the bank directly.
- Instead, **m marks** are added to the bank, each lasting **k rounds**.
- Active marks count toward the solvency threshold: the failure condition becomes `failed_neighbor_count + active_marks >= r`.
- Marks decay: after k rounds, they expire and are removed.
- This **unifies the two channels** through the solvency threshold `r`, making fear a mechanism that *lowers the effective solvency buffer* rather than an independent failure channel.

---

## 2. Files That Would Change

### 2.1 `src/twocascade/reference.py` — PRIMARY CHANGES

This is the validated oracle and the file with the most extensive modifications.

#### 2.1.1 `Node` dataclass (lines 19–28)

**Current:**
```python
@dataclass
class Node:
    index: int
    individual_fear: float
    failed: bool = False
    failed_neighbor_count: int = 0
```

**Proposed addition** — a list tracking active marks with their expiry round:

```python
@dataclass
class Node:
    index: int
    individual_fear: float
    failed: bool = False
    failed_neighbor_count: int = 0
    marks: list = field(default_factory=list)  # list of expiry-round ints
```

**Design choice:** Each element in `marks` is the round number at which that mark expires. For example, if `m=2` marks are added at round `t=3` with lifetime `k=3`, the list gains entries `[6, 6]` (expire at end of round 6). A derived property `active_mark_count` simply returns `len(self.marks)`.

**Alternative (counter-based):** Instead of a list of expiry times, use a fixed-size deque or array of length `k` counting marks-expiring-per-round. This is more cache-friendly for large `k` but harder to reason about. **Recommendation: list of expiry times for the Python oracle** (readability per §5 style), counter-based for the C++ port.

#### 2.1.2 `run_cascade()` function (lines 42–153)

**Signature change:** Add two parameters `m` and `k`.

```diff
-def run_cascade(adjacency, nodes, r, seed_indices, rng, record_history) -> CascadeResult:
+def run_cascade(adjacency, nodes, r, seed_indices, rng, record_history,
+                marks_per_fear: int = 0, mark_lifetime: int = 1) -> CascadeResult:
```

> Using `marks_per_fear=0` as default keeps the current direct-failure behavior: when `marks_per_fear == 0`, fear activation fails the bank directly (the §3.3 rule). When `marks_per_fear > 0`, fear activation adds marks instead.

**Changes within the round loop (lines 93–153), walk-through:**

| Line region | Current behavior | F2 behavior | Notes |
|---|---|---|---|
| **L95** `global_fear = ...` | Unchanged | Unchanged | `g_t = a_{t-1}/n` uses `new_failed_last_round`, which still counts only *actual failures*, not mark activations. |
| **L102–117** STEP 1 — evaluation | Reads `failed_neighbor_count` for solvency check; fear Bernoulli triggers failure. | Solvency check becomes `node.failed_neighbor_count + len(node.marks) >= r`. Fear Bernoulli success **does not** immediately mark as failing — instead, it records a "pending marks" action. | Must separate "activated by fear" from "failing" — fear activation queues marks for next round. |
| **L107–109** Solvency channel | `effective_failed_neighbor_count >= r` | `node.failed_neighbor_count + len(node.marks) >= r` | Marks count toward threshold. |
| **L111–114** Fear channel | `fails_by_fear = Bernoulli(f_i * g_t)` → bank added to `newly_failing_nodes` | `fear_activated = Bernoulli(f_i * g_t)` → bank added to `pending_mark_recipients` (not `newly_failing_nodes`) | Fear no longer fails directly. |
| **L116–117** Failure decision | `if fails_by_solvency or fails_by_fear` | `if fails_by_solvency` (only solvency can fail a bank; fear contributes indirectly through marks) | Key conceptual change. |
| **L130–134** STEP 2 — apply | Applies failures, updates neighbor counters. | Also applies: (1) add pending marks to recipients; (2) expire old marks. Both in the apply step to respect simultaneous update. | Mark addition and expiry happen in the apply step. |
| **New STEP** Mark decay | N/A | After applying failures and new marks, **expire marks** whose expiry round is the current round. | Must track current round number. |
| **L138–139** Halt check | `new_failures_this_round == 0 → break` | `new_failures_this_round == 0 AND no pending marks AND no active marks on any node → break` | **Critical change**: marks can trigger future failures even with no new failures this round. A bank might gain marks this round and reach threshold *next* round. Must continue while any marks are active. |

**Detailed pseudo-code for the modified round loop:**

```python
round_number = 0
while new_failed_last_round > 0 or any_active_marks(nodes):
    round_number += 1
    global_fear = new_failed_last_round / n

    # STEP 1: EVALUATE (frozen snapshot)
    newly_failing_nodes = []
    pending_marks = []  # list of (node, expiry_round)

    for node in nodes:
        if node.failed:
            continue

        # Mark decay: count only non-expired marks
        active = sum(1 for exp in node.marks if exp > round_number)
        effective = node.failed_neighbor_count + active

        # Channel 1: solvency (augmented by marks)
        fails_by_solvency = effective >= r

        # Channel 2: fear → marks (not direct failure)
        fear_activated = (fear_prob > 0.0 and rng.random() < fear_prob)

        if fails_by_solvency:
            newly_failing_nodes.append(node)
        elif fear_activated and marks_per_fear > 0:
            # Don't add marks to a node that's about to fail
            pending_marks.append((node, round_number + mark_lifetime))

    # STEP 2: APPLY
    # 2a. Apply failures
    for node in newly_failing_nodes:
        node.failed = True
    for node in newly_failing_nodes:
        for neighbor_index in adjacency[node.index]:
            nodes[neighbor_index].failed_neighbor_count += 1

    # 2b. Apply pending marks (simultaneous — take effect next round)
    for node, expiry in pending_marks:
        if not node.failed:  # don't add marks to freshly failed nodes
            for _ in range(marks_per_fear):
                node.marks.append(expiry)

    # 2c. Expire old marks (clean up)
    for node in nodes:
        node.marks = [exp for exp in node.marks if exp > round_number]

    # Bookkeeping
    new_failures_this_round = len(newly_failing_nodes)
    total_failed += new_failures_this_round
    new_failed_last_round = new_failures_this_round
    ...
```

#### 2.1.3 `estimate_systemic_probability()` (lines 320–378)

**Signature change:** Add `marks_per_fear` and `mark_lifetime` parameters, pass through to `run_cascade()`.

```diff
-def estimate_systemic_probability(n, p, r, mean_fear, concentration, seed_size,
-                                  theta, trials, rng, target_high_degree) -> float:
+def estimate_systemic_probability(n, p, r, mean_fear, concentration, seed_size,
+                                  theta, trials, rng, target_high_degree,
+                                  marks_per_fear: int = 0,
+                                  mark_lifetime: int = 1) -> float:
```

### 2.2 `src/twocascade/model.py` — NEW CONTENT

Currently empty. Should be populated with a parameter dataclass:

```python
@dataclass
class CascadeParams:
    n: int
    p: float
    r: int
    mean_fear: float           # μ
    concentration: float       # κ
    seed_size: int             # a
    theta: float               # systemic threshold
    marks_per_fear: int = 0    # m (0 = direct failure mode, per §3.3)
    mark_lifetime: int = 1     # k (rounds marks last)
    window_len: int = 1        # X (D-006 window length)
    target_high_degree: bool = False
```

This consolidates all model parameters into a single validated object per §5.5's directive: "parameters in a single validated dataclass."

### 2.3 Other files in `src/twocascade/`

| File | Current state | F2 impact |
|---|---|---|
| `analysis.py` | Empty/stub | No immediate change for F2 |
| `meanfield.py` | Empty/stub | Would eventually need the modified mean-field map |
| `plotting.py` | Empty/stub | No change |
| `runner.py` | Empty/stub | Would need to support loading F2 params from config |
| `__init__.py` | Empty | No change |

### 2.4 Test files

| File | F2 impact |
|---|---|
| `tests/test_mu0_bootstrap_threshold.py` | **No change needed** (see §6 below) |
| `tests/test_f2_marks.py` (NEW) | New test file needed for mark-specific validation |

---

## 3. Node Dataclass Design — Detailed Proposal

### Option A: Expiry-time list (recommended for Python)

```python
@dataclass
class Node:
    index: int
    individual_fear: float
    failed: bool = False
    failed_neighbor_count: int = 0
    marks: list[int] = field(default_factory=list)  # each entry = round when mark expires

    @property
    def active_mark_count(self) -> int:
        """Number of currently active marks (caller must have pruned expired marks)."""
        return len(self.marks)
```

**Pros:** Simple, readable, easy to debug (inspect which rounds marks expire). Each fear activation appends `m` copies of `current_round + k` to the list.

**Cons:** O(total marks ever) memory per node. For realistic `m` and `k` values (m ≤ 3, k ≤ 5), this is negligible.

### Option B: Round-bucketed counter (recommended for C++)

```python
# Conceptual: marks_by_expiry[round] = count of marks expiring that round
marks_by_expiry: dict[int, int] = field(default_factory=dict)
```

**Pros:** O(k) storage, O(1) decay (delete the current-round key). Better for C++ (fixed array of length `k`, circular buffer).

**Cons:** Slightly less readable. Not worth the complexity for the Python oracle.

### Recommendation

Use **Option A** for `reference.py` (readability is the priority per §5). Document Option B as the intended C++ design in comments.

---

## 4. New Parameters and Their Interactions

### 4.1 Parameter definitions

| Parameter | Symbol | Type | Constraints | Default |
|---|---|---|---|---|
| `marks_per_fear` | m | int | m ≥ 0 | 0 (= direct failure, §3.3 mode) |
| `mark_lifetime` | k | int | k ≥ 1 | 1 |

### 4.2 Interactions with existing parameters

| Existing param | Interaction with m/k | Notes |
|---|---|---|
| **r** (threshold) | **Direct interaction.** Marks count toward the threshold. With m marks and k rounds of persistence, a single fear activation can contribute up to m toward the r threshold. If m ≥ r, a single fear activation instantly sets up the bank to fail next round (assuming simultaneous update). | Consider requiring m < r for non-degenerate behavior. |
| **μ** (mean fear) | **Indirect.** μ controls the rate of fear activations; m controls how much each activation contributes. Effective "fear pressure" scales as μ·m·k (roughly: each round, a surviving bank accumulates ~μ·g_t·m marks, persisting k rounds). | The μ < 1 subcriticality argument (§3.3's "R_fear ≈ μ") no longer applies in the same form. Under F2, fear doesn't reproduce directly but *erodes* solvency buffers. The analytical framework changes. |
| **κ** (concentration) | No direct interaction. Still controls heterogeneity of f_i. | |
| **window_len** (X) | Orthogonal. X controls the temporal smoothing of g_t; m/k control the effect *of* g_t. Both are persistence mechanisms but on different axes (field persistence vs. mark persistence). | Could study jointly, but for MVP keep X=1 and vary m/k. |

### 4.3 Sensible defaults for testing

| Scenario | m | k | Rationale |
|---|---|---|---|
| **Baseline (§3.3)** | 0 | — | Direct failure mode. m=0 means fear fails directly. |
| **Mild marks** | 1 | 2 | Each fear activation adds 1 mark lasting 2 rounds. Gentle perturbation from baseline. |
| **Moderate marks** | 1 | 3 | 1 mark lasting 3 rounds. At r=2, a bank with 1 mark needs only 1 failed neighbor to fail. |
| **Aggressive marks** | 2 | 3 | 2 marks per activation, lasting 3 rounds. At r=2, a single fear activation makes the bank fail if *any* neighbor has failed, and at r=3 needs just 1 more neighbor. |
| **Degenerate** | r | k | Single fear activation → instant failure next round (equivalent to direct failure with a 1-round delay). Avoid. |

### 4.4 Key analytical difference from §3.3

Under §3.3: `R_fear ≈ μ` (subcritical amplifier — each failure causes ~μ new fear-failures next round).

Under F2: Fear doesn't produce failures directly. Instead, it produces marks that *lower the barrier* for solvency failures. The reproduction number becomes a complex function of the mark accumulation rate (μ·m·g_t), mark lifetime (k), network structure, and the solvency threshold (r). **The clean R_fear ≈ μ < 1 subcriticality result (§3.3's central structural fact) does NOT carry over.** This is the primary theoretical cost of F2 and should be a factor in the decision to adopt it.

---

## 5. Baseline Config File

```json
{
    "_comment": "F2 fear-marks baseline experiment",
    "_model_variant": "marks",
    "_created": "2026-06-04",

    "network": {
        "n": 4000,
        "p_scaling": {
            "alpha": 0.7,
            "beta_ref_n": 4000,
            "target_mean_degree": 10.0
        }
    },

    "solvency": {
        "r": 2
    },

    "fear": {
        "mean_fear": 0.3,
        "concentration": 50.0,
        "marks_per_fear": 1,
        "mark_lifetime": 2
    },

    "seed": {
        "seed_size_multiples_of_ac": [0.5, 0.7, 0.85, 1.0, 1.15, 1.3, 1.6, 2.0],
        "target_high_degree": false
    },

    "simulation": {
        "trials": 200,
        "theta": 0.5,
        "base_seed": 20260604,
        "record_history": false
    },

    "sweep": {
        "axis": "mean_fear",
        "values": [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    }
}
```

This config should be saved to `configs/f2_marks_baseline.json`.

A comparison config (`configs/f2_marks_comparison.json`) sweeping over `marks_per_fear ∈ {0, 1, 2}` and `mark_lifetime ∈ {1, 2, 3, 5}` at fixed μ would also be needed.

---

## 6. μ=0 Invariance Analysis

**Claim: At μ=0, the marks mechanism is completely inert. The existing test suite passes unchanged.**

**Proof sketch:**

1. When `mean_fear = 0.0`, `sample_individual_fears()` returns `[0.0] * n` (line 270 of reference.py).
2. Every node has `individual_fear = 0.0`.
3. The fear probability is `f_i * g_t = 0.0 * g_t = 0.0` for every node, every round.
4. The guard `fear_failure_probability > 0.0 and rng.random() < ...` (line 114) short-circuits to `False`.
5. No fear activation ever occurs → no marks are ever generated → `node.marks` stays `[]` for all nodes.
6. `active_mark_count = 0` for all nodes, all rounds.
7. The solvency check `failed_neighbor_count + 0 >= r` is identical to `failed_neighbor_count >= r`.
8. The halting condition change (checking for active marks) is also inert: no marks → extra condition is always False → loop terminates identically.
9. **No RNG draws are consumed** by the marks mechanism at μ=0 (the Bernoulli guard fires before `rng.random()`), so the RNG stream is identical.

**Conclusion:** At μ=0, the F2 engine produces bit-identical results to the current engine. All four tests in `test_mu0_bootstrap_threshold.py` will pass without modification:

- `test_mu0_run_is_reproducible` ✅
- `test_deep_subcritical_stays_small` ✅
- `test_deep_supercritical_percolates` ✅
- `test_empirical_threshold_matches_a_c` ✅

**Important caveat:** The test file calls `run_cascade()` without `marks_per_fear` or `mark_lifetime` arguments. With defaults of `marks_per_fear=0` (direct failure mode), the function behaves identically to the current implementation regardless of μ. Even with `marks_per_fear > 0`, μ=0 makes the mechanism inert.

---

## 7. Estimated Complexity

### Rating: **MEDIUM**

### Breakdown

| Dimension | Estimate | Detail |
|---|---|---|
| **Lines of code** (reference.py) | ~50–80 net new/modified | Node dataclass (+3 lines), run_cascade rewrite (~40 lines changed in the round loop), signature changes (~10 lines), mark utilities (~10 lines). |
| **Lines of code** (model.py) | ~30 new | Parameter dataclass with validation. |
| **Lines of code** (new tests) | ~100–150 new | Mark decay correctness, threshold interaction, μ=0 invariance, simultaneous update for marks, degenerate cases. |
| **Config files** | 1–2 new | Baseline + comparison sweep. |
| **New edge cases** | 5–8 | See §8 (Risks) below. |
| **Testing burden** | Moderate | Need hand-constructed graph tests to verify mark decay timing, threshold arithmetic, and simultaneous update. Monte Carlo comparison of F2 vs §3.3 behavior. |
| **C++ port impact** | Moderate | The mark data structure needs efficient representation (fixed-size circular buffer or per-round counter array). The halting condition change adds a scan. The apply step now has mark logic. Overall adds ~50–80 lines to the C++ engine too. |
| **Analytical impact** | **High** | The R_fear ≈ μ subcriticality analysis (§3.3 key structural fact) does not apply. Mean-field analysis would need a different framework — marks create a *delayed*, *threshold-mediated* interaction rather than a direct failure. This is the biggest cost. |

### Why "Medium" not "Small"

- The round loop changes are **not** a simple addition — they restructure the evaluation logic (separating "fear activated" from "failing"), add a new apply sub-step, and change the halting condition.
- The simultaneous-update invariant (§3.4) must be carefully maintained for marks: marks generated this round must not affect *this* round's solvency evaluation.
- The halting condition change is subtle and must be proven correct.
- Testing requires hand-constructed scenarios, not just Monte Carlo.

### Why "Medium" not "Large"

- No new data structures beyond a list field on Node.
- No changes to graph generation, fear distribution, or seed selection.
- The parameter space grows by only 2 dimensions (m, k) — manageable.
- μ=0 invariance is clean (no conditional logic needed in the test).

---

## 8. Risks and Implementation Pitfalls

### 8.1 Off-by-one in mark expiry

**Risk:** Marks expire one round too early or too late.

**Example:** Mark added at round t=3 with k=3. Should it be active at rounds 3, 4, 5 (3 rounds)? Or 4, 5, 6 (if simultaneous update delays activation by one round)? The answer depends on whether we count the activation round.

**Recommendation:** Define precisely: a mark added during round t's apply step (STEP 2) first appears in round t+1's evaluation (simultaneous update), and expires *after* round t+k's evaluation. So `expiry = t + k`, and the mark is active when `expiry > current_round` (evaluated at the *start* of the evaluation step, before incrementing the round counter).

**Test:** Hand-constructed graph, single node, m=1, k=2. Verify the mark is active for exactly 2 evaluation rounds.

### 8.2 Simultaneous update violation for marks

**Risk:** If marks are added to `node.marks` during STEP 1 (evaluation), they could affect *this round's* solvency check for the same node (if evaluated after the mark was added).

**Mitigation:** Use a separate `pending_marks` list in STEP 1; apply all marks in STEP 2. This mirrors the existing `newly_failing_nodes` pattern. The pseudo-code in §2.1.2 follows this pattern.

### 8.3 Marks on already-failed nodes

**Risk:** A node might receive fear marks in the same round it fails by solvency. These marks are wasted (failed nodes can't fail again), but if not handled, they could cause incorrect `active_mark_count` on a dead node — potentially confusing downstream analysis.

**Mitigation:** In STEP 2, check `if not node.failed` before applying pending marks. Also skip expired-mark cleanup for failed nodes (minor optimization, not correctness-critical).

### 8.4 Halting condition — false termination

**Risk:** Under the current code, the loop stops when `new_failed_last_round == 0`. With marks, this is **wrong**: a round might produce zero new failures but leave active marks on nodes. Those marks might tip a node over threshold next round (if a neighbor also fails), or marks might accumulate over multiple fear activations.

**More subtle risk:** Even if no marks are active, the `new_failed_last_round` being zero means `g_t+1 = 0`, which means no *new* fear activations, which means no new marks. So the halt is correct *if and only if* there are no active marks remaining.

**Mitigation:** Halt when `new_failed_last_round == 0 AND no active marks on any solvent node`. The marks-check adds an O(n) scan per round, which is acceptable.

**Even more subtle:** If marks are active but no new failures occurred, `g_t = 0` next round (since `new_failed_last_round = 0`), so no new marks can be generated. The only way existing marks cause failures is if `failed_neighbor_count + active_marks >= r` — but `failed_neighbor_count` didn't change this round (no new failures) and marks can only *decay*. So if marks didn't trigger a failure this round, they can't trigger one next round either (marks only decrease). **This means the halt condition can be simplified:** halt when `new_failures_this_round == 0 AND new_marks_this_round == 0`. If there were no failures and no new marks, the state is frozen and marks can only decay.

Wait — marks could have been applied *last* round (in the apply step) and only become visible *this* round. So the correct check is: halt when `new_failures_this_round == 0 AND no marks were applied last round`. Or more conservatively: halt when `new_failures_this_round == 0 AND no solvent node has active_marks > 0`.

**Recommendation:** Use the conservative O(n) check. Correctness over cleverness.

### 8.5 Interaction with the window-length extension (D-006)

**Risk:** The D-006 window-length parameter `X` generalizes `g_t` to a weighted sum over X past rounds. Combined with F2 marks (which persist k rounds), there are two independent persistence mechanisms. The halting condition becomes: halt when X consecutive rounds have no failures AND no active marks remain. Both conditions must be checked.

**Mitigation:** If F2 is adopted, implement it *before* the window-length extension. The window-length extension (slotted for Wk-9) builds on top of a stable engine.

### 8.6 Non-monotonic failure — false alarm

**Observation:** Under F2, could marks on a node expire, making the node's effective count drop *below* r, effectively "un-failing" a node? No — failure is absorbing (§3.1). Once failed, always failed. Marks only affect solvent nodes' threshold evaluation. But mark expiry does mean a solvent node's effective count can *decrease* between rounds. This is fine — it just means the node survived the pressure window.

### 8.7 RNG stream deviation for μ > 0

**Risk:** Under §3.3 at μ > 0, fear-activated nodes are immediately failed, removing them from future rounds. Under F2, they receive marks but stay solvent, meaning they're evaluated in future rounds (consuming more RNG draws for fear Bernoulli checks). This changes the RNG stream, making direct comparison between §3.3 and F2 results at the same seed impossible.

**Mitigation:** This is expected and acceptable. Compare §3.3 vs F2 statistically over many trials, not per-seed. At μ=0, both produce identical RNG streams (§6 above).

### 8.8 Impact on the C++ port (Wk 3–4)

**Risk:** If F2 is decided *after* the C++ port begins, the port must be reworked. If decided before, the C++ port is moderately more complex (mark data structure, modified halting, mark apply/decay in the hot loop).

**Recommendation:** Resolve F2 before starting the C++ port. The §10 action list already has "Resolve F2" as action #1.

---

## 9. Reporting Contract

### Files Changed
- `src/twocascade/reference.py` — Node dataclass, run_cascade() signature + round loop, estimate_systemic_probability() signature (WOULD change; no edits made)
- `src/twocascade/model.py` — new CascadeParams dataclass (WOULD be created; no edits made)

### Configs Generated
- `configs/f2_marks_baseline.json` — drafted in §5 above (NOT written to disk)
- `configs/f2_marks_comparison.json` — described but not drafted (NOT written to disk)

### Validation Status
- μ=0 invariance: **CONFIRMED** by analysis (§6). No test changes needed.
- Existing test suite (`test_mu0_bootstrap_threshold.py`): **WILL PASS** unchanged under F2 implementation, given default `marks_per_fear=0` or any value at μ=0.
- New tests needed: mark decay correctness, threshold arithmetic with marks, simultaneous update for marks, halting condition with active marks, degenerate cases (m ≥ r).

### Decisions to Log
- **No decisions made** — this is advisory only. The following decision is recommended:
  - **Proposed D-008:** "Assess F2 implementation lift as MEDIUM. If F2 is adopted, implement in reference.py before the C++ port. Key trade-off: F2 breaks the clean R_fear ≈ μ subcriticality result (§3.3's central structural fact), requiring new analytical treatment. Recommend either (a) dropping F2 for the MVP per §3.6's recommendation, or (b) treating F2 as a separate model variant with its own analytical framework."

---

## 10. Recommendation

The F2 marks mechanism is **implementable at medium effort** (~50–80 lines in reference.py, ~100–150 lines of new tests, 1–2 config files). The μ=0 invariance is clean. The main costs are:

1. **Analytical:** The R_fear ≈ μ subcriticality result — the project's "most important consequence" (§3.3) — does not carry over. The mean-field analysis would need reworking.
2. **Complexity:** The round loop becomes more complex (3-phase apply instead of 1-phase), and the halting condition needs careful treatment.
3. **C++ port:** Moderate additional complexity in the hot loop.

**Given that the D-006 window-length family already provides a fear-persistence handle** (and the pilot shows P(systemic) invariant in X — a clean result), and that the project's analytical path targets extending Janson's theorems (which is easier with the direct-failure R_fear ≈ μ structure), **the recommendation aligns with §3.6's existing recommendation: drop F2 for the MVP** and optionally revisit as a separate model variant in Wk-8 or later.

If F2 *is* adopted, implement it in reference.py first, validate with hand-constructed tests, then port to C++. Do not attempt both simultaneously.
