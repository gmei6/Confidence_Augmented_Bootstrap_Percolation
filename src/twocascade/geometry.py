import math
import numpy as np
from collections import deque
from dataclasses import dataclass
from typing import List, Dict, Tuple, Set, Optional

from twocascade.reference import Node, CascadeResult

def sample_torus_points(n: int, rng: np.random.Generator) -> np.ndarray:
    """Sample n points uniformly on the unit torus [0, 1)^2."""
    return rng.random((n, 2))

def get_bucket(point: np.ndarray, cell_size: float, num_cells: int) -> Tuple[int, int]:
    x = int(point[0] / cell_size)
    y = int(point[1] / cell_size)
    return (min(x, num_cells - 1), min(y, num_cells - 1))

def _build_bucket_adjacency(points: np.ndarray, radius: float) -> List[List[int]]:
    n = len(points)
    adjacency: List[List[int]] = [[] for _ in range(n)]
    if radius >= 1.0:
        for i in range(n):
            for j in range(n):
                if i != j:
                    adjacency[i].append(j)
        return adjacency
        
    num_cells = max(1, int(1.0 / radius))
    cell_size = 1.0 / num_cells
    radius_sq = radius**2
    
    buckets: Dict[Tuple[int, int], List[Tuple[int, np.ndarray]]] = {}
    for i, p in enumerate(points):
        b = get_bucket(p, cell_size, num_cells)
        if b not in buckets:
            buckets[b] = []
        buckets[b].append((i, p))
        
    for i, p1 in enumerate(points):
        bx, by = get_bucket(p1, cell_size, num_cells)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx = (bx + dx) % num_cells
                ny = (by + dy) % num_cells
                nb = (nx, ny)
                if nb in buckets:
                    for j, p2 in buckets[nb]:
                        if i < j:
                            diff = np.abs(p1 - p2)
                            diff = np.minimum(diff, 1.0 - diff)
                            if diff[0]**2 + diff[1]**2 < radius_sq:
                                adjacency[i].append(j)
                                adjacency[j].append(i)
    return adjacency

def build_rgg_adjacency(points: np.ndarray, radius: float) -> List[List[int]]:
    """Builds random geometric graph adjacency list using a grid-bucket index."""
    return _build_bucket_adjacency(points, radius)

def build_fear_adjacency(points: np.ndarray, ell: float) -> List[List[int]]:
    """Builds fear-radius graph adjacency using grid-bucket index."""
    return _build_bucket_adjacency(points, ell)

def build_soft_rgg_adjacency(points: np.ndarray, r_n: float, alpha_g: float, rng: np.random.Generator) -> List[List[int]]:
    """
    Builds soft RGG adjacency.
    Near field (dist <= r_n): same as hard RGG.
    Far field (dist > r_n): connection prob min(1, (dist/r_n)^-alpha_g).
    """
    n = len(points)
    adjacency: List[List[int]] = [[] for _ in range(n)]
    
    num_cells = max(1, int(1.0 / r_n))
    cell_size = 1.0 / num_cells
    r_n_sq = r_n**2
    
    buckets: Dict[Tuple[int, int], List[Tuple[int, np.ndarray]]] = {}
    for i, p in enumerate(points):
        b = get_bucket(p, cell_size, num_cells)
        if b not in buckets:
            buckets[b] = []
        buckets[b].append((i, p))
        
    for i, p1 in enumerate(points):
        bx, by = get_bucket(p1, cell_size, num_cells)
        
        near_cells = set()
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx = (bx + dx) % num_cells
                ny = (by + dy) % num_cells
                near_cells.add((nx, ny))
                
        for nb in near_cells:
            if nb in buckets:
                for j, p2 in buckets[nb]:
                    if i < j:
                        diff = np.abs(p1 - p2)
                        diff = np.minimum(diff, 1.0 - diff)
                        dist = np.sqrt(diff[0]**2 + diff[1]**2)
                        if dist <= r_n:
                            adjacency[i].append(j)
                            adjacency[j].append(i)
                        else:
                            prob = (dist / r_n)**(-alpha_g)
                            if rng.random() < prob:
                                adjacency[i].append(j)
                                adjacency[j].append(i)
                                
        for nb, cell_points in buckets.items():
            if nb in near_cells:
                continue
            
            cx = (nb[0] + 0.5) * cell_size
            cy = (nb[1] + 0.5) * cell_size
            diff_c = np.abs(p1 - np.array([cx, cy]))
            diff_c = np.minimum(diff_c, 1.0 - diff_c)
            dist_c = np.sqrt(diff_c[0]**2 + diff_c[1]**2)
            
            min_dist = max(r_n, dist_c - cell_size / np.sqrt(2))
            p_max = min(1.0, (min_dist / r_n)**(-alpha_g))
            
            valid_j = [j for j, p2 in cell_points if j > i]
            if not valid_j:
                continue
                
            num_candidates = rng.binomial(len(valid_j), p_max)
            if num_candidates == 0:
                continue
                
            candidates = rng.choice(valid_j, size=num_candidates, replace=False)
            for j in candidates:
                p2 = points[j]
                diff = np.abs(p1 - p2)
                diff = np.minimum(diff, 1.0 - diff)
                dist = np.sqrt(diff[0]**2 + diff[1]**2)
                
                prob = (dist / r_n)**(-alpha_g)
                if rng.random() < prob / p_max:
                    adjacency[i].append(j)
                    adjacency[j].append(i)
                    
    return adjacency

