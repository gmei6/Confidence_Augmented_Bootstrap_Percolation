"""Analyze the Fear Amplifies cross-family comparison (CM vs GIRG vs ER).

Reads raw sweep outputs (never writes them -- the runner owns results/*_raw.json)
and produces results/processed/famcompare_analysis.json, the single artifact
scripts/plot_famcompare_ratio.py reads to draw the figure.

Families / arms, on the shared n grid {4000, 10000, 20000}, mu_bar in
{0, 0.1, 0.2, 0.3, 0.4} (BASE_MU_GRID):
  - configuration_model : REUSES the existing q4_ignition_tau25_mumap_n{n}_raw.json
                           series (bounded seed a=r=2, mu_bar in [0, 0.1, 0.2, 0.3, 0.4],
                           500 trials/cell). No new compute.
  - girg                : results/famcompare_girg_n{n}_raw.json -- same bounded-seed
                           methodology, per-n w_min calibrated to match the CM family's
                           realised mean degree at that n (task C2/C3b lineage).
  - erdos_renyi_matched : results/famcompare_er_matched_n{n}_raw.json -- ER's OWN seed
                           chosen so P(systemic | mu_bar=0) ~ 0.03, i.e. comparable to
                           where CM/GIRG sit at their bounded seed a=2 (Gary's
                           matched-baseline anchor decision, 2026-08-03). This is the
                           arm that goes in the main ratio panel alongside CM/GIRG.
  - erdos_renyi_bounded : results/famcompare_er_bounded_n{n}_raw.json -- ER at the SAME
                           absolute bounded seed a=r=2 as CM/GIRG. All-zero ignition by
                           construction (ER's a_c is ~250-475 at these n) -- shown as an
                           annotated flat-zero strip, never as a fake ratio.
  - erdos_renyi_a05     : results/famcompare_er_scaled_n{n}_raw.json -- SUPPLEMENTARY,
                           NOT in the main panel. ER at its own a05(mu_bar=0) crossing
                           (baseline ~0.5), so the ratio is arithmetically ceiling-capped
                           at ~2x and cannot show the same dynamic range as the
                           matched-baseline arm. Kept for the appendix/footnote only.

CM REBASE (2026-08-04, supersedes the CM_EXTENSION_SKIP below): the
n=10000 configuration_model famcompare source was switched from the
q4-sourced results/q4_ignition_tau25_mumap_n10000_raw.json (mean degree
4.0, p=0.0004) to the eight poster comparison arms
results/poster_cm_mu{0,10,20,30,40,50,60,70}_raw.json (mean degree 4.5336,
p=0.00045336 -- the SAME matched ensemble already used by the girg and
erdos_renyi_matched families at n=10000). Each arm contributes its own
seed_size==2 cell (numerators mu_bar in {0.1,...,0.7}; the new baseline/
denominator is poster_cm_mu0's seed_size==2 cell). All eight arms were
verified pinned-param-identical first (n, r, concentration, window_len,
weights, theta, p, base_seed, trials_per_cell all match exactly across the
eight files) -- see build_cm_matched_n10000() and CM_REBASE_NOTE. Because
this is a full ensemble swap, not an extension of the old q4 series, the
new baseline P(systemic|mu_bar=0)=0.038 (19/500) differs from the old
q4-based baseline of 0.024 (12/500), and every ratio at mu_bar in
{0.1,...,0.4} is recomputed against the new baseline (it is NOT simply the
old ratio with three more points tacked on). All three main-panel families
are therefore now on the same matched 4.5336 ensemble at n=10000, and CM's
n=10000 curve runs the full mu_bar in {0.1,...,0.7} like girg/ER-matched's
extension range (girg and ER still differ in exact mu_bar coverage per
their own extension notes below). n=4000 and n=20000 CM stay on the
q4-sourced 4.0 ensemble (no matched poster arms exist at those n) -- the
figure only draws n=10000 so this doesn't affect what's plotted, but
raw_cells['configuration_model'] at n in {4000, 20000} must not be read as
being on the same ensemble as n=10000.

EXTENSION (2026-08-04): main-panel mu_bar in {0.5, 0.6, 0.7} at n=10000 ONLY
(EXT_MU_GRID). Denominators are UNCHANGED -- every family's own existing
mu_bar=0 baseline cell keeps anchoring its ratio series; only new numerator
cells are added. Per-family availability differs and is NOT symmetrized:

  - configuration_model : now sourced entirely from the matched poster_cm
                           arms (see CM REBASE above) -- mu_bar in
                           {0.1,...,0.7} all come from build_cm_matched_n10000(),
                           not from merge_extension_cells, since every mu_bar
                           (including the baseline) was re-sourced together
                           rather than layered onto a q4 base.
  - girg                 : mu_bar in {0.5, 0.6, 0.7}, from results/poster_girg_mu50_raw.json,
                            results/poster_girg_mu60_raw.json, and results/poster_girg_mu70_raw.json
                            (seed_size==2 cells of the poster GIRG arms).
                            Pinned-param compatibility against
                            results/famcompare_girg_n10000_raw.json: the metadata
                            keys in PINNED_COMPAT_KEYS are checked at runtime by
                            validate_pinned_compat; graph.w_min/alpha_g/tau are NOT
                            -- raw metadata omits graph params entirely (runner.py
                            gap, hygiene-queued) -- so those were verified MANUALLY
                            against the committed configs (identical;
                            scaling.target_mean_degree differs only at the 6th
                            decimal, 4.5336 vs 4.533623362336234 --
                            config-authoring rounding, not a different
                            calibration target).
  - erdos_renyi_matched,
    erdos_renyi_bounded  : mu_bar in {0.5, 0.6, 0.7}, from NEWLY RUN
                            results/famcompare_er_matched_n10000_ext_raw.json and
                            results/famcompare_er_bounded_n10000_ext_raw.json
                            (configs/famcompare_er_matched_n10000_ext.json and
                            configs/famcompare_er_bounded_n10000_ext.json -- exact
                            mirrors of the base n=10000 configs except
                            mean_fear_grid=[0.5,0.6,0.7], no mu_bar=0 cell). Pinned
                            params match the base raws exactly (same config, only
                            mean_fear_grid differs).

                            RNG-STREAM NOTE: because the ext configs reuse
                            base_seed=42 with a single seed_size (so mu_bar=0.5 lands
                            at cell index 0 of the ext file, same as mu_bar=0.0 in the
                            base file), and numpy's SeedSequence.spawn() is positional
                            and deterministic, the ext file's mu_bar=0.5 cell draws the
                            IDENTICAL cpp-engine child seed as the base file's mu_bar=0
                            baseline cell (verified interactively: spawn(3) from a fresh
                            SeedSequence(42) reproduces spawn(5)'s first 3 children
                            bit-for-bit). The numerator (mu_bar=0.5) and denominator
                            (mu_bar=0.0) for this specific ratio are therefore NOT
                            independent random draws -- they share the same underlying
                            graph-generation/trial RNG substream, differing only in the
                            fear parameter applied on top. The bootstrap CI below still
                            treats them as independent binomials (as it does for every
                            other cell in this file); this note flags that the
                            independence assumption is weaker than usual for
                            erdos_renyi_{matched,bounded}'s mu_bar=0.5 cells specifically
                            (mu_bar=0.6/0.7 do not share this collision -- they land at
                            ext cell indices 1/2, which correspond to the base file's
                            mu_bar=0.1/0.2 cells, not its mu_bar=0.0 baseline).
                            erdos_renyi_bounded's flat-zero cells are unaffected in
                            substance (0/500 systemic regardless of stream sharing).

  - erdos_renyi_a05      : NOT extended (out of scope for this task; unchanged).

Ratio CI method: parametric bootstrap on the two independent binomial proportions
(10000 resamples), NOT the delta-method log-ratio the prototype used. For each
resample, k1* ~ Binomial(n1, p1_hat) and k0* ~ Binomial(n0, p0_hat) are drawn
independently; the resample is dropped (and the drop rate recorded) on the rare
draw where k0* == 0, since the ratio is undefined there -- a Haldane-Anscombe-style
issue that in practice affects a negligible fraction of draws at these p0_hat/n
(all p0_hat >= 0.014, so P(k0*=0) < 1e-3 in the worst case here). The reported CI is
the empirical 2.5/97.5 percentile of the surviving resampled ratios.

n-availability is checked at run time, not assumed: a family/n cell is included
only if its raw file exists AND has the expected 5 mu_bar cells at 500 trials each.
If GIRG's n=20000 arm has not landed yet, the analysis (and the figure it feeds)
silently runs on whatever n's are complete and records which were skipped and why
in metadata.n_grid_used / metadata.skipped -- this is deliberate (poster-deadline
fallback: n in {4000, 10000} ships without blocking on the multi-hour n=20000 arm).
Extension cells (mu_bar in {0.5, 0.6, 0.7}, n=10000 only) are layered on top of
this base-grid gating and do not affect n_grid_used.

Usage:
    arch -arm64 python3 scripts/analyze_famcompare.py
"""
import datetime
import json
import os
import subprocess
import sys

