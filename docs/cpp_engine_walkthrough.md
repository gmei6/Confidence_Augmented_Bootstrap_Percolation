# C++ Engine Walkthrough

> A guided tour of `cpp/` for someone who knows the model (§3 of the tracker) and Python well, but is new to C++.
> Goal: after one focused session you can trace a cascade round by hand, explain the CSR layout, the seeding scheme,
> and the halting rule — and debug Week-5 analytics-vs-simulation disagreements against this code instead of around it.
>
> Written 2026-06-12 against the code as of Session 22 (25/25 tests passing). Line numbers refer to current files.

---

## 0. The map

Seven files, three layers (this is decision D-003: library core + thin CLI):

```
cpp/
├── CMakeLists.txt                      # build recipe: lib + CLI + tests
├── include/twocascade/
│   ├── graph.hpp     (header-only)    # CSR struct + Batagelj–Brandes G(n,p) + file loader
│   ├── rng.hpp       (header-only)    # seeding contract + Beta(α,β) fear sampler
│   └── engine.hpp                     # contracts: CascadeResult, CascadeBuffers, run_cascade decl
├── src/
│   ├── engine.cpp                     # THE cascade loop (only .cpp in the library)
│   └── main.cpp                       # CLI wrapper: arg parsing, two run modes, OpenMP loop
└── tests/test_engine.cpp              # 4 suites, hand-traceable cases
```

**Data flow per trial (Mode B):** `make_seeded_rng(base_seed, t)` → `sample_gnp_adjacency` →
`choose_random_seed` → `sample_individual_fears` → `run_cascade` → one line of
`failed_fraction rounds_completed` on stdout, which `runner.py::run_single_cell_cpp` parses.

**Reading order** (≈2.5–4 h total): §1 graph.hpp (30 min) → §2 rng.hpp (30 min) → §3 engine.hpp (15 min) →
§4 engine.cpp (60–90 min, the core) → §5 main.cpp (30 min) → §6 tests (20 min) → §7 CMake (15 min).
Skim §8 (idioms) first if raw C++ syntax is slowing you down; end with the §10 comprehension checks.

### Build & poke (do this first)

```bash
cd cpp
cmake -B build -DCMAKE_BUILD_TYPE=Release   # configure (once)

# Mac users should also add "-DCMAKE_OSX_ARCHITECTURES=arm64", so 
cpp % cmake -B build_learn -DCMAKE_BUILD_TYPE=Release -DCMAKE_OSX_ARCHITECTURES=arm64


cmake --build build                          # compile → build/twocascade_run, build/test_engine
ctest --test-dir build                       # or: ./build/test_engine  (prints per-suite progress)

# A real run you can play with (near Week-2 territory):
./build/twocascade_run --n 1000 --p 0.01 --r 2 --mu 0.3 --kappa 50 \
    --seed-size 10 --trials 100 --base-seed 42
# → 100 lines of "final_failed_fraction rounds_completed"
```

---

## 1. `graph.hpp` — CSR layout + Batagelj–Brandes sampling

Header-only (every function is `inline` — see §8 on why headers need that). Three pieces.

### 1.1 The CSRGraph struct (lines 13–17)

```cpp
struct CSRGraph {
    int n;
    std::vector<int> row_offsets;     // length n+1
    std::vector<int> column_indices;  // length = 2·(#edges), since undirected edges appear twice
};
```

**The one invariant to memorize:** the neighbors of node `v` are
`column_indices[row_offsets[v] .. row_offsets[v+1])` (half-open). `row_offsets[n]` == total entries.
This is exactly `scipy.sparse.csr_matrix`'s `indptr`/`indices` pair. Two flat arrays instead of a
`vector<vector<int>>` means neighbor iteration walks contiguous memory — the cache-locality point in §5.5
of the tracker. Every neighbor loop in the engine is the same four lines:

```cpp
int start = graph.row_offsets[idx];
int end   = graph.row_offsets[idx + 1];
for (int j = start; j < end; ++j) { int neighbor = graph.column_indices[j]; ... }
```

