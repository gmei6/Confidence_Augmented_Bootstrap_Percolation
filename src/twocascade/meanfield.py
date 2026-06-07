"""
Mean-field approximations and analytical threshold scaling laws.
"""

import numpy as np
from twocascade.model import janson_a_c

def scaling_ratio(mean_fear, r: int):
    """
    Theoretical scaling ratio of the critical seed size under the fear model:
    (1 - mean_fear) ** (r / (r - 1)).
    Supports both float and NumPy array inputs for mean_fear.
    """
    exponent = r / (r - 1)
    return (1.0 - mean_fear) ** exponent

def critical_seed_scaling(n: int, p: float, r: int, mean_fear) -> float:
    """
    Conjectured combined critical seed size scaling law:
    a_c(mu) = a_c(0) * scaling_ratio(mu, r).
    Supports both float and NumPy array inputs for mean_fear.
    """
    ac0 = janson_a_c(n, p, r)
    return ac0 * scaling_ratio(mean_fear, r)