def run_cascade_local_fear(adjacency: List[List[int]], fear_adjacency: List[List[int]], 
                           nodes: List[Node], r: int, seed_indices: List[int], 
                           rng: np.random.Generator, record_history: bool,
                           window_len: int = 1, weights: Optional[List[float]] = None) -> CascadeResult:
    """
    EXPERIMENTAL VARIANT ENGINE
    Runs the two channel cascade with a LOCAL fear field.
    """
    if window_len < 1:
        raise ValueError("window_len must be >= 1")
    if weights is not None:
        if len(weights) != window_len:
            raise ValueError(f"Length of weights ({len(weights)}) must match window_len ({window_len})")
        if any(w < 0 for w in weights):
            raise ValueError("All weights must be non-negative")
        if not math.isclose(sum(weights), 1.0, abs_tol=1e-9):
            raise ValueError("Weights must sum to 1.0")
    else:
        weights = [1.0 / window_len] * window_len

    n = len(nodes)

    for i in seed_indices:
        nodes[i].failed = True
    
    for i in seed_indices:
        for neighbor_index in adjacency[i]:
            nodes[neighbor_index].failed_neighbor_count += 1
            
    total_failed = sum(1 for node in nodes if node.failed)
    rounds_completed = 0
    history = [total_failed] if record_history else []
    
    failures_per_round = deque([set(seed_indices)], maxlen=window_len)
    
    while any(len(fs) > 0 for fs in failures_per_round):
        if total_failed == n:
            break

        newly_failing_nodes = []
        for node in nodes:
            if node.failed:
                continue
            
            effective_failed_neighbor_count = node.failed_neighbor_count
            fails_by_solvency = effective_failed_neighbor_count >= r

            # Local fear calculation
            local_fear = 0.0
            fear_ball_size = len(fear_adjacency[node.index]) + 1
            for k in range(1, window_len + 1):
                if k <= len(failures_per_round):
                    failed_set_t = failures_per_round[-k]
                    # Count how many in fear_adjacency + self failed at t
                    # (self can't fail at t if it's currently being evaluated, but we include it in denominator)
                    count_in_ball = sum(1 for j in fear_adjacency[node.index] if j in failed_set_t)
                    local_fear += weights[k - 1] * (count_in_ball / fear_ball_size)
            
            fear_failure_probability = node.individual_fear * local_fear
            fails_by_fear = (fear_failure_probability > 0.0 and rng.random() < fear_failure_probability)

            if fails_by_solvency or fails_by_fear:
                newly_failing_nodes.append(node)

        new_failures_this_round = set()
        for node in newly_failing_nodes:
            node.failed = True
            new_failures_this_round.add(node.index)
            for neighbor_index in adjacency[node.index]:
                nodes[neighbor_index].failed_neighbor_count += 1

        failures_per_round.append(new_failures_this_round)

        if len(failures_per_round) == window_len and all(len(fs) == 0 for fs in failures_per_round):
            break

        total_failed += len(newly_failing_nodes)
        rounds_completed += 1
        if record_history:
            history.append(total_failed)

    final_failed_fraction = total_failed / n

    return CascadeResult(
        final_failed_fraction=final_failed_fraction,
        total_failed=total_failed,
        rounds_completed=rounds_completed,
        history=history,
    )

