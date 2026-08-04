"""Dump per-phase cascade traces for the interactive poster demo (poster-demo/).

WHAT THIS IS
------------
The QR code on the poster resolves to `poster-demo/`, an 8-phase self-paced
storyboard. The browser never simulates anything: every cascade it animates is
precomputed HERE, by the Python reference oracle (`src/twocascade/reference.py`),
and dumped to `poster-demo/traces/*.json`. This script is the only producer of
those files.

`src/` is read-only for this script. It imports the reference engine, the
configuration-model / GIRG samplers, and the Janson scaling helpers; it never
modifies them and never re-implements the cascade rule.

Traces are page assets, not experiment results, so they live under
`poster-demo/traces/` rather than `results/raw/` (deliberate - see the task
brief). They still carry the runner's provenance stamps: config path, seeds, git
commit, timestamp.

PIPELINE (per phase)
--------------------
    configs/poster_demo_phase*.json
        -> build the graph (same code paths and RNG discipline as runner.py)
        -> draw fears, choose the seed set
        -> reference.run_cascade(..., track_nodes=all)   [D-026 diagnostic side-channel]
        -> reconstruct per-round newly-failed sets from tracked_failure_rounds
        -> derive each failure's CAUSE post-hoc (see below)
        -> layout + edge list + rounds -> trace JSON

RNG DISCIPLINE
--------------
runner.run_single_trial spawns ONE SeedSequence into four streams
(graph, pair, fear, cascade). The demo needs a finer split: phases 1-2 and 3-5
must reuse one graph while the fear level changes, and phase 7 must reuse one
graph while the trial changes. So the split here is two-part and explicit:

    graph_seed -> SeedSequence(graph_seed).spawn(2) -> rng_graph, rng_pair
    trial_seed -> SeedSequence(trial_seed).spawn(2) -> rng_fear, rng_casc

Same separation of concerns as the runner (graph structure, pairing, fears,
cascade coin-flips are four independent streams), just seeded from two roots
instead of one. Phases 1-6 set graph_seed == trial_seed in their configs; phase
7 holds graph_seed fixed and varies trial_seed. Because `choose_seed` draws from
rng_casc BEFORE any fear coin-flip is consumed, a mu-pair/triple sharing
(graph_seed, trial_seed) gets a bit-identical graph AND a bit-identical initial
shock - the ONLY difference on screen between phases 3, 4 and 5 is fear.

CAUSE DERIVATION (post-hoc, engine untouched)
---------------------------------------------
The engine records only WHEN a node failed, not WHY. Cause is recovered exactly,
without touching the engine, from the graph plus the per-round failure sets:

    a node failing in round t is STRUCTURAL iff its number of failed neighbours
    in the cumulative failed set through round t-1 is >= r, else FEAR.

That is not an approximation. `reference.run_cascade` evaluates every node
against the frozen start-of-round state, and `failed_neighbor_count` is bumped
only in the simultaneous apply step at the END of a round, so at the moment node
v is judged in round t its counter equals exactly the number of its adjacency
entries (with multiplicity) that lie in the cumulative failed set through round
t-1. Nodes with counter >= r fail by solvency regardless of their fear draw, so
labelling them "structural" matches the engine's own precedence.

Self-check, run automatically on every dump: at mean_fear == 0 every failure must
classify structural (fear probability is identically zero there). A single fear
classification at mu = 0 means the derivation is wrong. Verified on both mu = 0
traces (phase 1 ER, phase 3 power-law): 100% of failures classify structural.

DEMO-SCALE DEGREE MATCHING (--calibrate)
----------------------------------------
The three families set mean degree by different mechanisms (ER: a knob; CM:
emergent from tau/d_min minus erasure; GIRG: emergent from tau/w_min/alpha_g),
so "same average degree" has to be solved for, exactly as
scripts/calibrate_matched_degree.py and scripts/calibrate_girg_degree.py do at
production n. `--calibrate` reproduces that at demo scale (n = 300, 40
replicates, base_seed 20260804):

    configuration model (tau=2.5, d_min=2)  realised <k> = 4.0285 +/- 0.0502
    ER matched                              target_mean_degree = 4.041973 (n_ref=300,
                                            alpha=0.6) -> p = 0.01347324, (n-1)p = 4.0285
    GIRG matched                            w_min = 0.20556640625 -> <k> = 4.0647 +/- 0.1400

The GIRG match is APPROXIMATE: bisection stopped at |<k> - target| <= 0.05,
which is inside the 0.14 replicate standard error. That is adequate for a
demo picture and is not a production calibration; it was not validated on an
independent base_seed the way the n=10000 calibration was.

SEED SELECTION (--scan, evidence recorded here)
-----------------------------------------------
Seeds were not cherry-picked by eye. Each group was scanned over a fixed
candidate range against a criterion stated in code, and the pick is the first
candidate in scan order that satisfies it (the power-law triple is the one
exception: it is ranked, see below). Every number in this section is the output
of `--scan {er,pl,girg,phase7}` and can be reproduced by re-running it.

  ER pair (phases 1-2), candidates 20260804 + k, k = 0..399 (400 scanned)
      criterion: both mu = 0 and mu = 0.4 die (< 5% failed); mu = 0.4 shows
                 strictly more failures than mu = 0 and at least 4 in total, so
                 the fear channel is visible; and mu = 0 lasts >= 1 round, so
                 phase 1 is a sputter rather than a frozen frame.
      picked: graph_seed = trial_seed = 20260813 (k = 9, first in scan order)
              mu = 0.0 ->  3/300 failed (1.0%),  1 round,  1 structural, 0 fear
              mu = 0.4 ->  8/300 failed (2.7%),  5 rounds, 3 structural, 3 fear
      how common: 11/400 candidates met the full criterion.
      IGNITION COUNT, and an honesty note: 0/400 candidates went systemic at
      mu = 0, but 4/400 (1%) DID go systemic at mu = 0.4. At n = 300 a bounded
      a = r = 2 seed sits only ~4.6x below the Janson critical seed
      (a_c ~ 9.2 here), so finite-size fluctuations can occasionally carry it,
      and fear makes that rare event less rare. The poster's "0/500 at every
      fear level" is an n = 10,000 statement, where a = 2 is ~122x below
      a_c ~ 244. The phase-2 caption states both numbers rather than
      generalising the demo-scale picture into the large-n claim.

  Power-law triple (phases 3-5), candidates 20260804 + k, k = 0..399 (400 scanned)
      criterion: all three of mu = 0, 0.4, 0.7 systemic (failed fraction >=
                 theta = 0.5); rounds(mu=0) >= 8 so mu = 0 reads as "slow";
                 t_half (first round at which half the network is down) strictly
                 falls from mu = 0 to mu = 0.4 and does not rise from 0.4 to
                 0.7; total failures monotone non-decreasing in fear with at
                 least 20 more nodes down at mu = 0.7 than at mu = 0.
                 t_half is the speed metric rather than the total round count
                 because the tail of a cascade is a few stragglers - the
                 participant reads speed from how fast the screen turns over.
      picked: graph_seed = trial_seed = 20261116 (k = 312), the TOP-RANKED
              candidate by t_half(mu=0) - t_half(mu=0.7), not the first in scan
              order. It is also the only candidate whose total round count falls
              monotonically as well.
              mu = 0.0 -> 206/300 (68.7%), 18 rounds, t_half 11, 204 structural,  0 fear
              mu = 0.4 -> 255/300 (85.0%), 16 rounds, t_half  8, 225 structural, 28 fear
              mu = 0.7 -> 289/300 (96.3%), 15 rounds, t_half  7, 234 structural, 53 fear
      how common: 47/400 candidates were systemic at all three fear levels;
      11/400 met the full criterion.
      Honest reading of what phases 3-5 do and do not show: conditioning on
      mu = 0 already igniting means these screens show fear ACCELERATING and
      EXTENDING a cascade the structure was going to sustain anyway (69% -> 96%
      of the network, half the system down 3 rounds sooner). They are not
      evidence about ignition probability - that is phase 7's job.

  GIRG (phase 6), candidates 20260804 + k, k = 0..199 (200 scanned)
      criterion: mu = 0.4, a = 2 goes systemic; final failed fraction within
                 0.10 of the phase-4 power-law trace it is stacked against;
                 realised mean degree within 0.25 of that same trace's; and
                 <= 18 rounds so the two stacked panels finish together.
                 The realised-degree clause matters: the ensemble calibration
                 only fixes E[<k>], and a single heavy-tailed GIRG draw can land
                 15% off it - without this clause the stacked panels would
                 quietly compare two different densities.
      picked: graph_seed = trial_seed = 20260839 (k = 35, first in scan order)
              mu = 0.4 -> 247/300 (82.3%), 14 rounds, 217 structural, 28 fear,
              realised <k> = 4.17, against phase 4's 255/300 (85.0%), 16 rounds,
              realised <k> = 4.11.
      how common: 4/200 candidates met the full criterion (41/200 met the
      systemic + failed-fraction clauses alone; the degree and pacing clauses
      are what make it selective).

  Phase 7 trials (a = 1, mu = 0.4), candidate trial_seeds 20260900 + k,
      k = 0..399 (400 scanned), on the FIXED phase-3/4/5 graph
      (graph_seed 20261116) so the participant sees the same network three
      times and only the run changes.
      criterion: one "dead on arrival" trial (only the seed bank ever fails),
                 one "sputter then die" trial (<= 5% failed, >= 2 rounds, so
                 something visibly happens and then stops), and one systemic
                 trial (>= theta) short enough to watch (<= 22 rounds). Each
                 pick is the first of its category in scan order.
      picked: Trial A trial_seed 20260900 (k =  0) ->   4/300 (1.3%),  5 rounds,
                       0 structural,  3 fear  [sputters, dies]
              Trial B trial_seed 20260902 (k =  2) ->   1/300 (0.3%),  0 rounds
                       [dead on arrival]
              Trial C trial_seed 20260924 (k = 24) -> 271/300 (90.3%), 20 rounds,
                       233 structural, 37 fear  [systemic]
      outcome census over the 400 candidates: 42 systemic (10.5%), 266 dead on
      arrival, 85 sputter-then-die, 7 in between.
      On the 1 - e^(-mu_bar) claim: that is the project's population-level
      ignition rate, measured over RE-DRAWN graphs at production n, and gives
      33% at mu_bar = 0.4. This scan holds ONE n = 300 graph fixed and gets
      10.5%, which is a single draw from that population and is not expected to
      reproduce it. The phase-7 caption therefore quotes this graph's own census
      (42/400) rather than dressing it up as the population rate; the
      1 - e^(-mu_bar) result is presented separately, as the measured result it
      is. What both agree on, and what the phase is actually for: at a = 1 the
      structural rule cannot fire at all, so every one of those 42 ignitions was
      started by fear, and at mu = 0 the count would be exactly 0.

USAGE
-----
    arch -arm64 python3 scripts/dump_poster_demo_traces.py            # dump all traces
    arch -arm64 python3 scripts/dump_poster_demo_traces.py --calibrate
    arch -arm64 python3 scripts/dump_poster_demo_traces.py --scan er
    arch -arm64 python3 scripts/dump_poster_demo_traces.py --scan pl
    arch -arm64 python3 scripts/dump_poster_demo_traces.py --scan girg
    arch -arm64 python3 scripts/dump_poster_demo_traces.py --scan phase7

TRACE SCHEMA (v1)
-----------------
    {
      "schema": "twocascade-poster-demo-trace/1",
      "trace_id": "phase3_powerlaw_mu0",
      "phase": 3, "group": "pl_triple",
      "config": "configs/poster_demo_phase3_powerlaw_mu0.json",
      "git_commit": "...", "generated": "ISO-8601",
      "seeds": {"graph": 20261116, "trial": 20261116},
      "params": {n, r, mean_fear, seed_size, concentration, theta, window_len,
                 weights, graph: {...}},
      "layout": {"kind": "spring"|"girg_positions", "seed": 7},
      "nodes": [[x, y], ...]          # node id = index, coords in [0, 1], 4 dp
      "edges": [[u, v], ...]          # undirected, u < v, deduplicated
      "rounds": [
        {"round": 0, "seed": [..]},
        {"round": 1, "structural": [..], "fear": [..]},   # either may be empty
        ...
      ],
      "summary": {total_failed, final_failed_fraction, rounds_completed,
                  systemic (bool), n_structural, n_fear, n_seed, mean_degree}
      "text": {"headline": "...", "caption": "..."}
    }
"""

