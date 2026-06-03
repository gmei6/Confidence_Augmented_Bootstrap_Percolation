"""
Two-channel Cascade Engine (failed neighbors + global fear)

This is supposed to be readable, and is meant to be later implemented in C++. 
This file prioritizes readability over speed. We use:
- Plain data structures
- Explicit loops
- Descriptive names
"""

import math
import numpy as np
from dataclasses import dataclass

# --------------------------------------------------------------------------- #
# Data structures
# --------------------------------------------------------------------------- #

@dataclass
class Node:
    """One node. Holds only what the engine needs to run later"""
    index: int                              # Position in adjacency list
    individual_fear: float                  # f_i in [0, 1]. It is determined at t = 0
    failed: bool = False                    # status of the node. 
                                            # Failure is permanent. Once true, it's always true
    
    failed_neighbor_count: int = 0      # how many of the bank's neighbors
                                            # have already failed

@dataclass
class CascadeResult:
    """The result of running a single graph's cascade"""
    final_failed_fraction: float        # |A*| / n -- the final number of failed nodes over total nodes
    total_failed : int                  # |A*|
    rounds_completed: int               # Total number of rounds iterated
    history: list                       # The number of failed nodes at the end of each round. 


# --------------------------------------------------------------------------- #
# The cascade engine
# --------------------------------------------------------------------------- #
def run_cascade(adjacency: list[list[int]], nodes: list[Node], r: int, seed_indices: list[int], 
                rng: np.random.Generator, record_history: bool) -> CascadeResult:
    """Runs the two channel cascade till completion

    Parameters
    ----------
    adjacency : list[list[int]]    
        list of lists; adjacency[i] is the neighbor indices of bank i

    nodes: Node         
        list of Node objects, one per node, in index order

    r : int 
        Activated-neighbor threshold for the solvency channel
    
    seed_indices : list[int] 
        Indices of the initially failed banks A(0) (the shock)

    rng : np.random.Generator 
        A instance of np.random.Generator. Should be seeded so i can reproduce results later

    record_history : bool
        if True, record cumulative failures after every round.
 
    Returns
    -------
    CascadeResult    
    Notes
    -----
    Implements §3.2 (solvency channel), §3.3 (fear channel), and §3.4
    (simultaneous round structure). This is the reference oracle for the C++ port.
    """
    n = len(nodes)

    # ----- t = 0: apply the initial shock A(0) ----------------------------- #
    # We begin by marking the seed banks as failed, and then push the failures to their
    # neighbor's counters, so that the round 1's activation test sees them

    for i in seed_indices:
        nodes[i].failed = True
    
    for i in seed_indices:
        for neighbor_index in adjacency[i]:
            nodes[neighbor_index].failed_neighbor_count += 1
    
    total_failed = sum(1 for node in nodes if node.failed)

    new_failed_last_round = len(seed_indices)
    rounds_completed = 0
    history = [total_failed] if record_history else []

    # ----- rounds t = 1, 2, ... until a round produces no new failures ----- #
    while new_failed_last_round > 0:
        global_fear = new_failed_last_round / n

        # ================================================================== #
        # STEP 1 -- EVALUATE every solvent bank against the START-OF-ROUND
        # state. We only READ state in this loop; we change nothing yet. All
        # banks are judged against the same frozen snapshot.
        # ================================================================== #
        newly_failing_nodes = []
        for node in nodes:
            if node.failed:
                continue # we move onto the next node in nodes if the node is already failed
            
            effective_failed_neighbor_count = node.failed_neighbor_count
            # ---- Channel 1: solvency (>= r failed neighbors) ------------- #
            fails_by_solvency = effective_failed_neighbor_count >= r

            # ---- Channel 2: fear (Bernoulli with prob f_i * g_t) ---------- #
            fear_failure_probability = node.individual_fear * global_fear
            fear_draw_succeeds = rng.random() < fear_failure_probability
            fails_by_fear = fear_draw_succeeds

            if fails_by_solvency or fails_by_fear:
                newly_failing_nodes.append(node)

        # ================================================================== #
        # STEP 2 -- APPLY all gathered failures at once (simultaneous update).
        #
        # Why a separate apply step? If we had flipped a bank to "failed" inside
        # STEP 1 and immediately bumped its neighbor's counters, a neighbor
        # pushed up to >= r could then fail in this SAME round -- a mid-round
        # chain reaction. The spec forbids that: a bank pushed over its
        # threshold this round must fail NEXT round. Evaluating everyone against
        # the frozen snapshot first, and only then applying, enforces that
        # one-round delay.
        # ================================================================== #
        for node in newly_failing_nodes:
            node.failed = True
        for node in newly_failing_nodes:
            for neighbor_index in adjacency[node.index]:
                nodes[neighbor_index].failed_neighbor_count += 1

        # ---- round bookkeeping ---- #
        new_failures_this_round = len(newly_failing_nodes)
        if new_failures_this_round == 0:
            break
        total_failed += new_failures_this_round
        new_failed_last_round = new_failures_this_round
        rounds_completed += 1
        if record_history:
            history.append(total_failed)

    final_failed_fraction = total_failed / n

    return CascadeResult(
        final_failed_fraction=final_failed_fraction,
        total_failed=total_failed,
        rounds_completed=rounds_completed,
        history=history
    )





