"""
Task R (Q5, C-Q5(i) follow-up): cross-round remote-nucleation pilot.

remote_nucleation (src/twocascade/geometry.py) certifies a "nucleus" only within a
single round's new failures. Since failures are permanent, two lone remote failures
from DIFFERENT rounds that end up within r_n of each other should also count -- the
per-round-only check is a documented lower bound
(docs/queue/task_R_cross_round_remote_ignition.md, EXPLAINER.md SS7.5,
okf/open-questions.md Q5).

This is a PILOT, not a publication run: n=4000, a handful of trials/cell, meant only
to decide whether a fuller n-sweep is worth the compute. It does NOT modify
src/twocascade/geometry.py -- the cross-round clustering logic is duplicated here
rather than refactored into a shared helper, to avoid triggering this project's
baseline-isolation (worktree + full /verify) rule for a one-off research-diagnostic
script. Any future edit to remote_nucleation's clique-finding logic in geometry.py
MUST re-run tests/test_task_r_cross_round.py, which checks this script's duplicated
clustering reproduces remote_nucleation's loose-component DECOMPOSITION exactly on
single-round data. (Its per-component nucleus COUNT now differs by design:
_pooled_nucleus_count peels multiple cliques per component -- see below and
okf/changes/s-055-... -- whereas remote_nucleation counts one.)

Nucleus counting uses iterative maximal-clique PEELING, not one-nucleus-per-loose-
component. A naive one-per-component count (what remote_nucleation does per round)
collapses genuinely separate nuclei that a whole-trial pool has transitively bridged
into one giant loose component, undercounting badly at pool scale -- the flaw that
paused the first pilot (okf/changes/s-055-...). Peeling repeatedly removes the largest
remaining strict-r_n clique (>= r) from each component, recovering the separate nuclei.

Naive pooling across a whole trial has a confound: as the front consumes the torus,
the remaining "remote-eligible" area shrinks, so two individually-honest remote
failures from different rounds can end up close together by sheer geometric
coincidence (less remaining space), not genuine correlated secondary nucleation --
worse at higher mu_bar, which is exactly the regime a real g^2-type signal would be
hoped for. This script controls for it with a matched null model: at each round, the
real remote-ELIGIBLE pool (every currently-unfailed node > r_n from the real failed
set at that round) is computed, and K null replicates redraw the SAME per-round
COUNT of "fake" remote failures uniformly from that pool -- preserving the real
depletion/opportunity structure exactly, while destroying any genuine spatial
correlation among which specific nodes fear actually chose. The EXCESS of the real
pooled-cluster count over the null distribution (see analyze_task_r_cross_round.py),
not the raw pooled count, is treated as the evidence for genuine cross-round
nucleation.

K=1 is used only to characterize wall-clock/max-cost scaling, never for the
statistical excess test (no SD is estimable from a single null draw). The K in
{1, 10, 30} checkpoints in CONFIG let one pilot run report cost at all three
checkpoints from a single K=30 pass (each checkpoint's null totals are a prefix of
the full replicate sequence).

Cost note: the eligible-pool computation is O(n x |failed|) per round via numpy
broadcasting (not a grid-bucket index like _build_bucket_adjacency uses for
adjacency construction) -- deliberately the simplest correct approach for this
n=4000 pilot rather than a bespoke bucket-index rewrite; if the pilot's own timing
shows this doesn't scale to n=8000+, a bucket-index optimization is the flagged next
step, not built preemptively here.

Owns its raw output (results integrity rule): stamps config, seeds, and git commit
into results/q5_task_r_cross_round_raw.json.
"""

import os
import sys
import json
import time
import datetime
from multiprocessing import Pool

import numpy as np
import networkx as nx
from networkx.algorithms.clique import find_cliques

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(base_dir, "src"))

from twocascade.runner import get_git_commit_hash
from twocascade.reference import make_nodes, sample_individual_fears
from twocascade.geometry import (
    sample_torus_points,
    build_rgg_adjacency,
    run_cascade_local_fear,
    remote_nucleation,
)

