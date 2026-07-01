# Idea: Bound the peak generation size directly to prove sub-macroscopic $a_k$

**Status:** idea only — not started. Captured 2026-07-01, not yet scoped into a `task.md`.

**Relevant research question:** Q1 follow-up (§9 of `docs/PROJECT_TRACKER.md`) — the
**Asymptotic Decoupling Conjecture**, Tier 2 (D-025, `docs/research/other/janson_reformulation_with_fear.md` §5).

## The gap this targets

Both `section2-reformulation/index.html` (§4.1, clock collapse) and
`docs/research/other/janson_reformulation_with_fear.md` (§5) invoke the assumption

$$a_k = o(n) \quad \text{w.h.p., for every generation } k,$$

to justify telescoping $\sum_{j=1}^{k(t)} g_j = T_{k(t)-1}/n \approx t/n$ and linearizing
$\log(1 - f_i g_j)$. This "sub-macroscopic generation sizes" assumption is currently just
asserted ("holds near the critical phase boundary"), not proven. It is the concentration
half (Tier 2) of the Asymptotic Decoupling Conjecture — Tier 1 (exact conditional i.i.d.
given the fear field) is already proven per D-025.

## The idea

Rather than bound $a_k$ generation-by-generation, find the generation $k^*$ at which
$a_k$ is largest and bound $\max_k a_k$ directly. Since $a_k \le \max_j a_j$ for every
$k$, one peak bound of the form $\max_k a_k = o(n)$ w.h.p. would establish the
sub-macroscopic assumption for *all* generations at once, rather than requiring a
separate argument at each $k$.

Rough shape of the approach (to be worked out, not started):
1. Characterize where the peak generation is expected to sit relative to the
   solvency-channel saddle-node tangency (§4 of `AGENTS.md` / the mean-field map) —
   plausibly near the inflection of the mean-field cascade trajectory, since generation
   sizes should grow while the map is expanding and shrink once it turns over.
2. Get a deterministic (mean-field) bound on the generation size at that point, then a
   concentration bound (e.g. martingale / Azuma-type, following the branching-process
   machinery already used for the fear-only subcriticality lemma in §2 of the Tiered
   Stance, D-009) showing the *realized* peak stays within $o(n)$ of the deterministic
   one w.h.p.
3. Check whether this reuses machinery already in `janson_reformulation_with_fear.md`
   (the leave-$m$-out conditioning from §5.1) or needs new tools.

## Why this might be tractable where a per-$k$ bound isn't

A per-generation argument has to control $a_k$ at every $k$ simultaneously (a union
bound over a growing number of generations, which can leak probability). Bounding the
single peak sidesteps that — it's one random variable ($\max_k a_k$) instead of a
process.

## Open before starting

- Whether this is worth pursuing now or scoping out of the write-up entirely is an open
  design question for the 2026-07-01 advisor meeting (§9 Q1 follow-up).
- Not yet a `task.md` / `implementation_plan.md` per the §IV artifact process in
  `AGENTS.md` — this file is a placeholder for the idea, not a commitment to do the work.
