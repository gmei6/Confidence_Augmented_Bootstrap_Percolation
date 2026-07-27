"""Self-verifying regeneration of the Q4 cascade-boundary figure tau_c(mu, n) at a = 8.

This script exists so the advisor-facing figure is not trusted on prose. It
independently re-derives every number it draws, straight from the 28 runner-produced
raws, and ASSERTS those numbers against the constants quoted on the advisor card. If
the data on disk stop supporting the claim, the script fails loudly instead of
quietly drawing a different picture under the same caption.

What it re-derives from the raws (it does NOT read
results/processed/q4_psys_boundary_analysis.json, so this is an independent check of
scripts/analyze_q4_psys_boundary.py, not a re-read of its output):

  provenance
    - exactly 28 raws, one per committed config
    - a single, uniform metadata.git_commit, and never the "dirty-or-unknown" sentinel
    - realized seed_size_grid == [8] in every raw
    - metadata.engine == "python" in every raw  (so no C++ result is being trusted;
      see walkthrough-q4-boundary.md section 6 for why §5.4 is N/A here)
    - trials_per_cell == 500 and 196 (tau, mu, n) cells total
    - theta read from each raw's metadata (NOT hardcoded) and required to be uniform
    - tau parsed from the filename cross-checked against the config's graph.tau, so
      the filename-as-database dependency is checked rather than assumed

  claims
    - the P = 0.5 boundary yields 27 points (one grid-censored corner at
      n = 2000, mu = 0.90)
    - reduced fit  tau_c = a0 + c*log2(n/2000) + D*mu^2
      a0 = 2.6295, c = -0.09607, D = 0.96039, R^2 = 0.96964
    - full quadratic adds B*mu with B = -0.030 +/- 0.119, i.e. CONSISTENT WITH ZERO.
      The script asserts |B| / sigma_B < 1 so that no future re-run can quietly
      license a linear-in-mu claim this data does not support.
    - single-argument logistic collapse of the 196-cell surface: chi2/dof = 33.70,
      which is asserted to be LARGE (>= 10) because the misfit is part of the
      reported result, not a blemish to be hidden.

Output:
    results/figures/q4_psys_boundary_advisor.png

This is a descriptive fit on a finite grid at one fixed seed size a = 8. It is not a
law, a theorem, or an asymptotic scaling form. See walkthrough-q4-boundary.md.

Usage:
    python scripts/verify_q4_psys_boundary_figure.py
"""

import os
import re
import sys
import json
import glob

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW_GLOB = os.path.join(BASE_DIR, "results", "q4_psys_boundary_n*_tau*_raw.json")
CFG_DIR = os.path.join(BASE_DIR, "configs")
FIG_DIR = os.path.join(BASE_DIR, "results", "figures")
FIG_PATH = os.path.join(FIG_DIR, "q4_psys_boundary_advisor.png")

N_REF = 2000.0          # the log2(n / N_REF) pivot; n = 2000 is the smallest n run
P_LEVEL = 0.5           # the contour being located

# ---- the claims this figure makes, as machine-checked constants -------------
# Values quoted on the advisor card / walkthrough, to the precision quoted there.
EXPECT = {
    "n_raws": 28,
    "n_cells": 196,
    "trials_per_cell": 500,
    "seed_size": 8,
    "n_boundary_points": 27,
    "censored": (2000, 0.90),
    "a0": 2.6295,
    "c": -0.09607,
    "D": 0.96039,
    "R2": 0.96964,
    "B": -0.030,
    "B_stderr": 0.119,
    "chi2_per_dof": 33.70,
}
# Tolerances: each constant is quoted to a fixed number of decimals, so the
# assertion is "agrees at the quoted precision", i.e. half a unit in the last place.
TOL = {"a0": 5e-4, "c": 5e-5, "D": 5e-5, "R2": 5e-5,
       "B": 5e-3, "B_stderr": 5e-3, "chi2_per_dof": 5e-2}

# ---- ordinal single-hue ramp (n is an ordered quantity, not four identities).
# Blue sequential steps 250/350/450/600; light end clears the 2:1 ordinal floor
# against a light surface. Text stays in ink colors, never the series color.
RAMP = ["#86b6ef", "#5598e7", "#2a78d6", "#184f95"]
INK = "#0b0b0b"
INK_2 = "#52514e"
INK_MUTED = "#8a8880"
SURFACE = "#fcfcfb"

FAILURES = []


def check(label, ok, detail=""):
    """Record a claim check. Every check is printed; failures abort at the end."""
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAILURES.append(f"{label}: {detail}")
    return ok


def check_close(label, got, key):
    exp, tol = EXPECT[key], TOL[key]
    return check(label, abs(got - exp) <= tol,
                 f"got {got:.6g}, expected {exp:g} +/- {tol:g}")


