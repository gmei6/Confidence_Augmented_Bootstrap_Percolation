#!/usr/bin/env python3
"""
benchmark_scaling.py — Find this machine's limits for the two-channel cascade.

A measurement / profiling tool (NOT a science result). It answers:
  1. How does per-cascade wall time grow with n, and what is the largest n
     that stays under a per-cascade time budget?  (the "ceiling")
  2. How many cascades/sec can this machine sustain (single- and multi-threaded)?
  3. How well does the C++ OpenMP core scale across cores?
  4. How much faster is the C++ core than the pure-Python reference?
  5. How much memory does a cascade need at each n?
  6. Given the throughput, how long would 1e6 / 1e7 cascades take here
     (laptop-vs-PACE feasibility, ties to the advisor brief's realization budgets)?

It treats the built C++ binary (cpp/build/twocascade_run) as a black box via its
CLI, and the pure-Python engine (src/twocascade/reference.py) in-process.

Governance notes:
  * Reproducible: fixed base seed, logged git commit / platform / config.
  * Writes ONLY to <repo>/docs/benchmarks/ — never results/raw or results/figures.
  * Does not import or modify the protected oracle's behavior; read-only use.

Usage (run on YOUR machine, from anywhere):
    python scripts/benchmark_scaling.py                 # full suite, sensible defaults
    python scripts/benchmark_scaling.py --mode nsweep   # just the size-ceiling sweep
    python scripts/benchmark_scaling.py --mode threads  # just the OpenMP scaling
    python scripts/benchmark_scaling.py --engine python # if the C++ core isn't built
    python scripts/benchmark_scaling.py --help          # all knobs
"""

from __future__ import annotations

import argparse
import csv
import datetime as _dt
import json
import os
import platform
import re
import resource
import subprocess
import sys
import time
from pathlib import Path


# --------------------------------------------------------------------------- #
# Repo / engine location
# --------------------------------------------------------------------------- #
def find_repo_root(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).resolve()
    # scripts/benchmark_scaling.py -> repo root is the parent of scripts/
    here = Path(__file__).resolve()
    if here.parent.name == "scripts":
        return here.parent.parent
    return Path.cwd()


def import_python_engine(repo: Path):
    """Import the pure-Python reference engine + model helpers from <repo>/src."""
    src = repo / "src"
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))
    from twocascade import reference as ref  # type: ignore
    from twocascade import model as mdl  # type: ignore
    return ref, mdl


# --------------------------------------------------------------------------- #
# Platform / provenance
# --------------------------------------------------------------------------- #
def _sysctl(key: str) -> str | None:
    try:
        out = subprocess.run(["sysctl", "-n", key], capture_output=True, text=True, check=True)
        return out.stdout.strip()
    except Exception:
        return None


def detect_platform() -> dict:
    info = {
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "processor": platform.processor() or None,
        "logical_cpus": os.cpu_count(),
        "python": platform.python_version(),
    }
    try:
        import numpy as _np  # noqa
        info["numpy"] = _np.__version__
    except Exception:
        info["numpy"] = None

    if platform.system() == "Darwin":
        info["cpu_brand"] = _sysctl("machdep.cpu.brand_string")
        info["hw_model"] = _sysctl("hw.model")
        physcpu = _sysctl("hw.physicalcpu")
        memb = _sysctl("hw.memsize")
        info["physical_cpus"] = int(physcpu) if physcpu and physcpu.isdigit() else None
        info["ram_gb"] = round(int(memb) / 1024**3, 1) if memb and memb.isdigit() else None
    elif platform.system() == "Linux":
        try:
            with open("/proc/cpuinfo") as f:
                for line in f:
                    if line.startswith("model name"):
                        info["cpu_brand"] = line.split(":", 1)[1].strip()
                        break
        except Exception:
            info["cpu_brand"] = None
        try:
            with open("/proc/meminfo") as f:
                for line in f:
                    if line.startswith("MemTotal"):
                        kb = int(re.search(r"(\d+)", line).group(1))
                        info["ram_gb"] = round(kb / 1024**2, 1)
                        break
        except Exception:
            info["ram_gb"] = None
    return info


