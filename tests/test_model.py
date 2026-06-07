"""
Unit tests for twocascade.model formulas and validations.
"""

import pytest
import math
from twocascade.model import (
    CascadeParams,
    calculate_beta,
    calculate_p_n,
    janson_t_c,
    janson_a_c
)
from twocascade.meanfield import critical_seed_scaling

def test_cascade_params_validation():
    """Verify CascadeParams validations raise error on invalid configurations."""
    p = CascadeParams(
        n=100, p=0.1, r=2, mean_fear=0.3, concentration=50.0,
        seed_size=10, theta=0.5
    )
    assert p.n == 100
    
    with pytest.raises(ValueError, match="n must be positive"):
        CascadeParams(n=0, p=0.1, r=2, mean_fear=0.3, concentration=50.0, seed_size=10, theta=0.5)
        
    with pytest.raises(ValueError, match="p must be in"):
        CascadeParams(n=100, p=1.2, r=2, mean_fear=0.3, concentration=50.0, seed_size=10, theta=0.5)
        
    with pytest.raises(ValueError, match="r must be >= 2"):
        CascadeParams(n=100, p=0.1, r=1, mean_fear=0.3, concentration=50.0, seed_size=10, theta=0.5)
        
    with pytest.raises(ValueError, match="mean_fear must be in"):
        CascadeParams(n=100, p=0.1, r=2, mean_fear=-0.1, concentration=50.0, seed_size=10, theta=0.5)
        
    with pytest.raises(ValueError, match="concentration must be positive"):
        CascadeParams(n=100, p=0.1, r=2, mean_fear=0.3, concentration=0.0, seed_size=10, theta=0.5)

    with pytest.raises(ValueError, match="seed_size must be in"):
        CascadeParams(n=100, p=0.1, r=2, mean_fear=0.3, concentration=50.0, seed_size=105, theta=0.5)


def test_janson_formulas():
    """Verify analytical formulas for critical timescale and seed sizes."""
    n = 2000
    p = 0.005
    r = 2
    
    tc = janson_t_c(n, p, r)
    assert math.isclose(tc, 20.0, rel_tol=1e-9)
    
    ac = janson_a_c(n, p, r)
    assert math.isclose(ac, 10.0, rel_tol=1e-9)
    
    ac_mu = critical_seed_scaling(n, p, r, mean_fear=0.5)
    assert math.isclose(ac_mu, 2.5, rel_tol=1e-9)
