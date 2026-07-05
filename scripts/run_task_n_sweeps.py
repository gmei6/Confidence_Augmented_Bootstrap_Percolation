import json
import os
import sys

# Ensure src/ is in pythonpath
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(base_dir, "src"))

from twocascade.runner import run_sweep

def main():
    # Q4 Phase 1 tilt companions: gamma=+1.0 already ran via configs/q4_phase1.json
    # (results/q4_phase1_raw.json). The gamma0/gamma_neg1 configs complete the
    # gamma in {-1, 0, +1} axis required by C-Q4(i) tilt monotonicity, on paired
    # trials (shared base_seed=42).
    #
    # Phase 1b: the Phase 1 seed grid (multiples of the G(n,p) Janson a_c, floor
    # 260) turned out entirely supercritical on the tau=2.5 configuration model
    # (P(systemic)~1 in every cell), so the transition is invisible there. The
    # phase1b configs sweep a in {2,...,32} where the pilot located the actual
    # transition, at 200 trials/cell.
    configs = [
        "configs/q4_phase1_gamma0.json",
        "configs/q4_phase1_gamma_neg1.json",
        "configs/q4_phase1b_gammaneg1.json",
        "configs/q4_phase1b_gamma0.json",
        "configs/q4_phase1b_gammapos1.json",
    ]

    for cfg in configs:
        cfg_path = os.path.join(base_dir, cfg)
        with open(cfg_path) as f:
            raw_out = json.load(f)["output"]["raw_filepath"]
        if os.path.exists(os.path.join(base_dir, raw_out)):
            print(f"Skipping {cfg}: {raw_out} already exists.")
            continue
        print(f"Running sweep for {cfg}...")
        run_sweep(cfg_path)
        print(f"Finished sweep for {cfg}.")

if __name__ == "__main__":
    main()