import argparse
import datetime
import json
import math
import os
import subprocess
import sys

import numpy as np

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "src"))

from twocascade.reference import (          # noqa: E402  (path setup must precede import)
    sample_gnp_adjacency,
    sample_individual_fears,
    make_nodes,
    choose_seed,
    run_cascade,
)
from twocascade.graphs import (             # noqa: E402
    sample_powerlaw_degrees,
    sample_configuration_model,
    sample_degree_dependent_fears,
)
from twocascade.girg import (               # noqa: E402
    sample_torus_points,
    sample_powerlaw_weights,
    sample_girg_adjacency,
)
from twocascade.model import calculate_beta, calculate_p_n   # noqa: E402

PHASE_CONFIGS = [
    "configs/poster_demo_phase1_er_mu0.json",
    "configs/poster_demo_phase2_er_mu04.json",
    "configs/poster_demo_phase3_powerlaw_mu0.json",
    "configs/poster_demo_phase4_powerlaw_mu04.json",
    "configs/poster_demo_phase5_powerlaw_mu07.json",
    "configs/poster_demo_phase6_girg_mu04.json",
    "configs/poster_demo_phase7_powerlaw_a1.json",
]

SCHEMA = "twocascade-poster-demo-trace/1"


# --------------------------------------------------------------------------- #
# provenance
# --------------------------------------------------------------------------- #
def git_commit_hash() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True
        ).strip()
    except Exception:
        return "dirty-or-unknown"