`convert_to_csr` (19–38) flattens a temporary `vector<vector<int>>` adjacency into this form. Build-side
code uses the nested vector (easy to append to), then converts once — the "acceptable first cut → CSR
optimization" path from tracker §5.5, both in one function.

### 1.2 `sample_gnp_adjacency` (40–106) — Batagelj–Brandes skip-sampling

The naive G(n,p) sampler flips n(n−1)/2 coins. Batagelj–Brandes instead asks "how many non-edges until
the next edge?" — a geometric random variable — and jumps straight there, giving O(n + edges) (tracker §5.2).

The state is a linearized walk over the **lower triangle** (pairs with `column < row`):

- Line 78: `jump = log(1−u) / log(1−p)` — inverse-CDF sampling of Geometric(p). Compare: numpy's
  `rng.geometric`. The `one_minus_u` epsilon guard (73–76) prevents `log(0)` when `u` draws exactly 1.0.
- Lines 80–84: clamp the jump before the `double → int` cast. Casting a too-large double to int is
  **undefined behavior** in C++ (not a Python-style soft overflow) — this is a UBSan-motivated guard (D-017/D-018 era).
- Lines 89–92: the wrap. `column` overflowing the current row's width spills into the next row:
  `while (column >= row) { column -= row; row += 1; }`.
- Lines 94–97: record the edge **in both directions** (undirected).

Edge cases short-circuit before any of this: `p==0` → empty graph (49–51); `p==1` → complete graph (53–63).

Line 101–103: neighbor lists are **sorted** before CSR conversion. The comment is worth reading: this is
for a *canonical, deterministic layout* — `reference.py` does not sort, and the engine is order-independent,
so this is about reproducible memory layout, not correctness.

### 1.3 `load_graph_from_file` (108–146) — the Prong-A door

Reads the dump format Python writes for cross-validation (§5.4): header `n m`, then `m` lines of `u v`.
Validates index ranges and **rejects self-loops**; sorts and converts like the sampler. This is how "load
*the same graph* in C++" from the tracker's cross-language validation is implemented. The artifacts in
`results/raw/xval*/` (graph.txt / seed.txt / failed.txt) are this pipeline's inputs and outputs.

---

## 2. `rng.hpp` — the seeding contract + Beta sampling

### 2.1 Why not just `mt19937_64(base_seed + trial)`? (lines 15–55)

Two problems with naive seeding, both solved here:

1. **Collisions across cells:** `(base_seed=42, trial=1)` and `(base_seed=43, trial=0)` would be the same
   stream under raw addition. Fix: hash `base_seed` through **SplitMix64** (15–27, a standard 64-bit
   finalizer — three xor-shift-multiply rounds) *before* adding `trial_index` (line 45). Now
   `hash(42)+1 ≠ hash(43)+0`. There is a regression test pinning exactly this pair (test_engine.cpp:51–62).
2. **Poor initialization:** a Mersenne Twister has 2.5 KB of internal state; seeding it from one 64-bit
   value initializes it weakly, and *similar* seeds give *correlated* early output. Fix: a second SplitMix64
   expands the combined seed into 512 bits (16 × 32-bit words, lines 47–52) fed through `std::seed_seq`.

`make_seeded_rng(base_seed, trial_index)` is the tracker §5.4 requirement made concrete: *"seed each
realization as a deterministic function of (base_seed, realization_index) so parallel runs stay reproducible
and order-independent."* Every trial owns its stream from birth; OpenMP scheduling order cannot matter.

### 2.2 `sample_individual_fears` (67–104) — Beta(μκ, (1−μ)κ) by hand

`<random>` has no beta distribution, so it uses the standard identity: if X ~ Gamma(α,1) and Y ~ Gamma(β,1)
independently, then **X/(X+Y) ~ Beta(α,β)** (lines 89–101). numpy does the same internally.

Three guards, each mapping to a tracker fact (F3 / D-002):

- `μ == 0` → all fears exactly 0.0, **no RNG consumed** (78–80). This preserves the "μ=0 is the deterministic
  Janson baseline" property — load-bearing for Prong A (§4.3 below).