def get_git_commit(repo: Path) -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=str(repo), capture_output=True, text=True, check=True,
        )
        return out.stdout.strip()
    except Exception:
        return "unknown"


# --------------------------------------------------------------------------- #
# Parameter scaling
# --------------------------------------------------------------------------- #
def compute_p_and_degree(n: int, args, mdl) -> tuple[float, float]:
    """Return (p, mean_degree) for system size n under the chosen regime."""
    if args.scaling == "fixed":
        deg = args.fixed_degree
        p = min(1.0, deg / max(1, n - 1))
        return p, p * (n - 1)
    # Janson regime: p_n = beta * n^-alpha, beta frozen at n_ref (matches configs/*).
    beta = mdl.calculate_beta(args.target_mean_degree, args.n_ref, args.alpha)
    p = mdl.calculate_p_n(beta, n, args.alpha)
    return p, p * (n - 1)


def seed_size_for(n: int, p: float, r: int, mult: float, mdl) -> int:
    try:
        ac0 = mdl.janson_a_c(n, p, r)
    except Exception:
        ac0 = 1.0
    return max(r, round(mult * ac0))


# --------------------------------------------------------------------------- #
# Memory helpers
# --------------------------------------------------------------------------- #
def _maxrss_bytes_to_bytes(ru_maxrss: int) -> int:
    # ru_maxrss is bytes on macOS/BSD, kilobytes on Linux.
    return ru_maxrss if platform.system() == "Darwin" else ru_maxrss * 1024


def measure_cpp_peak_rss(cpp_bin: str, n, p, r, mu, kappa, a, seed, threads) -> int | None:
    """Peak resident set of one short C++ run, via /usr/bin/time. None if unavailable."""
    cmd = [
        cpp_bin, "--n", str(n), "--p", repr(p), "--r", str(r), "--mu", str(mu),
        "--kappa", str(kappa), "--seed-size", str(a), "--trials", "2",
        "--base-seed", str(seed), "--window-len", "1",
    ]
    env = {**os.environ, "OMP_NUM_THREADS": str(threads)}
    is_mac = platform.system() == "Darwin"
    time_flag = "-l" if is_mac else "-v"
    if not os.path.exists("/usr/bin/time"):
        return None
    try:
        res = subprocess.run(["/usr/bin/time", time_flag] + cmd,
                             capture_output=True, text=True, env=env, timeout=120)
    except Exception:
        return None
    err = res.stderr
    if is_mac:
        m = re.search(r"(\d+)\s+maximum resident set size", err)
        if m:
            return int(m.group(1))  # bytes on macOS
    else:
        m = re.search(r"Maximum resident set size \(kbytes\):\s*(\d+)", err)
        if m:
            return int(m.group(1)) * 1024
    return None


# --------------------------------------------------------------------------- #
# Engine runners
# --------------------------------------------------------------------------- #
def run_cpp(cpp_bin: str, n, p, r, mu, kappa, a, trials, seed, threads) -> dict:
    """Run `trials` cascades through the C++ binary; return timing + sanity stats."""
    cmd = [
        cpp_bin, "--n", str(n), "--p", repr(p), "--r", str(r), "--mu", str(mu),
        "--kappa", str(kappa), "--seed-size", str(a), "--trials", str(trials),
        "--base-seed", str(seed), "--window-len", "1",
    ]
    env = {**os.environ, "OMP_NUM_THREADS": str(threads)}
    t0 = time.perf_counter()
    res = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=3600)
    wall = time.perf_counter() - t0
    if res.returncode != 0:
        raise RuntimeError(f"C++ engine failed (rc={res.returncode}): {res.stderr.strip()}")
    ffs = []
    for line in res.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        ffs.append(float(line.split()[0]))
    if len(ffs) != trials:
        raise RuntimeError(f"expected {trials} trials, parsed {len(ffs)}")
    return {
        "wall_s": wall,
        "per_cascade_s": wall / trials,
        "cascades_per_s": trials / wall if wall > 0 else float("inf"),
        "mean_failed_fraction": sum(ffs) / len(ffs),
        "trials": trials,
        "threads": threads,
    }


