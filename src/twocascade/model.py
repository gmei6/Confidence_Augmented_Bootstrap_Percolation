"""
Model configurations, parameters, and Janson bootstrap percolation analytical benchmarks.
"""

import math
from dataclasses import dataclass
from typing import List, Optional

@dataclass(frozen=True)
class CascadeParams:
    """Parameters for a single Two-Channel Cascade simulation run."""
    n: int
    p: float
    r: int
    mean_fear: float
    concentration: float
    seed_size: int
    theta: float
    window_len: int = 1
    weights: Optional[List[float]] = None
    target_high_degree: bool = False

    def __post_init__(self):
        """Validate parameters upon initialization."""
        if self.n <= 0:
            raise ValueError(f"n must be positive, got {self.n}")
        if not (0.0 <= self.p <= 1.0):
            raise ValueError(f"p must be in [0, 1], got {self.p}")
        if 0.0 < self.p < 1e-15:
            raise ValueError(f"p is too small ({self.p} < 1e-15), which could cause underflow division by zero in graph generation")
        if self.r < 2:
            raise ValueError(f"r must be >= 2, got {self.r}")
        if not (0.0 <= self.mean_fear <= 1.0):
            raise ValueError(f"mean_fear must be in [0, 1], got {self.mean_fear}")
        if self.concentration <= 0.0:
            raise ValueError(f"concentration must be positive, got {self.concentration}")
        if not (0 <= self.seed_size <= self.n):
            raise ValueError(f"seed_size must be in [0, n], got {self.seed_size}")
        if not (0.0 <= self.theta <= 1.0):
            raise ValueError(f"theta must be in [0, 1], got {self.theta}")
        if self.window_len < 1:
            raise ValueError(f"window_len must be >= 1, got {self.window_len}")
        if self.weights is not None:
            if len(self.weights) != self.window_len:
                raise ValueError(f"Length of weights ({len(self.weights)}) must match window_len ({self.window_len})")
            if any(w < 0.0 for w in self.weights):
                raise ValueError("All weights must be non-negative")
            if not math.isclose(sum(self.weights), 1.0, abs_tol=1e-9):
                raise ValueError("Weights must sum to 1.0")


def calculate_beta(target_mean_degree: float, n_ref: int, alpha: float) -> float:
    """Calculate the frozen scaling coefficient beta."""
    if n_ref <= 0:
        raise ValueError("n_ref must be positive")
    return target_mean_degree / (n_ref ** (1.0 - alpha))


def calculate_p_n(beta: float, n: int, alpha: float) -> float:
    """Calculate Erdős-Rényi edge probability p using Janson scaling."""
    if n <= 0:
        raise ValueError("n must be positive")
    p = beta * (n ** (-alpha))
    return min(1.0, max(0.0, p))


def janson_t_c(n: int, p: float, r: int) -> float:
    """Critical time-scale t_c = ((r-1)! / (n * p^r))^{1/(r-1)}."""
    if n <= 0 or p <= 0.0 or r < 2:
        raise ValueError("Invalid parameters for t_c calculation")
    denom = n * (p ** r)
    if denom <= 0.0:
        raise ValueError("p^r underflow to zero, connectivity is too low for Janson threshold calculations")
    return (math.factorial(r - 1) / denom) ** (1.0 / (r - 1))


def janson_a_c(n: int, p: float, r: int) -> float:
    """Critical seed size a_c = (1 - 1/r) * t_c at mu = 0."""
    return (1.0 - 1.0 / r) * janson_t_c(n, p, r)


def combined_a_c(n: int, p: float, r: int, mean_fear: float) -> float:
    """Conjectured combined critical seed size scaling law: a_c(mu) = a_c(0) * (1-mu)^{r/(r-1)}."""
    ac0 = janson_a_c(n, p, r)
    exponent = r / (r - 1)
    return ac0 * ((1.0 - mean_fear) ** exponent)
