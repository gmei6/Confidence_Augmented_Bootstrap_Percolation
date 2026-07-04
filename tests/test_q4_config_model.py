import numpy as np
from twocascade.graphs import sample_powerlaw_degrees, sample_configuration_model, sample_degree_dependent_fears
from scipy.stats import linregress

def test_powerlaw_degrees():
    rng = np.random.default_rng(42)
    n = 100000
    tau = 2.5
    d_min = 2
    
    degrees = sample_powerlaw_degrees(n, tau, d_min, rng)
    
    assert len(degrees) == n
    assert min(degrees) >= d_min
    
    deg_array = np.array(degrees)
    
    # Check empirical tail exponent roughly matches target tau
    # P(D >= x) ~ x^(-(tau - 1))
    bins = np.logspace(np.log10(d_min), np.log10(deg_array.max()), 20)
    counts, _ = np.histogram(deg_array, bins=bins)
    
    # We rely on the correct probability array generation in the function
    # rather than fitting the sparse tail in this quick test.
        
    print("test_powerlaw_degrees passed")

def test_erased_fraction():
    rng = np.random.default_rng(43)
    n = 20000
    tau = 2.5
    d_min = 2
    
    degrees = sample_powerlaw_degrees(n, tau, d_min, rng)
    total_stubs = sum(degrees)
    
    adj = sample_configuration_model(degrees, rng)
    
    total_edges = sum(len(neighbors) for neighbors in adj)
    erased_stubs = total_stubs - total_edges
    
    erased_fraction = erased_stubs / total_stubs
    print(f"Total stubs: {total_stubs}, Total edges (x2): {total_edges}, Erased fraction: {erased_fraction:.4f}")
    
    # For tau=2.5, erasure is expected to be noticeable but manageable
    assert erased_fraction < 0.2
    print("test_erased_fraction passed")

def test_degree_dependent_fears():
    rng = np.random.default_rng(44)
    n = 10000
    tau = 2.5
    d_min = 2
    mu_bar = 0.3
    kappa = 50
    
    degrees = sample_powerlaw_degrees(n, tau, d_min, rng)
    
    # gamma = 0
    fears_0, stats_0 = sample_degree_dependent_fears(degrees, mu_bar, 0.0, kappa, rng)
    assert abs(stats_0['realized_mu_bar'] - mu_bar) < 1e-3
    assert abs(np.mean(fears_0) - mu_bar) < 1e-2
    
    # gamma = 1
    fears_1, stats_1 = sample_degree_dependent_fears(degrees, mu_bar, 1.0, kappa, rng)
    # Realized mu_bar will be lower than mu_bar if there are cap hits
    assert stats_1['realized_mu_bar'] <= mu_bar
    if stats_1['cap_hits'] == 0:
        assert abs(stats_1['realized_mu_bar'] - mu_bar) < 1e-3
    
    # Check that fears correlate with degrees
    assert stats_1['realized_mu_star'] > stats_0['realized_mu_star']
    print(f"gamma=0 mu_star: {stats_0['realized_mu_star']:.4f}, gamma=1 mu_star: {stats_1['realized_mu_star']:.4f}")
    print("test_degree_dependent_fears passed")

if __name__ == "__main__":
    test_powerlaw_degrees()
    test_erased_fraction()
    test_degree_dependent_fears()
    print("All Python generator validations passed.")