def tau_from_filename(path):
    m = re.search(r"_tau(\d+p\d+)_raw\.json$", os.path.basename(path))
    if not m:
        raise ValueError(f"cannot parse tau from filename: {path}")
    return float(m.group(1).replace("p", "."))


def load_surface():
    """Load the 196-cell P(systemic) surface, verifying provenance as we go."""
    files = sorted(glob.glob(RAW_GLOB))
    if not files:
        raise FileNotFoundError(
            f"No raw files matched {RAW_GLOB}.\n"
            f"Regenerate them first:  python scripts/run_q4_psys_boundary.py")

    print("\n=== provenance checks ===")
    check("28 raw files present", len(files) == EXPECT["n_raws"], f"found {len(files)}")

    rows, commits, seed_sizes, engines, thetas, trials = [], set(), set(), set(), set(), set()
    for fp in files:
        with open(fp) as f:
            d = json.load(f)
        md = d["metadata"]
        commits.add(md["git_commit"])
        engines.add(md["engine"])
        thetas.add(md["theta"])
        trials.add(md["trials_per_cell"])
        seed_sizes.update(d["sweep_parameters"]["seed_size_grid"])

        tau = tau_from_filename(fp)
        # cross-check the filename against the committed config it came from
        cfg_name = os.path.basename(fp).replace("_raw.json", ".json")
        cfg_path = os.path.join(CFG_DIR, cfg_name)
        with open(cfg_path) as f:
            cfg = json.load(f)
        cfg_tau = cfg["pinned_params"]["graph"]["tau"]
        if abs(cfg_tau - tau) > 1e-12 or cfg["pinned_params"]["n"] != md["n"]:
            FAILURES.append(f"{cfg_name}: config (n={cfg['pinned_params']['n']}, "
                            f"tau={cfg_tau}) does not match raw (n={md['n']}, tau={tau})")

        theta = md["theta"]
        for cell in d["results"]:
            ff = np.asarray(cell["failed_fractions"], dtype=float)
            P = float(np.mean(ff >= theta))
            rows.append(dict(n=md["n"], tau=tau, mu=cell["mean_fear"],
                             a=cell["seed_size"], P=P, nt=len(ff),
                             se=float(np.sqrt(P * (1 - P) / len(ff)))))

    check("filename tau / n agree with the committed configs (28/28)",
          not any("does not match raw" in f for f in FAILURES))
    check("single uniform git_commit across all raws", len(commits) == 1, str(sorted(commits)))
    check("git_commit is not the 'dirty-or-unknown' sentinel",
          "dirty-or-unknown" not in commits)
    check("realized seed size is exactly a = 8 everywhere",
          seed_sizes == {EXPECT["seed_size"]}, str(sorted(seed_sizes)))
    check("engine is 'python' in every raw (no C++ result trusted; §5.4 N/A)",
          engines == {"python"}, str(sorted(engines)))
    check("theta uniform and read from metadata, not hardcoded",
          len(thetas) == 1, f"theta = {sorted(thetas)}")
    check("trials_per_cell == 500 everywhere", trials == {EXPECT["trials_per_cell"]},
          str(sorted(trials)))
    check(f"{EXPECT['n_cells']} cells on the (tau, mu, n) grid",
          len(rows) == EXPECT["n_cells"], f"got {len(rows)}")
    check("every cell has exactly 500 trials",
          all(r["nt"] == EXPECT["trials_per_cell"] for r in rows))

    rows.sort(key=lambda r: (r["n"], r["tau"], r["mu"]))
    return rows, sorted(commits)[0]


def interp_cross(xs, ys, level=P_LEVEL):
    xs, ys = np.asarray(xs, float), np.asarray(ys, float)
    idx = np.argsort(xs)
    xs, ys = xs[idx], ys[idx]
    out = []
    for i in range(len(xs) - 1):
        y0, y1 = ys[i], ys[i + 1]
        if (y0 - level) * (y1 - level) <= 0 and y0 != y1:
            out.append(float(xs[i] + (level - y0) * (xs[i + 1] - xs[i]) / (y1 - y0)))
    return out


