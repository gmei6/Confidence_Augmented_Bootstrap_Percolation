import math
import numpy as np
from typing import List, Set, Tuple

def sample_torus_points(n: int, rng: np.random.Generator) -> np.ndarray:
    return rng.uniform(0, 1, (n, 2))

def sample_powerlaw_weights(n: int, tau: float, w_min: float, rng: np.random.Generator) -> np.ndarray:
    u = rng.uniform(0, 1, n)
    return w_min * (u ** (-1.0 / (tau - 1.0)))

def sample_girg_adjacency_slow(points: np.ndarray, weights: np.ndarray, alpha_g: float, rng: np.random.Generator) -> List[List[int]]:
    n = len(points)
    adj = [[] for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            dx = abs(points[i,0] - points[j,0])
            dy = abs(points[i,1] - points[j,1])
            dx = min(dx, 1.0 - dx)
            dy = min(dy, 1.0 - dy)
            dist_sq = dx*dx + dy*dy
            if dist_sq == 0:
                continue
            p = min(1.0, (weights[i] * weights[j] / (n * dist_sq)) ** alpha_g)
            if rng.random() < p:
                adj[i].append(j)
                adj[j].append(i)
    return adj

def sample_girg_adjacency(points: np.ndarray, weights: np.ndarray, alpha_g: float, rng: np.random.Generator) -> List[List[int]]:
    """Block-vectorized, exact GIRG adjacency sampler.

    Samples from exactly the same per-pair measure as sample_girg_adjacency_slow:
    p_ij = min(1, (w_i * w_j / (n * d^2)) ** alpha_g) with torus distance d,
    independently across pairs (i, j). RNG consumption order differs from the
    scalar loop (one block draw per row-block instead of one draw per pair), so
    equivalence is statistical, not bit-identical — same standard as the C++
    cross-validation checks (constitution §5.4).

    Constitution §I (no dense n x n adjacency): this function never
    materializes an (n, n) array. Per-block temporaries are shape
    (block_rows, n - start) at most, with block_rows << n, so peak memory is
    O(block * n), not O(n^2).
    """
    n = len(points)
    # min(1, x)**a == min(1, x**a) only for a > 0; the model requires it anyway.
    assert alpha_g > 0, "sample_girg_adjacency requires alpha_g > 0"
    adj = [[] for _ in range(n)]
    if n < 2:
        return adj

    x = points[:, 0]
    y = points[:, 1]
    block_size = 512

    for start in range(0, n, block_size):
        end = min(start + block_size, n)
        rows = np.arange(start, end)          # row indices in this block
        cols = np.arange(start, n)            # only j >= start can satisfy j > i for i in [start, end)

        # Block temporary of shape (block_rows, len(cols)) <= (block_size, n) —
        # never the full n x n matrix. Satisfies the no-dense-adjacency rule.
        dx = np.abs(x[rows, None] - x[None, cols])
        dx = np.minimum(dx, 1.0 - dx)
        dy = np.abs(y[rows, None] - y[None, cols])
        dy = np.minimum(dy, 1.0 - dy)
        d2 = dx * dx + dy * dy

        zero_dist = (d2 == 0.0)
        d2_safe = np.where(zero_dist, 1.0, d2)  # avoid div-by-zero; overwritten below

        wi = weights[rows, None]
        wj = weights[None, cols]
        p = np.minimum(1.0, (wi * wj) / (n * d2_safe)) ** alpha_g

        # Only j > i pairs are valid; zero-distance pairs are skipped, matching
        # the slow loop's `if dist_sq == 0: continue`.
        j_gt_i = cols[None, :] > rows[:, None]
        p = np.where(j_gt_i & ~zero_dist, p, 0.0)

        u = rng.random(p.shape)  # one rng call per block
        local_rows, local_cols = np.nonzero(u < p)
        for lr, lc in zip(local_rows, local_cols):
            i = start + int(lr)
            j = start + int(lc)
            adj[i].append(j)
            adj[j].append(i)

    return adj

def sample_degree_dependent_fears(weights: np.ndarray, mu_bar: float, gamma: float, kappa: float, rng: np.random.Generator) -> List[float]:
    n = len(weights)
    mean_w = np.mean(weights)
    z_n = np.mean((weights / mean_w) ** gamma)
    fears = []
    eps = 1e-3
    for w in weights:
        mu_w = min(mu_bar * ((w / mean_w) ** gamma) / z_n, 1.0 - eps)
        f = rng.beta(mu_w * kappa, (1.0 - mu_w) * kappa)
        fears.append(f)
    return fears

def build_fear_adjacency(points: np.ndarray, ell: float) -> List[List[int]]:
    n = len(points)
    adj = [[] for _ in range(n)]
    ell_sq = ell * ell
    for i in range(n):
        for j in range(i+1, n):
            dx = abs(points[i,0] - points[j,0])
            dy = abs(points[i,1] - points[j,1])
            dx = min(dx, 1.0 - dx)
            dy = min(dy, 1.0 - dy)
            if dx*dx + dy*dy <= ell_sq:
                adj[i].append(j)
                adj[j].append(i)
    return adj

class Node:
    def __init__(self, index: int, individual_fear: float):
        self.index = index
        self.individual_fear = individual_fear
        self.failed = False
        self.failed_neighbor_count = 0

def run_cascade_local_fear(adjacency: List[List[int]], fear_adjacency: List[List[int]], 
                           nodes: List[Node], r: int, seed_indices: List[int], rng: np.random.Generator):
    n = len(nodes)
    
    for i in seed_indices:
        nodes[i].failed = True
        for neighbor in adjacency[i]:
            nodes[neighbor].failed_neighbor_count += 1
            
    total_failed = len(seed_indices)
    history = [total_failed]
    failures_last_round = set(seed_indices)
    
    # Precompute fear ball sizes
    # A node is in its own fear ball conceptually? 
    # Actually Q5 says "#{j in B(x_i, ell)}". 
    # Usually the node itself is in B(x_i, ell), so denominator is len(fear_adjacency[i]) + 1
    fear_ball_sizes = [len(fear_adjacency[i]) + 1 for i in range(n)]
    
    active = len(failures_last_round) > 0
    rounds = 0
    
    while active:
        active = False
        rounds += 1
        
        if total_failed == n:
            break
            
        newly_failing_nodes = []
        for node in nodes:
            if node.failed:
                continue
                
            fails_by_solvency = node.failed_neighbor_count >= r
            
            # compute local fear
            # How many neighbors in fear_adjacency failed last round?
            # Plus the node itself? But the node is not failed if we are here.
            local_fear_count = sum(1 for neighbor in fear_adjacency[node.index] if neighbor in failures_last_round)
            g_t_i = local_fear_count / fear_ball_sizes[node.index]
            
            fear_failure_probability = node.individual_fear * g_t_i
            fails_by_fear = (fear_failure_probability > 0.0 and rng.random() < fear_failure_probability)
            
            if fails_by_solvency or fails_by_fear:
                newly_failing_nodes.append(node)
                
        failures_last_round = set()
        for node in newly_failing_nodes:
            node.failed = True
            failures_last_round.add(node.index)
            for neighbor in adjacency[node.index]:
                nodes[neighbor].failed_neighbor_count += 1
                
        if len(newly_failing_nodes) > 0:
            active = True
            total_failed += len(newly_failing_nodes)
            history.append(total_failed)
            
    return total_failed / n, rounds, history