CONFIG = {
    "n": 4000,
    "r": 2,
    "concentration": 50,
    "theta": 0.5,
    "window_len": 5,
    "weights": [0.2, 0.2, 0.2, 0.2, 0.2],
    "mean_degree_c": 2.0,
    "seed_layout": "disc",
    "seed_size": 30,
    "mean_fear_grid": [0.2, 0.4, 0.6],
    "trials_per_cell": 10,
    "base_seed": 20260718,
    "stats_cutoff": 0.75,
    "null_replicate_checkpoints": [1, 10, 30],
}

OUTPUT_PATH = "results/q5_task_r_cross_round_raw.json"


def _torus_dist_sq(a, b):
    """Squared torus distance between point arrays a (n,2) and b (m,2) -> (n,m)."""
    diff = np.abs(a[:, None, :] - b[None, :, :])
    diff = np.minimum(diff, 1.0 - diff)
    return np.sum(diff ** 2, axis=-1)


def _pooled_nucleus_count(remote_indices, points, r_n, r):
    """
    Cross-round generalization of remote_nucleation's internal clustering: given a
    POOLED set of already-certified-remote node indices (from possibly many
    rounds), build the loose graph (edges within 2*r_n), then per connected
    component of size >= r, rebuild the strict r_n subgraph and iteratively PEEL
    maximal cliques (largest first) of size >= r, counting one nucleus per peeled
    clique. This differs from remote_nucleation, which counts one nucleus per
    component -- see the module docstring and okf/changes/s-055-... for why the
    one-per-component rule undercounts at whole-trial-pool scale.

    DUPLICATED from remote_nucleation's post-filtering logic
    (src/twocascade/geometry.py) by design -- see this file's module docstring.

    Returns: (nucleus_count, list of {members, component_size, component_id,
              nuclei_in_component, possible_merged_component} dicts, one per
              nucleus found). component_id groups nuclei peeled from the same
              loose component (so the number of distinct component_ids equals the
              old one-per-component count -- the geometric-decomposition parity
              the test checks against remote_nucleation). nuclei_in_component is
              how many nuclei were peeled from that component (> 1 is exactly the
              collapse the old rule hid). possible_merged_component
              (component_size >= 2*r) is a coarse size-based triage flag retained
              from before, now largely subsumed by nuclei_in_component.
    """
    remote_indices = list(remote_indices)
    if len(remote_indices) < r:
        return 0, []

    rem_points = points[remote_indices]
    n_rem = len(rem_points)
    d_sq = _torus_dist_sq(rem_points, rem_points)
    loose_r_sq = (2 * r_n) ** 2
    iu, ju = np.triu_indices(n_rem, k=1)
    loose_edges = d_sq[iu, ju] <= loose_r_sq

    G = nx.Graph()
    G.add_nodes_from(remote_indices)
    for a, b, keep in zip(iu, ju, loose_edges):
        if keep:
            G.add_edge(remote_indices[a], remote_indices[b])

    nuclei = []
    for comp_id, comp in enumerate(nx.connected_components(G)):
        if len(comp) < r:
            continue
        comp_list = list(comp)
        c_points = points[comp_list]
        m = len(comp_list)
        d_sq_c = _torus_dist_sq(c_points, c_points)
        strict_r_sq = r_n ** 2
        C = nx.Graph()
        C.add_nodes_from(comp_list)
        iuc, juc = np.triu_indices(m, k=1)
        strict_edges = d_sq_c[iuc, juc] <= strict_r_sq
        for a, b, keep in zip(iuc, juc, strict_edges):
            if keep:
                C.add_edge(comp_list[a], comp_list[b])

        # Iteratively PEEL maximal cliques rather than counting one nucleus per
        # loose component (the old rule -- see okf/changes/s-055-...): repeatedly
        # take the LARGEST remaining strict-r_n clique of size >= r as one
        # nucleus and remove its members, until no clique >= r remains. This
        # recovers the multiple genuinely-separate nuclei that a large pool can
        # transitively bridge into one loose (2*r_n) component. Every strict
        # r_n-clique lies wholly inside one loose component, so peeling per
        # component == peeling over the whole strict graph.
        #
        # Largest-first (not smallest-first) is deliberate and conservative: a
        # dense blob of k mutually-close points is one K_k clique, peeled as ONE
        # nucleus, never shattered into k/r spurious small ones. It is a greedy
        # disjoint-clique cover, not a proven maximum -- adequate for a pilot.
        comp_cliques = []
        while C.number_of_nodes() >= r:
            best_clique = max(find_cliques(C), key=len, default=[])
            if len(best_clique) < r:
                break
            comp_cliques.append(best_clique)
            C.remove_nodes_from(best_clique)

        for clq in comp_cliques:
            nuclei.append({
                "members": clq,
                "component_size": len(comp_list),
                "component_id": comp_id,
                "nuclei_in_component": len(comp_cliques),
                "possible_merged_component": len(comp_list) >= 2 * r,
            })

    return len(nuclei), nuclei


