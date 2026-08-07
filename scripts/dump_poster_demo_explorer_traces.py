"""Dump the graph-explorer grid of cascade traces for the poster demo's final
screen (poster-demo/traces/phase11_*.json + poster-demo/traces/phase11_manifest.json).

WHAT THIS IS
------------
The demo's last screen lets a visitor pick a base random-graph model (Erdos-
Renyi / power-law / GIRG) and tune that model's own parameters via preset
chips, then watch the SAME fixed cascade (one bank fails, fear on) play out on
the resulting graph. Nothing simulates client-side, so every (model, knob)
combination the UI can select has to exist as a precomputed trace file ahead
of time. This script is the only producer of that grid.

This is phase 11 of the demo (screens 1-10 are the existing landing/structure/
single/stacked/chooser sequence dumped by dump_poster_demo_traces.py; this is
a new, separate screen appended after the chooser). It reuses every reusable
piece of that pipeline -- build_graph, draw_fears, run_traced_cascade,
reconstruct_rounds, derive_causes, compute_layout, edge_list, git_commit_hash,
build_trace, validate_trace, write_trace -- by importing that module directly
(`import dump_poster_demo_traces as base`) rather than reimplementing any
cascade or graph logic. `src/` is read-only here, exactly as it is there.

WHY NO PER-COMBO CONFIG JSON FILES
-----------------------------------
Phases 1-7 each have their own configs/poster_demo_phase*.json, one config per
trace, because each of those traces is a hand-picked, individually-curated
moment in the poster's narrative (seeds scanned and selected against a stated
criterion -- see the module docstring of dump_poster_demo_traces.py). This
screen is different in kind: it is a systematic 33-cell sweep over a fixed
grid of knob values, with ONE deterministic seed per cell and no curation
("whatever the cascade does is what gets shown" -- explicit, agreed design
decision). Writing 33 near-duplicate config JSON files for a mechanically
enumerable sweep would be pure duplication. This script IS the reproducibility
record instead: every graph parameter, every seed, and the seed-derivation
rule are all here in one place, and poster-demo/traces/phase11_manifest.json
(the OTHER thing this script writes) is the source of truth for what the
front end resolves a UI selection to. This is a deliberate departure from the
one-config-per-trace convention used for phases 1-7, not an oversight.

THE THREE KNOB SETS (agreed with the project owner, not renegotiable here)
----------------------------------------------------------------------------
  Erdos-Renyi (gnp):            mean degree only.      presets {3, 4.5, 6}
  power-law (configuration_model): tau only, d_min = 2. presets {2.2, 2.5, 3.0}
  GIRG:                          tau, alpha_g, AND mean degree.
                                  presets tau {2.2, 2.5, 3.0}
                                          alpha_g {0.8, 1.2, 2.0}
                                          mean degree {3, 4.5, 6}   (27 combos)
  Total: 3 + 3 + 27 = 33 traces.

For Erdos-Renyi, mean degree is a closed-form knob: scaling.target_mean_degree
is solved via calculate_beta/calculate_p_n exactly as the gnp branch of
build_graph already does, with n_ref = n = 300 so (n-1)p lands the target
exactly at demo scale (the same convention configs/poster_demo_phase1_er_mu0.json
uses). No bisection.

For power-law, mean degree is NOT a knob -- it is an emergent consequence of
(tau, d_min) plus erasure (see scripts/calibrate_matched_degree.py). d_min is
pinned at 2 (matches every existing power-law config in this repo) and tau is
the only knob. The realised mean degree is whatever comes out; it is read off
each trace's own summary.mean_degree and surfaced in the UI as a computed, not
chosen, value. This script does NOT bisect anything to hit a target power-law
degree, and must not start doing so.

For GIRG, mean degree IS solved for, per combo, by the exact bisection method
in scripts/calibrate_girg_degree.py's solve_w_min(): at fixed (n, tau,
alpha_g), w_min is bisected until the realised mean degree (averaged over
`replicates` independent graphs, deterministic given a base_seed) lands within
`tol` of the target. This script imports solve_w_min directly rather than
reimplementing bisection. It runs at DEMO scale (n = 300, not the production
n = 10000) with fewer replicates than the production default of 20 -- cheap
enough to afford at n = 300, but never fewer than 10 so the bisection target
stays a signal, not noise (see GIRG_CAL below). Per calibrate_girg_degree.py's
own honesty caveat, this is adequate for a demo, not a production-grade
calibration, and that framing carries over here unchanged.

If a GIRG combo's bisection bracket [w_lo, w_hi] does not straddle the target
mean degree, solve_w_min returns w_min = None and this script does NOT
generate a trace for that combo -- it records the failure (with the bracket
diagnostics) in the manifest and moves on. If bisection brackets the target
but does not converge to `tol` within `max_iter` iterations, the trace IS
still generated, using the best w_min found (the last bisection midpoint) --
that is the "solved w_min" the brief asks for, just imperfectly solved -- and
the manifest records converged: false plus the achieved-vs-target residual so
nothing is silently passed off as an exact match. Either way, a failure is
never quietly patched over with a substituted target.

FIXED CASCADE SETTINGS (identical for all 33 combos, matching the
poster_demo_phase7_powerlaw_a1.json finale convention: one bank fails, fear
on, watch what spreads)
----------------------------------------------------------------------------
    n = 300, r = 2, seed_size = 1, mean_fear = 0.4, concentration = 50,
    theta = 0.5, window_len = 5, weights = [0.2]*5, target_high_degree = false,
    fear.type = "global", fear.gamma = 0.0.
Layout: spring (seed 7) for Erdos-Renyi/power-law, girg_positions (real torus
coordinates) for GIRG -- exactly as existing phases already do.

SEEDING
-------
One trial per combo, no curation or scanning: whatever the cascade does is
what gets shown. Seeds are derived systematically from a fixed base so the
whole grid is reproducible from this script alone:

    graph_seed = trial_seed = SEED_BASE + combo_index    (SEED_BASE = 20261200)

combo_index enumerates all 33 combos in this fixed, documented order:
    0, 1, 2       Erdos-Renyi, mean degree in [3, 4.5, 6], in that order
    3, 4, 5       power-law, tau in [2.2, 2.5, 3.0], in that order
    6 .. 32       GIRG, nested loops tau (outer) x alpha_g (middle) x
                  mean degree (inner), each list in the order given above:
                      idx = 6 + tau_i * 9 + alpha_i * 3 + degree_i

USAGE
-----
    arch -arm64 python3 scripts/dump_poster_demo_explorer_traces.py

Writes poster-demo/traces/phase11_*.json (up to 33 files) and
poster-demo/traces/phase11_manifest.json (always written, one entry per
attempted combo, successes and failures both).
"""