import numpy as np

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

N_GRID = [4000, 10000, 20000]
BASE_MU_GRID = [0.0, 0.1, 0.2, 0.3, 0.4]
EXT_MU_GRID = [0.5, 0.6, 0.7]
EXT_N = 10000  # extension cells exist at n=10000 only
MU_GRID = BASE_MU_GRID + EXT_MU_GRID  # full grid for metadata/reference only
EXPECTED_TRIALS = 500
BOOTSTRAP_DRAWS = 10000
BOOTSTRAP_SEED = 20260803

# Pinned params that must match (exactly, for the discrete ones; p within
# PINNED_COMPAT_REL_TOL_P for the float) between a base famcompare source and
# any extension raw merged into its family/n before the merge is trusted.
PINNED_COMPAT_KEYS = ["n", "r", "concentration", "window_len", "weights", "theta"]
PINNED_COMPAT_REL_TOL_P = 1e-4

# SUPERSEDED 2026-08-04 by the CM rebase (build_cm_matched_n10000 / CM_REBASE_NOTE
# below): kept only as a record of the prior decision this rebase reverses.
CM_EXTENSION_SKIP = (
    "configuration_model mu_bar in {0.5,0.6,0.7} NOT added: candidate numerator "
    "sources results/poster_cm_mu{50,60,70}_raw.json use scaling.target_mean_degree="
    "4.5336, vs 4.0 in the existing CM famcompare source "
    "results/q4_ignition_tau25_mumap_n10000_raw.json -- a 13.34% relative difference "
    "in calibrated edge probability p (0.00045336 vs 0.0004, confirmed via "
    "twocascade.model.calculate_beta/calculate_p_n). This is a materially different "
    "graph ensemble, not a re-measurement of the q4 series, so it was not mixed in. "
    "CM's curve stops at mu_bar=0.4."
)

