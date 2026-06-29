# implementation_plan.md — Interactive cascade visualization

## Parity scope (made explicit per AGENTS.md §IV)
**N/A — out of scope by construction.** This is a standalone illustrative web
demo. It does **not** touch the C++ engine, the Python reference oracle, or any
results artifact. There is therefore no Python↔C++ parity work this session, and
no cross-validation (§5.4) is required or claimed. The JS engine is a *third,
explicitly-illustrative* engine, labeled as such; it is deliberately **not**
cross-validated against the oracle (doing so would be Option B/C, not chosen).

## Files (all new)
```
viz/
├── index.html      # layout: graph canvas + sliders + live panel + legend + banner
├── cascade.js      # RNG, Beta sampler, §3.4 engine, trace precompute, animation
├── style.css       # styling
└── README.md       # "illustrative, NOT the validated engine" disclaimer + run notes
.github/workflows/pages.yml   # deploy viz/ to GitHub Pages (Actions source)
task.md / implementation_plan.md   # this session's mandated artifacts
```
Nothing under `src/`, `cpp/src/`, `results/`, or the oracle is modified → no
worktree isolation needed (AGENTS.md §III: standalone new files edited in place).

## cascade.js design
- **RNG:** seeded `mulberry32` — reproducible from the seed field.
- **Graph:** $G(n,p)$ by sampling each unordered pair w.p. $p$ ($O(n^2)$, fine at
  $n \le 150$); adjacency lists.
- **Fear:** `sampleBeta(α,β)` = `Gamma(α)/(Gamma(α)+Gamma(β))` with Marsaglia–Tsang
  Gamma (Box–Muller normal). Guards: `α<=0 → 0`, `β<=0 → 1` (covers μ=0, μ=1).
- **Engine `runCascade(params)`** returns the full trace:
  - seed `a` random banks at `t=0` (channel = seed); init failed-neighbor counters.
  - each round, compute `g = prevNew/n`; evaluate every solvent bank against
    **frozen** counters: `count >= r → solvency`, else `rand < f_i*g → fear`;
    collect new failures; **then** mutate (set failed, bump neighbor counters).
  - halt when no new failures. Record per-round `{t, newNodes:[{node,channel}], g,
    a_t, A}` and per-node `failRound` / `failChannel`.
- **Animation:** precompute trace, reveal one round per tick; Play/Step/Reset.
- **Re-run on parameter change** (slider `change` event) → rebuild + reset.

## index.html / UI
- vis-network **vendored locally** (`viz/vendor/`, no CDN, no build step) — a CDN
  dependency left the page blank on `file://`/offline opens; vendoring fixed it.
  Nodes colored by current revealed channel via `{background, border}`.
- Sliders: `r∈{2,3,4}`, `μ∈[0,1]`, `κ∈[0.5,200]`, `a∈[1,30]`, `p∈[0,0.3]`,
  `n∈[30,150]`, each with a tooltip giving symbol → §3 meaning + units.
- Live panel: round, `g_t` thermometer (scaled to run-max for visibility) + value,
  `a_t`, `A(t)/n`, systemic flag at θ=0.5.
- Legend for the four colors; prominent illustrative-scope banner.

## Hosting
`.github/workflows/pages.yml` publishes `viz/` via the GitHub Pages **Actions**
source (uploads `viz/` as the Pages artifact). Triggers on push to `main` /
`antigravity` touching `viz/**`, plus `workflow_dispatch`. Gary enables Pages
(source = GitHub Actions) in repo settings; the deploy URL appears in the run.

## Verification (proportional — illustrative demo, not a result)
- Open locally and confirm: a supercritical setting percolates; `μ=0` shows **no**
  fear-colored nodes (pure Janson) and the $g_t$ thermometer plays no role; raising
  `μ` adds fear-colored failures that amplify but do not self-ignite (thermometer
  spikes then decays). Sliders re-run; seed reproduces.
- No automated test suite added (no engine/oracle change). The §5.4/§5.6 gate does
  not apply — explicitly recorded in walkthrough notes.

## Steps
1. task.md + implementation_plan.md (done).
2. `viz/cascade.js` → `viz/index.html` → `viz/style.css` → `viz/README.md`.
3. `.github/workflows/pages.yml`.
4. Open locally, sanity-check the animation, iterate.
