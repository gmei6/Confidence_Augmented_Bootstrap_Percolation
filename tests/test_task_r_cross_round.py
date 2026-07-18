"""
Task R correctness checks for scripts/run_task_r_cross_round.py's duplicated
clustering logic (see that script's module docstring for why it's duplicated
rather than refactored into src/twocascade/geometry.py).

Any future edit to remote_nucleation's clique-finding logic in geometry.py must
re-run this file.
"""
import os
import sys

import numpy as np

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(base_dir, "src"))
sys.path.insert(0, os.path.join(base_dir, "scripts"))

from twocascade.geometry import remote_nucleation, sample_torus_points
from run_task_r_cross_round import _pooled_nucleus_count


def test_pooled_matches_remote_nucleation_on_random_scenarios():
    """The duplicated clustering must reproduce remote_nucleation's GEOMETRIC
    decomposition exactly on single-round data: the number of distinct loose
    components that yield an r-clique (the set of nuc["component_id"] values)
    must equal remote_nucleation's own one-per-component count. The peeled
    nucleus count can only ever be >= that (peeling splits multi-clique
    components), never fewer -- so both the component-level exact parity and the
    peeled-count lower bound are asserted.

    (Before the S-055 peeling fix this asserted pooled_count == official
    directly. Peeling deliberately changed the count contract -- test-semantics
    case (b) -- so the invariant that actually protects geometric-primitive
    fidelity, component parity, is asserted instead. See okf/changes/s-055-....)"""
    rng = np.random.default_rng(101)
    n, r_n, r = 300, 0.06, 2

    for trial in range(20):
        points = sample_torus_points(n, rng)
        previously_failed = set(rng.choice(n, size=40, replace=False).tolist())
        candidates = [i for i in range(n) if i not in previously_failed]
        new_failures = rng.choice(candidates, size=15, replace=False).tolist()

        official = remote_nucleation(new_failures, previously_failed, points, r_n, r)

        pf_points = points[list(previously_failed)]
        remote = []
        for i in new_failures:
            diff = np.abs(pf_points - points[i])
            diff = np.minimum(diff, 1.0 - diff)
            if np.min(np.sum(diff ** 2, axis=1)) > r_n ** 2:
                remote.append(i)

        pooled_count, nuclei = _pooled_nucleus_count(remote, points, r_n, r)
        n_components = len({nuc["component_id"] for nuc in nuclei})
        assert n_components == official, (trial, n_components, official)
        assert pooled_count >= official, (trial, pooled_count, official)

    print("test_pooled_matches_remote_nucleation_on_random_scenarios passed")


def test_peeling_splits_bridged_disjoint_cliques():
    """The S-055 fix: two genuinely disjoint r-cliques that an unrelated
    intervening point bridges into ONE loose (2*r_n) component must count as 2
    nuclei (peeled), even though the old one-per-component rule -- and
    remote_nucleation -- collapse them to 1. Points (x, 0.5), r_n=0.05 (strict),
    loose = 2*r_n = 0.10:
      0.30,0.33  -> strict edge (clique A)
      0.47,0.50  -> strict edge (clique B)
      0.40       -> bridge: > r_n from all (joins no clique) but <= 2*r_n from
                    0.33 and 0.47, chaining A-bridge-B into one loose component."""
    r_n, r = 0.05, 2
    points = np.array([
        [0.30, 0.5], [0.33, 0.5],   # clique A
        [0.47, 0.5], [0.50, 0.5],   # clique B
        [0.40, 0.5],                # loose bridge only
    ])
    idx = [0, 1, 2, 3, 4]

    count, nuclei = _pooled_nucleus_count(idx, points, r_n, r)
    # One loose component (the old rule -- and remote_nucleation -- would say 1)...
    assert len({nuc["component_id"] for nuc in nuclei}) == 1, nuclei
    # ...but peeling recovers the two disjoint nuclei.
    assert count == 2, (count, nuclei)
    member_sets = sorted(sorted(nuc["members"]) for nuc in nuclei)
    assert member_sets == [[0, 1], [2, 3]], member_sets
    assert all(nuc["nuclei_in_component"] == 2 for nuc in nuclei), nuclei
    print("test_peeling_splits_bridged_disjoint_cliques passed")


def test_cross_round_pairing_detected():
    """Two remote failures constructed as if from DIFFERENT rounds (neither round
    alone has >= r remote failures) must still be found as one nucleus once
    pooled -- this is the whole point of Task R."""
    r_n, r = 0.05, 2
    points = np.array([[0.5, 0.5], [0.51, 0.5]] + [[0.9, 0.9]] * 8)
    round_a_remote = [0]
    round_b_remote = [1]

    assert _pooled_nucleus_count(round_a_remote, points, r_n, r)[0] == 0
    assert _pooled_nucleus_count(round_b_remote, points, r_n, r)[0] == 0

    pooled = round_a_remote + round_b_remote
    count, nuclei = _pooled_nucleus_count(pooled, points, r_n, r)
    assert count == 1
    assert set(nuclei[0]["members"]) == {0, 1}
    print("test_cross_round_pairing_detected passed")


def test_merged_component_flag_threshold():
    """possible_merged_component is a coarse size-based triage flag
    (component_size >= 2*r), not a claim of genuine merging. This test just
    confirms the threshold is applied as documented."""
    r_n, r = 0.05, 2
    points_4 = np.array([[0.5, 0.5], [0.51, 0.5], [0.52, 0.5], [0.53, 0.5]])
    count, nuclei = _pooled_nucleus_count([0, 1, 2, 3], points_4, r_n, r)
    assert count == 1
    assert nuclei[0]["component_size"] == 4
    assert nuclei[0]["possible_merged_component"] is True  # 4 >= 2*r

    points_2 = points_4[:2]
    count2, nuclei2 = _pooled_nucleus_count([0, 1], points_2, r_n, r)
    assert count2 == 1
    assert nuclei2[0]["component_size"] == 2
    assert nuclei2[0]["possible_merged_component"] is False  # 2 < 2*r
    print("test_merged_component_flag_threshold passed")


if __name__ == "__main__":
    test_pooled_matches_remote_nucleation_on_random_scenarios()
    test_peeling_splits_bridged_disjoint_cliques()
    test_cross_round_pairing_detected()
    test_merged_component_flag_threshold()
    print("All Task R cross-round tests passed.")
