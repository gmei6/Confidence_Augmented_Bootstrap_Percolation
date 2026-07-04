import argparse
import json
import os
import sys

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(base_dir, "src"))

from twocascade.analysis import evaluate_binomial_dispersion
from twocascade.plotting import plot_overdispersion_ratio

def analyze_task_f(raw_files, t_eval=3, output_dir="results/figures"):
    dispersion_rows = []
    r_val = None
    
    for filepath in raw_files:
        if not os.path.exists(filepath):
            print(f"Warning: file {filepath} not found, skipping.")
            continue
            
        with open(filepath, "r") as f:
            data = json.load(f)
            
        meta = data["metadata"]
        n = meta["n"]
        r = meta["r"]
        base_seed = meta.get("base_seed", 42)
        if r_val is None:
            r_val = r
            
        for cell in data["results"]:
            mean_fear = cell["mean_fear"]
            seed_multiple = cell["seed_multiple"]
            seed_size = cell["seed_size"]
            s_histories = cell["s_histories"]
            
            failures_at_t = []
            for history in s_histories:
                val = history[t_eval] if t_eval < len(history) else history[-1]
                failures_at_t.append(val)
                
            res = evaluate_binomial_dispersion(
                failures_at_t=failures_at_t,
                seed_size=seed_size,
                n=n,
                seed=base_seed + n  # offset seed for different n
            )
            
            row = {
                "n": n,
                "mean_fear": mean_fear,
                "seed_multiple": seed_multiple,
                "dispersion_ratio": res["dispersion_ratio"],
                "ci_low": res["ci"][0],
                "ci_high": res["ci"][1],
                "pi_t": res["pi_t"]
            }
            dispersion_rows.append(row)
            print(f"n={n}, mu={mean_fear}, a/ac0={seed_multiple}: D_t = {row['dispersion_ratio']:.3f} CI [{row['ci_low']:.3f}, {row['ci_high']:.3f}]")
            
    if dispersion_rows:
        os.makedirs("results/processed", exist_ok=True)
        with open("results/processed/task_f_dispersion.json", "w") as f:
            json.dump(dispersion_rows, f, indent=2)
            
        plot_overdispersion_ratio(
            dispersion_rows=dispersion_rows,
            t_round=t_eval,
            r=r_val,
            output_dir=output_dir,
            filename="counting_process_overdispersion_r2.png"
        )
        print(f"Saved figure to {output_dir}/counting_process_overdispersion_r2.png")
    else:
        print("No valid data processed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Task F analysis.")
    parser.add_argument("--files", nargs="*", default=[
        "results/raw/counting_process_n1000.json",
        "results/raw/counting_process_n2000.json",
        "results/raw/counting_process_n4000.json",
        "results/raw/counting_process_n8000.json"
    ])
    parser.add_argument("--t", type=int, default=3, help="Round to evaluate dispersion")
    args = parser.parse_args()
    
    analyze_task_f(args.files, t_eval=args.t)
