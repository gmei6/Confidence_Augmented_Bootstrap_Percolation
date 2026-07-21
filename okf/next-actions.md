---
type: Concept
title: "§10 — Next Actions"
description: "Live list of the next few concrete steps; overwritten each session."
mutability: live
---

# §10 — Next Actions 🟢 *(overwrite each session — keep it to the next few concrete steps)*

1. **Refresh `advisor-update-2026-07-22/index.html` with this session's results (NEW, 2026-07-18)
   — not yet done.** The site (built via Ultraplan, S-051-era) predates all of this session's
   work and needs updating before the meeting:
   - **Q4(iii) ignition gate (Tasks S→W).** Gate holds. The μ̄=0.4 branch declines
     0.134→0.116→0.062→0.050→0.044→0.034 over n∈{4000..160000} and is **still declining**, not
     flattening: Cochran–Armitage trend on the pooled replicate + n=160000 gives z=−3.31,
     p=0.0009 (`docs/queue/reports/task_v_report.md`). ⚠️ The earlier "finite-size transient
     flattening after n=20000 (χ²=1.70, p≈0.43)" reading is **superseded** — it came from a
     single 500-trial series and does not survive doubling the trials. Do not put it on the site.
   - **Q3 ν (Tasks T→W).** Current committed fit is **7-point**, n∈{1000..80000}:
     **ν(μ=0)=5.61±0.18** (R²=0.953), **ν(μ=0.3)=4.82±0.15** (R²=0.978)
     (`results/processed/task_a_nu_n10000.json`). ⚠️ T's n=20000 values (6.29±0.39, 4.90±0.22)
     are **superseded** — do not cite them.
   - ⚠️ **Do NOT present a "shared n≈20000 crossover" story.** Task W tested exactly that and
     concluded the opposite: the apparent flattening is **not** a shared crossover — ν widths,
     ignition point estimates, and the Task U slope all fail to flatten. The earlier
     "same flattening pattern / notable cross-experiment observation" framing is retracted.
   - The `plot_fear_field_concentration` savefig/close bug is now fixed (`df0575d`) — can drop
     from any "known defects" list if the site has one.
   - Tasks Q and R are **DONE** (both AUDIT PASS) — see the Resolved block below. Present as
     results, not as open items.
   - `gh-axi` was installed (session tooling, not research) — not meeting-relevant, don't
     include.
   Figures to (re)embed as base64, same convention as the original 3: an updated
   `finite_size_scaling_r2_n10000.png` (regenerated, now 7-point) and, if a Q4-gate figure gets
   made, that too — check `results/figures/` after regenerating.
2. **Email Prof. Dhara before 2026-07-22** — send once item 1's site refresh is done, so the
   email and the leave-behind site tell the same story.
3. **Optional future — Task R Option B (supra-r_n cross-round test).** The *only* valid way
   to actually test C-Q5(i) cross-round spatial correlation is a supra-r_n cross-type statistic
   (pair-correlation g(d) / Ripley cross-K between early- and late-round remote-nucleus
   centroids at d ∈ (r_n, k·r_n]). Deferred (D-035); pick up only if the advisor wants a
   cross-round correlation probe. Task O's cross-round lower-bound caveat stays OPEN until then.
4. **Queue hygiene — the queue is empty; S/T/U/V/W all closed.** `d70dbd8`'s commit body
   records V, W, and U as having cleared `/verify` (reviewer sign-off, critic PASS, AUDIT PASS).
   S and T have no gate of their own but were **superseded** by W, which was gated: S's ignition
   series is now the 6-point run to n=160000, T's ν fit is now the 7-point fit above. Residual
   caveat: U's and W's task files asked for a *human* at the gate and got a blind one — a
   process gap, not an ungated result. ⚠️ Closure records for these tasks live in **commit
   bodies and `okf/changes/`**, not in `docs/queue/reports/` — a missing report file does not
   mean a task is open (this misread cost a session).

**Resolved 2026-07-19 (S-056/S-057):**
- **Task Q (S-054): merged `c4ef634`.** ε-cap water-filling fix landed; unblocked Task X.
- **Task X (S-056): DONE, AUDIT PASS.** C-Q4(i) γ=0→+1 leg confirmed cap-free; C-Q4(ii)
  size-biased collapse REFUTED (μ̄ ≻ μ*, ratio 2.05). Report: `docs/queue/reports/task_x_report.md`.
- **Task R (S-057): DONE, AUDIT PASS.** Counting bug fixed (peeling, `e066fd8`); the strict-
  r_n-clique cross-round metric is structurally blind (D-035), z-test retired; C-Q5(i)
  cross-round question stays OPEN (Option B is the valid test — item 3). Supersedes the
  S-055 block. Report: `docs/queue/reports/task_r_cross_round_report.md`.

**Resolved 2026-07-18:** item 3 ("review and commit the S-046/S-047 primary-checkout working
tree") was already committed as `fb0ac42` before this session started — removed as stale, no PR
needed. Npm-install proposal came back: installed `gh-axi` (low-risk, real token savings);
skipped `chrome-devtools-axi` (defer until browser-automation work starts) and `tasks-axi`
(doesn't appear to exist under that name in the AXI ecosystem — flagged, not installed).
Environment note: run simulations with `arch -arm64 python3` (Rosetta/numpy mismatch).

**Cleared 2026-07-18 (Gary's call):** the "Study the Math" deep-dive and its gating prerequisite
reading queue, and the `graphs.py` configuration-model vectorization perf item — Gary will pick
up the modeling intuition via the `advisor-update-2026-07-22/` site instead. If the perf item
matters again later, it's still recorded in `EXPLAINER.md` §12 and `graphs.py:30-45`.