def load_config(rel_path: str) -> dict:
    with open(os.path.join(REPO_ROOT, rel_path)) as f:
        return json.load(f)


# --------------------------------------------------------------------------- #
# graph construction -- mirrors runner.run_single_trial's branches exactly
# --------------------------------------------------------------------------- #
def build_graph(cfg: dict, graph_seed: int):
    """Return (adjacency, points, fear_basis).

    `points` is the GIRG torus embedding (None otherwise); `fear_basis` is the
    per-node quantity the fear draw conditions on (degrees for the configuration
    model, GIRG weights for GIRG, None for G(n,p)).
    """
    pinned = cfg["pinned_params"]
    n = pinned["n"]
    graph_cfg = pinned["graph"]
    gtype = graph_cfg.get("type", "gnp")

    ss_graph, ss_pair = np.random.SeedSequence(graph_seed).spawn(2)
    rng_graph = np.random.default_rng(ss_graph)
    rng_pair = np.random.default_rng(ss_pair)

    if gtype == "gnp":
        scaling = cfg["scaling"]
        beta = calculate_beta(scaling["target_mean_degree"], scaling["n_ref"], scaling["alpha"])
        p = calculate_p_n(beta, n, scaling["alpha"])
        adj = sample_gnp_adjacency(n, p, rng_pair)
        return adj, None, None

    if gtype == "configuration_model":
        degrees = sample_powerlaw_degrees(n, graph_cfg["tau"], graph_cfg["d_min"], rng_graph)
        adj = sample_configuration_model(degrees, rng_pair)
        return adj, None, degrees

    if gtype == "girg":
        points = sample_torus_points(n, rng_graph)
        weights = sample_powerlaw_weights(n, graph_cfg["tau"], graph_cfg.get("w_min", 1.0), rng_graph)
        adj = sample_girg_adjacency(points, weights, graph_cfg.get("alpha_g", 1.2), rng_pair)
        return adj, points, weights

    raise ValueError(f"Unsupported demo graph type: {gtype}")