- `μ == 1` → all 1.0 (81–84). Point mass, the κ→∞-style degenerate edge.
- `x + y == 0.0` underflow (96–99): for tiny κ both gamma shapes are ≪1 and both draws can underflow to 0.
  Fallback: Bernoulli(μ) on {0,1} — which is *exactly the κ→0 limit of the Beta* (the tracker's "two-point at
  {0,1}" limit in F3). The fallback isn't a hack; it's the correct asymptotic. Pinned by the κ=1e−25 test.

---

## 3. `engine.hpp` — the contracts

Three declarations; read the doc-comments, they are the spec.

**`CascadeResult` (13–18)** mirrors `twocascade.reference.CascadeResult` field-for-field:
`final_failed_fraction` (|A*|/n), `total_failed` (|A*|), `rounds_completed`, `history`. Convention:
**`history[0]` is the post-seed count** (cumulative, starts at |seed|, not 0).

**`CascadeBuffers` (24–43)** — the no-reallocation trick, and the unit of thread ownership:

```cpp
std::vector<uint8_t> failed;             // 0/1 status (uint8_t, NOT bool — see §8)
std::vector<int> failed_neighbor_count;  // the §5.2 per-node counter
std::vector<int> solvent_nodes;          // shrinking active list
std::vector<int> newly_failing_nodes;    // per-round scratch
```

`reset(n)` uses `assign`/`resize`, which reuse the heap allocation already owned by the vector (capacity is
kept; only the *size* changes). Across thousands of trials per cell, this turns per-trial allocation churn
into ~zero. One `CascadeBuffers` per thread = the "no shared mutable state in the parallel realization loop"
rule from §5.5.

**`run_cascade(...)` (67–77)** — note *how* things are passed: `graph` by `const&` (never copied — §5.5),
`rng` and `buffers` by mutable reference (both are consumed/scribbled on), scalars by value. The weights
contract is in the comment: empty ⇒ uniform 1/X; otherwise length == window_len, non-negative, sum to 1
within 1e-9, validated inside.

---

## 4. `engine.cpp` — the cascade loop, line by line

The only translation unit in the library. This is §3.3–§3.4 of the tracker as code. Structure:

```
validation (16–42) → seeding (44–79) → window init (87–99) → loop { full-collapse check (103) →
fear field (109–116) → evaluate (118–132) → update (134–146) → window shift (150–158) →
halting check (160–172) → bookkeeping (174–185) } → result (188–192)
```

### 4.1 Setup

- **Weights validation (16–37):** empty → uniform `1/window_len`; else length/sign/sum checks. Throws
  `std::invalid_argument` (≈ Python `raise ValueError`).
- **Seeding (45–79):** mark seeds failed; then for each seed, bump `failed_neighbor_count` on every
  neighbor — the counter design from §5.2: *counters are only ever updated when a node fails*, so each edge
  is touched at most twice over the whole cascade ⇒ O(edges) for the solvency channel. Then rebuild the
  solvent list and recount `total_failed` from the array (the recount, not `seed_indices.size()`, is what
  tolerates duplicate seed indices — but see Sharp edge #1).
- **Window init (87–91):** `failures_per_round` starts as `[a₀]` where `a₀ = |seed|`. This vector **is** the
  memory window of D-006/D-010 — `g_t` will be read off it. For the default X=1 it just holds last round's count.

### 4.2 The loop invariant

```cpp
while (is_any_positive(failures_per_round)) {
    if (total_failed == n) break;        // full collapse: nothing left to fail
```

Why is "window has any nonzero entry" the right *continue* condition? Because it's exactly "either channel
could still fire": solvency can only newly trigger in a round directly after counters changed (i.e., after a
round with failures), and fear fires with probability `f_i · g_t`, which is nonzero iff the window has mass.
Window all-zero ⇒ both channels dead ⇒ genuine absorbing state (§3.4, generalized to X by D-006's
"X consecutive quiet rounds").

### 4.3 Fear field (109–116)

$g_t = \frac{1}{n}\sum_{k=1}^{X} w_k\, a_{t-k}$, computed as:

```cpp
for (int k = 1; k <= window_len; ++k)
    if (k <= failures_per_round.size())
        global_fear += weights_to_use[k-1] * failures_per_round[size() - k];
global_fear /= n;
```

Indexing: `failures_per_round[size()−k]` is $a_{t-k}$ (the window stores oldest→newest, so the most recent
round is at the back and gets $w_1$). The `k <= size()` guard handles early rounds when fewer than X rounds
exist: missing terms contribute **zero, with no renormalization** — equivalent to defining $a_t = 0$ for
$t < 0$ (zero-padded history). Deliberate, and invisible at X=1.

Round 1 sanity check against §3.3: window is `[a₀]`, so $g_1 = a/n$ — "fear essentially off for any
sub-linear seed," exactly as the tracker says.

### 4.4 Evaluation phase (118–132) — the most load-bearing lines in the repo

```cpp
for (int idx : buffers.solvent_nodes) {
    bool fails_by_solvency = buffers.failed_neighbor_count[idx] >= r;          // Channel 1 (§3.2)
    double fear_failure_probability = individual_fears[idx] * global_fear;      // f_i · g_t
    bool fails_by_fear = (fear_failure_probability > 0.0 &&
                          u_dist(rng) < fear_failure_probability);              // Channel 2 (§3.3)
    if (fails_by_solvency || fails_by_fear) buffers.newly_failing_nodes.push_back(idx);
}
```

Two deliberate asymmetries in RNG consumption:

1. The fear Bernoulli **is drawn even when the node already fails by solvency** (no short-circuit between
   channels — `fails_by_solvency` is computed first but doesn't gate the draw). Uniform consumption pattern,
   independent of solvency outcomes.
2. The fear draw is **skipped entirely when `f_i · g_t == 0`** (the `> 0.0 &&` short-circuit). Consequence:
   at μ=0 every `f_i` is 0.0, so the engine consumes **zero** random numbers during the cascade — the run is
   fully determined by graph + seed set. That is precisely what makes the §5.4 **Prong A** test possible:
   dump a graph from Python, run both engines on it at μ=0, demand *identical* failed sets despite
   numpy/PCG64 and mt19937_64 having unrelated streams.

Failure is decided from `failed_neighbor_count` and `g_t` **as they stood at the start of the round** —
nobody marked failed mid-scan can influence anyone else this round.

### 4.5 Update phase (134–146) — simultaneity made concrete

Only after the full scan: mark `newly_failing_nodes` failed, then push their counter increments to neighbors.
Collect-then-commit **is** §3.4's "each round, simultaneously." (Counters of already-failed neighbors get
incremented too — harmless, they're out of `solvent_nodes` and never re-read.)

### 4.6 Window shift + halting (150–172)

The window is a fixed-size vector emulating a deque (the "circular-buffer deque emulation" of D-017):
while growing, append (157); once at size X, shift-left by one and overwrite the back (151–155) — O(X) with
X ≤ ~8, cheaper than a real `std::deque`'s allocation behavior.

The halting check fires only when the window is **full** and **all-zero** → `break` *before* the bookkeeping
block (174–178). Consequences worth internalizing:

- `new_failures` is 0 whenever the break fires, so `total_failed` is unaffected — but `rounds_completed`
  is **not** incremented for that final quiet round, and `history` doesn't get a new entry for it.
- For X=1: a round with 0 new failures halts immediately, uncounted ⇒ `rounds_completed` = number of rounds
  with ≥1 failure. (Test Case 1: single seed that ignites nothing → `rounds_completed == 0`.)
- For X>1: *intermediate* quiet rounds (window not yet all-zero) **are** counted — see test Case 4, where the
  window goes `[1] → [1,0] → [0,0]` and `rounds_completed` ends at 1, history `{1, 1}`.
- The window must be full before the all-zero check can fire; during the growing phase the loop-top
  `is_any_positive` is the only guard (it would catch an all-zero growing window, e.g. an empty seed list).

### 4.7 Solvent-list compaction (180–185)

```cpp
buffers.solvent_nodes.erase(
    std::remove_if(begin, end, [&buffers](int i){ return buffers.failed[i] != 0; }),
    end);
```

The **erase–remove idiom** (§8): `remove_if` packs survivors to the front and returns the new logical end;
`erase` trims the tail. In-place, O(|solvent|), no allocation. Python equivalent:
`solvent = [i for i in solvent if not failed[i]]` — minus the new list. This keeps each round's evaluation
scan proportional to the *current* solvent count, not n.

---

## 5. `main.cpp` — the CLI (the E1 boundary, decision D-003)

The "thin wrapper": parse args → validate → run one of two modes → print. No science lives here.

### 5.1 Parsing & precedence (64–143)

Hand-rolled `argv` loop (82–102) — a deliberate zero-dependency choice. Flags map 1:1 to model parameters;
defaults: `kappa=50`, `window_len=1`, `trials=1`, `base_seed=0`. The precedence rules (D-017's "seed
parameter precedence") are hard errors, not silent picks: `--seed-file` and `--seed-size` are mutually
exclusive (105–108); `--dump-failed-set` demands exactly 1 trial plus both `--graph-file` and `--seed-file`.
Validation enforces the frozen spec at the door: `r >= 2` (§3.2's "use r ≥ 2"), `μ ∈ [0,1]`, `κ > 0`.
Everything is validated **before** any parallel region — see 5.3 for why that placement is load-bearing.

### 5.2 Mode A — `--dump-failed-set` (146–177): Prong A in the flesh

Load graph + seeds from files → one deterministic RNG `make_seeded_rng(base_seed, 0)` → one cascade →
print the **sorted failed set** to stdout. At μ=0 this is RNG-free after setup (§4.4), so Python and C++
must produce *identical* sets on the same graph. `tests/test_cpp_validation.py` drives this; the
`results/raw/xval*/` directories are its artifacts.

### 5.3 Mode B — the trial loop (179–237)

Setup: static graph/seeds are loaded **once** if files were given; otherwise each trial generates its own
G(n,p) and random seed set. Then:

```cpp
std::vector<CascadeBuffers> thread_buffers(max_threads);   // one buffer set per thread (205)
#pragma omp parallel                                        // (211)
{
    CascadeBuffers& buffers = thread_buffers[thread_id];    // private scratch — §5.5's no-shared-state
    #pragma omp for schedule(dynamic)                       // (219)
    for (int t = 0; t < trials; ++t) {
        std::mt19937_64 rng = make_seeded_rng(base_seed, t);   // per-trial stream (221)
        ...
        outcomes[t] = ...;                                     // distinct slot per trial — no race
    }
}
```

Five details worth owning:

- **Order-independence:** trial `t`'s stream depends only on `(base_seed, t)`, never on which thread runs it
  or in what order — `schedule(dynamic)` can shuffle work freely without touching reproducibility (§5.4).
- **`schedule(dynamic)`:** trial durations are wildly uneven near criticality (the bimodality — some runs die
  in 3 rounds, some consume the graph). Dynamic scheduling stops one unlucky thread from becoming the tail.
- **The exception note (208–210):** C++ exceptions cannot cross an OpenMP parallel boundary — a throw inside
  would `std::terminate` the process. Hence *all* validation happens before the pragma. This is why the
  engine's own throws are unreachable here: main pre-validates everything the engine checks.
- **The `run_graph` binding (225–229):** `const CSRGraph& run_graph = has_static_graph ? static_graph : generated_graph;`
  picks shared-static vs per-trial graph **without copying either**. `generated_graph` is declared *outside*
  the ternary so the reference never dangles (C++ lifetime rule a Python dev never had to think about).
- **RNG consumption order per trial** is fixed: graph → seed choice → fears → cascade draws, all from the one
  stream. Reordering any of these would silently change every μ>0 result for a given seed.

`choose_random_seed` (44–57) is a partial Fisher–Yates shuffle — sampling without replacement, the C++
analogue of `rng.choice(n, size=a, replace=False)` — sorted afterwards (canonical output, and never duplicates:
relevant for Sharp edge #1).

Output (240–254): one line per trial, `failed_fraction rounds_completed`, fixed 6 decimals, stdout or
`--output`. Note what's *absent*: no JSON, no config echo, no metadata. The C++ side stays dumb; provenance
(config, seeds, git hash per §5.4) is `runner.py`'s job.

### 5.4 The Python side of the handshake (`src/twocascade/runner.py`)

`run_single_cell_cpp` builds the exact flag list, derives the 64-bit `--base-seed` from a numpy
`SeedSequence`, pins **`OMP_NUM_THREADS=1`** per worker (parallelism lives at the Python process pool /
cell level per D-019 — C++ threading inside each cell would thrash), enforces a 600 s timeout, and parses
stdout expecting exactly `trials_per_cell` two-field lines. Malformed or short output is a hard
`RuntimeError`, never a silent partial result.

---

## 6. `tests/test_engine.cpp` — what is pinned down

**Why `TEST_ASSERT` instead of `assert`** (9–15): `assert` compiles to nothing under `NDEBUG`, which Release
builds define — the suite would vacuously pass. The macro prints file:line and exits 1 in every build type.

The four suites, and the regression each one guards:

- **`test_rng_seeding` (17–65):** same (seed, trial) ⇒ identical streams; different seed or trial ⇒ different
  streams; and the **(42,1) vs (43,0) collision** that existed under naive `base_seed + trial` addition (51–62).
- **`test_gnp_generator` (67–120):** p=0 and p=1 exactly; for random p: no self-loops, **strictly sorted
  duplicate-free rows**, and full symmetry (every (u,v) has its (v,u)).
- **`test_beta_generator` (122–161):** μ∈{0,1} point masses; sample mean within 0.02 of μ at n=10⁴; and the
  κ=1e−25 underflow path ⇒ all draws in {0,1} with ≈μ fraction of ones (the two-point limit, §2.2).
- **`test_cascade_engine` (163–231):** a 3-node path graph `0–1–2`, hand-traceable. Case 1: one seed, r=2,
  nothing spreads (`rounds_completed == 0`). Case 2: seeds {0,2}, node 1 has 2 failed neighbors → full
  collapse in 1 round. Case 3: same but X=2 — pins the `total_failed == n` early break. Case 4: one seed,
  X=2 — pins intermediate-quiet-round semantics (window `[1]→[1,0]→[0,0]`, `rounds_completed == 1`,
  history `{1,1}`). Cases 3–4 are the ones to re-read after §4.6.

What these do **not** cover: statistical behavior at scale (μ-sweeps, bimodality, threshold location). That
lives on the Python side — `tests/test_cpp_validation.py` (Prongs A & B) and the pytest suite. The C++ tests
pin *mechanics*; the Python tests pin *physics*.

---

## 7. `CMakeLists.txt` — the build, decoded

If you've only ever `pip install`-ed, read this as "the packaging metadata, except it also chooses compiler
flags." CMake **configures** (generates build scripts into `build/`), then **builds**.

- **Targets (56–69):** `twocascade_core` — the library, compiled from `engine.cpp` alone, with
  `include/` exported `PUBLIC` (anything linking the lib inherits the include path). `twocascade_run` and
  `test_engine` both just link the core. This is D-003's structure: a future pybind11 module would be a
  fourth target over the same core, no rewrite.
- **Build types (8–25):** default Release (`-O3`). Debug = `-O0 -g` + sanitizers, **per-platform** (D-018):
  ASan+UBSan on Linux, **UBSan only on macOS** — Apple Clang 17's ASan runtime deadlocks before `main()` on
  macOS 26.5 (re-entrant malloc during shadow-memory init; the comment block at 13–18 is the incident report).
  Full ASan coverage happens on Linux (PACE/CI).
- **Native tuning (27–42):** `-mcpu=native` on Apple arm64, `-march=native` elsewhere (D-017's per-arch
  dispatch), behind a `USE_NATIVE_MARCH` option (turn OFF on PACE — compute nodes may differ from the build
  node). Open §9 item: the `check_cxx_compiler_flag` probe for `-mcpu=native` currently fails on AppleClang 17,
  so local builds silently carry no native flag. Perf nicety, not correctness.
- **OpenMP (44–61):** *optional* — `find_package(OpenMP)` may fail and the build degrades to single-threaded
  (matters: `runner.py` pins OMP to 1 thread anyway). The Homebrew `libomp` hint block must precede
  `find_package` to have any effect (the comment records that a misplaced duplicate was removed in S-021).

---

## 8. C++ idioms in this codebase, for the Python-fluent

| You see | It means | Python intuition |
|---|---|---|
| `const CSRGraph& g` | read-only alias, no copy | like passing any object — but C++ *copies by default*; `&` opts out, `const` makes it read-only |
| `std::mt19937_64& rng` | mutable reference | the callee advances *your* RNG state, like passing `np.random.Generator` |
| `#ifndef / #define / #endif` guards | include-once protection | why double-`import` is safe in Python, done manually |
| `inline` on header functions | "duplicate definitions across .cpp files are one entity" | without it, two files including `graph.hpp` = linker error (ODR) |
| `static_cast<int>(x)` | explicit, checked-at-compile-time cast | `int(x)`, but visible and greppable |
| `std::vector<uint8_t> failed` | byte array for flags | `vector<bool>` is a packed-bitfield oddity (no real byte addressing); `uint8_t` keeps it a plain fast array |
| `v.assign(n, 0)` vs `v.resize(n)` vs `v.reserve(n)` | set contents / set size / pre-allocate **capacity** only | capacity ≠ size is the whole CascadeBuffers trick — `assign` reuses the old heap block |
| `[&buffers](int i) { ... }` | lambda capturing by reference | `lambda i: failed[i] != 0` with a closure |
| erase–remove idiom | in-place filter | `lst = [x for x in lst if keep(x)]`, without allocating |
| `throw std::invalid_argument(...)` | exception | `raise ValueError(...)` |
| `struct X { ... };` + `X{a, b, c}` | plain record + aggregate init | `dataclass` + positional constructor |
| `#pragma omp parallel` / `omp for` | compiler directive: thread team / split loop | closest: `multiprocessing.Pool`, but shared-memory threads |
| RAII (no `free`/`del` anywhere) | destructors release memory at scope exit | what `with` does for files, applied to *all* resources |

---

## 9. Sharp edges — read before debugging Week-5 disagreements

1. **Duplicate seed indices would corrupt counters.** Seeding bumps `failed_neighbor_count` once *per entry*
   of `seed_indices`; a duplicated index double-increments its neighbors (the `total_failed` recount is
   immune, the counters are not). No current caller can produce duplicates (`choose_random_seed` is
   without-replacement; Python-side dumps are sets) — but hand-written `seed.txt` files must keep entries unique.
2. **Early-round window weights are truncated, not renormalized** (§4.3). At X=1 invisible; at X>1 the first
   X−1 rounds see slightly less fear mass than the steady-state formula suggests. Matches the zero-padded-history
   reading of D-006; keep it in mind if early-round dynamics ever look "too quiet" in an X>1 study.
3. **`rounds_completed` does not count terminal quiet rounds** (§4.6). For X=1 it equals "rounds with ≥1
   failure." If you ever compare durations against a differently-conventioned implementation, reconcile
   conventions before declaring a bug. (The D-006 duration result — ≈13.5→31.5 rounds as X grows — used the
   reference engine's matching convention.)
4. **`history[0]` is the post-seed count**, not 0, and `history` is cumulative (mirrors `reference.py`).
5. **Fear draws are consumed for solvency-doomed nodes too, but never when `f_i·g_t == 0`** (§4.4). The
   second half is what makes μ=0 RNG-free and Prong A possible. If anyone "optimizes" the `> 0.0` guard away
   or short-circuits on solvency, cross-validation breaks silently — statistical results stay right, but
   determinism and stream-replay both change.
6. **Never expect bit-identical results across languages.** numpy PCG64 and `std::mt19937_64` share no
   stream; even the gamma samplers consume different counts of underlying uniforms. Cross-language truth is
   Prong A (μ=0 exact sets) + Prong B (μ>0 statistics within Monte-Carlo error) — exactly §5.4.
7. **`--base-seed` semantics differ between modes.** Mode B seeds trial `t` with `(base_seed, t)`; Mode A
   uses `(base_seed, 0)`. Re-running Mode B with the same base seed replays the *whole cell* exactly.
8. **The binary at `cpp/build/twocascade_run` is what `runner.py` invokes** (hardcoded `CPP_BIN`). If you
   rebuild into `build_debug/`, the sweeps won't see it — rebuild `build/` (Release) before timing anything.

---

## 10. Comprehension checks

Work these without looking, then check against §11. If all eight are comfortable, you own this code.

1. Node `v` sits in a CSR graph. Write the loop that visits its neighbors. What is `row_offsets[n]`?
2. Trace test Case 2 by hand (path `0–1–2`, seeds {0,2}, r=2, μ=0, X=1): give the per-round window contents,
   `total_failed`, `rounds_completed`, and `history`.
3. Why must `(base_seed=42, trial=1)` and `(base_seed=43, trial=0)` give different streams, and what in
   `make_seeded_rng` guarantees it?
4. At μ=0, how many random numbers does `run_cascade` consume, and which single sub-expression enforces that?
   What project-level test depends on it?
5. State the halting rule for general X. Why does the loop *also* need `is_any_positive` at the top when the
   all-zero check exists? When does a round not increment `rounds_completed`?
6. Why does `CascadeBuffers::reset` use `assign` instead of constructing fresh vectors? Where does each
   OpenMP thread get its buffers, and why is sharing one set across threads forbidden?
7. Why is every parameter validated *before* the `#pragma omp parallel` block rather than inside the engine call?
8. Why does the test suite define `TEST_ASSERT` instead of using `assert`?

## 11. Answers (compact)

1. `for (int j = row_offsets[v]; j < row_offsets[v+1]; ++j) use(column_indices[j]);` — `row_offsets[n]` is
   the total entry count (= 2·edges), the sentinel closing the last half-open range.
2. Post-seed: failed {0,2}, window `[2]`, total 2, history `[2]`. Round 1: node 1's counter is 2 ≥ r → fails;
   window → `[1]`, total 3, rounds 1, history `[2,3]`. Loop top: `total_failed == n` → break. Final: 3, 1, `[2,3]`.
3. Naive addition collides (42+1 = 43+0). The base seed is hashed through SplitMix64 *first*, so the streams
   are built from `hash(42)+1` vs `hash(43)+0` — unrelated values. Pinned at test_engine.cpp:51–62.
4. Zero. `fear_failure_probability > 0.0 && u_dist(rng) < ...` — the short-circuit skips the draw whenever
   `f_i·g_t == 0`, which at μ=0 is always. Prong A of §5.4 (identical failed sets on a shared graph) depends on it.
5. Halt when the last X rounds all produced zero failures ("window empty," D-006), checked only once the
   window is full; plus an immediate break on `total_failed == n`. `is_any_positive` covers the growing phase
   (window not yet full) and is the loop's formal invariant. The round that completes the all-zero window
   breaks *before* bookkeeping, so it is never counted.
6. `assign` keeps the vector's existing capacity — no reallocation across thousands of trials. Each thread
   indexes `thread_buffers[omp_get_thread_num()]`; sharing would be a data race on `failed` /
   `failed_neighbor_count` (and §5.5 forbids shared mutable state in the realization loop).
7. An exception escaping an OpenMP parallel region calls `std::terminate` — it cannot propagate across the
   boundary. Pre-validation makes the engine's throws unreachable in the parallel context.
8. Release builds define `NDEBUG`, which compiles `assert` away — the suite would pass vacuously. The custom
   macro survives all build types (and CMake's comment says exactly this).

---

## 12. Where this fits Week 5

When the mean-field overlay disagrees with the empirical boundary, the first triage question is "is the
engine doing §3 as written?" — and the answer now has addresses: the fear field is engine.cpp:109–116, the
two-channel OR is 122–132, simultaneity is 134–146, halting is 160–172. The second question, "is the
disagreement statistical?", is a `--trials` / seed question in main.cpp + runner.py. Only after both come
the analytics. That triage order is the practical payoff of this walkthrough.

