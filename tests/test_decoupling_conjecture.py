import math
import numpy as np
import scipy.stats as stats
import pytest
from twocascade.reference import sample_gnp_adjacency, sample_individual_fears

def run_sequential_fifo_cascade(n: int, p: float, r: int, seed_size: int, 
                                 individual_fears: list[float], rng: np.random.Generator) -> tuple[list[int], int, list[int]]:
    """
    Runs one realization of the coupled sequential FIFO cascade model.
    
    This function implements the sequential edge-exposure process mapped to discrete 
    generations as formulated in Section 2 of the Janson reformulation document. 
    It exposes edges from active nodes in FIFO queue order, tracks generation 
    sizes, and updates the global fear field g_k at generational boundaries.
    
    Parameters:
        n: System size.
        p: Solvency edge probability.
        r: Solvency threshold.
        seed_size: Number of initial seed failures.
        individual_fears: List of beta-distributed node susceptibilities.
        rng: Random number generator.
        
    Returns:
        Y: List of activation steps for all nodes (with 0 for seed nodes).
        T_halt: Cumulative steps at halting.
        a_g: List of generation sizes.
    """
    adjacency = sample_gnp_adjacency(n, p, rng)
    seed_indices = rng.choice(n, size=seed_size, replace=False).tolist()
    
    active = set(seed_indices)
    used = []
    
    T = [seed_size]
    a_g = [seed_size]
    
    M = [0] * n
    U = rng.uniform(0, 1, size=(n, 2 * n + 5))
    
    for u in seed_indices:
        used.append(u)
        for neighbor in adjacency[u]:
            M[neighbor] += 1
            
    Y = [2 * n] * n
    for u in seed_indices:
        Y[u] = 0
        
    k = 1
    while True:
        T_prev = T[k-1]
        T_prev2 = T[k-2] if k >= 2 else 0
        
        S_k = []
        for i in range(n):
            if i not in active and M[i] >= r:
                S_k.append(i)
                # Find the step at which the r-th neighbor of i was processed
                count = 0
                activation_step = T_prev
                for step, u in enumerate(used):
                    if u in adjacency[i]:
                        count += 1
                        if count == r:
                            activation_step = step + 1
                            break
                Y[i] = activation_step
                
        a_prev = a_g[k-1]
        g_k = a_prev / n
        
        F_k = []
        for i in range(n):
            if i not in active and i not in S_k:
                if U[i, k] < individual_fears[i] * g_k:
                    F_k.append(i)
                    Y[i] = T_prev
                    
        G_k = S_k + F_k
        a_k = len(G_k)
        
        if a_k == 0:
            T.append(T_prev)
            a_g.append(0)
            break
            
        for u in G_k:
            active.add(u)
            used.append(u)
            for neighbor in adjacency[u]:
                M[neighbor] += 1
                
        T.append(T_prev + a_k)
        a_g.append(a_k)
        k += 1
        if k >= 2 * n:
            break
            
    return Y, T[-1], a_g

def get_survival_probs(n: int, p: float, r: int, seed_size: int, mean_fear: float, 
                       concentration: float, trials: int, rng: np.random.Generator) -> tuple[list[int], list[int]]:
    """
    Generates samples of activation times from both the coupled sequential process 
    and the independent decoupled geometric-solvency clock process.
    
    This matches the independent limit derivation in Section 5 of the reformulation doc.
    
    Parameters:
        n: System size.
        p: Edge probability.
        r: Solvency threshold.
        seed_size: Seed size.
        mean_fear: Mean individual fear (mu).
        concentration: Beta concentration parameter (kappa).
        trials: Number of simulation trials.
        rng: Random number generator.
        
    Returns:
        coupled_times: Activation steps for non-seeds in the coupled system.
        decoupled_times: Activation steps for non-seeds in the decoupled system.
    """
    coupled_times = []
    decoupled_times = []
    
    for _ in range(trials):
        fears = sample_individual_fears(n, mean_fear, concentration, rng)
        Y_coupled, T_halt, _ = run_sequential_fifo_cascade(n, p, r, seed_size, fears, rng)
        
        non_seeds = [i for i in range(n) if Y_coupled[i] > 0]
        for idx in non_seeds:
            coupled_times.append(min(Y_coupled[idx], T_halt + 1))
            
        for idx in non_seeds:
            f_i = fears[idx]
            if f_i > 0:
                y_fear = rng.geometric(f_i / n) if f_i / n < 1.0 else 1
            else:
                y_fear = float('inf')
                
            marks = 0
            y_solv = float('inf')
            for step in range(1, T_halt + 2):
                if rng.random() < p:
                    marks += 1
                if marks >= r:
                    y_solv = step
                    break
            y_ind = min(y_solv, y_fear)
            decoupled_times.append(min(y_ind, T_halt + 1))
            
    return coupled_times, decoupled_times

def test_decoupling_conjecture():
    """Numerically verifies the Asymptotic Decoupling Conjecture via Kolmogorov-Smirnov test."""
    # Use deterministic seeding for strict reproducibility per §5.4
    rng = np.random.default_rng(42)
    r = 2
    mean_fear = 0.3  # Mean individual susceptibility (mu = 0.3)
    concentration = 10.0  # Beta concentration parameter (kappa = 10.0)
    trials = 30  # Number of trials is chosen to yield a statistically large sample (~30,000 steps)
    
    # We test at system size N = 1000 to observe asymptotic decoupling behavior
    n = 1000
    p = 8.0 / n  # Solvency mean degree of 8.0 is in the subcritical solvency regime
    seed_size = int(math.ceil(2.0 * n**0.3))
    
    coupled, decoupled = get_survival_probs(n, p, r, seed_size, mean_fear, concentration, trials, rng)
    ks_stat, _ = stats.ks_2samp(coupled, decoupled)
    
    # Assert that the maximum vertical distance (KS statistic) between the two CDFs is small.
    # A threshold of 0.05 is chosen because the sample size is large (N_sample ~ 30000),
    # meaning the KS distance verifies that the coupled sequential process concentrates
    # and decouples near the independent geometric-solvency limit in the thermodynamic limit.
    assert ks_stat < 0.05, f"KS statistic {ks_stat:.4f} is too large, decoupling check failed"