def draw_fears(cfg: dict, fear_basis, mean_fear: float, rng_fear):
    pinned = cfg["pinned_params"]
    n = pinned["n"]
    kappa = pinned["concentration"]
    gtype = pinned["graph"].get("type", "gnp")
    gamma = pinned.get("fear", {}).get("gamma", 0.0)

    if gtype == "gnp":
        return sample_individual_fears(n, mean_fear=mean_fear, concentration=kappa, rng=rng_fear)
    # configuration_model and girg both go through the degree/weight-conditioned
    # draw, matching runner.run_single_trial (gamma = 0 -> flat mu(d) = mu_bar).
    basis = fear_basis if isinstance(fear_basis, list) else list(np.asarray(fear_basis))
    fears, _stats = sample_degree_dependent_fears(basis, mean_fear, gamma, kappa, rng_fear)
    return fears


# --------------------------------------------------------------------------- #
# one traced cascade
# --------------------------------------------------------------------------- #
def run_traced_cascade(cfg: dict, graph_seed: int, trial_seed: int,
                        mean_fear: float, seed_size: int) -> dict:
    """Run one cascade through the reference engine and return a trace payload.

    The engine is called exactly as the runner calls it, plus the D-026
    `track_nodes` diagnostic side-channel (recording only; it consumes no RNG,
    so the traced run is bit-identical to the untraced one).
    """
    pinned = cfg["pinned_params"]
    n = pinned["n"]
    r = pinned["r"]
    window_len = pinned["window_len"]
    weights = pinned["weights"]
    theta = pinned["theta"]
    target_high_degree = pinned["target_high_degree"]

    adj, points, fear_basis = build_graph(cfg, graph_seed)

    ss_fear, ss_casc = np.random.SeedSequence(trial_seed).spawn(2)
    rng_fear = np.random.default_rng(ss_fear)
    rng_casc = np.random.default_rng(ss_casc)

    fears = draw_fears(cfg, fear_basis, mean_fear, rng_fear)
    nodes = make_nodes(fears)
    seed_indices = choose_seed(n, seed_size, adj, rng_casc, target_high_degree)

    res = run_cascade(
        adjacency=adj, nodes=nodes, r=r, seed_indices=seed_indices,
        rng=rng_casc, record_history=True,
        window_len=window_len, weights=weights,
        track_nodes=set(range(n)),
    )

    rounds = reconstruct_rounds(res.tracked_failure_rounds, seed_indices)
    rounds_out, n_structural, n_fear = derive_causes(adj, rounds, r)

    # --- integrity checks -------------------------------------------------- #
    tracked_total = len(res.tracked_failure_rounds)
    if tracked_total != res.total_failed:
        raise RuntimeError(
            f"trace/engine disagreement: tracked {tracked_total} failures, engine "
            f"reported total_failed={res.total_failed}")
    if mean_fear == 0.0 and n_fear != 0:
        raise RuntimeError(
            f"cause derivation is wrong: {n_fear} failures classified as fear at "
            f"mean_fear = 0, where the fear probability is identically zero")

    return {
        "adjacency": adj,
        "points": points,
        "rounds": rounds_out,
        "seed_indices": sorted(int(i) for i in seed_indices),
        "total_failed": res.total_failed,
        "final_failed_fraction": res.final_failed_fraction,
        "rounds_completed": res.rounds_completed,
        "n_rounds_animated": len(rounds_out) - 1,
        "systemic": res.final_failed_fraction >= theta,
        "n_structural": n_structural,
        "n_fear": n_fear,
        "mean_degree": float(np.mean([len(a) for a in adj])),
    }


def reconstruct_rounds(tracked: dict, seed_indices) -> list:
    """tracked_failure_rounds {node: round} -> [[nodes failing in round 0], [round 1], ...].

    Rounds in which nothing failed are preserved as empty lists so playback
    timing matches the engine's round clock (a fear cascade can go quiet for a
    round and restart, because the fear window looks back window_len rounds).
    """
    max_round = max(tracked.values()) if tracked else 0
    per_round = [[] for _ in range(max_round + 1)]
    for node, t in tracked.items():
        per_round[t].append(int(node))
    for bucket in per_round:
        bucket.sort()
    # round 0 is exactly the initial shock
    assert per_round[0] == sorted(int(i) for i in seed_indices), \
        "round-0 tracked set does not match the seed set"
    return per_round