import networkx as nx

def remote_failures(new_failures: List[int], previously_failed: Set[int], points: np.ndarray, r_n: float) -> int:
    """Number of new failures at distance > r_n from any previously failed node."""
    if not previously_failed or not new_failures:
        return 0
    count = 0
    pf_points = points[list(previously_failed)]
    for i in new_failures:
        p1 = points[i]
        diff = np.abs(pf_points - p1)
        diff = np.minimum(diff, 1.0 - diff)
        dist_sq = np.sum(diff**2, axis=1)
        if np.min(dist_sq) > r_n**2:
            count += 1
    return count

def coverage_entropy(new_failures: List[int], points: np.ndarray) -> float:
    """Shannon entropy of failure distribution on 16x16 grid."""
    if not new_failures:
        return 0.0
    grid_counts = np.zeros((16, 16))
    for i in new_failures:
        p = points[i]
        x = min(15, int(p[0] * 16))
        y = min(15, int(p[1] * 16))
        grid_counts[x, y] += 1
    
    probs = grid_counts[grid_counts > 0] / len(new_failures)
    entropy = -np.sum(probs * np.log(probs))
    return entropy / np.log(256)

def front_radius(new_failures: List[int], points: np.ndarray, seed_indices: List[int]) -> float:
    """0.9 quantile of distance from seed centroid to new failures."""
    if not new_failures or not seed_indices:
        return 0.0
    ref = points[seed_indices[0]]
    diffs = points[seed_indices] - ref
    diffs = diffs - np.round(diffs)
    centroid = (ref + np.mean(diffs, axis=0)) % 1.0
    
    diff_fail = np.abs(points[new_failures] - centroid)
    diff_fail = np.minimum(diff_fail, 1.0 - diff_fail)
    dists = np.sqrt(np.sum(diff_fail**2, axis=1))
    return float(np.quantile(dists, 0.9))

def remote_nucleation(new_failures: List[int], previously_failed: Set[int], points: np.ndarray, r_n: float, r: int) -> int:
    if not previously_failed or len(new_failures) == 0:
        return 0
    remote = []
    pf_points = points[list(previously_failed)]
    for i in new_failures:
        p1 = points[i]
        diff = np.abs(pf_points - p1)
        diff = np.minimum(diff, 1.0 - diff)
        dist_sq = np.sum(diff**2, axis=1)
        if np.min(dist_sq) > r_n**2:
            remote.append(i)
            
    if len(remote) < r:
        return 0
        
    G = nx.Graph()
    G.add_nodes_from(remote)
    rem_points = points[remote]
    n_rem = len(remote)
    for i in range(n_rem):
        for j in range(i+1, n_rem):
            diff = np.abs(rem_points[i] - rem_points[j])
            diff = np.minimum(diff, 1.0 - diff)
            if np.sum(diff**2) <= (2*r_n)**2:
                G.add_edge(remote[i], remote[j])
                
    nuclei_count = 0
    from networkx.algorithms.clique import find_cliques
    for comp in nx.connected_components(G):
        if len(comp) >= r:
            C = nx.Graph()
            comp_list = list(comp)
            C.add_nodes_from(comp_list)
            c_points = points[comp_list]
            for i in range(len(comp_list)):
                for j in range(i+1, len(comp_list)):
                    diff = np.abs(c_points[i] - c_points[j])
                    diff = np.minimum(diff, 1.0 - diff)
                    if np.sum(diff**2) <= r_n**2:
                        C.add_edge(comp_list[i], comp_list[j])
            
            max_clique = max((len(c) for c in find_cliques(C)), default=0)
            if max_clique >= r:
                nuclei_count += 1
                
    return nuclei_count