# --------------------------------------------------------------------------- #
# Graph generation: Erdos-Renyi G(n, p)
# --------------------------------------------------------------------------- #
def sample_gnp_adjacency(n: int, p: float, rng: np.random.Generator) -> list[list[int]]: 
    """Generates G(n, p) as an adjacency list with the Batagelj-Brandes method

    Parameters
    ----------
    n : int
        The number of nodes
    
    p : float
        The probability that an edge exists between any 2 nodes
    
    rng : np.random.Generator
        A random object to help us get random numbers

    Returns
    -------
    graph : list[list[int]]
        The adjacency list of the graph
    
    Raises
    ------
    ValueError
        If the inputted number of nodes or the probability are invalid
    Notes
    -----
    Uses the Batagelj–Brandes skip algorithm (§3.1) to generate G(n,p)
    in O(n + edges) time without enumerating all pairs.
    """
    
    adjacency = [[] for _ in range(n)]

    if p < 0.0 or p > 1.0:
        raise ValueError("The inputted probability, p, is not within the range of [0, 1]")
    
    if n < 0:
        raise ValueError("The inputted number of nodes, n, is negative.")

    if p == 0.0:
        return adjacency                # there's no edges, so we don't need anything
    
    if p == 1.0:
        for v in range(n):              # the graph is fully connected
            for w in range(v):
                adjacency[v].append(w)
                adjacency[w].append(v)
        return adjacency

    log_one_minus_p = math.log(1.0 - p)

    row = 1         # The current row. Since row 0 has no columns, we start at 1
    column = -1     # Current Column. -1 so that we start at the first column of our current row

    while row < n:
        # We determine how many pairs to skip before the next edge occurs
        uniform_sample = rng.random()
        geometric_jump = int(math.log(1.0 - uniform_sample) / log_one_minus_p)

        # Skip the pairs and our row and column now is at the next kept pair/edge
        column = column + 1 + geometric_jump
        
        # If our column went past the end of row v, which has columns 0, 1, 2, ... , v-2, v-1, 
        # then we subtract the row width and move onto the next row, until we're within range. 
        while column >= row and row < n:
            column = column - row
            row += 1
        
        if row < n:
            adjacency[row].append(column)
            adjacency[column].append(row)

    return adjacency

# --------------------------------------------------------------------------- #
# Individual fear: truncated normal via rejection sampling
# --------------------------------------------------------------------------- #
def sample_individual_fears(n: int, mean_fear: float, concentration: float, rng: np.random.Generator) -> list[float]:
    """Draw f_i ~ Beta(alpha, beta) with alpha = mean*kappa, beta = (1-mean)*kappa,
    so E[f] = mean_fear exactly and var = mean_fear*(1-mean_fear)/(kappa+1).
    
    Parameters
    ----------
    n : int
        Number of nodes

    mean_fear :
        Average fear for all nodes
    
    concentration : float
        How clustered the values are around the mean_fear

    rng : np.random.Generator
        Random object to generate random numbers

    Returns
    -------
    rng.beta(alpha, beta, size=n).tolist() : list[float]
        A list of fears for all n nodes in the graph. 

    Raises
    ------
    ValueError
        If the mean_fear isn't in [0,1] or if the concentration is negative.
    """
    if not 0.0 <= mean_fear <= 1.0:
        raise ValueError("mean_fear must be in [0, 1]")
    if concentration <= 0.0:
        raise ValueError("concentration (kappa) must be positive")
    if mean_fear == 0.0:
        return [0.0] * n          # alpha = 0 -> point mass at 0 (Janson baseline)
    if mean_fear == 1.0:
        return [1.0] * n
    alpha = mean_fear * concentration
    beta = (1.0 - mean_fear) * concentration
    return rng.beta(alpha, beta, size=n).tolist()

