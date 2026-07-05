"""
Task N Phase 2 figure: thin wrapper over scripts/plot_task_n.py that renders
the n = 10000 tilt analysis (results/processed/task_n_phase2_n10000_analysis.json)
to results/figures/q4_tilt_monotonicity_r2_n10000.png. Read-only on analysis
artifacts, same as the Phase 1b plotter.
"""

import importlib.util
import os

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

spec = importlib.util.spec_from_file_location(
    "plot_task_n", os.path.join(base_dir, "scripts", "plot_task_n.py"))
plot_task_n = importlib.util.module_from_spec(spec)
spec.loader.exec_module(plot_task_n)

plot_task_n.ANALYSIS_PATH = os.path.join(
    base_dir, "results/processed/task_n_phase2_n10000_analysis.json")
plot_task_n.FIG_PATH = os.path.join(
    base_dir, "results/figures/q4_tilt_monotonicity_r2_n10000.png")

if __name__ == "__main__":
    plot_task_n.main()
