"""Analyze the Q4 P(systemic) cascade-boundary sweep and refit tau_c(mu, n) at a=8.

Reads the runner-produced raws results/q4_psys_boundary_n{n}_tau{tag}_raw.json,
builds the P(systemic) surface over (tau, mu, n), locates the P=0.5 boundary by
linear interpolation along tau at fixed mu, and fits the EMPIRICAL boundary form

    tau_c(mu, n) = a0 + c * log2(n / 2000) + B * mu + D * mu^2

plus a single-argument logistic collapse of the full surface

    P = 1 / (1 + exp((tau - (tc0 + D*mu^2 + c*log2(n/2000))) / w)).

This is a descriptive fit on a finite grid, not a law, theorem, or asymptotic
scaling form. See walkthrough.md for the caveats.

Outputs (script owns nothing in results/ except these regenerable artifacts):
    results/figures/q4_psys_boundary_heatmap.png
    results/figures/q4_psys_boundary_fitted.png
    results/figures/q4_psys_boundary_collapse.png
    results/processed/q4_psys_boundary_analysis.json

Usage:
    python scripts/analyze_q4_psys_boundary.py
"""

import os
import sys
import json
import glob

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(base_dir, "src"))

RAW_GLOB = os.path.join(base_dir, "results", "q4_psys_boundary_n*_tau*_raw.json")
FIG_DIR = os.path.join(base_dir, "results", "figures")
PROC_DIR = os.path.join(base_dir, "results", "processed")
THETA = 0.5  # systemic iff final failed fraction >= theta


def load_rows():
    """Load every raw cell into a tidy list of dicts."""
    rows = []
    commits = set()
    seed_sizes = set()
    files = sorted(glob.glob(RAW_GLOB))
    if not files:
        raise FileNotFoundError(f"No raw files matched {RAW_GLOB}")
    for fp in files:
        with open(fp) as f:
            d = json.load(f)
        md = d["metadata"]
        n = md["n"]
        commits.add(md["git_commit"])
        seed_sizes.update(d["sweep_parameters"]["seed_size_grid"])
        # tau is a graph parameter, not in metadata -> recover from the filename
        tau = float(os.path.basename(fp).split("_tau")[1].split("_raw")[0].replace("p", "."))
        for cell in d["results"]:
            ff = np.asarray(cell["failed_fractions"])
            nt = len(ff)
            P = float(np.mean(ff >= THETA))
            rows.append(dict(
                n=n, tau=tau, mu=cell["mean_fear"], a=cell["seed_size"],
                P=P, se=float(np.sqrt(P * (1 - P) / nt)), nt=nt,
            ))
    rows.sort(key=lambda r: (r["n"], r["tau"], r["mu"]))
    return rows, files, sorted(commits), sorted(seed_sizes)


def interp_cross(xs, ys, level=0.5):
    """Linear-interpolated crossings of ys(xs) through `level`."""
    xs = np.asarray(xs, dtype=float)
    ys = np.asarray(ys, dtype=float)
    idx = np.argsort(xs)
    xs, ys = xs[idx], ys[idx]
    out = []
    for i in range(len(xs) - 1):
        y0, y1 = ys[i], ys[i + 1]
        if (y0 - level) * (y1 - level) <= 0 and y0 != y1:
            out.append(float(xs[i] + (level - y0) * (xs[i + 1] - xs[i]) / (y1 - y0)))
    return out