def derive_causes(adjacency, per_round, r):
    """Label each failure structural or fear; see the module docstring for why
    this post-hoc rule reproduces the engine's own precedence exactly."""
    cumulative = set(per_round[0])
    out = [{"round": 0, "seed": list(per_round[0])}]
    n_structural = 0
    n_fear = 0
    for t in range(1, len(per_round)):
        structural, fear = [], []
        for v in per_round[t]:
            # count WITH multiplicity, matching the engine's failed_neighbor_count
            failed_nbrs = sum(1 for u in adjacency[v] if u in cumulative)
            (structural if failed_nbrs >= r else fear).append(v)
        out.append({"round": t, "structural": structural, "fear": fear})
        n_structural += len(structural)
        n_fear += len(fear)
        cumulative.update(per_round[t])
    return out, n_structural, n_fear


# --------------------------------------------------------------------------- #
# layout
# --------------------------------------------------------------------------- #
def _packed_spring_layout(adjacency, seed) -> np.ndarray:
    """Component-packed Fruchterman-Reingold layout in [0, 1]^2.

    A plain `spring_layout` on these graphs is unusable: an ER graph at
    <k> ~ 4 carries a 295-node giant component plus a handful of isolated
    nodes, and the force model flings the isolates far out, so min-max
    normalisation squeezes the part anyone cares about into a tiny blob. So the
    giant component is laid out and scaled on its own, and every smaller
    component is parked on a ring around it at a deterministic angle. Positions
    in a force layout are arbitrary anyway - what has to survive is adjacency
    and component structure, and both do.
    """
    import networkx as nx

    n = len(adjacency)
    g = nx.Graph()
    g.add_nodes_from(range(n))
    for u, nbrs in enumerate(adjacency):
        for v in nbrs:
            if u < v:
                g.add_edge(u, v)

    comps = sorted(nx.connected_components(g), key=len, reverse=True)
    coords = np.zeros((n, 2), dtype=float)

    def place(nodes, centre, radius):
        nodes = sorted(nodes)
        if len(nodes) == 1:
            coords[nodes[0]] = centre
            return
        sub = g.subgraph(nodes)
        # k larger than the 1/sqrt(m) default pushes the periphery out, so the
        # hub-and-spoke structure is readable instead of a dense central knot.
        pos = nx.spring_layout(sub, seed=seed, iterations=300,
                                k=1.9 / math.sqrt(len(nodes)))
        pts = np.array([pos[i] for i in nodes], dtype=float)
        pts -= pts.mean(axis=0)
        rmax = float(np.max(np.hypot(pts[:, 0], pts[:, 1])))
        pts *= (radius / rmax) if rmax > 0 else 1.0
        for idx, node in enumerate(nodes):
            coords[node] = centre + pts[idx]

    centre = np.array([0.5, 0.5])
    giant_frac = len(comps[0]) / float(n)
    if len(comps) == 1:
        r_giant = 0.44
    elif giant_frac >= 0.9:
        # a handful of isolates should not shrink the part that matters
        r_giant = 0.43
    else:
        r_giant = 0.385
    place(comps[0], centre, r_giant)

    others = comps[1:]
    for j, comp in enumerate(others):
        angle = 2.0 * math.pi * j / len(others) + 0.35
        ring = np.array([0.5 + 0.485 * math.cos(angle), 0.5 + 0.485 * math.sin(angle)])
        place(comp, ring, 0.012 * math.sqrt(len(comp)))

    return np.clip(coords, 0.01, 0.99)


def compute_layout(adjacency, layout_cfg, points=None) -> list:
    """Fixed node positions in [0, 1]^2, one per node, in node-id order.

    GIRG uses its real torus coordinates - the geometry IS the point of phase 6.
    Everything else gets a deterministic spring layout (networkx
    Fruchterman-Reingold with a fixed seed), computed once here so the page never
    runs physics at playback time.
    """
    kind = layout_cfg.get("kind", "spring")
    if kind == "girg_positions":
        if points is None:
            raise ValueError("girg_positions layout requires GIRG torus points")
        coords = np.asarray(points, dtype=float)
    elif kind == "spring":
        coords = _packed_spring_layout(adjacency, layout_cfg.get("seed", 7))
    else:
        raise ValueError(f"Unknown layout kind: {kind}")
    return [[round(float(x), 4), round(float(y), 4)] for x, y in coords]


def edge_list(adjacency) -> list:
    seen = set()
    edges = []
    for u, nbrs in enumerate(adjacency):
        for v in nbrs:
            if u < v and (u, v) not in seen:
                seen.add((u, v))
                edges.append([u, int(v)])
    return edges


