import os
import sys
import json

# Ensure src/ is in pythonpath
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(base_dir, "src"))

from twocascade.analysis import analyze_sweep, fit_scaling_exponent, pool_scaling_exponent_fits
from twocascade.plotting import plot_extended_scaling_validation

def main():
    configs = [
        "configs/scaling_law_validation_r2_n1000.json",
        "configs/scaling_law_validation_r2_n2000.json",
        "configs/scaling_law_validation_r2_n4000.json",
        "configs/scaling_law_validation_r3_n1000.json",
        "configs/scaling_law_validation_r3_n2000.json",
        "configs/scaling_law_validation_r3_n4000.json",
        "configs/scaling_law_validation_r4_n1000.json",
        "configs/scaling_law_validation_r4_n2000.json",
        "configs/scaling_law_validation_r4_n4000.json",
    ]

    fits_by_r = {2: [], 3: [], 4: []}

    print("Analyzing sweeps and extracting scaling exponent fits...")
    for cfg in configs:
        cfg_path = os.path.join(base_dir, cfg)
        with open(cfg_path, 'r') as f:
            cfg_data = json.load(f)
        
        raw_filepath = os.path.join(base_dir, cfg_data["output"]["raw_filepath"])
        
        if not os.path.exists(raw_filepath):
            print(f"Warning: {raw_filepath} not found. Did the sweep finish?")
            continue
            
        with open(raw_filepath, 'r') as rf:
            raw_data = json.load(rf)
            
        analyzed_data = analyze_sweep(raw_data)
        try:
            fit = fit_scaling_exponent(analyzed_data)
        except ValueError as e:
            print(f"Skipping {cfg}: {e}")
            continue
        
        r = fit["r"]
        fits_by_r[r].append(fit)

    print("\n--- Scaling Law Exponent Results ---")
    for r, fits in fits_by_r.items():
        if not fits:
            continue
        try:
            pooled = pool_scaling_exponent_fits(fits)
            print(f"\nr = {r}")
            print(f"  Pooled gamma: {pooled['gamma']:.4f} ± {pooled['gamma_err']:.4f}")
            print(f"  Theory gamma: {pooled['gamma_theory']:.4f}")
            print(f"  R^2:          {pooled['r_squared']:.4f}")
            print(f"  N values:     {pooled['n_values']}")
        except Exception as e:
            print(f"\nr = {r}: Failed to pool fits - {e}")

    output_dir = os.path.join(base_dir, "results", "figures")
    filename = "extended_scaling_validation.png"
    print(f"\nGenerating plot {filename} in {output_dir}...")
    plot_extended_scaling_validation(fits_by_r, output_dir, filename)
    print("Done.")

if __name__ == "__main__":
    main()
