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
    mu(d) = min(mu_bar * (d / <D>)^gamma / Z_n(gamma), 1 - epsilon)
    where Z_n(gamma) = 1/n * sum((d_i / <D>)^gamma)
    
    Returns:
        fears: list of fear values
        stats: dictionary with cap_hits, realized_mu_bar, realized_mu_star
    """
    n = len(degrees)
    deg_array = np.array(degrees, dtype=float)
    avg_d = deg_array.mean()
    
    epsilon = 1e-3
    
    if gamma == 0:
        mu_d = np.full(n, mu_bar)
    else:
        term = (deg_array / avg_d) ** gamma
        Z_n = term.mean()
        mu_d = mu_bar * term / Z_n
        
    cap_mask = mu_d > (1 - epsilon)
    cap_hits = int(cap_mask.sum())
    
    mu_d = np.minimum(mu_d, 1 - epsilon)
    
    realized_mu_bar = float(mu_d.mean())
    if avg_d > 0:
        realized_mu_star = float(np.mean(mu_d * deg_array) / avg_d)
    else:
        realized_mu_star = 0.0
        
    stats = {
        "cap_hits": cap_hits,
        "realized_mu_bar": realized_mu_bar,
        "realized_mu_star": realized_mu_star
    }
    
    if mu_bar == 0.0:
        return [0.0] * n, stats

    # For safety, avoid mu_d exactly 0 for Beta parameters
    mu_d = np.maximum(mu_d, 1e-9)

    fears = rng.beta(mu_d * kappa, (1 - mu_d) * kappa)
    return fears.tolist(), stats