import datetime
import json
import os
import subprocess
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "src"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import dump_poster_demo_traces as base            # noqa: E402  (path setup must precede import)
import calibrate_girg_degree as girg_cal          # noqa: E402

TRACE_DIR = "poster-demo/traces"
MANIFEST_PATH = os.path.join(TRACE_DIR, "phase11_manifest.json")
MANIFEST_SCHEMA = "twocascade-poster-demo-explorer-manifest/1"

N = 300
SEED_BASE = 20261200

FIXED_CASCADE = {
    "n": N,
    "r": 2,
    "seed_size": 1,
    "mean_fear": 0.4,
    "concentration": 50,
    "theta": 0.5,
    "window_len": 5,
    "weights": [0.2, 0.2, 0.2, 0.2, 0.2],
    "target_high_degree": False,
}

ER_DEGREES = [3, 4.5, 6]
PL_TAUS = [2.2, 2.5, 3.0]
GIRG_TAUS = [2.2, 2.5, 3.0]
GIRG_ALPHAS = [0.8, 1.2, 2.0]
GIRG_DEGREES = [3, 4.5, 6]

# Demo-scale GIRG bisection: cheaper than the production n=10000/20-replicate
# default (calibrate_girg_degree.py), but never below 10 replicates so the
# bisection target is a signal, not noise (per the task brief). tol is looser
# than calibrate_girg_degree.py's n=10000 default of 0.02, matching this
# repo's own n=300 precedent (phase6's config used tol=0.05 with 40
# replicates); 14 replicates at n=300 is cheap enough to afford a slightly
# tighter bracket walk than that without the runtime of 40.
GIRG_CAL = {
    "replicates": 14,
    "base_seed": 20260804,
    "tol": 0.1,
    "w_lo": 0.02,
    "w_hi": 10.0,
    "max_iter": 30,
}


def fmt(x) -> str:
    """Filesystem/id-safe formatting for a knob float: 4.5 -> '4p5', 2.2 -> '2p2'."""
    return ("%g" % x).replace(".", "p").replace("-", "m")