def run_python(ref, n, p, r, mu, kappa, a, trials, seed, measure_mem=False) -> dict:
    """Run `trials` cascades through the pure-Python reference engine, in-process."""
    import numpy as np
    import tracemalloc
    rng = np.random.default_rng(seed)
    py_peak = None
    if measure_mem:
        tracemalloc.start()
        tracemalloc.reset_peak()
    t0 = time.perf_counter()
    ff_sum = 0.0
    for _ in range(trials):
        adj = ref.sample_gnp_adjacency(n, p, rng)
        fears = ref.sample_individual_fears(n, mean_fear=mu, concentration=kappa, rng=rng)
        nodes = ref.make_nodes(fears)
        seeds = ref.choose_seed(n, a, adj, rng, False)
        out = ref.run_cascade(adjacency=adj, nodes=nodes, r=r, seed_indices=seeds,
                              rng=rng, record_history=False)
        ff_sum += out.final_failed_fraction
    wall = time.perf_counter() - t0
    if measure_mem:
        py_peak = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()
    return {
        "wall_s": wall,
        "per_cascade_s": wall / trials,
        "cascades_per_s": trials / wall if wall > 0 else float("inf"),
        "mean_failed_fraction": ff_sum / trials,
        "trials": trials,
        "threads": 1,
        "py_peak_bytes": py_peak,
    }


def _choose_trials(per_cascade_est: float, measure_seconds: float,
                   min_trials: int, max_trials: int) -> int:
    if per_cascade_est <= 0:
        return max_trials
    return max(min_trials, min(max_trials, int(measure_seconds / per_cascade_est)))


