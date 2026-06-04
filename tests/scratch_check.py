import numpy as np
import math
from twocascade.reference import (
    sample_gnp_adjacency,
    sample_individual_fears,
    make_nodes,
    choose_seed,
    run_cascade,
)

def final_failed_fraction(n, p, r, mu, a, rng):
    adjacency = sample_gnp_adjacency(n, p, rng)
    fears = sample_individual_fears(n, mean_fear=mu, concentration=50.0, rng=rng)
    nodes = make_nodes(fears)
    seed_indices = choose_seed(n, seed_size=a, adjacency=adjacency, rng=rng, target_high_degree=False)
    result = run_cascade(adjacency, nodes, r=r, seed_indices=seed_indices, rng=rng, record_history=False)
    return result.final_failed_fraction

def estimate_p_systemic(n, p, r, mu, a, reps, rng):
    fractions = [final_failed_fraction(n, p, r, mu, a, rng) for _ in range(reps)]
    return np.mean(np.array(fractions) >= 0.5)

def find_empirical_threshold(n, p, r, mu, reps, rng):
    # Search around the conjectured value: a_c(mu) = a_c(0) * (1-mu)**(r/(r-1))
    t_c_val = (math.factorial(r - 1) / (n * p ** r)) ** (1.0 / (r - 1))
    ac_zero = (1.0 - 1.0 / r) * t_c_val
    conjectured_ac = ac_zero * (1.0 - mu)**(r / (r - 1))
    
    print(f"--- Sweep for mu={mu}, conjectured ac={conjectured_ac:.2f} (ac_zero={ac_zero:.2f}) ---")
    
    # Let's sweep seed sizes in a wide range around conjectured_ac
    start_a = max(r, int(conjectured_ac * 0.4))
    end_a = max(r + 5, int(conjectured_ac * 2.2))
    seed_range = list(range(start_a, end_a + 1))
    
    results = []
    for a in seed_range:
        p_sys = estimate_p_systemic(n, p, r, mu, a, reps, rng)
        results.append((a, p_sys))
        print(f"  seed a={a}: P(sys)={p_sys:.3f}")
        
    # Find interpolated crossing at 0.5
    for i in range(1, len(results)):
        a_prev, p_prev = results[i-1]
        a_curr, p_curr = results[i]
        if p_prev < 0.5 <= p_curr:
            t = (0.5 - p_prev) / (p_curr - p_prev)
            return a_prev + t * (a_curr - a_prev)
    return None

if __name__ == "__main__":
    r = 2
    n_ref = 4000
    alpha = 0.7
    target_mean_degree = 10.0
    beta = target_mean_degree / n_ref**(1.0 - alpha)
    
    rng = np.random.default_rng(20260604)
    reps = 80
    
    for n in [1000, 2000, 4000]:
        p = beta * n**(-alpha)
        print(f"\n==================== N = {n} ====================")
        th_0 = find_empirical_threshold(n, p, r, 0.0, reps, rng)
        th_25 = find_empirical_threshold(n, p, r, 0.25, reps, rng)
        th_50 = find_empirical_threshold(n, p, r, 0.5, reps, rng)
        
        print(f"\nResults for N = {n}:")
        print(f"  th(0)   = {th_0}")
        print(f"  th(0.25) = {th_25}")
        print(f"  th(0.5)  = {th_50}")
        
        if th_0 is not None:
            if th_25 is not None:
                ratio_25 = th_25 / th_0
                expected_25 = (1 - 0.25)**(r/(r-1))
                print(f"  mu=0.25 ratio: {ratio_25:.3f} vs expected: {expected_25:.3f} (diff: {ratio_25 - expected_25:.3f})")
            if th_50 is not None:
                ratio_50 = th_50 / th_0
                expected_50 = (1 - 0.5)**(r/(r-1))
                print(f"  mu=0.5 ratio: {ratio_50:.3f} vs expected: {expected_50:.3f} (diff: {ratio_50 - expected_50:.3f})")

