import os
import sys

# Ensure src/ is in pythonpath
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(base_dir, "src"))

from twocascade.runner import run_sweep

def main():
    configs = [
        "configs/finite_size_r2_n1000.json",
        "configs/finite_size_r2_n2000.json",
        "configs/finite_size_r2_n5000.json"
    ]

    for cfg in configs:
        cfg_path = os.path.join(base_dir, cfg)
        print(f"Running sweep for {cfg}...")
        run_sweep(cfg_path)
        print(f"Finished sweep for {cfg}.")

if __name__ == "__main__":
    main()