def make_cfg(graph_cfg: dict, scaling: dict | None = None) -> dict:
    """Assemble the minimal cfg dict build_trace/run_traced_cascade expect,
    with the fixed cascade settings baked in and only `graph` (and `scaling`,
    for gnp) varying per combo."""
    pinned = {
        "n": N,
        "r": FIXED_CASCADE["r"],
        "concentration": FIXED_CASCADE["concentration"],
        "theta": FIXED_CASCADE["theta"],
        "window_len": FIXED_CASCADE["window_len"],
        "weights": FIXED_CASCADE["weights"],
        "target_high_degree": FIXED_CASCADE["target_high_degree"],
        "graph": graph_cfg,
        "fear": {"type": "global", "gamma": 0.0},
    }
    cfg = {"pinned_params": pinned}
    if scaling is not None:
        cfg["scaling"] = scaling
    return cfg


def build_and_write(trace_id: str, cfg: dict, seed: int, layout_cfg: dict, text: dict,
                     extra: dict | None = None):
    """Run one combo through the shared pipeline and write its trace file.
    Returns (trace_dict, rel_path)."""
    trace = base.build_trace(
        cfg,
        "generated:scripts/dump_poster_demo_explorer_traces.py (phase11 sweep, no per-combo config)",
        trace_id, 11, "explorer",
        FIXED_CASCADE["mean_fear"], FIXED_CASCADE["seed_size"],
        seed, seed, layout_cfg, text, extra=extra,
    )
    rel_path = os.path.join(TRACE_DIR, trace_id + ".json")
    base.write_trace(trace, rel_path)
    return trace, rel_path


# --------------------------------------------------------------------------- #
# Erdos-Renyi combos (indices 0-2)
# --------------------------------------------------------------------------- #
def do_gnp():
    rows = []
    for i, deg in enumerate(ER_DEGREES):
        idx = i
        seed = SEED_BASE + idx
        graph_cfg = {"type": "gnp"}
        scaling = {"target_mean_degree": float(deg), "n_ref": N, "alpha": 0.6}
        cfg = make_cfg(graph_cfg, scaling)
        trace_id = f"phase11_gnp_deg{fmt(deg)}"
        text = {
            "headline": f"Erdos-Renyi, mean degree {deg}",
            "caption": (
                f"Every pair of banks connects independently. Mean degree {deg} is a "
                f"chosen knob here, solved exactly for n = {N} (no bisection needed). "
                f"One bank fails, fear is on at 0.4, watch what spreads."
            ),
        }
        try:
            trace, rel_path = build_and_write(
                trace_id, cfg, seed, {"kind": "spring", "seed": 7}, text,
            )
            rows.append({
                "combo_index": idx, "model": "gnp",
                "knobs": {"mean_degree_target": deg},
                "trace_id": trace_id, "trace_path": f"traces/{trace_id}.json",  # page-relative: fetched by poster-demo/app.js from poster-demo/
                "graph_seed": seed, "trial_seed": seed,
                "realized_mean_degree": trace["summary"]["mean_degree"],
                "girg_calibration": None,
                "status": "ok",
            })
            print(f"  [ok] {trace_id}: realised <k> = {trace['summary']['mean_degree']:.4f} "
                  f"({trace['summary']['total_failed']} failed)")
        except Exception as exc:                                    # noqa: BLE001
            rows.append({
                "combo_index": idx, "model": "gnp",
                "knobs": {"mean_degree_target": deg},
                "trace_id": trace_id, "trace_path": None,
                "graph_seed": seed, "trial_seed": seed,
                "realized_mean_degree": None, "girg_calibration": None,
                "status": "failed", "diagnostics": str(exc),
            })
            print(f"  [FAIL] {trace_id}: {exc}")
    return rows