def run_trial(args):
    (mu, child_seed, cfg) = args
    n, r = cfg["n"], cfg["r"]
    s_graph, s_fear, s_casc, s_null = child_seed.spawn(4)
    rng_graph = np.random.default_rng(s_graph)
    rng_fear = np.random.default_rng(s_fear)
    rng_casc = np.random.default_rng(s_casc)
    rng_null = np.random.default_rng(s_null)

    r_n = float(np.sqrt(cfg["mean_degree_c"] * np.log(n) / (np.pi * n)))
    points = sample_torus_points(n, rng_graph)
    adj = build_rgg_adjacency(points, r_n)

    fears = sample_individual_fears(n, mean_fear=mu, concentration=cfg["concentration"],
                                    rng=rng_fear)

    center = sample_torus_points(1, rng_casc)[0]
    diff = np.abs(points - center)
    diff = np.minimum(diff, 1.0 - diff)
    seeds = np.argsort(np.sum(diff ** 2, axis=1))[:cfg["seed_size"]].tolist()

    nodes = make_nodes(list(fears))
    round_log = []
    res = run_cascade_local_fear(
        adjacency=adj, fear_adjacency=None, nodes=nodes, r=r,
        seed_indices=seeds, rng=rng_casc, record_history=True,
        window_len=cfg["window_len"], weights=cfg["weights"],
        round_log=round_log)

    theta, cutoff = cfg["theta"], cfg["stats_cutoff"]
    previously_failed_set = set(seeds)
    previously_failed_mask = np.zeros(n, dtype=bool)
    previously_failed_mask[seeds] = True
    cum = len(seeds)

    real_remote_pool = []      # (node_idx, round_t) pairs, pooled across the trial
    per_round_n_nuc = []       # existing per-round metric, via the OFFICIAL remote_nucleation
    per_round_eligible = []    # per round: {eligible: idx array, count_real_remote: int}
    t_theta = None

    for t, new_set in enumerate(round_log, start=1):
        cum += len(new_set)
        g_t = cum / n
        if t_theta is None and g_t >= theta:
            t_theta = t
        if (cum - len(new_set)) / n > cutoff:
            break  # matches Task O's stats_cutoff convention

        new_list = sorted(new_set)
        failed_points = points[previously_failed_mask]

        # Official per-round metric -- same function, same call pattern as Task O.
        n_nuc_this_round = remote_nucleation(new_list, previously_failed_set, points, r_n, r)
        per_round_n_nuc.append({"t": t, "g_t": g_t, "n_nuc": n_nuc_this_round})

        # Independently certify which of this round's failures are remote (same
        # distance rule remote_failures/remote_nucleation use internally), keeping
        # indices (not just a count) for cross-round pooling.
        round_remote = []
        if len(failed_points) > 0 and len(new_list) > 0:
            d_sq = _torus_dist_sq(points[new_list], failed_points)
            min_d_sq = d_sq.min(axis=1)
            round_remote = [new_list[i] for i in range(len(new_list)) if min_d_sq[i] > r_n ** 2]
        for idx in round_remote:
            real_remote_pool.append((idx, t))

        # Full remote-ELIGIBLE pool (every unfailed node > r_n from previously_failed),
        # needed by the null model -- NOT just which nodes fear actually chose.
        unfailed_idx = np.where(~previously_failed_mask)[0]
        if len(failed_points) > 0 and len(unfailed_idx) > 0:
            d_sq = _torus_dist_sq(points[unfailed_idx], failed_points)
            eligible_idx = unfailed_idx[d_sq.min(axis=1) > r_n ** 2]
        else:
            eligible_idx = unfailed_idx
        per_round_eligible.append({"eligible": eligible_idx, "count_real_remote": len(round_remote)})

        previously_failed_set |= new_set
        previously_failed_mask[new_list] = True

    # --- Real pooled cross-round nucleus count (both attribution conventions) ---
    real_pool_indices = [idx for idx, t in real_remote_pool]
    real_cross_round_n_nuc, real_nuclei = _pooled_nucleus_count(real_pool_indices, points, r_n, r)

    idx_to_round = dict(real_remote_pool)
    real_nuclei_meta = []
    for nuc in real_nuclei:
        rounds_in_clique = [idx_to_round[i] for i in nuc["members"]]
        real_nuclei_meta.append({
            "size": len(nuc["members"]),
            "component_size": nuc["component_size"],
            "component_id": nuc["component_id"],
            "nuclei_in_component": nuc["nuclei_in_component"],
            "possible_merged_component": nuc["possible_merged_component"],
            "latest_round": max(rounds_in_clique),
            "earliest_round": min(rounds_in_clique),
            "round_gap": max(rounds_in_clique) - min(rounds_in_clique),
        })

    per_round_nuclei_total = sum(row["n_nuc"] for row in per_round_n_nuc)

    # --- Null model: K replicates, cost checkpoints (latest-failing convention
    # only for null, per the plan's scope trim -- dual attribution is real-only). ---
    max_k = max(cfg["null_replicate_checkpoints"])
    null_totals_by_checkpoint = {str(k): [] for k in cfg["null_replicate_checkpoints"]}
    cost_seconds_by_checkpoint = {}
    running_null_totals = []
    t_start = time.perf_counter()
    for rep in range(max_k):
        null_pool_indices = []
        for row in per_round_eligible:
            k_this_round = row["count_real_remote"]
            if k_this_round == 0 or len(row["eligible"]) == 0:
                continue
            draw_n = min(k_this_round, len(row["eligible"]))
            drawn = rng_null.choice(row["eligible"], size=draw_n, replace=False)
            null_pool_indices.extend(drawn.tolist())
        null_count, _ = _pooled_nucleus_count(null_pool_indices, points, r_n, r)
        running_null_totals.append(null_count)
        if (rep + 1) in cfg["null_replicate_checkpoints"]:
            cost_seconds_by_checkpoint[str(rep + 1)] = time.perf_counter() - t_start
            null_totals_by_checkpoint[str(rep + 1)] = list(running_null_totals)

    return {
        "mean_fear": mu,
        "final_failed_fraction": res.final_failed_fraction,
        "rounds_completed": res.rounds_completed,
        "systemic": res.final_failed_fraction >= theta,
        "per_round_n_nuc": per_round_n_nuc,
        "per_round_nuclei_total": per_round_nuclei_total,
        "real_cross_round_n_nuc": real_cross_round_n_nuc,
        "real_nuclei_meta": real_nuclei_meta,
        "null_totals_by_checkpoint": null_totals_by_checkpoint,
        "cost_seconds_by_checkpoint": cost_seconds_by_checkpoint,
    }