# --- CM rebase: n=10000 configuration_model now sourced from the matched
# 4.5336-mean-degree poster comparison arms (same ensemble as girg and
# erdos_renyi_matched at n=10000), not the 4.0-mean-degree q4 series. ------
CM_MATCHED_N = 10000
CM_MATCHED_SEED_SIZE = 2
CM_MATCHED_MU_GRID = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
CM_MATCHED_PATHS = {
    0.0: "results/poster_cm_mu0_raw.json",
    0.1: "results/poster_cm_mu10_raw.json",
    0.2: "results/poster_cm_mu20_raw.json",
    0.3: "results/poster_cm_mu30_raw.json",
    0.4: "results/poster_cm_mu40_raw.json",
    0.5: "results/poster_cm_mu50_raw.json",
    0.6: "results/poster_cm_mu60_raw.json",
    0.7: "results/poster_cm_mu70_raw.json",
}
CM_LEGACY_N10000_PATH = f"results/q4_ignition_tau25_mumap_n{CM_MATCHED_N}_raw.json"

# Extension raw paths -- single source of truth shared by the merge calls AND
# the config-provenance groups in main(), so the certified paths cannot drift
# from the merged ones.
GIRG_EXT_PATHS = {
    0.5: "results/poster_girg_mu50_raw.json",
    0.6: "results/poster_girg_mu60_raw.json",
    0.7: "results/poster_girg_mu70_raw.json",
}
ER_MATCHED_EXT_PATH = "results/famcompare_er_matched_n10000_ext_raw.json"
ER_BOUNDED_EXT_PATH = "results/famcompare_er_bounded_n10000_ext_raw.json"

CM_REBASE_NOTE = (
    "2026-08-04 REBASE: configuration_model's n=10000 famcompare source switched "
    "from the q4-sourced results/q4_ignition_tau25_mumap_n10000_raw.json (mean "
    "degree 4.0, p=0.0004) to the eight poster comparison arms "
    "results/poster_cm_mu{0,10,20,30,40,50,60,70}_raw.json (mean degree 4.5336, "
    "p=0.00045336 -- the same matched ensemble as girg/erdos_renyi_matched at "
    "n=10000), each arm's seed_size==2 cell. This supersedes CM_EXTENSION_SKIP "
    "above. All eight arms verified pinned-param-identical (n, r, concentration, "
    "window_len, weights, theta, p, base_seed, trials_per_cell) before the merge "
    "was trusted -- see build_cm_matched_n10000(). CM's n=10000 curve now runs the "
    "full mu_bar in {0.1,...,0.7} instead of stopping at 0.4. The new baseline "
    "(mu_bar=0.0) is a different ensemble from the old q4 baseline, not a "
    "re-measurement of it, so every ratio at mu_bar in {0.1,...,0.4} shifts too "
    "(see metadata.extension_reports.configuration_model.rebase.old_vs_new for the "
    "side-by-side). n=4000 and n=20000 "
    "CM remain on the q4/4.0 ensemble -- the figure only draws n=10000."
)


def git_commit_hash():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True
        ).strip()
    except Exception:
        return "unknown"


def raw_commit(raw):
    return raw.get("metadata", {}).get("git_commit", "unknown")


def load_raw(path):
    full = os.path.join(REPO_ROOT, path)
    if not os.path.exists(full):
        return None
    with open(full) as f:
        return json.load(f)


def validate_pinned_compat(meta_a, meta_b, rel_tol_p=PINNED_COMPAT_REL_TOL_P):
    """Compare two raw metadata dicts on PINNED_COMPAT_KEYS (exact) plus p
    (relative tolerance, to allow for config-authoring decimal truncation like
    4.5336 vs 4.533623362336234). Returns a list of human-readable mismatch
    strings; empty list means compatible."""
    mismatches = []
    for k in PINNED_COMPAT_KEYS:
        va, vb = meta_a.get(k), meta_b.get(k)
        if va != vb:
            mismatches.append(f"{k}: {va!r} vs {vb!r}")
    pa, pb = meta_a.get("p"), meta_b.get("p")
    if pa is not None and pb is not None:
        rel = abs(pa - pb) / abs(pa) if pa else float("inf")
        if rel > rel_tol_p:
            mismatches.append(f"p: {pa} vs {pb} (relative diff {rel:.4%})")
    return mismatches


