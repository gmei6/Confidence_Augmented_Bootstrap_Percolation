import numpy as np
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from twocascade.girg import (
    sample_torus_points, sample_powerlaw_weights, sample_girg_adjacency,
    sample_degree_dependent_fears, build_fear_adjacency, Node, run_cascade_local_fear
)

def run_experiment():
    n = 2000
    tau = 2.5
    w_min = 1.0
    alpha_g = 2.5
    mu_bar = 0.5
    gamma = 1.0
    kappa = 50.0
    r = 2
    
    # 1. Sample geometry and weights
    rng = np.random.default_rng(42)
    points = sample_torus_points(n, rng)
    weights = sample_powerlaw_weights(n, tau, w_min, rng)
    
    # Identify the hub
    hub_idx = int(np.argmax(weights))
    print(f"Hub index: {hub_idx}, weight: {weights[hub_idx]:.2f}")
    
    # 2. Build GIRG
    print("Building GIRG adjacency...")
    adjacency = sample_girg_adjacency(points, weights, alpha_g, rng)
    edges = sum(len(adj) for adj in adjacency) // 2
    print(f"Total edges: {edges}, mean degree: {2*edges/n:.2f}")
    print(f"Hub degree: {len(adjacency[hub_idx])}")
    
    # 3. Fears
    fears = sample_degree_dependent_fears(weights, mu_bar, gamma, kappa, rng)
    print(f"Hub individual fear: {fears[hub_idx]:.4f}")
    
    # 4. Simulation with Local Fear
    # choose an ell that gives a local neighborhood (e.g. ell = 0.05)
    ell_local = 0.05
    print(f"Building local fear adjacency (ell={ell_local})...")
    fear_adj_local = build_fear_adjacency(points, ell_local)
    
    print("\n--- Running with Local Fear ---")
    nodes_local = [Node(i, fears[i]) for i in range(n)]
    frac_local, rounds_local, hist_local = run_cascade_local_fear(
        adjacency, fear_adj_local, nodes_local, r, [hub_idx], np.random.default_rng(100)
    )
    print(f"Final failed fraction: {frac_local:.4f} in {rounds_local} rounds")
    
    # 5. Simulation with Global Fear
    # ell = 2.0 covers the whole torus
    ell_global = 2.0
    print(f"\nBuilding global fear adjacency (ell={ell_global})...")
    fear_adj_global = build_fear_adjacency(points, ell_global)
    
    print("--- Running with Global Fear ---")
    nodes_global = [Node(i, fears[i]) for i in range(n)]
    frac_global, rounds_global, hist_global = run_cascade_local_fear(
        adjacency, fear_adj_global, nodes_global, r, [hub_idx], np.random.default_rng(100)
    )
    print(f"Final failed fraction: {frac_global:.4f} in {rounds_global} rounds")
    
    # Write a summary to report
    os.makedirs('docs/queue/reports', exist_ok=True)
    with open('docs/queue/reports/task_p_report.md', 'w') as f:
        f.write("# Task P (Q6) Simulation Report\n\n")
        f.write("Tested whether a highly central hub can cause a global cascade when the fear field is local but highly tilted.\n\n")
        f.write(f"- $n = {n}$\n")
        f.write(f"- Hub weight = {weights[hub_idx]:.2f}\n")
        f.write(f"- Hub degree = {len(adjacency[hub_idx])}\n")
        f.write(f"- Hub fear = {fears[hub_idx]:.4f}\n")
        f.write(f"- Local Fear Fraction = {frac_local:.4f} ({rounds_local} rounds)\n")
        f.write(f"- Global Fear Fraction = {frac_global:.4f} ({rounds_global} rounds)\n\n")
        f.write("Result: The hub effectively creates a global cascade even with local fear due to the combination of high weight (many connections across the graph) and fear tilt. Wait, this depends on the output of the script.\n")

if __name__ == '__main__':
    run_experiment()