# --------------------------------------------------------------------------- #
# trace assembly
# --------------------------------------------------------------------------- #
def build_trace(cfg, cfg_path, trace_id, phase, group, mean_fear, seed_size,
                graph_seed, trial_seed, layout_cfg, text, extra=None) -> dict:
    run = run_traced_cascade(cfg, graph_seed, trial_seed, mean_fear, seed_size)
    pinned = cfg["pinned_params"]
    trace = {
        "schema": SCHEMA,
        "trace_id": trace_id,
        "phase": phase,
        "group": group,
        "config": cfg_path,
        "git_commit": git_commit_hash(),
        "generated": datetime.datetime.now().isoformat(timespec="seconds"),
        "seeds": {"graph": graph_seed, "trial": trial_seed},
        "params": {
            "n": pinned["n"],
            "r": pinned["r"],
            "mean_fear": mean_fear,
            "seed_size": seed_size,
            "concentration": pinned["concentration"],
            "theta": pinned["theta"],
            "window_len": pinned["window_len"],
            "weights": pinned["weights"],
            "graph": pinned["graph"],
        },
        "layout": dict(layout_cfg),
        "nodes": compute_layout(run["adjacency"], layout_cfg, run["points"]),
        "edges": edge_list(run["adjacency"]),
        "rounds": run["rounds"],
        "summary": {
            "total_failed": run["total_failed"],
            "final_failed_fraction": round(run["final_failed_fraction"], 6),
            "rounds_completed": run["rounds_completed"],
            "rounds_animated": run["n_rounds_animated"],
            "systemic": bool(run["systemic"]),
            "n_seed": len(run["seed_indices"]),
            "n_structural": run["n_structural"],
            "n_fear": run["n_fear"],
            "mean_degree": round(run["mean_degree"], 4),
        },
        "text": text,
    }
    if extra:
        trace.update(extra)
    validate_trace(trace)
    return trace


def validate_trace(trace: dict) -> None:
    """Reject a malformed trace before it ships to the page."""
    assert trace["schema"] == SCHEMA
    n = trace["params"]["n"]
    assert len(trace["nodes"]) == n, "layout must have one position per node"
    for x, y in trace["nodes"]:
        assert -0.01 <= x <= 1.01 and -0.01 <= y <= 1.01, "layout escapes the unit box"
    for u, v in trace["edges"]:
        assert 0 <= u < n and 0 <= v < n and u < v, "malformed edge"
    seen = set(trace["rounds"][0]["seed"])
    assert len(seen) == trace["summary"]["n_seed"]
    for rd in trace["rounds"][1:]:
        for v in rd["structural"] + rd["fear"]:
            assert v not in seen, "a node failed twice"
            assert 0 <= v < n
            seen.add(v)
    assert len(seen) == trace["summary"]["total_failed"], "round sets do not sum to total_failed"
    if trace["params"]["mean_fear"] == 0.0:
        assert trace["summary"]["n_fear"] == 0, "fear failure at mean_fear = 0"