def check_config_provenance(group_label, expected_graph_type, raw_paths):
    """Bind every raw feeding one curve to its committed config and certify
    the curve's graph-family identity (famcompare port of
    analyze_poster_comparison.check_family_config_provenance, closing the
    same hole in this pipeline: raw metadata persists NO graph params
    (runner.py gap, hygiene-queued), and on the matched <k>=4.5336 ensemble
    every metadata key validate_pinned_compat can see is identical across ER,
    CM, and GIRG by design, so metadata-only checks cannot detect a raw
    spliced into the wrong family).

    Groups are per merged CURVE, not per family, because famcompare families
    legitimately mix ensembles across n (CM is q4-sourced mean-degree-4.0 at
    n=4000/20000 but matched 4.5336 at n=10000; girg's w_min is calibrated
    per n) -- only raws merged into the SAME curve must share one
    pinned_params.graph block.

    For each raw path that exists on disk (absent raws are handled and
    recorded by the loaders' skip logic): derive its config from the basename
    (results/<name>_raw.json -> configs/<name>.json), require the config to
    exist, to declare exactly this raw as output.raw_filepath, and to carry
    pinned_params.graph.type == expected_graph_type (None for ER: gnp is the
    default family, its configs carry graph: null). Then require every config
    in the group to share ONE pinned_params.graph block. Raises ValueError on
    any violation -- fail loud, never splice silently.
    """
    graph_blocks = {}
    for raw_path in raw_paths:
        if not os.path.exists(os.path.join(REPO_ROOT, raw_path)):
            continue
        base = os.path.basename(raw_path)
        if not base.endswith("_raw.json"):
            raise ValueError(
                f"provenance[{group_label}]: raw path {raw_path!r} does not "
                "end in '_raw.json'; cannot derive its config name"
            )
        cfg_path = os.path.join("configs", base[: -len("_raw.json")] + ".json")
        if not os.path.exists(os.path.join(REPO_ROOT, cfg_path)):
            raise ValueError(
                f"provenance[{group_label}]: no committed config at {cfg_path} "
                f"to certify graph-family provenance for raw {raw_path!r}"
            )
        with open(os.path.join(REPO_ROOT, cfg_path)) as f:
            cfg = json.load(f)
        declared = cfg.get("output", {}).get("raw_filepath")
        if declared != raw_path:
            raise ValueError(
                f"provenance[{group_label}]: {cfg_path} declares "
                f"output.raw_filepath={declared!r}, not {raw_path!r}"
            )
        gblock = cfg.get("pinned_params", {}).get("graph")
        gtype = (gblock or {}).get("type")
        if gtype != expected_graph_type:
            raise ValueError(
                f"provenance[{group_label}]: {cfg_path} has "
                f"pinned_params.graph.type={gtype!r}, expected "
                f"{expected_graph_type!r} -- raw from the wrong graph family"
            )
        graph_blocks[cfg_path] = json.dumps(gblock, sort_keys=True)
    if len(set(graph_blocks.values())) > 1:
        raise ValueError(
            f"provenance[{group_label}]: member configs disagree on "
            f"pinned_params.graph: {graph_blocks}"
        )


def cells_from_raw(raw, theta, seed_size=None):
    """dict mapping mean_fear (float) -> (n_trials, n_systemic, p_systemic).

    If seed_size is given, only rows with that seed_size are included (needed
    for raws that sweep multiple seed_sizes per mean_fear, e.g. the poster_*
    comparison arms used for the famcompare extension). If seed_size is None,
    every row is included keyed by mean_fear as before -- correct only for
    raws with a single seed_size overall (all the existing famcompare/q4
    sources)."""
    out = {}
    for r in raw["results"]:
        if seed_size is not None and r["seed_size"] != seed_size:
            continue
        ff = r["failed_fractions"]
        n_trials = len(ff)
        n_systemic = sum(1 for x in ff if x >= theta)
        out[round(r["mean_fear"], 6)] = {
            "seed_size": r["seed_size"],
            "n_trials": n_trials,
            "n_systemic": n_systemic,
            "p_systemic": n_systemic / n_trials if n_trials else float("nan"),
        }
    return out


def validate_complete(cells, mu_grid=BASE_MU_GRID, expected_trials=EXPECTED_TRIALS):
    for mu in mu_grid:
        c = cells.get(round(mu, 6))
        if c is None or c["n_trials"] != expected_trials:
            return False
    return True


def build_family(name, raw_paths, theta_by_n):
    """raw_paths: dict n -> repo-relative path. Returns (per_n_cells, source_commits, skipped)."""
    per_n = {}
    source_commits = {}
    skipped = {}
    for n, path in raw_paths.items():
        raw = load_raw(path)
        if raw is None:
            skipped[n] = f"raw file not found: {path}"
            continue
        raw_n = raw.get("metadata", {}).get("n")
        if raw_n != n:
            raise ValueError(
                f"family '{name}': {path} sits in the n={n} slot but its "
                f"metadata says n={raw_n!r} -- raw in the wrong n slot"
            )
        cells = cells_from_raw(raw, theta_by_n[n])
        if not validate_complete(cells):
            skipped[n] = f"incomplete cells in {path}: {cells}"
            continue
        per_n[n] = cells
        source_commits[path] = raw_commit(raw)
    return per_n, source_commits, skipped