def main():
    rows, commit = load_surface()
    ns = sorted({r["n"] for r in rows})
    mus = sorted({r["mu"] for r in rows})

    # ---- locate the P = 0.5 contour in tau, at each (n, mu) ----
    boundary, censored = [], []
    for n in ns:
        for mu in mus:
            pts = sorted((r["tau"], r["P"]) for r in rows if r["n"] == n and r["mu"] == mu)
            xs = interp_cross([t for t, _ in pts], [p for _, p in pts])
            if xs:
                boundary.append(dict(n=n, mu=mu, tau_c=xs[0]))
            else:
                censored.append((n, mu))

    print("\n=== boundary-location checks ===")
    check(f"{EXPECT['n_boundary_points']} boundary points located",
          len(boundary) == EXPECT["n_boundary_points"], f"got {len(boundary)}")
    check("exactly one grid-censored corner, at n=2000, mu=0.90",
          len(censored) == 1 and censored[0][0] == EXPECT["censored"][0]
          and abs(censored[0][1] - EXPECT["censored"][1]) < 1e-9, str(censored))

    bmu = np.array([b["mu"] for b in boundary])
    btc = np.array([b["tau_c"] for b in boundary])
    bL = np.log2(np.array([b["n"] for b in boundary]) / N_REF)
    ss_tot = float(np.sum((btc - btc.mean()) ** 2))

    # ---- reduced fit (the one plotted and quoted) ----
    def quad_nolin(X, a0, c, D):
        mu, L = X
        return a0 + c * L + D * mu ** 2

    p_r, cov_r = curve_fit(quad_nolin, (bmu, bL), btc, p0=[2.6, -0.1, 1.0], maxfev=20000)
    e_r = np.sqrt(np.diag(cov_r))
    a0, c_n, D = map(float, p_r)
    resid = btc - quad_nolin((bmu, bL), *p_r)
    R2_r = float(1 - np.sum(resid ** 2) / ss_tot)
    rmse_r = float(np.sqrt(np.mean(resid ** 2)))

    print("\n=== fit  tau_c = a0 + c*log2(n/2000) + D*mu^2  (27 points) ===")
    for nm, v, e in zip(["a0", "c", "D"], p_r, e_r):
        print(f"      {nm:2s} = {v: .5f} +/- {e:.5f}")
    print(f"      R2 = {R2_r:.5f}   rmse = {rmse_r:.5f} (tau units)")
    check_close("a0 matches the quoted 2.6295", a0, "a0")
    check_close("c  matches the quoted -0.09607", c_n, "c")
    check_close("D  matches the quoted 0.96039", D, "D")
    check_close("R2 matches the quoted 0.96964", R2_r, "R2")
    check("c < 0 and resolved (|c|/sigma > 3): boundary moves DOWN in tau as n grows",
          c_n < 0 and abs(c_n) / e_r[1] > 3, f"|c|/sigma = {abs(c_n)/e_r[1]:.1f}")

    # ---- full quadratic: the linear-in-mu term must stay consistent with zero ----
    def quad(X, a0, c, B, D):
        mu, L = X
        return a0 + c * L + B * mu + D * mu ** 2

    p_q, cov_q = curve_fit(quad, (bmu, bL), btc, p0=[2.4, -0.1, 0.3, 0.5], maxfev=20000)
    e_q = np.sqrt(np.diag(cov_q))
    B, sB = float(p_q[2]), float(e_q[2])
    R2_q = float(1 - np.sum((btc - quad((bmu, bL), *p_q)) ** 2) / ss_tot)
    print(f"\n=== full quadratic (adds B*mu):  B = {B: .5f} +/- {sB:.5f}   R2 = {R2_q:.5f} ===")
    check_close("B matches the quoted -0.030", B, "B")
    check_close("sigma_B matches the quoted 0.119", sB, "B_stderr")
    check("B is CONSISTENT WITH ZERO (|B|/sigma_B < 1) -- no linear-in-mu claim licensed",
          abs(B) / sB < 1.0, f"|B|/sigma_B = {abs(B)/sB:.2f}")
    check("dropping B costs < 0.001 in R2 (justifies the reduced form)",
          abs(R2_q - R2_r) < 1e-3, f"dR2 = {R2_q - R2_r:.2e}")

    # ---- logistic collapse: asserted to be a BAD fit, because it is ----
    X = np.array([[r["tau"], r["mu"], np.log2(r["n"] / N_REF)] for r in rows])
    y = np.array([r["P"] for r in rows])
    sig = np.array([max(r["se"], 1e-3) for r in rows])

    def logi(X, tc0, D2, c2, w):
        return 1.0 / (1.0 + np.exp((X[:, 0] - (tc0 + D2 * X[:, 1] ** 2 + c2 * X[:, 2])) / w))

    p_l, _ = curve_fit(logi, X, y, p0=[2.6, 1.0, -0.1, 0.12],
                       sigma=sig, absolute_sigma=True, maxfev=40000)
    dof = len(y) - len(p_l)
    chi2_dof = float(np.sum(((y - logi(X, *p_l)) / sig) ** 2) / dof)
    print(f"\n=== single-argument logistic collapse: chi2/dof = {chi2_dof:.2f} (dof={dof}) ===")
    check_close("chi2/dof matches the quoted 33.70", chi2_dof, "chi2_per_dof")
    check("chi2/dof >= 10, i.e. the constant-width collapse UNDERFITS (reported, not hidden)",
          chi2_dof >= 10)

    if FAILURES:
        print("\n" + "=" * 72)
        print(f"{len(FAILURES)} CHECK(S) FAILED -- figure NOT written:")
        for f in FAILURES:
            print("  - " + f)
        print("=" * 72)
        raise SystemExit(1)
    print("\nAll claim checks passed. Drawing the figure.")

    # ================== figure ==================
    os.makedirs(FIG_DIR, exist_ok=True)
    fig = plt.figure(figsize=(8.0, 5.8), facecolor=SURFACE)
    ax = fig.add_axes([0.105, 0.135, 0.755, 0.625])
    ax.set_facecolor(SURFACE)

    mm = np.linspace(0, max(mus), 200)
    for col, n in zip(RAMP, ns):
        bs = sorted([b for b in boundary if b["n"] == n], key=lambda b: b["mu"])
        yy = a0 + c_n * np.log2(n / N_REF) + D * mm ** 2
        ax.plot(mm, yy, "-", color=col, lw=2, alpha=0.95, zorder=2)
        ax.plot([b["mu"] for b in bs], [b["tau_c"] for b in bs], "o", color=col, ms=8,
                zorder=3, markeredgecolor=SURFACE, markeredgewidth=2, label=f"n = {n:,}")
        # direct label at the right end of each fitted curve (4 series, all labeled,
        # so identity is never carried by color alone)
        ax.annotate(f"n = {n:,}", xy=(mm[-1], yy[-1]), xytext=(8, 0),
                    textcoords="offset points", va="center", fontsize=9.5,
                    color=INK_2, annotation_clip=False)

    # mark the one grid-censored corner rather than letting it silently vanish
    _, muc = censored[0]
    ax.plot([muc], [3.56], "^", color=INK_MUTED, ms=9, zorder=3, clip_on=False)
    ax.annotate("censored: P never crosses 0.5\non the $\\tau$ grid  ($n$ = 2,000, $\\mu$ = 0.90)",
                xy=(muc, 3.56), xytext=(-12, 0), textcoords="offset points",
                ha="right", va="center", fontsize=8.5, color=INK_MUTED, linespacing=1.4)

    ax.set_xlabel(r"$\mu$   mean fear", fontsize=11, color=INK_2, labelpad=8)
    ax.set_ylabel(r"$\tau_c$   tail exponent at which P(systemic) $=0.5$",
                  fontsize=11, color=INK_2, labelpad=8)
    ax.grid(True, color="#e6e5e1", lw=0.8, zorder=0)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#d8d7d2")
    ax.tick_params(colors=INK_2, labelsize=9.5)
    ax.set_xlim(-0.03, max(mus) + 0.04)
    ax.set_ylim(2.30, 3.62)
    leg = ax.legend(frameon=False, fontsize=9.5, labelcolor=INK_2,
                    loc="upper left", handletextpad=0.4, borderpad=0.2)
    leg.set_title("simulated size $n$", prop={"size": 9})
    leg.get_title().set_color(INK_MUTED)

    fig.text(0.015, 0.965, "Where the cascade boundary sits",
             fontsize=15, color=INK, va="top", fontweight="bold")
    fig.text(0.015, 0.912,
             f"Points: interpolated P = 0.5 crossings, {len(boundary)} of 28 grid cells.\n"
             f"Lines: $\\tau_c = {a0:.3f} {c_n:+.3f}\\,\\log_2(n/2000) + {D:.3f}\\,\\mu^2$"
             f"   ($R^2 = {R2_r:.3f}$, RMSE {rmse_r:.3f} in $\\tau$; "
             "no linear-in-$\\mu$ term is resolved).\n"
             "Descriptive fit on a finite grid at fixed seed size $a=8$ "
             "($r=2$, $\\theta=0.5$, config. model $d_{\\min}=2$, $\\gamma=0$) — not a law.",
             fontsize=8.5, color=INK_2, va="top", linespacing=1.7)
    fig.text(0.015, 0.018,
             f"98,000 Python-engine runs · 500 trials/cell · base_seed 42 · "
             f"raws stamped {commit[:7]} · scripts/verify_q4_psys_boundary_figure.py",
             fontsize=7.5, color=INK_MUTED)

    fig.savefig(FIG_PATH, dpi=150, facecolor=SURFACE)
    plt.close(fig)

    if not os.path.exists(FIG_PATH):
        raise SystemExit(f"figure was not written to {FIG_PATH}")
    print(f"wrote {FIG_PATH}  ({os.path.getsize(FIG_PATH)} bytes)")


if __name__ == "__main__":
    sys.exit(main())