def main():
    cfg = CONFIG
    ss = np.random.SeedSequence(cfg["base_seed"])
    child_seeds = ss.spawn(len(cfg["mean_fear_grid"]) * cfg["trials_per_cell"])

    tasks = []
    idx = 0
    for mu in cfg["mean_fear_grid"]:
        for _ in range(cfg["trials_per_cell"]):
            tasks.append((mu, child_seeds[idx], cfg))
            idx += 1

    print(f"Task R cross-round pilot: {len(cfg['mean_fear_grid'])} cells x "
          f"{cfg['trials_per_cell']} trials = {len(tasks)} trials, "
          f"K checkpoints {cfg['null_replicate_checkpoints']}")
    n_workers = os.cpu_count() or 4
    chunksize = max(1, len(tasks) // (n_workers * 4))
    t0 = time.perf_counter()
    with Pool() as pool:
        results = pool.map(run_trial, tasks, chunksize=chunksize)
    wall = time.perf_counter() - t0
    print(f"Done in {wall:.1f}s wall-clock")

    out = {
        "metadata": {
            "task": "R (Q5 cross-round remote-nucleation pilot)",
            **{k: v for k, v in cfg.items()},
            "git_commit": get_git_commit_hash(),
            "timestamp": datetime.datetime.now().isoformat(),
            "engine": "python (run_cascade_local_fear)",
            "wall_clock_seconds": wall,
        },
        "results": results,
    }
    out_path = os.path.join(base_dir, OUTPUT_PATH)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(out, f)
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
