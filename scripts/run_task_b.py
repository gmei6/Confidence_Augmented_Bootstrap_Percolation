import os
import sys
import json
from pathlib import Path

# Ensure src/ is in pythonpath
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(base_dir, "src"))

from twocascade.runner import run_sweep
from twocascade.analysis import analyze_sweep, load_raw_results
from twocascade.plotting import plot_theta_robustness, plot_kappa_robustness

def run_part1_theta_robustness():
    print("=== PART 1: Theta-Robustness Sweeps ===")
    figures_dir = os.path.join(base_dir, "results", "figures")
    os.makedirs(figures_dir, exist_ok=True)
    
    thetas = [0.2, 0.35, 0.5, 0.65, 0.8]
    
    for r in [2, 3, 4]:
        raw_path = os.path.join(base_dir, "results", "raw", f"sweep_wk3_4_r{r}.json")
        if not os.path.exists(raw_path):
            print(f"Warning: Raw sweep file not found at {raw_path}. Skipping r={r}.")
            continue
            
        print(f"Loading raw results for r={r} from {raw_path}...")
        raw_data = load_raw_results(raw_path)
        
        analyzed_sweeps_by_theta = {}
        for theta in thetas:
            print(f"  Analyzing sweep at theta = {theta}...")
            analyzed = analyze_sweep(raw_data, theta=theta)
            analyzed_sweeps_by_theta[str(theta)] = analyzed
            
        filename = f"theta_robustness_r{r}.png"
        print(f"  Generating boundary robustness plot: {filename}...")
        plot_theta_robustness(analyzed_sweeps_by_theta, figures_dir, filename=filename)
        print(f"  Saved robustness plot to {os.path.join(figures_dir, filename)}")

def run_part2_kappa_robustness():
    print("\n=== PART 2: Kappa-Robustness Sweeps ===")
    figures_dir = os.path.join(base_dir, "results", "figures")
    os.makedirs(figures_dir, exist_ok=True)
    
    kappas = [2.0, 10.0, 50.0, 200.0]
    analyzed_sweeps_by_kappa = {}
    
    cpp_bin = os.path.join(base_dir, "cpp", "build", "twocascade_run")
    if not os.path.exists(cpp_bin):
        print(f"ERROR: C++ binary not found at {cpp_bin}. Please build it first in Release mode.")
        print("Run: cd cpp && mkdir -p build && cd build && cmake -DCMAKE_BUILD_TYPE=Release .. && make")
        return
        
    for kappa in kappas:
        kappa_int = int(kappa)
        config_path = os.path.join(base_dir, "configs", f"kappa_sweep_r2_k{kappa_int}.json")
        
        if not os.path.exists(config_path):
            print(f"Error: Config file {config_path} not found.")
            continue
            
        with open(config_path, "r") as f:
            cfg = json.load(f)
        raw_output_path = os.path.join(base_dir, cfg["output"]["raw_filepath"])
        
        # Idempotent execution
        if not os.path.exists(raw_output_path):
            print(f"Running sweep for kappa = {kappa}...")
            run_sweep(config_path, engine="cpp")
        else:
            print(f"Raw results for kappa = {kappa} already exist at {raw_output_path}. Skipping simulation.")
            
        print(f"Loading raw results for kappa = {kappa}...")
        raw_data = load_raw_results(raw_output_path)
        analyzed = analyze_sweep(raw_data)
        analyzed_sweeps_by_kappa[str(kappa)] = analyzed
        
    filename = "kappa_robustness_r2.png"
    print(f"Generating kappa robustness plot: {filename}...")
    plot_kappa_robustness(analyzed_sweeps_by_kappa, figures_dir, filename=filename)
    print(f"Saved kappa robustness plot to {os.path.join(figures_dir, filename)}")

if __name__ == "__main__":
    run_part1_theta_robustness()
    run_part2_kappa_robustness()
    print("\nTask B execution script completed successfully.")
