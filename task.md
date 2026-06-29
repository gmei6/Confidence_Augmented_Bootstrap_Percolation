# task.md — Interactive cascade visualization (illustrative web demo)

## Goal
A self-contained, online-renderable visualization that demonstrates how the
two-channel cascade works and what each model variable means — for both general
teaching and as an artifact for the 2026-07-01 advisor meeting.

## What is being built
A static GitHub Pages site (`viz/`) with a **live, illustrative** JavaScript
reimplementation of the §3.4 dynamics:
- Force-directed node-link graph of $G(n,p)$ at small $n$ (≤150) so individual
  banks are visible.
- Four-color channel attribution per node: **seed / solvency / fear / solvent**
  — making the two failure channels visually explicit.
- Full sliders for $r, \mu, \kappa, a, p, n$ (each tooltip-mapped to its §3
  meaning) + seed field + Step/Play/Reset.
- Live variable panel: round $t$, the panic field $g_t = a_{t-1}/n$ (thermometer),
  new failures $a_t$, cumulative fraction $A(t)/n$, and the $|A^*|/n \ge \theta$
  (θ=0.5) systemic flag.

## Theoretical invariants under test / on display
This demo **illustrates**, it does not validate. The relevant model facts it must
render faithfully (so the demo is honest even though it is not the oracle):
- §3.4 simultaneous update: evaluate all banks against frozen state, then mutate.
- §3.3 fear field is **incremental** ($g_t = a_{t-1}/n$, $a_0 = a$) and fear is a
  **subcritical amplifier** ($R_\text{fear} \approx \mu < 1$) — the $g_t$
  thermometer should visibly spike then decay, never self-sustain.
- $f_i \sim \text{Beta}(\mu\kappa,(1-\mu)\kappa)$ so $E[f]=\mu$, with the
  $\mu=0/\mu=1$ Gamma-shape guards (LESSONS §2).
- Solvency channel: fail iff $\ge r$ failed neighbors.

## Explicit non-goals / scope guard
- **Not** the validated engine. A prominent banner states "illustrative at small
  $n$ — the mechanism, not the asymptotic/validated regime." It must never be
  cited as a result.
- No change to `src/`, `cpp/src/`, `reference.py` (oracle), or `results/`.
- Not the research regime ($n \ge 1000$); small $n$ is deliberate for visibility.

## Conjectures (F#) affected
None. This is a standalone illustrative demo; it tests no falsifiable conjecture
and resolves no fork.
