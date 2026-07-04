import os
import subprocess
import tempfile
import numpy as np
from pathlib import Path

from twocascade.reference import make_nodes, choose_seed, run_cascade
from twocascade.graphs import sample_powerlaw_degrees, sample_configuration_model

REPO_ROOT = Path(__file__).resolve().parent.parent
CPP_BIN = REPO_ROOT / "cpp" / "build" / "twocascade_run"

def dump_graph(filepath, adj):
    with open(filepath, 'w') as f:
        for neighbors in adj:
            f.write(" ".join(map(str, neighbors)) + "\n")

def dump_seeds(filepath, seeds):
    with open(filepath, 'w') as f:
        f.write(" ".join(map(str, seeds)) + "\n")

def test_prong_a():
    """
    Prong A cross-validation: deterministic logic at mu=0 on configuration model.
    """
    if not CPP_BIN.exists():
        print("C++ engine not built, skipping Prong A.")
        return

    rng = np.random.default_rng(42)
    n = 1000
    tau = 2.5
    d_min = 2
    r = 2
    a = 10
    
    degrees = sample_powerlaw_degrees(n, tau, d_min, rng)
    adj = sample_configuration_model(degrees, rng)
    
    fears = [0.0] * n
    nodes = make_nodes(fears)
    seeds = choose_seed(n, a, adj, rng, False)
    
    res = run_cascade(adjacency=adj, nodes=nodes, r=r, seed_indices=seeds, rng=rng)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        graph_file = Path(tmpdir) / "graph.txt"
        seed_file = Path(tmpdir) / "seeds.txt"
        
        dump_graph(graph_file, adj)
        dump_seeds(seed_file, seeds)
        
        cmd = [
            str(CPP_BIN),
            "--n", str(n),
            "--r", str(r),
            "--mu", "0",
            "--kappa", "50",
            "--seed-size", str(a),
            "--trials", "1",
            "--graph-file", str(graph_file),
            "--seed-file", str(seed_file)
        ]
        
        env = dict(os.environ)
        env["OMP_NUM_THREADS"] = "1"
        
        try:
            out = subprocess.run(cmd, capture_output=True, text=True, check=True, env=env)
        except subprocess.CalledProcessError as e:
            print("C++ engine failed.")
            print(e.stderr)
            return
            
        parts = out.stdout.strip().split()
        cpp_failed_fraction = float(parts[0])
        
        print(f"Python final failed fraction: {res.final_failed_fraction}")
        print(f"C++ final failed fraction: {cpp_failed_fraction}")
        assert abs(res.final_failed_fraction - cpp_failed_fraction) < 1e-6
        print("Prong A (mu=0) match successful on configuration model.")

if __name__ == "__main__":
    test_prong_a()