# --------------------------------------------------------------------------- #
# Mode: n-sweep with auto-stop (the size ceiling)
# --------------------------------------------------------------------------- #
def run_nsweep(args, mdl, cpp_bin, ref) -> list[dict]:
    print("\n" + "=" * 72)
    print(f"SIZE SWEEP  ({'C++' if cpp_bin else 'Python'} primary)  "
          f"regime={args.scaling}  r={args.r}  mu={args.mu}  seed_mult={args.seed_multiple}")
    print("  (single-threaded per-cascade cost; auto-stops past the time budget)")
    print("=" * 72)
    header = f"{'n':>9} {'deg':>6} {'seed':>6} {'s/cascade':>12} {'casc/s':>10} {'mem':>9} {'meanFF':>7}"
    print(header)
    print("-" * len(header))

    rows = []
    t_start = time.perf_counter()
    for n in args.n_list:
        if time.perf_counter() - t_start > args.max_total_seconds:
            print(f"[stop] total time budget ({args.max_total_seconds}s) reached.")
            break
        p, deg = compute_p_and_degree(n, args, mdl)
        a = seed_size_for(n, p, args.r, args.seed_multiple, mdl)

        try:
            if cpp_bin:
                cal = run_cpp(cpp_bin, n, p, args.r, args.mu, args.kappa, a,
                              args.calib_trials, args.base_seed, 1)
            else:
                cal = run_python(ref, n, p, args.r, args.mu, args.kappa, a,
                                 max(2, args.calib_trials // 2), args.base_seed)
        except Exception as e:
            print(f"{n:>9}  [error] {e}")
            rows.append({"n": n, "p": p, "mean_degree": deg, "seed_size": a, "error": str(e)})
            continue

        per_cascade = cal["per_cascade_s"]
        if per_cascade > args.max_seconds_per_cascade:
            print(f"{n:>9} {deg:>6.1f} {a:>6} {per_cascade:>12.4f}  -> exceeds "
                  f"{args.max_seconds_per_cascade}s/cascade budget; ceiling reached.")
            rows.append({"n": n, "p": p, "mean_degree": deg, "seed_size": a,
                         "per_cascade_s": per_cascade, "ceiling": True})
            break

        trials = _choose_trials(per_cascade, args.measure_seconds,
                                args.min_trials, args.max_trials)
        if cpp_bin:
            m = run_cpp(cpp_bin, n, p, args.r, args.mu, args.kappa, a, trials, args.base_seed, 1)
            peak = measure_cpp_peak_rss(cpp_bin, n, p, args.r, args.mu, args.kappa, a,
                                        args.base_seed, 1) if args.measure_mem else None
            m["peak_rss_bytes"] = peak
        else:
            m = run_python(ref, n, p, args.r, args.mu, args.kappa, a, trials,
                           args.base_seed, measure_mem=args.measure_mem)
            peak = m.get("py_peak_bytes")
            m["peak_rss_bytes"] = peak

        mem_str = f"{peak/1024**2:>7.1f}M" if peak else "    n/a"
        print(f"{n:>9} {deg:>6.1f} {a:>6} {m['per_cascade_s']:>12.5f} "
              f"{m['cascades_per_s']:>10.1f} {mem_str:>9} {m['mean_failed_fraction']:>7.3f}")
        m.update({"n": n, "p": p, "mean_degree": deg, "seed_size": a, "ceiling": False})
        rows.append(m)
    return rows


# --------------------------------------------------------------------------- #
# Mode: OpenMP thread scaling (C++ only)
# --------------------------------------------------------------------------- #
def run_thread_scaling(args, mdl, cpp_bin) -> list[dict]:
    if not cpp_bin:
        return []
    ncpu = os.cpu_count() or 1
    thread_list = [k for k in args.threads_list if k <= ncpu]
    if ncpu not in thread_list:
        thread_list.append(ncpu)
    thread_list = sorted(set(thread_list))

    n = args.thread_bench_n
    p, deg = compute_p_and_degree(n, args, mdl)
    a = seed_size_for(n, p, args.r, args.seed_multiple, mdl)
    trials = args.thread_bench_trials

    print("\n" + "=" * 72)
    print(f"OPENMP THREAD SCALING  (n={n}, deg={deg:.1f}, trials={trials}, "
          f"logical CPUs={ncpu})")
    print("=" * 72)
    head = f"{'threads':>8} {'wall_s':>9} {'casc/s':>10} {'speedup':>8} {'efficiency':>11}"
    print(head)
    print("-" * len(head))

    rows = []
    base_thr = None
    for k in thread_list:
        m = run_cpp(cpp_bin, n, p, args.r, args.mu, args.kappa, a, trials, args.base_seed, k)
        if base_thr is None:
            base_thr = m["cascades_per_s"]
        speedup = m["cascades_per_s"] / base_thr if base_thr else 1.0
        eff = speedup / k
        print(f"{k:>8} {m['wall_s']:>9.3f} {m['cascades_per_s']:>10.1f} "
              f"{speedup:>7.2f}x {eff*100:>9.0f}%")
        m.update({"n": n, "speedup": speedup, "efficiency": eff})
        rows.append(m)
    return rows


# --------------------------------------------------------------------------- #
# Mode: C++ vs Python head-to-head
# --------------------------------------------------------------------------- #
def run_compare(args, mdl, cpp_bin, ref) -> list[dict]:
    if not (cpp_bin and ref):
        return []
    print("\n" + "=" * 72)
    print("C++ vs PYTHON  (single-threaded, same parameters)")
    print("=" * 72)
    head = f"{'n':>8} {'cpp s/casc':>12} {'py s/casc':>12} {'speedup':>9}"
    print(head)
    print("-" * len(head))
    rows = []
    for n in args.compare_n_list:
        p, deg = compute_p_and_degree(n, args, mdl)
        a = seed_size_for(n, p, args.r, args.seed_multiple, mdl)
        try:
            c = run_cpp(cpp_bin, n, p, args.r, args.mu, args.kappa, a,
                        max(20, args.min_trials), args.base_seed, 1)
            py = run_python(ref, n, p, args.r, args.mu, args.kappa, a,
                            max(5, args.min_trials // 2), args.base_seed)
        except Exception as e:
            print(f"{n:>8}  [error] {e}")
            continue
        ratio = py["per_cascade_s"] / c["per_cascade_s"] if c["per_cascade_s"] > 0 else float("inf")
        print(f"{n:>8} {c['per_cascade_s']:>12.5f} {py['per_cascade_s']:>12.5f} {ratio:>8.0f}x")
        rows.append({"n": n, "cpp_per_cascade_s": c["per_cascade_s"],
                     "py_per_cascade_s": py["per_cascade_s"], "speedup": ratio})
    return rows


# --------------------------------------------------------------------------- #
# Feasibility extrapolation
# --------------------------------------------------------------------------- #
def _fmt_duration(seconds: float) -> str:
    if seconds < 90:
        return f"{seconds:.0f}s"
    if seconds < 90 * 60:
        return f"{seconds/60:.1f} min"
    if seconds < 48 * 3600:
        return f"{seconds/3600:.1f} h"
    return f"{seconds/86400:.1f} days"


def run_extrapolation(args, nsweep_rows, thread_rows) -> list[dict]:
    usable = [r for r in nsweep_rows if not r.get("ceiling") and not r.get("error")
              and r.get("cascades_per_s")]
    if not usable:
        return []
    best_speedup = max((r["speedup"] for r in thread_rows), default=1.0)

    # Reference sizes: the explicit finite-size targets that fall within reach.
    ref_ns = [r for r in usable if r["n"] in args.extrapolate_n]
    if not ref_ns:
        ref_ns = [usable[len(usable) // 2], usable[-1]]

    print("\n" + "=" * 72)
    print("FEASIBILITY  (time to complete a full realization budget on THIS machine)")
    print(f"  assuming best observed OpenMP speedup of {best_speedup:.2f}x across cores")
    print("=" * 72)
    head = f"{'n':>9} {'1-thread/s':>11} {'all-core/s':>11} " + \
           " ".join(f"{int(t):>10.0e}".replace('e+0', 'e') for t in args.target_cascades)
    print(head)
    print("-" * len(head))

    rows = []
    for r in ref_ns:
        thr1 = r["cascades_per_s"]
        thr_par = thr1 * best_speedup
        cols = []
        targets = {}
        for t in args.target_cascades:
            secs = t / thr_par
            cols.append(f"{_fmt_duration(secs):>10}")
            targets[f"{t:.0e}"] = secs
        print(f"{r['n']:>9} {thr1:>11.1f} {thr_par:>11.1f} " + " ".join(cols))
        rows.append({"n": r["n"], "throughput_1thread": thr1,
                     "throughput_allcore_est": thr_par, "seconds_for_targets": targets})
    return rows


# --------------------------------------------------------------------------- #
# Output
# --------------------------------------------------------------------------- #
def write_outputs(out_dir: Path, payload: dict) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path = out_dir / f"benchmark_{stamp}.json"
    with open(json_path, "w") as f:
        json.dump(payload, f, indent=2)

    csv_path = out_dir / f"benchmark_nsweep_{stamp}.csv"
    rows = payload.get("nsweep", [])
    if rows:
        keys = ["n", "p", "mean_degree", "seed_size", "per_cascade_s",
                "cascades_per_s", "peak_rss_bytes", "mean_failed_fraction",
                "trials", "ceiling", "error"]
        with open(csv_path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
            w.writeheader()
            for r in rows:
                w.writerow(r)
    return json_path, csv_path


def maybe_plot(out_dir: Path, payload: dict) -> Path | None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return None
    ns = [(r["n"], r["per_cascade_s"], r.get("cascades_per_s")) for r in payload.get("nsweep", [])
          if r.get("per_cascade_s") and not r.get("ceiling") and not r.get("error")]
    thr = [(r["threads"], r["speedup"]) for r in payload.get("threads", [])]
    if not ns and not thr:
        return None
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    if ns:
        xs = [a for a, _, _ in ns]
        ys = [b for _, b, _ in ns]
        axes[0].loglog(xs, ys, "o-")
        axes[0].set_xlabel("n (banks)")
        axes[0].set_ylabel("seconds / cascade (1 thread)")
        axes[0].set_title("Per-cascade cost vs system size")
        axes[0].grid(True, which="both", alpha=0.3)
    if thr:
        ks = [a for a, _ in thr]
        sp = [b for _, b in thr]
        axes[1].plot(ks, sp, "o-", label="measured")
        axes[1].plot(ks, ks, "--", color="gray", label="ideal")
        axes[1].set_xlabel("OpenMP threads")
        axes[1].set_ylabel("speedup vs 1 thread")
        axes[1].set_title("OpenMP scaling")
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
    fig.tight_layout()
    stamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    png = out_dir / f"benchmark_plot_{stamp}.png"
    fig.savefig(png, dpi=120)
    plt.close(fig)
    return png


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def parse_args(argv=None):
    P = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    P.add_argument("--repo-root", default=None, help="repo root (default: parent of scripts/)")
    P.add_argument("--cpp-bin", default=None, help="path to twocascade_run (default: <repo>/cpp/build/twocascade_run)")
    P.add_argument("--engine", choices=["cpp", "python", "both"], default="both")
    P.add_argument("--mode", choices=["all", "nsweep", "threads", "compare"], default="all")

    P.add_argument("--r", type=int, default=2)
    P.add_argument("--mu", type=float, default=0.3)
    P.add_argument("--kappa", type=float, default=50.0)
    P.add_argument("--seed-multiple", type=float, default=1.0, help="seed = round(mult * a_c(0))")

    P.add_argument("--scaling", choices=["janson", "fixed"], default="janson")
    P.add_argument("--alpha", type=float, default=0.7, help="Janson exponent (needs 1/r<alpha<1)")
    P.add_argument("--target-mean-degree", type=float, default=8.0)
    P.add_argument("--n-ref", type=int, default=1000)
    P.add_argument("--fixed-degree", type=float, default=10.0, help="mean degree if --scaling fixed")

    P.add_argument("--n-list", default="1000,2000,5000,10000,20000,50000,100000,200000,500000,1000000")
    P.add_argument("--compare-n-list", default="1000,5000,20000")
    P.add_argument("--extrapolate-n", default="10000,50000")
    P.add_argument("--target-cascades", default="1e6,1e7")

    P.add_argument("--max-seconds-per-cascade", type=float, default=2.0, help="ceiling: stop sweep past this")
    P.add_argument("--max-total-seconds", type=float, default=240.0, help="overall budget for the sweep")
    P.add_argument("--measure-seconds", type=float, default=1.5, help="target measurement time per n")
    P.add_argument("--calib-trials", type=int, default=3)
    P.add_argument("--min-trials", type=int, default=5)
    P.add_argument("--max-trials", type=int, default=2000)

    P.add_argument("--thread-bench-n", type=int, default=5000)
    P.add_argument("--thread-bench-trials", type=int, default=240)
    P.add_argument("--threads-list", default="1,2,4,8,16")

    P.add_argument("--base-seed", type=int, default=20260617)
    P.add_argument("--no-mem", action="store_true", help="skip memory measurement")
    P.add_argument("--no-plot", action="store_true", help="skip the PNG plot")
    P.add_argument("--out-dir", default=None, help="default: <repo>/docs/benchmarks")
    return P.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    args.n_list = [int(x) for x in str(args.n_list).split(",") if x]
    args.compare_n_list = [int(x) for x in str(args.compare_n_list).split(",") if x]
    args.extrapolate_n = [int(x) for x in str(args.extrapolate_n).split(",") if x]
    args.threads_list = [int(x) for x in str(args.threads_list).split(",") if x]
    args.target_cascades = [float(x) for x in str(args.target_cascades).split(",") if x]
    args.measure_mem = not args.no_mem

    if not (1.0 / args.r < args.alpha < 1.0) and args.scaling == "janson":
        sys.exit(f"alpha must satisfy 1/r < alpha < 1 (got alpha={args.alpha}, r={args.r}).")

    repo = find_repo_root(args.repo_root)
    out_dir = Path(args.out_dir) if args.out_dir else repo / "docs" / "benchmarks"

    # Resolve C++ binary
    cpp_bin = None
    if args.engine in ("cpp", "both"):
        cand = Path(args.cpp_bin) if args.cpp_bin else repo / "cpp" / "build" / "twocascade_run"
        if cand.exists():
            cpp_bin = str(cand)
        elif args.engine == "cpp":
            sys.exit(f"C++ binary not found at {cand}. Build it first:\n"
                     f"  cd {repo}/cpp && cmake -S . -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build -j")
        else:
            print(f"[warn] C++ binary not found at {cand}; falling back to Python only.")

    # Resolve Python engine
    ref = None
    if args.engine in ("python", "both"):
        try:
            ref, _mdl_unused = import_python_engine(repo)
        except Exception as e:
            if args.engine == "python":
                sys.exit(f"Could not import the Python engine from {repo}/src: {e}")
            print(f"[warn] Python engine import failed ({e}); C++ only.")
    # model helpers are always needed for scaling math
    _, mdl = import_python_engine(repo)

    plat = detect_platform()
    print("=" * 72)
    print("TWO-CHANNEL CASCADE — SCALING BENCHMARK")
    print("=" * 72)
    print(f"machine : {plat.get('cpu_brand') or plat['processor']}  "
          f"({plat.get('physical_cpus') or '?'} phys / {plat['logical_cpus']} logical cores, "
          f"{plat.get('ram_gb','?')} GB RAM)")
    print(f"os/py   : {plat['system']} {plat['release']} / Python {plat['python']} / numpy {plat['numpy']}")
    print(f"repo    : {repo}  @ {get_git_commit(repo)}")
    print(f"engines : C++={'yes' if cpp_bin else 'no'}  Python={'yes' if ref else 'no'}")
    print("NOTE    : these numbers describe THIS machine only.")

    payload = {
        "meta": {
            "timestamp": _dt.datetime.now().isoformat(),
            "git_commit": get_git_commit(repo),
            "platform": plat,
            "args": {k: v for k, v in vars(args).items()},
            "cpp_bin": cpp_bin,
        },
        "nsweep": [], "threads": [], "compare": [], "feasibility": [],
    }

    primary_bin = cpp_bin if (cpp_bin and args.engine != "python") else None

    if args.mode in ("all", "nsweep"):
        payload["nsweep"] = run_nsweep(args, mdl, primary_bin, ref)
    if args.mode in ("all", "threads"):
        payload["threads"] = run_thread_scaling(args, mdl, cpp_bin)
    if args.mode in ("all", "compare"):
        payload["compare"] = run_compare(args, mdl, cpp_bin, ref)
    if args.mode == "all":
        payload["feasibility"] = run_extrapolation(args, payload["nsweep"], payload["threads"])

    json_path, csv_path = write_outputs(out_dir, payload)
    png = None if args.no_plot else maybe_plot(out_dir, payload)

    print("\n" + "=" * 72)
    print("SAVED")
    print(f"  {json_path}")
    print(f"  {csv_path}")
    if png:
        print(f"  {png}")
    print("=" * 72)


if __name__ == "__main__":
    main()