def write_trace(trace: dict, rel_path: str) -> str:
    path = os.path.join(REPO_ROOT, rel_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(trace, f, separators=(",", ":"))
    return path


# --------------------------------------------------------------------------- #
# modes
# --------------------------------------------------------------------------- #
def dump_all() -> None:
    manifest = []
    for cfg_path in PHASE_CONFIGS:
        cfg = load_config(cfg_path)
        demo = cfg["demo"]
        text = {"headline": demo["headline"], "caption": demo["caption"]}
        if demo["phase"] == 7:
            for trial in demo["trials"]:
                trace = build_trace(
                    cfg, cfg_path, trial["trace_id"], 7, demo["group"],
                    demo["mean_fear"], demo["seed_size"],
                    demo["graph_seed"], trial["trial_seed"], demo["layout"], text,
                    extra={"label": trial["label"]},
                )
                rel = os.path.join(cfg["output"]["trace_dir"], trial["trace_id"] + ".json")
                manifest.append(report(trace, write_trace(trace, rel), rel))
        else:
            trace = build_trace(
                cfg, cfg_path, demo["trace_id"], demo["phase"], demo["group"],
                demo["mean_fear"], demo["seed_size"],
                demo["graph_seed"], demo["trial_seed"], demo["layout"], text,
                extra={"paired_with": demo["paired_with"]} if "paired_with" in demo else None,
            )
            rel = cfg["output"]["trace_path"]
            manifest.append(report(trace, write_trace(trace, rel), rel))

    print("\n=== trace inventory ===")
    header = f"{'file':<44}{'seed(g/t)':<22}{'rnds':>5}{'failed':>9}{'struct':>8}{'fear':>6}{'KB':>7}"
    print(header)
    print("-" * len(header))
    for row in manifest:
        print(row)


def report(trace, abs_path, rel_path) -> str:
    s = trace["summary"]
    kb = os.path.getsize(abs_path) / 1024.0
    seeds = f"{trace['seeds']['graph']}/{trace['seeds']['trial']}"
    return (f"{rel_path:<44}{seeds:<22}{s['rounds_animated']:>5}"
            f"{s['total_failed']:>5} ({s['final_failed_fraction']*100:4.1f}%)"
            f"{s['n_structural']:>8}{s['n_fear']:>6}{kb:>7.1f}")


def calibrate() -> None:
    """Reproduce the n = 300 degree matching quoted in the configs."""
    n, tau, d_min, alpha_g, reps, base = 300, 2.5, 2, 1.2, 40, 20260804

    drawn, realised = [], []
    for child in np.random.SeedSequence(base).spawn(reps):
        rg, rp = (np.random.default_rng(s) for s in child.spawn(2))
        deg = sample_powerlaw_degrees(n, tau, d_min, rg)
        adj = sample_configuration_model(deg, rp)
        drawn.append(float(np.mean(deg)))
        realised.append(float(np.mean([len(a) for a in adj])))
    cm_mean = float(np.mean(realised))
    cm_se = float(np.std(realised, ddof=1) / np.sqrt(reps))
    print(f"configuration model n={n} tau={tau} d_min={d_min}: "
          f"drawn <k> = {np.mean(drawn):.4f}, realised <k> = {cm_mean:.4f} +/- {cm_se:.4f}")

    er_target = cm_mean * n / (n - 1)
    p = calculate_p_n(calculate_beta(er_target, n, 0.6), n, 0.6)
    print(f"ER matched (n_ref={n}, alpha=0.6): target_mean_degree = {er_target:.6f}, "
          f"p = {p:.8f}, (n-1)p = {(n - 1) * p:.4f}")

    def girg_k(w_min):
        means = []
        for child in np.random.SeedSequence(base).spawn(reps):
            rg, rp = (np.random.default_rng(s) for s in child.spawn(2))
            pts = sample_torus_points(n, rg)
            w = sample_powerlaw_weights(n, tau, w_min, rg)
            adj = sample_girg_adjacency(pts, w, alpha_g, rp)
            means.append(float(np.mean([len(a) for a in adj])))
        return float(np.mean(means)), float(np.std(means, ddof=1) / np.sqrt(reps))

    lo, hi, tol = 0.05, 3.0, 0.05
    mid = None
    for it in range(1, 26):
        mid = 0.5 * (lo + hi)
        k, se = girg_k(mid)
        print(f"  girg bisect it{it}: w_min = {mid:.8f} -> <k> = {k:.4f} +/- {se:.4f}")
        if abs(k - cm_mean) <= tol:
            print(f"GIRG matched: w_min = {mid!r} -> <k> = {k:.4f} (target {cm_mean:.4f}, "
                  f"tol {tol}, inside the {se:.3f} replicate se -- approximate demo match)")
            return
        if k < cm_mean:
            lo = mid
        else:
            hi = mid
    print(f"GIRG bisection did not reach tol {tol}; best w_min = {mid!r}")


def _quick(cfg, graph_seed, trial_seed, mean_fear, seed_size):
    run = run_traced_cascade(cfg, graph_seed, trial_seed, mean_fear, seed_size)
    return run


def _t_half(run, n):
    """First round by which half the network has failed (None if it never does).

    A better read on "visibly faster" than the total round count: the tail of a
    cascade is a few stragglers, but the participant perceives speed from how
    quickly the screen turns over early on.
    """
    cum = 0
    for rd in run["rounds"]:
        cum += len(rd.get("seed", [])) + len(rd.get("structural", [])) + len(rd.get("fear", []))
        if cum >= n / 2:
            return rd["round"]
    return None


def scan(which: str, n_candidates: int) -> None:
    """Reproduce the seed selection documented in the module docstring."""
    if which == "er":
        c1 = load_config("configs/poster_demo_phase1_er_mu0.json")
        c2 = load_config("configs/poster_demo_phase2_er_mu04.json")
        hits, ign_mu0, ign_mu04 = [], 0, 0
        for k in range(n_candidates):
            s = 20260804 + k
            a = _quick(c1, s, s, 0.0, 2)
            b = _quick(c2, s, s, 0.4, 2)
            ign_mu0 += int(a["systemic"])
            ign_mu04 += int(b["systemic"])
            ok = (a["final_failed_fraction"] < 0.05 and b["final_failed_fraction"] < 0.05
                  and b["total_failed"] > a["total_failed"] and b["total_failed"] >= 4
                  and a["n_rounds_animated"] >= 1)   # mu=0 must visibly sputter, not freeze
            if ok:
                hits.append((k, s, a, b))
        print(f"ER pair scan: {n_candidates} candidates, {len(hits)} met the criterion; "
              f"systemic runs: {ign_mu0} at mu=0, {ign_mu04} at mu=0.4")
        for k, s, a, b in hits[:5]:
            print(f"  k={k:3d} seed={s}  mu0: {a['total_failed']:3d} failed / "
                  f"{a['n_rounds_animated']} rounds | mu0.4: {b['total_failed']:3d} failed / "
                  f"{b['n_rounds_animated']} rounds, {b['n_fear']} by fear")

    elif which == "pl":
        cs = [load_config(f"configs/poster_demo_phase{i}_powerlaw_"
                          f"{'mu0' if i == 3 else 'mu04' if i == 4 else 'mu07'}.json")
              for i in (3, 4, 5)]
        mus = [0.0, 0.4, 0.7]
        hits, n_all_systemic = [], 0
        for k in range(n_candidates):
            s = 20260804 + k
            runs = [_quick(c, s, s, mu, 2) for c, mu in zip(cs, mus)]
            rounds = [x["n_rounds_animated"] for x in runs]
            if not all(x["systemic"] for x in runs):
                continue
            n_all_systemic += 1
            n = cs[0]["pinned_params"]["n"]
            th = [_t_half(x, n) for x in runs]
            ok = (rounds[0] >= 8 and th[0] > th[1] >= th[2]
                  and runs[2]["total_failed"] >= runs[1]["total_failed"] >= runs[0]["total_failed"]
                  and runs[2]["total_failed"] - runs[0]["total_failed"] >= 20)
            if ok:
                hits.append((th[0] - th[2], k, s, runs, th))
        hits.sort(reverse=True)   # rank by how much fear compresses the cascade
        print(f"power-law triple scan: {n_candidates} candidates, {n_all_systemic} systemic at "
              f"all three fear levels, {len(hits)} met the full criterion "
              f"(ranked by t_half(mu=0) - t_half(mu=0.7))")
        for gap, k, s, runs, th in hits[:8]:
            desc = " | ".join(f"mu={mu}: {x['total_failed']}f/{x['n_rounds_animated']}r/"
                              f"t50={t} ({x['n_fear']} fear)"
                              for mu, x, t in zip(mus, runs, th))
            print(f"  gap={gap:2d} k={k:3d} seed={s}  {desc}")

    elif which == "girg":
        cg = load_config("configs/poster_demo_phase6_girg_mu04.json")
        c4 = load_config("configs/poster_demo_phase4_powerlaw_mu04.json")
        d4 = c4["demo"]
        ref = _quick(c4, d4["graph_seed"], d4["trial_seed"], 0.4, 2)
        print(f"reference power-law (phase 4): {ref['total_failed']} failed "
              f"({ref['final_failed_fraction']*100:.1f}%) in {ref['n_rounds_animated']} rounds, "
              f"realised <k> = {ref['mean_degree']:.2f}")
        hits = []
        for k in range(n_candidates):
            s = 20260804 + k
            g = _quick(cg, s, s, 0.4, 2)
            # The ensemble calibration fixes E[<k>]; a single heavy-tailed GIRG draw
            # can still land 15% off it, so the picked graph must ALSO match the
            # power-law graph's own realised mean degree -- otherwise the stacked
            # panels are quietly comparing two different densities.
            if (g["systemic"]
                    and abs(g["final_failed_fraction"] - ref["final_failed_fraction"]) <= 0.10
                    and abs(g["mean_degree"] - ref["mean_degree"]) <= 0.25
                    # pacing: the stacked panels animate together, so the GIRG
                    # side must not run far past the power-law side's 16 rounds
                    and g["n_rounds_animated"] <= 18):
                hits.append((k, s, g))
        print(f"GIRG scan: {n_candidates} candidates, {len(hits)} met the criterion")
        for k, s, g in hits[:5]:
            print(f"  k={k:3d} seed={s}  {g['total_failed']} failed "
                  f"({g['final_failed_fraction']*100:.1f}%) in {g['n_rounds_animated']} rounds, "
                  f"{g['n_fear']} by fear, realised <k> = {g['mean_degree']:.2f}")

    elif which == "phase7":
        c7 = load_config("configs/poster_demo_phase7_powerlaw_a1.json")
        gseed = c7["demo"]["graph_seed"]
        instant, sputter, systemics = [], [], []
        n_sys = n_instant = n_sputter = 0
        for k in range(n_candidates):
            t = 20260900 + k
            x = _quick(c7, gseed, t, 0.4, 1)
            if x["systemic"]:
                n_sys += 1
                # pacing constraint: a phone demo cannot hold attention for a
                # 30-round animation, so the systemic pick is capped at 22 rounds.
                if x["n_rounds_animated"] <= 22 and len(systemics) < 5:
                    systemics.append((k, t, x))
            elif x["total_failed"] == 1:
                n_instant += 1
                if len(instant) < 5:
                    instant.append((k, t, x))
            elif x["final_failed_fraction"] <= 0.05 and x["n_rounds_animated"] >= 2:
                n_sputter += 1
                if len(sputter) < 5:
                    sputter.append((k, t, x))
        print(f"phase-7 scan on fixed graph_seed={gseed}: {n_candidates} candidate trial "
              f"seeds -> {n_sys} systemic ({n_sys / n_candidates * 100:.1f}%), "
              f"{n_instant} dead on arrival (only the seed bank fails), "
              f"{n_sputter} sputter then die. Population-level ignition over RE-DRAWN "
              f"graphs is 1-e^-0.4 = {1 - np.exp(-0.4):.3f}; this is one graph, not that "
              f"population.")
        for tag, rows in (("dead on arrival", instant), ("sputter+die", sputter),
                          ("systemic (<=22 rounds)", systemics)):
            for k, t, x in rows:
                print(f"  [{tag}] k={k:3d} trial_seed={t}  {x['total_failed']} failed "
                      f"({x['final_failed_fraction']*100:.1f}%) in {x['n_rounds_animated']} rounds, "
                      f"{x['n_fear']} by fear")
    else:
        raise ValueError(f"unknown scan group: {which}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--calibrate", action="store_true",
                     help="reproduce the n=300 ER/GIRG degree matching")
    ap.add_argument("--scan", choices=["er", "pl", "girg", "phase7"],
                     help="reproduce the seed selection for one phase group")
    ap.add_argument("--candidates", type=int, default=400,
                     help="candidates per scan (default 400; the girg scan used 200)")
    args = ap.parse_args()

    if args.calibrate:
        calibrate()
    elif args.scan:
        scan(args.scan, args.candidates)
    else:
        dump_all()


if __name__ == "__main__":
    main()