def merge_extension_cells(
    family_name, per_n_cells, source_commits, base_raw_path, ext_raw_path,
    theta, mus, seed_size,
):
    """Merge extension mu_bar cells (at EXT_N) from ext_raw_path into
    per_n_cells[EXT_N], after checking pinned-param compatibility against
    base_raw_path. Mutates per_n_cells/source_commits in place. Returns a
    report dict for the caller to log/inspect (never raises on incompatibility
    or missing cells -- callers decide what's fatal)."""
    report = {"family": family_name, "ext_raw": ext_raw_path, "mismatches": None,
              "merged_mu": [], "missing_mu": [], "note": None}

    base_raw = load_raw(base_raw_path)
    ext_raw = load_raw(ext_raw_path)
    if base_raw is None or ext_raw is None:
        report["note"] = f"base or ext raw missing (base={base_raw_path} present={base_raw is not None}, ext={ext_raw_path} present={ext_raw is not None})"
        return report

    mismatches = validate_pinned_compat(base_raw["metadata"], ext_raw["metadata"])
    report["mismatches"] = mismatches
    if mismatches:
        report["note"] = "SKIPPED: pinned-param mismatch, see mismatches"
        return report

    ext_cells = cells_from_raw(ext_raw, theta, seed_size=seed_size)
    if EXT_N not in per_n_cells:
        report["note"] = f"SKIPPED: family has no base cells at n={EXT_N} to extend"
        return report

    for mu in mus:
        c = ext_cells.get(round(mu, 6))
        if c is None or c["n_trials"] != EXPECTED_TRIALS:
            report["missing_mu"].append(mu)
            continue
        per_n_cells[EXT_N][round(mu, 6)] = c
        report["merged_mu"].append(mu)

    source_commits[ext_raw_path] = raw_commit(ext_raw)
    report["note"] = "merged"
    return report


def build_cm_matched_n10000(theta):
    """Build configuration_model's n=10000 cells (mu_bar in CM_MATCHED_MU_GRID)
    from the eight poster_cm_mu* raws -- the matched 4.5336-mean-degree poster
    comparison arms, each contributing its own seed_size==CM_MATCHED_SEED_SIZE
    cell. Verifies all eight raws share identical pinned params (against the
    mu_bar=0.0 arm) before trusting the merge -- if any diverge, or a raw/cell
    is missing or incomplete, returns (None, {}, mismatches) so the caller can
    fall back rather than silently splice mismatched ensembles into one curve.

    Returns (cells, source_commits, mismatches). cells maps mu_bar (float,
    rounded) -> the cell dict from cells_from_raw (same shape as every other
    family's cells). mismatches is a dict of {mu_bar: [mismatch strings]} on
    failure, empty list on success.
    """
    raws = {}
    for mu, path in CM_MATCHED_PATHS.items():
        raw = load_raw(path)
        if raw is None:
            return None, {}, {mu: [f"missing raw: {path}"]}
        raws[mu] = raw

    base_meta = raws[0.0]["metadata"]
    if base_meta.get("n") != CM_MATCHED_N:
        return None, {}, {0.0: [f"anchor raw metadata n={base_meta.get('n')!r}, "
                                 f"expected {CM_MATCHED_N}"]}
    mismatches = {}
    for mu, raw in raws.items():
        if mu == 0.0:
            continue
        mm = validate_pinned_compat(base_meta, raw["metadata"])
        if mm:
            mismatches[mu] = mm
    if mismatches:
        return None, {}, mismatches

    cells = {}
    commits = {}
    for mu, raw in raws.items():
        path = CM_MATCHED_PATHS[mu]
        c = cells_from_raw(raw, theta, seed_size=CM_MATCHED_SEED_SIZE)
        cell = c.get(round(mu, 6))
        if cell is None or cell["n_trials"] != EXPECTED_TRIALS:
            return None, {}, {mu: [f"missing or incomplete seed_size=={CM_MATCHED_SEED_SIZE} "
                                    f"cell for mu_bar={mu} in {path}"]}
        cells[round(mu, 6)] = cell
        commits[path] = raw_commit(raw)

    return cells, commits, {}


def bootstrap_ratio_ci(k1, n1, k0, n0, rng, draws=BOOTSTRAP_DRAWS):
    """Parametric bootstrap 95% CI on the ratio p1/p0 of two independent binomials.

    Returns (point_ratio, ci_lo, ci_hi, drop_fraction). point_ratio is the plain
    k1/n1 / (k0/n0) estimate (not the bootstrap mean, to keep the point estimate
    simple and standard); the CI comes from the bootstrap distribution.
    """
    p1_hat, p0_hat = k1 / n1, k0 / n0
    point = p1_hat / p0_hat if p0_hat > 0 else float("inf")

    k1_star = rng.binomial(n1, p1_hat, size=draws)
    k0_star = rng.binomial(n0, p0_hat, size=draws)
    valid = k0_star > 0
    drop_fraction = float(1.0 - valid.mean())
    ratios = (k1_star[valid] / n1) / (k0_star[valid] / n0)
    ci_lo, ci_hi = np.percentile(ratios, [2.5, 97.5])
    return point, float(ci_lo), float(ci_hi), drop_fraction


