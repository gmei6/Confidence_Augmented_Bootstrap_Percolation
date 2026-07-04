import os
import sys

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(base_dir, "src"))

from twocascade.analysis import load_raw_results, analyze_clock_collapse_bias
from twocascade.plotting import plot_clock_collapse_bias

def main():
    n_values = [1000, 2000, 4000, 8000]
    raw_by_n = {}
    
    print("Loading raw results...")
    for n in n_values:
        raw_path = os.path.join(base_dir, "results", "raw", f"fear_concentration_n{n}.json")
        if not os.path.exists(raw_path):
            print(f"Error: Raw file {raw_path} not found.")
            return
            
        raw_by_n[n] = load_raw_results(raw_path)

    print("Analyzing clock collapse bias...")
    bias_results = analyze_clock_collapse_bias(raw_by_n)
    
    figures_dir = os.path.join(base_dir, "results", "figures")
    print(f"Plotting bias and saving to {figures_dir}...")
    plot_clock_collapse_bias(bias_results, figures_dir, "clock_collapse_bias.png")
    
    print("Task H complete!")

if __name__ == "__main__":
    main()