# --------------------------------------------------------------------------- #
# power-law combos (indices 3-5) -- tau only, degree is emergent and reported
# --------------------------------------------------------------------------- #
def do_powerlaw():
    rows = []
    for i, tau in enumerate(PL_TAUS):
        idx = 3 + i
        seed = SEED_BASE + idx
        graph_cfg = {"type": "configuration_model", "tau": float(tau), "d_min": 2}
        cfg = make_cfg(graph_cfg)
        trace_id = f"phase11_pl_tau{fmt(tau)}"
        text = {
            "headline": f"Power-law, tau {tau}",
            "caption": (
                f"A few hubs hold most of the links. tau = {tau}, d_min = 2. Mean degree "
                f"is not a knob on this path, it is whatever this tau produces, read off "
                f"below as a computed value. One bank fails, fear is on at 0.4."
            ),
        }
        try:
            trace, rel_path = build_and_write(
                trace_id, cfg, seed, {"kind": "spring", "seed": 7}, text,
            )
            rows.append({
                "combo_index": idx, "model": "configuration_model",
                "knobs": {"tau": tau},
                "trace_id": trace_id, "trace_path": f"traces/{trace_id}.json",  # page-relative: fetched by poster-demo/app.js from poster-demo/
                "graph_seed": seed, "trial_seed": seed,
                "realized_mean_degree": trace["summary"]["mean_degree"],
                "girg_calibration": None,
                "status": "ok",
            })
            print(f"  [ok] {trace_id}: realised <k> = {trace['summary']['mean_degree']:.4f} "
                  f"(emergent, {trace['summary']['total_failed']} failed)")
        except Exception as exc:                                    # noqa: BLE001
            rows.append({
                "combo_index": idx, "model": "configuration_model",
                "knobs": {"tau": tau},
                "trace_id": trace_id, "trace_path": None,
                "graph_seed": seed, "trial_seed": seed,
                "realized_mean_degree": None, "girg_calibration": None,
                "status": "failed", "diagnostics": str(exc),
            })
            print(f"  [FAIL] {trace_id}: {exc}")
    return rows


# --------------------------------------------------------------------------- #
# GIRG combos (indices 6-32) -- tau x alpha_g x degree, degree bisected via w_min
# --------------------------------------------------------------------------- #
def do_girg():
    rows = []
    for ti, tau in enumerate(GIRG_TAUS):
        for ai, alpha_g in enumerate(GIRG_ALPHAS):
            for di, deg in enumerate(GIRG_DEGREES):
                idx = 6 + ti * 9 + ai * 3 + di
                seed = SEED_BASE + idx
                trace_id = f"phase11_girg_tau{fmt(tau)}_ag{fmt(alpha_g)}_deg{fmt(deg)}"

                bisect = girg_cal.solve_w_min(
                    target=float(deg), n=N, tau=float(tau), alpha_g=float(alpha_g),
                    replicates=GIRG_CAL["replicates"], base_seed=GIRG_CAL["base_seed"],
                    tol=GIRG_CAL["tol"], w_lo=GIRG_CAL["w_lo"], w_hi=GIRG_CAL["w_hi"],
                    max_iter=GIRG_CAL["max_iter"],
                )
                cal_record = {
                    "target_mean_degree": deg,
                    "w_min": bisect["w_min"],
                    "achieved_mean_degree": bisect["achieved_mean_degree"],
                    "achieved_se": bisect["achieved_se"],
                    "iterations": bisect["iterations"],
                    "converged": bisect["converged"],
                    "w_lo": GIRG_CAL["w_lo"], "w_hi": GIRG_CAL["w_hi"],
                    "replicates": GIRG_CAL["replicates"], "base_seed": GIRG_CAL["base_seed"],
                    "tol": GIRG_CAL["tol"],
                    "diagnostics": bisect.get("diagnostics"),
                }

                if bisect["w_min"] is None:
                    # bracket did not straddle the target -- do NOT substitute a
                    # different value; record the failure and move on.
                    rows.append({
                        "combo_index": idx, "model": "girg",
                        "knobs": {"tau": tau, "alpha_g": alpha_g, "mean_degree_target": deg},
                        "trace_id": trace_id, "trace_path": None,
                        "graph_seed": seed, "trial_seed": seed,
                        "realized_mean_degree": None,
                        "girg_calibration": cal_record,
                        "status": "bisection_not_bracketed",
                        "diagnostics": bisect["diagnostics"],
                    })
                    print(f"  [FAIL] {trace_id}: bisection not bracketed -- {bisect['diagnostics']}")
                    continue

                graph_cfg = {"type": "girg", "tau": float(tau),
                              "w_min": bisect["w_min"], "alpha_g": float(alpha_g)}
                cfg = make_cfg(graph_cfg)
                conv_note = "" if bisect["converged"] else (
                    f" (bisection did NOT converge to tol {GIRG_CAL['tol']}; using best w_min "
                    f"found, achieved <k> = {bisect['achieved_mean_degree']:.3f} vs target {deg})"
                )
                text = {
                    "headline": f"GIRG, tau {tau}, alpha_g {alpha_g}, mean degree ~{deg}",
                    "caption": (
                        f"Same kind of hubs as power-law, but every bank sits somewhere on a "
                        f"map: tau = {tau}, alpha_g = {alpha_g} (how strongly geometry decides "
                        f"who connects). Mean degree is not directly settable here, so w_min "
                        f"was bisected to target {deg}{conv_note}. One bank fails, fear on at "
                        f"0.4."
                    ),
                }
                try:
                    trace, rel_path = build_and_write(
                        trace_id, cfg, seed, {"kind": "girg_positions"}, text,
                    )
                    rows.append({
                        "combo_index": idx, "model": "girg",
                        "knobs": {"tau": tau, "alpha_g": alpha_g, "mean_degree_target": deg},
                        "trace_id": trace_id, "trace_path": f"traces/{trace_id}.json",  # page-relative: fetched by poster-demo/app.js from poster-demo/
                        "graph_seed": seed, "trial_seed": seed,
                        "realized_mean_degree": trace["summary"]["mean_degree"],
                        "girg_calibration": cal_record,
                        "status": "ok" if bisect["converged"] else "ok_not_converged",
                    })
                    conv_str = "converged" if bisect["converged"] else "NOT converged"
                    print(f"  [ok, {conv_str}] {trace_id}: w_min={bisect['w_min']:.5f} "
                          f"cal <k>={bisect['achieved_mean_degree']:.3f} "
                          f"this-trace <k>={trace['summary']['mean_degree']:.3f} "
                          f"iters={bisect['iterations']}")
                except Exception as exc:                             # noqa: BLE001
                    rows.append({
                        "combo_index": idx, "model": "girg",
                        "knobs": {"tau": tau, "alpha_g": alpha_g, "mean_degree_target": deg},
                        "trace_id": trace_id, "trace_path": None,
                        "graph_seed": seed, "trial_seed": seed,
                        "realized_mean_degree": None,
                        "girg_calibration": cal_record,
                        "status": "trace_build_failed",
                        "diagnostics": str(exc),
                    })
                    print(f"  [FAIL] {trace_id}: trace build failed after successful bisection -- {exc}")
    return rows


