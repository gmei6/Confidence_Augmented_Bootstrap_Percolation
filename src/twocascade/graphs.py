import numpy as np

def sample_powerlaw_degrees(n: int, tau: float, d_min: int, rng: np.random.Generator) -> list[int]:
    """
    Sample n degrees from a power-law distribution P(D=k) ∝ k^(-tau) for k >= d_min.
    If the sum of degrees is odd, add one stub to a uniformly chosen vertex.
    """
    k_max = max(1000000, n * 10)
    k_vals = np.arange(d_min, k_max + 1)
    probs = k_vals ** (-tau)
    probs /= probs.sum()
    
    degrees = rng.choice(k_vals, size=n, p=probs)
    
    if degrees.sum() % 2 != 0:
        idx = rng.integers(0, n)
        degrees[idx] += 1
        
    return degrees.tolist()

def sample_configuration_model(degrees: list[int], rng: np.random.Generator) -> list[list[int]]:
    """
    Generate an erased configuration model graph from the given degree sequence.
    Returns an adjacency list (simple graph).
    """
    n = len(degrees)
    
    stubs = np.empty(sum(degrees), dtype=int)
    offset = 0
    for i, d in enumerate(degrees):
        stubs[offset:offset + d] = i
        offset += d
        
    rng.shuffle(stubs)
    
    adj_sets = [set() for _ in range(n)]
    
    for i in range(0, len(stubs), 2):
        u = stubs[i]
        v = stubs[i+1]
        if u != v:
            adj_sets[u].add(v)
            adj_sets[v].add(u)
            
    return [list(neighbors) for neighbors in adj_sets]

