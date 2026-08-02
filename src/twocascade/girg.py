import math
import numpy as np
from typing import List, Set, Tuple

def sample_torus_points(n: int, rng: np.random.Generator) -> np.ndarray:
    return rng.uniform(0, 1, (n, 2))

def sample_powerlaw_weights(n: int, tau: float, w_min: float, rng: np.random.Generator) -> np.ndarray:
    u = rng.uniform(0, 1, n)
    return w_min * (u ** (-1.0 / (tau - 1.0)))

def sample_girg_adjacency_reference(points: np.ndarray, weights: np.ndarray, alpha_g: float, rng: np.random.Generator) -> List[List[int]]:
    """The original O(n^2) sampler, kept verbatim as the oracle for the indexed one.

    Every pair is evaluated, so this is unambiguously correct and unambiguously
    too slow: an 11x500 sweep at n=10000 is ~2.7e11 pair evaluations. It stays
    here because `sample_girg_adjacency` is now an algorithm rather than a
    transcription of the definition, and an algorithm needs something to be
    checked against. `tests/test_girg.py` compares the two distributionally.
    """
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


# --- the indexed sampler -----------------------------------------------------
#
# The model is p_ij = min(1, (w_i w_j / (n d_ij^2))^alpha), with d the distance
# on the unit torus. That probability is STRICTLY POSITIVE at every distance, so
# the obvious "only look at nearby cells" spatial index does not approximate this
# model — it samples a different one, agreeing on edge count while losing the
# long-range tail. That tail is the entire subject of a GIRG-vs-configuration-
# model comparison, so the truncating version would produce a plausible and wrong
# figure. Nothing here truncates.
#
# The scheme is Bringmann-Keusch-Lengler. Levels l = 2..L carry grids of 2^l
# cells per side. A pair of points is handled at the coarsest level at which
# their cells are non-touching (Chebyshev cell distance >= 2 with the torus wrap);
# pairs still touching at the deepest level L are enumerated directly. Those two
# cases are disjoint and cover every pair exactly once, because cell distance is
# monotone in l: a child pair's distance is at least 2*parent - 1, so the set of
# levels at which two cells touch is a prefix {2..l*-1} and l* is unique.
#
# Within a non-touching cell pair the cells are separated by a known minimum
# distance d_min, which bounds the connection probability from above by
# p_bar = min(1, (W_a W_b / (n d_min^2))^alpha) with W the largest weight in each
# group. Candidates are then drawn by geometric skipping against p_bar and kept
# with probability p_ij / p_bar. Every pair still gets its exact p_ij; the saving
# is that the overwhelming majority of pairs, whose p_bar is tiny, are skipped
# over rather than visited. Points are grouped by weight layer within each cell
# so that one heavy vertex cannot inflate p_bar for its whole cell.


def _cell_layer_groups(cell_points, weights, w_min):
    """Split one cell's point indices into weight layers.

    Layer t holds w in [2^t w_min, 2^(t+1) w_min). Keyed that way so a group is
    homogeneous to within a factor of two, but the bound returned is the group's
    ACTUAL maximum weight, which is tighter than the layer's ceiling and just as
    valid an upper bound.
    """
    groups = {}
    for i in cell_points:
        w = float(weights[i])
        t = int(math.floor(math.log2(w / w_min))) if w > w_min else 0
        g = groups.get(t)
        if g is None:
            groups[t] = g = [[], 0.0]
        g[0].append(i)
        if w > g[1]:
            g[1] = w
    return list(groups.values())


def _torus_cell_gap(a, b, m):
    """Minimum distance along one axis between cell index a and cell index b.

    Cells are half-open intervals of width 1/m, so two cells whose wrapped index
    distance is k are separated by at least (k-1)/m — zero when they touch. The
    wrap is what makes cells on opposite edges of the unit square neighbours, and
    getting it wrong here shows up as a deficit of exactly those edges.
    """
    d = abs(a - b)
    d = min(d, m - d)
    return (d - 1) / m if d > 1 else 0.0


def _torus_cheb(a, b, m):
    d = abs(a - b)
    return min(d, m - d)