def main():
    print("=== phase 11 explorer grid ===")
    print(f"n = {N}, seed_base = {SEED_BASE}, fixed cascade = {FIXED_CASCADE}\n")

    print("-- Erdos-Renyi (3 combos) --")
    gnp_rows = do_gnp()
    print("\n-- power-law (3 combos) --")
    pl_rows = do_powerlaw()
    print("\n-- GIRG (27 combos) --")
    girg_rows = do_girg()

    all_rows = gnp_rows + pl_rows + girg_rows
    all_rows.sort(key=lambda r: r["combo_index"])

    n_ok = sum(1 for r in all_rows if r["status"] in ("ok", "ok_not_converged"))
    n_not_converged = sum(1 for r in all_rows if r["status"] == "ok_not_converged")
    n_failed = sum(1 for r in all_rows if r["status"] not in ("ok", "ok_not_converged"))

    manifest = {
        "schema": MANIFEST_SCHEMA,
        "phase": 11,
        "git_commit": base.git_commit_hash(),
        "generated": datetime.datetime.now().isoformat(timespec="seconds"),
        "seed_base": SEED_BASE,
        "fixed_cascade_params": FIXED_CASCADE,
        "presets": {
            "gnp": {"mean_degree": ER_DEGREES},
            "configuration_model": {"tau": PL_TAUS, "d_min": 2},
            "girg": {"tau": GIRG_TAUS, "alpha_g": GIRG_ALPHAS, "mean_degree": GIRG_DEGREES},
        },
        "girg_calibration_settings": GIRG_CAL,
        "combos": all_rows,
    }

    manifest_abs = os.path.join(REPO_ROOT, MANIFEST_PATH)
    os.makedirs(os.path.dirname(manifest_abs), exist_ok=True)
    with open(manifest_abs, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"\n=== summary ===")
    print(f"{n_ok}/{len(all_rows)} combos produced a trace "
          f"({n_not_converged} of those with a non-converged GIRG bisection)")
    print(f"{n_failed}/{len(all_rows)} combos failed outright (no trace written)")
    if n_failed:
        print("failures:")
        for r in all_rows:
            if r["status"] not in ("ok", "ok_not_converged"):
                print(f"  combo {r['combo_index']} ({r['model']}, {r['knobs']}): "
                      f"{r['status']} -- {r.get('diagnostics')}")
    print(f"\nwrote {MANIFEST_PATH}")


if __name__ == "__main__":
    main()