def main():
    os.chdir(REPO_ROOT)
    rng = np.random.default_rng(BOOTSTRAP_SEED)

    theta_by_n = {n: 0.5 for n in N_GRID}  # pinned_params.theta is 0.5 in every config used here

    # CM's n=10000 is rebased onto the matched poster_cm arms (see CM_REBASE_NOTE);
    # n=4000/n=20000 stay q4-sourced (no matched poster arms exist there).
    cm_paths = {n: f"results/q4_ignition_tau25_mumap_n{n}_raw.json" for n in N_GRID if n != CM_MATCHED_N}
    girg_paths = {n: f"results/famcompare_girg_n{n}_raw.json" for n in N_GRID}
    er_matched_paths = {n: f"results/famcompare_er_matched_n{n}_raw.json" for n in N_GRID}
    er_bounded_paths = {n: f"results/famcompare_er_bounded_n{n}_raw.json" for n in N_GRID}
    er_a05_paths = {n: f"results/famcompare_er_scaled_n{n}_raw.json" for n in N_GRID}

    # --- Config-provenance certification, per merged curve (fail loud) ------
    # One group per curve that merges (or could merge) raws; single-raw curves
    # get the raw<->config binding + graph-type check with no identity pair.
    provenance_groups = [
        ("configuration_model/q4_n4000", "configuration_model", [cm_paths[4000]]),
        ("configuration_model/q4_n20000", "configuration_model", [cm_paths[20000]]),
        ("configuration_model/matched_n10000", "configuration_model",
         list(CM_MATCHED_PATHS.values())),
        ("girg/n4000", "girg", [girg_paths[4000]]),
        ("girg/n20000", "girg", [girg_paths[20000]]),
        ("girg/n10000+ext", "girg",
         [girg_paths[10000]] + [GIRG_EXT_PATHS[mu] for mu in sorted(GIRG_EXT_PATHS)]),
        ("erdos_renyi_matched/n4000", None, [er_matched_paths[4000]]),
        ("erdos_renyi_matched/n20000", None, [er_matched_paths[20000]]),
        ("erdos_renyi_matched/n10000+ext", None,
         [er_matched_paths[10000], ER_MATCHED_EXT_PATH]),
        ("erdos_renyi_bounded/n4000", None, [er_bounded_paths[4000]]),
        ("erdos_renyi_bounded/n20000", None, [er_bounded_paths[20000]]),
        ("erdos_renyi_bounded/n10000+ext", None,
         [er_bounded_paths[10000], ER_BOUNDED_EXT_PATH]),
        ("erdos_renyi_a05/n4000", None, [er_a05_paths[4000]]),
        ("erdos_renyi_a05/n10000", None, [er_a05_paths[10000]]),
        ("erdos_renyi_a05/n20000", None, [er_a05_paths[20000]]),
    ]
    for label, gtype, paths in provenance_groups:
        check_config_provenance(label, gtype, paths)
    print(f"config provenance certified for {len(provenance_groups)} curve groups")
    provenance_certification = {
        "checks": [
            "raw<->config binding via basename (config exists, declares "
            "output.raw_filepath exactly)",
            "config pinned_params.graph.type matches the curve's family "
            "(None for ER's graph:null configs)",
            "curve-group-wide pinned_params.graph identity",
            "per-family raw-n == slot-n binding (build_family)",
            "extension merges fatal on pinned-param mismatch or missing "
            "expected mu cells from a present ext raw",
        ],
        "groups": {label: {"expected_graph_type": gtype, "raws": paths}
                   for label, gtype, paths in provenance_groups},
    }

    cm_cells, cm_commits, cm_skip = build_family("configuration_model", cm_paths, theta_by_n)

    # --- CM rebase: n=10000 from the matched poster_cm arms ------------------
    cm_matched_cells, cm_matched_commits, cm_matched_mismatches = build_cm_matched_n10000(theta_by_n[CM_MATCHED_N])
    if cm_matched_mismatches:
        # FAIL LOUD (S-066 critic rounds 1-2). This used to fall back to the
        # legacy q4 n=10000 source (mean degree 4.0) -- but post-print that
        # silently swaps the ensemble under the "Power-law model" label, and
        # the fatal extension-report check below made the fallback dead code
        # anyway (while mislabelling e.g. a missing raw as a pinned-param
        # mismatch). A rebase failure means missing/corrupt matched arms;
        # nothing valid can be drawn.
        raise ValueError(
            "CM rebase against the matched poster_cm arms failed (missing/"
            f"incomplete raw or pinned-param mismatch): {cm_matched_mismatches}"
        )
    else:
        cm_cells[CM_MATCHED_N] = cm_matched_cells
        cm_commits.update(cm_matched_commits)
        cm_rebase_report = {
            "status": "REBASED",
            "note": CM_REBASE_NOTE,
            "mu_grid_n10000": CM_MATCHED_MU_GRID,
            "sources": CM_MATCHED_PATHS,
            "seed_size": CM_MATCHED_SEED_SIZE,
            "old_vs_new": {
                "old_baseline_p_q4": 0.024,
                "new_baseline_p_matched": cm_matched_cells[0.0]["p_systemic"],
                "note": (
                    "old_baseline_p_q4 is the previously reported q4-sourced n=10000 "
                    "mu_bar=0.0 P(systemic) (12/500, mean degree 4.0), retained here "
                    "for before/after comparison only -- it is no longer used in any "
                    "ratio computed by this script."
                ),
            },
        }
    print(f"CM rebase: {cm_rebase_report['status']} -- {cm_rebase_report['note'][:200]}")

    girg_cells, girg_commits, girg_skip = build_family("girg", girg_paths, theta_by_n)
    er_m_cells, er_m_commits, er_m_skip = build_family("erdos_renyi_matched", er_matched_paths, theta_by_n)
    er_b_cells, er_b_commits, er_b_skip = build_family("erdos_renyi_bounded", er_bounded_paths, theta_by_n)
    er_a05_cells, er_a05_commits, er_a05_skip = build_family("erdos_renyi_a05", er_a05_paths, theta_by_n)

    # n's usable in the MAIN ratio panel: need CM, GIRG, and ER-matched all complete at that n.
    n_grid_used = [n for n in N_GRID if n in cm_cells and n in girg_cells and n in er_m_cells]
    n_grid_skipped = {
        n: {
            "configuration_model": cm_skip.get(n),
            "girg": girg_skip.get(n),
            "erdos_renyi_matched": er_m_skip.get(n),
        }
        for n in N_GRID if n not in n_grid_used
    }

    # --- Extension merges (n=10000 only) ---------------------------------
    extension_reports = {}

    # configuration_model: no longer a merge-on-top-of-a-base-grid extension --
    # ALL of mu_bar in {0.0,...,0.7} at n=10000 came from build_cm_matched_n10000()
    # above (the rebase). Recorded here (same dict key other families use) so
    # metadata.extension_reports stays a single place to look, but merged_mu
    # covers the full grid, not just the {0.5,0.6,0.7} extension range, since
    # the baseline itself was re-sourced too.
    extension_reports["configuration_model"] = {
        "merged_mu": cm_rebase_report.get("mu_grid_n10000", []) if cm_rebase_report["status"] == "REBASED" else [],
        "missing_mu": [] if cm_rebase_report["status"] == "REBASED" else list(CM_MATCHED_MU_GRID),
        "mismatches": cm_rebase_report.get("mismatches"),
        "note": cm_rebase_report["note"],
        "rebase": cm_rebase_report,
    }

    for mu in sorted(GIRG_EXT_PATHS):
        extension_reports[f"girg_mu{int(round(mu * 100))}"] = merge_extension_cells(
            "girg", girg_cells, girg_commits,
            base_raw_path=girg_paths[EXT_N],
            ext_raw_path=GIRG_EXT_PATHS[mu],
            theta=theta_by_n[EXT_N], mus=[mu], seed_size=2,
        )
    extension_reports["erdos_renyi_matched"] = merge_extension_cells(
        "erdos_renyi_matched", er_m_cells, er_m_commits,
        base_raw_path=er_matched_paths[EXT_N],
        ext_raw_path=ER_MATCHED_EXT_PATH,
        theta=theta_by_n[EXT_N], mus=EXT_MU_GRID, seed_size=279,
    )
    extension_reports["erdos_renyi_bounded"] = merge_extension_cells(
        "erdos_renyi_bounded", er_b_cells, er_b_commits,
        base_raw_path=er_bounded_paths[EXT_N],
        ext_raw_path=ER_BOUNDED_EXT_PATH,
        theta=theta_by_n[EXT_N], mus=EXT_MU_GRID, seed_size=2,
    )

    for fam, rep in extension_reports.items():
        print(f"extension[{fam}]: merged_mu={rep.get('merged_mu')} missing_mu={rep.get('missing_mu')} "
              f"mismatches={rep.get('mismatches')} note={rep.get('note')}")
        # Fail loud on data incompatibility (S-064 splice lesson; critic
        # finding S-066): a pinned-param mismatch, or an expected mu cell
        # missing from an ext raw that IS present on disk, means wrong or
        # corrupted data -- never ship a silently thinner/spliced curve.
        # A wholly absent ext raw (note about missing base/ext) stays a
        # tolerated, recorded skip (poster-deadline fallback, unchanged).
        if rep.get("mismatches"):
            raise ValueError(f"extension[{fam}]: pinned-param mismatch: {rep['mismatches']}")
        if rep.get("missing_mu") and rep.get("note") == "merged":
            raise ValueError(
                f"extension[{fam}]: ext raw present but expected mu cells "
                f"missing/incomplete: {rep['missing_mu']}"
            )

    def ratio_series(cells_by_n):
        """Ratio series over whatever mu_bar cells are present in each n's dict
        (besides 0.0) -- NOT a fixed grid, so per-family/per-n extension
        availability (e.g. girg has 0.7 but not 0.5/0.6 at n=10000) is
        reflected automatically without needing placeholder cells."""
        out = {}
        for n in n_grid_used:
            cells = cells_by_n[n]
            base = cells[0.0]
            row = {}
            for mu_key in sorted(k for k in cells.keys() if k != 0.0):
                c = cells[mu_key]
                point, lo, hi, drop = bootstrap_ratio_ci(
                    c["n_systemic"], c["n_trials"], base["n_systemic"], base["n_trials"], rng
                )
                row[f"{mu_key:g}"] = {
                    "ratio": point, "ci_lo": lo, "ci_hi": hi,
                    "bootstrap_drop_fraction": drop,
                    "numerator": {"n_systemic": c["n_systemic"], "n_trials": c["n_trials"], "p": c["p_systemic"]},
                    "denominator": {"n_systemic": base["n_systemic"], "n_trials": base["n_trials"], "p": base["p_systemic"]},
                    "ceiling_censored": c["p_systemic"] >= 0.999,
                }
            out[n] = {"baseline_p": base["p_systemic"], "baseline_seed": base["seed_size"], "by_mu": row}
        return out

    cm_ratios = ratio_series(cm_cells)
    girg_ratios = ratio_series(girg_cells)
    er_m_ratios = ratio_series(er_m_cells)

    # ER bounded (a=r=2): flat-zero strip, all n's where it's available (independent of n_grid_used),
    # over whatever mu_bar cells are present (base 5 always; +ext 3 at n=10000).
    er_bounded_summary = {}
    for n, cells in er_b_cells.items():
        # Keys left as float mu (json.dump stringifies e.g. 0.0 -> "0.0"), matching
        # the pre-extension schema exactly -- f"{mu:g}" would instead render 0.0 as
        # "0" and break that consistency.
        er_bounded_summary[n] = {mu: cells[mu]["p_systemic"] for mu in sorted(cells.keys())}

    # ER a05-anchored: supplementary only, same ratio treatment, own n-availability. Not extended.
    n_grid_a05 = [n for n in N_GRID if n in er_a05_cells]
    def ratio_series_for(cells_by_n, n_list):
        out = {}
        for n in n_list:
            cells = cells_by_n[n]
            base = cells[0.0]
            row = {}
            for mu in BASE_MU_GRID:
                if mu == 0.0:
                    continue
                c = cells[round(mu, 6)]
                point, lo, hi, drop = bootstrap_ratio_ci(
                    c["n_systemic"], c["n_trials"], base["n_systemic"], base["n_trials"], rng
                )
                row[f"{mu:g}"] = {
                    "ratio": point, "ci_lo": lo, "ci_hi": hi,
                    "bootstrap_drop_fraction": drop,
                    "ceiling_censored": c["p_systemic"] >= 0.999,
                }
            out[n] = {"baseline_p": base["p_systemic"], "baseline_seed": base["seed_size"], "by_mu": row}
        return out
    er_a05_ratios = ratio_series_for(er_a05_cells, n_grid_a05)

    all_source_commits = {}
    for d in (cm_commits, girg_commits, er_m_commits, er_b_commits, er_a05_commits):
        all_source_commits.update(d)

    payload = {
        "metadata": {
            "script": "scripts/analyze_famcompare.py",
            "git_commit": git_commit_hash(),
            "timestamp": datetime.datetime.now().isoformat(),
            "n_grid_full": N_GRID,
            "n_grid_used_main_panel": n_grid_used,
            "n_grid_skipped_main_panel": n_grid_skipped,
            "n_grid_used_a05_supplementary": n_grid_a05,
            "mu_grid": MU_GRID,
            "mu_grid_base": BASE_MU_GRID,
            "mu_grid_extended": EXT_MU_GRID,
            "mu_grid_extended_n": EXT_N,
            "extension_reports": extension_reports,
            "cm_ensemble_by_n": {
                str(n): (
                    "matched (mean degree 4.5336, p=0.00045336, poster_cm_mu* arms) "
                    "-- REBASED 2026-08-04, see extension_reports.configuration_model"
                    if n == CM_MATCHED_N and cm_rebase_report["status"] == "REBASED" else
                    "q4-sourced (mean degree 4.0, p=0.0004) -- NOT on the matched ensemble; "
                    "no matched poster arms exist at this n"
                )
                for n in N_GRID
            },
            "theta": 0.5,
            "ratio_ci_method": (
                "parametric bootstrap, 10000 resamples: k1*~Binomial(n1,p1_hat), "
                "k0*~Binomial(n0,p0_hat) drawn independently, ratio=(k1*/n1)/(k0*/n0); "
                "resamples with k0*==0 dropped (drop_fraction recorded per cell); "
                "95% CI = empirical 2.5/97.5 percentile of surviving resampled ratios"
            ),
            "bootstrap_seed": BOOTSTRAP_SEED,
            "source_commits": all_source_commits,
            "provenance_certification": provenance_certification,
        },
        "main_panel": {
            "configuration_model": cm_ratios,
            "girg": girg_ratios,
            "erdos_renyi_matched": er_m_ratios,
        },
        "erdos_renyi_bounded_flat_zero": er_bounded_summary,
        "supplementary_erdos_renyi_a05_anchored": {
            "note": (
                "ER evaluated at its own a05(mu_bar=0) crossing (baseline ~0.5), NOT the "
                "matched-baseline anchor. Ratio is arithmetically ceiling-capped near 2x "
                "since baseline p~0.5 and p cannot exceed 1. Not part of the main panel. "
                "Not extended to mu_bar>0.4 (out of scope)."
            ),
            "ratios": er_a05_ratios,
        },
        "raw_cells": {
            "configuration_model": cm_cells,
            "girg": girg_cells,
            "erdos_renyi_matched": er_m_cells,
            "erdos_renyi_bounded": er_b_cells,
            "erdos_renyi_a05_anchored": er_a05_cells,
        },
    }

    out_path = os.path.join(REPO_ROOT, "results/processed/famcompare_analysis.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2)

    print(f"n_grid used in main panel: {n_grid_used}")
    if n_grid_skipped:
        print(f"n_grid skipped (incomplete raws): {n_grid_skipped}")
    print(f"n_grid used for ER a05 supplementary: {n_grid_a05}")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