def sample_girg_adjacency(points: np.ndarray, weights: np.ndarray, alpha_g: float, rng: np.random.Generator) -> List[List[int]]:
    n = len(points)
    adj: List[List[int]] = [[] for _ in range(n)]
    if n < 2:
        return adj

    # The upper bound relies on x -> x^alpha being increasing. For alpha <= 0 it
    # is not, p_bar would no longer bound p_ij, and every rejection step would be
    # wrong. No caller passes such a value; fall back rather than be silently
    # incorrect if one ever does.
    if alpha_g <= 0:
        return sample_girg_adjacency_reference(points, weights, alpha_g, rng)

    w = np.asarray(weights, dtype=float)
    w_min = float(w.min())
    if not (w_min > 0.0) or not np.isfinite(w).all():
        return sample_girg_adjacency_reference(points, weights, alpha_g, rng)

    xs = np.asarray(points, dtype=float)[:, 0]
    ys = np.asarray(points, dtype=float)[:, 1]

    # Aim for ~4 points per cell at the deepest level, so that the direct
    # enumeration there stays linear in n. L >= 2 because a 2x2 grid has no
    # non-touching cells at all and so could not start the recursion.
    L = max(2, min(8, int(math.ceil(0.5 * math.log2(max(n / 4.0, 4.0))))))

    def cell_index(m):
        cx = np.minimum((xs * m).astype(np.int64), m - 1)
        cy = np.minimum((ys * m).astype(np.int64), m - 1)
        return cx, cy

    # Cell membership per level, plus each point's own cell coordinates.
    cells_at = {}
    coords_at = {}
    for lvl in range(2, L + 1):
        m = 1 << lvl
        cx, cy = cell_index(m)
        coords_at[lvl] = (cx, cy)
        buckets = {}
        for i in range(n):
            buckets.setdefault((int(cx[i]), int(cy[i])), []).append(i)
        cells_at[lvl] = buckets

    n_float = float(n)

    def exact_p(i, j):
        dx = abs(xs[i] - xs[j]); dx = min(dx, 1.0 - dx)
        dy = abs(ys[i] - ys[j]); dy = min(dy, 1.0 - dy)
        d2 = dx * dx + dy * dy
        if d2 == 0.0:
            return 0.0
        base = w[i] * w[j] / (n_float * d2)
        return 1.0 if base >= 1.0 else base ** alpha_g

    def connect(i, j):
        adj[i].append(j)
        adj[j].append(i)

    # --- non-touching cell pairs, level by level ---------------------------
    for lvl in range(2, L + 1):
        m = 1 << lvl
        buckets = cells_at[lvl]
        parent_m = m >> 1
        group_cache = {}

        def groups_of(key, pts):
            g = group_cache.get(key)
            if g is None:
                group_cache[key] = g = _cell_layer_groups(pts, w, w_min)
            return g

        for (ax, ay), a_pts in buckets.items():
            # Candidates are the children of the parent's 3x3 neighbourhood: any
            # cell outside that is handled at a coarser level. Filtering to
            # Chebyshev >= 2 leaves exactly the pairs whose first non-touching
            # level is this one. At lvl == 2 the parent grid is 2x2, where every
            # cell touches every other, so the parent test is vacuous and this
            # level correctly absorbs all remaining pairs.
            pax, pay = ax >> 1, ay >> 1
            # A SET, not a nested loop straight into the body: at lvl == 2 the
            # parent grid is 2x2, so (pax-1) % 2 and (pax+1) % 2 are the same
            # parent and the naive 3x3 sweep would visit — and therefore sample —
            # each candidate cell twice. Every pair between those cells would get
            # two independent chances to connect, roughly doubling long-range
            # edges while leaving short-range ones alone. That is the exact shape
            # of error this whole port is supposed to avoid.
            candidates = set()
            for dpx in (-1, 0, 1):
                for dpy in (-1, 0, 1):
                    qx = (pax + dpx) % parent_m
                    qy = (pay + dpy) % parent_m
                    for bx in (2 * qx, 2 * qx + 1):
                        for by in (2 * qy, 2 * qy + 1):
                            candidates.add((bx, by))

            for (bx, by) in candidates:
                if (bx, by) <= (ax, ay):
                    continue  # unordered pair, visit once
                if max(_torus_cheb(ax, bx, m), _torus_cheb(ay, by, m)) < 2:
                    continue
                b_pts = buckets.get((bx, by))
                if not b_pts:
                    continue
                gx = _torus_cell_gap(ax, bx, m)
                gy = _torus_cell_gap(ay, by, m)
                d_min_sq = gx * gx + gy * gy
                if d_min_sq <= 0.0:
                    continue  # unreachable: Chebyshev >= 2 forces a gap
                for a_idx, wa_max in groups_of((ax, ay), a_pts):
                    for b_idx, wb_max in groups_of((bx, by), b_pts):
                        base = wa_max * wb_max / (n_float * d_min_sq)
                        p_bar = 1.0 if base >= 1.0 else base ** alpha_g
                        na, nb = len(a_idx), len(b_idx)
                        if p_bar >= 1.0:
                            for i in a_idx:
                                for j in b_idx:
                                    if rng.random() < exact_p(i, j):
                                        connect(i, j)
                            continue
                        if p_bar <= 0.0:
                            continue
                        total = na * nb
                        log1m = math.log1p(-p_bar)
                        pos = -1
                        while True:
                            u = rng.random()
                            if u <= 0.0:
                                break
                            pos += 1 + int(math.floor(math.log(u) / log1m))
                            if pos >= total:
                                break
                            i = a_idx[pos // nb]
                            j = b_idx[pos % nb]
                            if rng.random() < exact_p(i, j) / p_bar:
                                connect(i, j)

    # --- touching cells at the deepest level, enumerated exactly ------------
    m = 1 << L
    buckets = cells_at[L]
    for (ax, ay), a_pts in buckets.items():
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                bx = (ax + dx) % m
                by = (ay + dy) % m
                if (bx, by) < (ax, ay):
                    continue
                if (bx, by) == (ax, ay):
                    for u_i in range(len(a_pts)):
                        for v_i in range(u_i + 1, len(a_pts)):
                            i, j = a_pts[u_i], a_pts[v_i]
                            if rng.random() < exact_p(i, j):
                                connect(i, j)
                    continue
                b_pts = buckets.get((bx, by))
                if not b_pts:
                    continue
                for i in a_pts:
                    for j in b_pts:
                        if rng.random() < exact_p(i, j):
                            connect(i, j)

    for lst in adj:
        lst.sort()
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