def sample_degree_dependent_fears(
    degrees: list[int], mu_bar: float, gamma: float, kappa: float, rng: np.random.Generator
) -> tuple[list[float], dict]:
    """
    Sample degree-dependent fears from a Beta distribution.
    f_i | d_i ~ Beta(mu(d_i) * kappa, (1 - mu(d_i)) * kappa)

    For gamma != 0, mu(d) comes from an iterative water-filling renormalization: nodes whose
    raw mu(d) would exceed the (1 - epsilon) cap are pinned at the cap, and the remaining
    nodes' weights (d_i / <D>)^gamma are rescaled so the *population* mean lands back on
    mu_bar -- unlike the single-pass Z_n normalization, whose Z_n includes soon-to-be-capped
    nodes and so silently undershoots mu_bar for gamma > 0 on heavy-tailed degree sequences
    (see docs/queue/reports/task_n_phase2_report.md).

    Returns:
        fears: list of fear values
        stats: dict with cap_hits, realized_mu_bar, realized_mu_star, degenerate,
               infeasible, cap_fill_iterations, non_finite_weight_count.

               `infeasible` is the ONLY flag that means the aggregate realized_mu_bar may
               not track mu_bar -- it is True iff mu_bar is structurally unreachable given
               this weight shape even after full redistribution (including the case where
               forced-cap non-finite-weight nodes alone already exceed mu_bar*n).
               `non_finite_weight_count > 0` means one or more nodes had a non-finite raw
               weight (e.g. a zero-degree node under gamma < 0) and were pinned at the cap
               as a defensive fallback; BY ITSELF (i.e. with infeasible == False) this does
               NOT compromise the aggregate mean, only the fact that those specific nodes'
               mu_d came from a fallback rather than the normal formula. `degenerate` is
               `infeasible or (non_finite_weight_count > 0)`, kept for convenience -- always
               check `infeasible` directly before trusting realized_mu_bar, never `degenerate`.

               Only cap_hits/realized_mu_bar/realized_mu_star are currently read by any
               caller (scripts/analyze_task_n.py's cap_diagnostics); infeasible/degenerate/
               cap_fill_iterations/non_finite_weight_count are diagnostic and not yet wired
               into any production analysis path -- available for a future caller to use,
               not proof that one already does.
    """
    n = len(degrees)
    if n == 0:
        raise ValueError("sample_degree_dependent_fears: degrees must be non-empty")

    if mu_bar == 0.0:
        # mu_bar == 0.0 means every individual fear must be exactly 0 -- there is no valid
        # redistribution that gives some nodes positive fear while others compensate
        # negative (fear can't go below 0), so the tilt/cap machinery below is not just
        # skippable but *inapplicable*. Return trivial, self-consistent stats rather than
        # building them from an intermediate mu_d that the all-zero fears then override.
        stats = {
            "cap_hits": 0,
            "realized_mu_bar": 0.0,
            "realized_mu_star": 0.0,
            "infeasible": False,
            "degenerate": False,
            "cap_fill_iterations": 0,
            "non_finite_weight_count": 0,
        }
        return [0.0] * n, stats

    deg_array = np.array(degrees, dtype=float)
    avg_d = deg_array.mean()

    epsilon = 1e-3
    cap = 1 - epsilon

    infeasible = False
    cap_fill_iterations = 0
    non_finite_weight_count = 0

    if gamma == 0:
        mu_d = np.full(n, mu_bar)
        if mu_bar > cap:
            # Consistency with the gamma != 0 path: the population target itself already
            # exceeds the cap, so every node's fear silently undershoots mu_bar -- flag it
            # rather than leaving this branch as the one silent-undershoot case in the
            # function.
            infeasible = True
    else:
        with np.errstate(divide="ignore", invalid="ignore"):
            # A zero-degree node with gamma < 0 legitimately produces +inf here (0**negative);
            # handled explicitly via the isfinite guard below, so the warning is suppressed
            # rather than masking a real error.
            term = (deg_array / avg_d) ** gamma
        non_finite = ~np.isfinite(term)
        non_finite_weight_count = int(non_finite.sum())
        if non_finite_weight_count > 0:
            # e.g. a zero-degree node under gamma < 0 -> term = inf, i.e. unbounded relative
            # weight. The correct water-filling limit for that is to pin the node at the cap
            # permanently. This does NOT by itself set `infeasible` -- if capping these nodes
            # still leaves the target reachable for the rest, the aggregate mean comes out
            # exact (see the loop below, which sets `infeasible` independently if it doesn't).
            term = np.where(non_finite, 0.0, term)  # placeholder; value is irrelevant, these
                                                      # nodes are forced into `capped` below and
                                                      # never re-tested against it (see the `|
                                                      # non_finite` in the membership test)

        capped = non_finite.copy()
        tol = 1e-9
        target_total = mu_bar * n
        k = 0.0
        # Capped-set membership is monotone non-decreasing in k (adding a node to the capped
        # set only raises the mass-per-remaining-weight ratio for the rest), so it can grow
        # at most n times before stabilizing -- n+1 is a proven bound, not a guessed one.
        max_iters = n + 1
        for it in range(max_iters):
            n_capped = int(capped.sum())
            w_uncapped_sum = term[~capped].sum()
            target_mass = target_total - n_capped * cap
            if w_uncapped_sum <= 0 or target_mass < 0:
                # mu_bar is structurally unreachable under this weight shape even giving
                # every uncapped node its full share (this also correctly catches the case
                # where forced-cap non-finite-weight nodes ALONE already exceed mu_bar*n) --
                # a legitimate edge case, not a bug. This is the only place `infeasible` is
                # set, so it precisely means "the aggregate mean may not track mu_bar."
                # `capped` and `k` below are left at whatever they were at the END of the
                # last iteration that WAS feasible (or the initial non_finite/0.0 seed, if
                # infeasible on iteration 0) -- a matched pair from that iteration, not a
                # stale mismatch: no k exists that makes *this* iteration's target_mass work,
                # by definition, so falling back to the last valid (capped, k) pair is the
                # intended best-effort result, not an accident of break-before-reassignment.
                infeasible = True
                cap_fill_iterations = it
                break
            k = target_mass / w_uncapped_sum
            # non_finite nodes have a placeholder term of 0.0, so `k * term` would test as
            # "uncapped" here despite their true (infinite) weight -- OR them in unconditionally
            # so they can never leave the capped set once forced in.
            new_capped = ((k * term) > (cap + tol)) | non_finite
            if np.array_equal(new_capped, capped):
                cap_fill_iterations = it
                break
            capped = new_capped
        else:
            raise RuntimeError(
                "sample_degree_dependent_fears: water-filling failed to converge within "
                f"the proven n+1={max_iters} bound -- this indicates a real bug, not a "
                "legitimate degenerate case."
            )

        mu_d = np.where(capped, cap, k * term)

    if gamma == 0:
        # No water-filling ran; mu_d is still the raw (unclipped) uniform value here.
        cap_hits = int((mu_d > cap).sum())
    else:
        # mu_d already has capped nodes pinned at exactly `cap` by construction (the
        # np.where above), so re-testing `mu_d > cap` here would always read zero --
        # cap_hits must come from the water-filling loop's own `capped` determination.
        cap_hits = int(capped.sum())

    mu_d = np.minimum(mu_d, cap)

    realized_mu_bar = float(mu_d.mean())
    if avg_d > 0:
        realized_mu_star = float(np.mean(mu_d * deg_array) / avg_d)
    else:
        realized_mu_star = 0.0

    stats = {
        "cap_hits": cap_hits,
        "realized_mu_bar": realized_mu_bar,
        "realized_mu_star": realized_mu_star,
        "infeasible": infeasible,
        "degenerate": infeasible or (non_finite_weight_count > 0),
        "cap_fill_iterations": cap_fill_iterations,
        "non_finite_weight_count": non_finite_weight_count,
    }

    # For safety, avoid mu_d exactly 0 for Beta parameters
    mu_d = np.maximum(mu_d, 1e-9)

    fears = rng.beta(mu_d * kappa, (1 - mu_d) * kappa)
    return fears.tolist(), stats