# --------------------------------------------------------------------------- #
# Seed selection and a small experiment driver
# --------------------------------------------------------------------------- #
def choose_seed(n: int, seed_size: int, adjacency: list[list[int]], rng: np.random.Generator, target_high_degree: bool) -> list[int]:
    """Samples the initial set of active nodes in the graph, i.e. A(0), but has the option to target the highest degree banks

    Parameters
    ----------
    n : int
        Number of nodes
    
    seed_size : int
        Number of nodes in the initial active set

    adjacency : list[list[int]]
        List which represents the connection of the nodes
    
    rng : np.random.Generator
        A random object to help us get random numbers

    Returns
    -------
    graph : list[int]
        Set of initially active nodes
    """
    if target_high_degree:
        banks_by_degree = sorted(range(n), key=lambda i: len(adjacency[i]), reverse=True)
        return banks_by_degree[:seed_size]
    return rng.choice(n, size=seed_size, replace=False).tolist()

def make_nodes(individual_fears: list[float]) -> list[Node]:
    """Builds a list of node objects from the bank fears

    individual_fears : list[float]
        a list of the individual fear of each bank
    
    Returns
    -------
    list[Node]
    """
    return [Node(index = i, individual_fear=fear) for i, fear in enumerate(individual_fears)]
    

def estimate_systemic_probability(n: int, p: float, r: int, mean_fear: float, concentration: float, seed_size: int, 
                                  theta: float, trials: int, rng: np.random.Generator, target_high_degree: bool) -> float:
    """Runs the graph multiple times for the given parameters to determine the average amount of percolation we see

    Parameters
    ----------
    n : int
        Number of nodes
    
    p : float
        Probability that an edge exists between any 2 given nodes
    
    mean_fear : float
        The average fear for each node

    concentration : float
        How concentrated around the mean_fear the individual fears will be 
    
    seed_size : int
        Number of nodes in the initial active set

    theta : float
        The percentage of nodes that need to fail in order to count the run as a "systemic failure" or that the graph percolates
    
    trials : int
        Number of trials of the graph to run with the given parameters

    target_high_degree : bool
        Whether the initial set should be targeting the vertices with high degrees

    rng : np.random.Generator
        A random object to help us get random numbers

    Returns
    -------
    probability : float
        The portion of trials that have counted as "almost percolated" or "percolated

    Raises
    ------
    ValueError
        If the trials are non-positive or if the seed_size > n
    """
    if trials <= 0:
        raise ValueError("The number of trials cannot be negative or zero.")
    
    if seed_size > n:
        raise ValueError("The seed_size cannot be greater than n")
    systemic_count = 0
    for _ in range(trials):
        adjacency = sample_gnp_adjacency(n=n, p=p, rng=rng)
        fears = sample_individual_fears(n=n, mean_fear=mean_fear, concentration=concentration, rng=rng)

        nodes = make_nodes(individual_fears=fears)
        seed_indices = choose_seed(n=n, seed_size=seed_size, adjacency=adjacency, rng=rng, target_high_degree=target_high_degree)
        result = run_cascade(adjacency=adjacency, nodes=nodes, r=r, seed_indices=seed_indices, rng=rng, record_history=False)
        if result.final_failed_fraction >= theta:
            systemic_count += 1
    return systemic_count / trials
    


if __name__ == "__main__":
    rng = np.random.default_rng(0)
    n = 500
    adjacency = sample_gnp_adjacency(n, p=0.02, rng=rng)
    fears = sample_individual_fears(n, mean_fear=0.3, concentration=0.5, rng=rng)
    banks = make_nodes(fears)
    seed_indices = choose_seed(n, seed_size=5, adjacency=adjacency, rng=rng, target_high_degree=False)
    result = run_cascade(adjacency, banks, r=2, seed_indices=seed_indices,
                         rng=rng, record_history=True)
    print(f"failed fraction = {result.final_failed_fraction:.3f} "
          f"over {result.rounds_completed} rounds")
    print(f"cumulative failures per round = {result.history}")