def main():
    os.makedirs(FIG_DIR, exist_ok=True)
    os.makedirs(PROC_DIR, exist_ok=True)

    rows, files, commits, seed_sizes = load_rows()
    ns = sorted({r["n"] for r in rows})
    taus = sorted({r["tau"] for r in rows})
    mus = sorted({r["mu"] for r in rows})
    print(f"loaded {len(files)} raws -> {len(rows)} cells")
    print(f"  n   = {ns}")
    print(f"  tau = {taus}")
    print(f"  mu  = {mus}")
    print(f"  git_commit(s) in raws : {commits}")
    print(f"  seed_size_grid values : {seed_sizes}")

    # ---- P = 0.5 boundary ----
    boundary = []      # tau crossing at fixed mu
    boundary_mu = []   # mu crossing at fixed tau
    for n in ns:
        for mu in mus:
            pts = sorted((r["tau"], r["P"]) for r in rows if r["n"] == n and r["mu"] == mu)
            for tc in interp_cross([t for t, _ in pts], [p for _, p in pts]):
                boundary.append(dict(n=n, mu=mu, tau_c=tc))
    for n in ns:
        for tau in taus:
            pts = sorted((r["mu"], r["P"]) for r in rows if r["n"] == n and r["tau"] == tau)
            for mc in interp_cross([m for m, _ in pts], [p for _, p in pts]):
                boundary_mu.append(dict(n=n, tau=tau, mu_c=mc))

    print(f"\n=== P=0.5 boundary points (tau_c at fixed mu): {len(boundary)} ===")
    for n in ns:
        bs = sorted([b for b in boundary if b["n"] == n], key=lambda b: b["mu"])
        print(f"  n={n:6d}: " + "  ".join(f"mu={b['mu']:.2f}->{b['tau_c']:.3f}" for b in bs))

    bmu = np.array([b["mu"] for b in boundary])
    btc = np.array([b["tau_c"] for b in boundary])
    bL = np.log2(np.array([b["n"] for b in boundary]) / 2000.0)

    # ---- boundary fit: tau_c = a0 + c*log2(n/2000) + B*mu + D*mu^2 ----
    def quad(X, a0, c, B, D):
        mu, L = X
        return a0 + c * L + B * mu + D * mu ** 2

    p_q, cov_q = curve_fit(quad, (bmu, bL), btc, p0=[2.4, -0.1, 0.3, 0.5], maxfev=20000)
    e_q = np.sqrt(np.diag(cov_q))
    yh = quad((bmu, bL), *p_q)
    ss_tot = np.sum((btc - np.mean(btc)) ** 2)
    R2_q = float(1 - np.sum((btc - yh) ** 2) / ss_tot)
    rmse_q = float(np.sqrt(np.mean((btc - yh) ** 2)))
    print("\n=== boundary fit  tau_c = a0 + c*log2(n/2000) + B*mu + D*mu^2 ===")
    for nm, v, e in zip(["a0", "c", "B", "D"], p_q, e_q):
        print(f"  {nm:2s} = {v:8.4f} +/- {e:.4f}")
    print(f"  R2 = {R2_q:.4f}   rmse = {rmse_q:.4f} (tau units)")

    # ---- reduced (mu^2-only) boundary fit, used for the plotted surface ----
    def quad_nolin(X, a0, c, D):
        mu, L = X
        return a0 + c * L + D * mu ** 2

    p_r, cov_r = curve_fit(quad_nolin, (bmu, bL), btc, p0=[2.6, -0.1, 1.0], maxfev=20000)
    e_r = np.sqrt(np.diag(cov_r))
    yh_r = quad_nolin((bmu, bL), *p_r)
    R2_r = float(1 - np.sum((btc - yh_r) ** 2) / ss_tot)
    rmse_r = float(np.sqrt(np.mean((btc - yh_r) ** 2)))
    a0, c_n, D = p_r
    print("\n=== reduced boundary fit  tau_c = a0 + c*log2(n/2000) + D*mu^2 ===")
    for nm, v, e in zip(["a0", "c", "D"], p_r, e_r):
        print(f"  {nm:2s} = {v:8.4f} +/- {e:.4f}")
    print(f"  R2 = {R2_r:.4f}   rmse = {rmse_r:.4f}")

    # ---- full-surface single-argument logistic collapse ----
    X = np.array([[r["tau"], r["mu"], np.log2(r["n"] / 2000.0)] for r in rows])
    y = np.array([r["P"] for r in rows])
    sig = np.array([max(r["se"], 1e-3) for r in rows])

    def logi(X, tc0, D2, c2, w):
        tau, mu, L = X[:, 0], X[:, 1], X[:, 2]
        return 1.0 / (1.0 + np.exp((tau - (tc0 + D2 * mu ** 2 + c2 * L)) / w))

    p_l, cov_l = curve_fit(logi, X, y, p0=[2.6, 1.0, -0.1, 0.12],
                           sigma=sig, absolute_sigma=True, maxfev=40000)
    e_l = np.sqrt(np.diag(cov_l))
    yhl = logi(X, *p_l)
    R2_l = float(1 - np.sum((y - yhl) ** 2) / np.sum((y - np.mean(y)) ** 2))
    dof = len(y) - len(p_l)
    chi2 = float(np.sum(((y - yhl) / sig) ** 2))
    print("\n=== full-surface logistic collapse  P=1/(1+exp((tau-(tc0+D*mu^2+c*log2(n/2000)))/w)) ===")
    for nm, v, e in zip(["tc0", "D", "c", "w"], p_l, e_l):
        print(f"  {nm:3s} = {v:8.4f} +/- {e:.4f}")
    print(f"  R2 = {R2_l:.4f}   chi2/dof = {chi2/dof:.2f} (dof={dof})")

    # ================= figures =================
    # heatmaps of the P surface, with the P=0.5 boundary overlaid
    fig, axes = plt.subplots(1, len(ns), figsize=(4.2 * len(ns), 4.0), constrained_layout=True)
    if len(ns) == 1:
        axes = [axes]
    for ax, n in zip(axes, ns):
        G = np.full((len(taus), len(mus)), np.nan)
        for r in rows:
            if r["n"] == n:
                G[taus.index(r["tau"]), mus.index(r["mu"])] = r["P"]
        im = ax.imshow(G, origin="lower", aspect="auto", vmin=0, vmax=1, cmap="viridis",
                       extent=[min(mus), max(mus), min(taus), max(taus)])
        bs = sorted([b for b in boundary if b["n"] == n], key=lambda b: b["mu"])
        if bs:
            ax.plot([b["mu"] for b in bs], [b["tau_c"] for b in bs], "w.-", lw=1.5, ms=6)
        ax.set_title(f"n={n}")
        ax.set_xlabel(r"$\mu$ (mean fear)")
        if ax is axes[0]:
            ax.set_ylabel(r"$\tau$ (degree tail exponent)")
    fig.colorbar(im, ax=axes, label="P(systemic)", shrink=0.8)
    fig.suptitle("P(systemic) over $(\\mu,\\tau)$; white = interpolated P=0.5 boundary "
                 "[seed a=8, r=2, $\\theta$=0.5]")
    fig.savefig(os.path.join(FIG_DIR, "q4_psys_boundary_heatmap.png"), dpi=130)
    plt.close(fig)

    # boundary points + fitted surface
    plt.figure(figsize=(7, 5.3))
    cols = plt.cm.plasma(np.linspace(0.12, 0.85, len(ns)))
    mm = np.linspace(0, max(mus), 100)
    for col, n in zip(cols, ns):
        bs = sorted([b for b in boundary if b["n"] == n], key=lambda b: b["mu"])
        plt.plot([b["mu"] for b in bs], [b["tau_c"] for b in bs], "o", color=col, ms=7, label=f"n={n}")
        plt.plot(mm, a0 + c_n * np.log2(n / 2000.0) + D * mm ** 2, "-", color=col, lw=1.8, alpha=0.8)
    plt.xlabel(r"$\mu$  (mean fear)", fontsize=12)
    plt.ylabel(r"$\tau_c$  :  P(systemic) = 0.5", fontsize=12)
    plt.title(f"Empirical boundary  $\\tau_c=${a0:.2f}${c_n:+.3f}\\log_2(n/2000)+{D:.2f}\\mu^2$\n"
              "seed a=8, r=2, $\\theta$=0.5, config-model $d_{min}$=2  (fit, not a law)",
              fontsize=11)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "q4_psys_boundary_fitted.png"), dpi=140)
    plt.close()

    # single-argument collapse
    u = X[:, 0] - (p_l[1] * X[:, 1] ** 2 + p_l[2] * X[:, 2])
    plt.figure(figsize=(7, 5.3))
    sc = plt.scatter(u, y, c=X[:, 2], cmap="plasma", s=28, edgecolor="k", lw=0.2)
    uu = np.linspace(u.min(), u.max(), 200)
    plt.plot(uu, 1 / (1 + np.exp((uu - p_l[0]) / p_l[3])), "k-", lw=2,
             label=f"logistic (R$^2$={R2_l:.3f}, $\\chi^2$/dof={chi2/dof:.0f})")
    plt.xlabel("collapse variable  $u=\\tau-{:.2f}\\mu^2-({:.3f})\\log_2(n/2000)$".format(p_l[1], p_l[2]),
               fontsize=11)
    plt.ylabel("P(systemic)")
    plt.colorbar(sc, label="$\\log_2(n/2000)$")
    plt.title(f"Single-argument collapse of the full P surface ({len(rows)} cells)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "q4_psys_boundary_collapse.png"), dpi=140)
    plt.close()

    # ================= processed output =================
    out = {
        "description": "Empirical P(systemic)=0.5 cascade boundary tau_c(mu, n) at seed size a=8. "
                       "Descriptive fit on a finite grid; not a law or asymptotic scaling form.",
        "theta": THETA,
        "source_raws": [os.path.relpath(f, base_dir) for f in files],
        "git_commits_in_raws": commits,
        "seed_size_grid_values": [int(s) for s in seed_sizes],
        "grid": {"n": ns, "tau": taus, "mu": mus, "n_cells": len(rows)},
        "p_surface": rows,
        "boundary_tau_at_fixed_mu": boundary,
        "boundary_mu_at_fixed_tau": boundary_mu,
        "fit_boundary_quadratic": {
            "form": "tau_c = a0 + c*log2(n/2000) + B*mu + D*mu^2",
            "params": dict(zip(["a0", "c", "B", "D"], map(float, p_q))),
            "stderr": dict(zip(["a0", "c", "B", "D"], map(float, e_q))),
            "R2": R2_q, "rmse": rmse_q, "n_points": len(boundary),
        },
        "fit_boundary_mu2_only": {
            "form": "tau_c = a0 + c*log2(n/2000) + D*mu^2",
            "params": dict(zip(["a0", "c", "D"], map(float, p_r))),
            "stderr": dict(zip(["a0", "c", "D"], map(float, e_r))),
            "R2": R2_r, "rmse": rmse_r, "n_points": len(boundary),
        },
        "fit_logistic_collapse": {
            "form": "P = 1/(1+exp((tau-(tc0+D*mu^2+c*log2(n/2000)))/w))",
            "params": dict(zip(["tc0", "D", "c", "w"], map(float, p_l))),
            "stderr": dict(zip(["tc0", "D", "c", "w"], map(float, e_l))),
            "R2": R2_l, "chi2": chi2, "dof": int(dof), "chi2_per_dof": chi2 / dof,
        },
    }
    out_path = os.path.join(PROC_DIR, "q4_psys_boundary_analysis.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nwrote {out_path}")
    print(f"wrote 3 figures to {FIG_DIR}")


if __name__ == "__main__":
    main()
