---
mutability: frozen
type: concept
---

# §3 — Model Specification (3.6: modeling forks — all decided)

### 3.6 Open modeling forks (decide deliberately — track in §11)

- **F1 — Incremental vs. cumulative fear field. ✅ DECIDED (D-005, D-006, 2026-06-03): INCREMENTAL, $g_t = a_{t-1}/n$.** Fear is a transient amplifier with bounded gain $\approx 1/(1-\mu)$; per-failure total fear offspring $= \mu < 1$ (subcritical); the all-solvent state stays linearly stable; §3.4 absorbing state is genuine. Economically: news-flow panic, salience decays when failures stop. *Rejected:* cumulative ($g_t = A(t-1)/n$) — makes the all-solvent state linearly unstable for any $\mu>0$ (linearized growth $1+\mu$), eliminates the critical-seed barrier, demotes $r$ to a correction, and breaks §3.4's absorbing-state claim; NOT retained as a reported contrast (D-005 supersedes §3.6's prior "ideally report both"). *Extension (D-006):* normalized memory-window family $g_t = (1/n)\sum_{k=1}^X w_k a_{t-k}$, $\sum w_k = 1$ (exemplar $X=4$, $w = 0.50/0.25/0.15/0.10$); $X=1$ is the decided model; halting rule generalizes to "window empty" ($X$ consecutive quiet rounds); pilot ($n=2000$, 300--400 paired trials) confirms $P(\text{systemic})$ invariant in $X$ within $\pm 0.03$ (boundary depends only on kernel mass $= \mu$); cascade duration scales with $X$ ($\approx 13.5\to31.5$ rounds at $\mu=0.5$); study slotted Wk-9/stretch.
- **F2 — The $m$/$k$ "fear marks" mechanism. ✅ DECIDED (D-008, 2026-06-04): DROPPED.** The original summary's $m/k$ fear marks mechanism (fear feeds temporary marks that lower the effective solvency threshold $r$) is dropped for the MVP. Standardize on the simple direct-failure fear channel of §3.3. *Rationale:* The marks mechanism violates Janson-regime scaling assumptions (even $m=1$ mark lowers the solvency barrier to $r-1$, making $np^{r-1} \to \infty$ and trivially satisfying solvency, destroying the sharp threshold dichotomy). Furthermore, marks stack, breaking the subcritical amplifier property ($R_{\text{fear}} \approx \mu < 1$) when $m \ge r$ or mark lifetimes accumulate, and render the mean-field analysis mathematically intractable by replacing the scalar map with a high-dimensional coupled map. Dropping it preserves the clean direct-failure engine and avoids a parameter space explosion ($r, \mu, m, k$).
- **F3 — Fear distribution. ✅ DECIDED (D-002, 2026-06-02): Beta$(\alpha,\beta)$.** Individual fear
  $f_i\sim\text{Beta}(\mu\kappa,(1-\mu)\kappa)$, so $E[f]=\mu$ exactly with no truncation artifact;
  concentration $\kappa$ tunes heterogeneity independently of the mean ($\sigma^2=\mu(1-\mu)/(\kappa+1)$),
  and the limits are clean ($\kappa\to\infty$ point mass at $\mu$; $\kappa\to0$ two-point at $\{0,1\}$;
  $\mu=0$ the Janson baseline). **Two-point** (a fraction "immune" with $f=0$, rest susceptible —
  direct link to Watts's immune nodes / Ruan's blocked nodes) is kept as a **robustness variant**.
  *Rejected:* truncated-normal — its realized mean $\ne\mu$ near 0/1 (nominal $0.1\to0.164$ at
  $\sigma=0.15$), silently mislabeling the sole sweep axis, which is the one quantity the dynamics
  depend on (§4: fear-failures $\approx\mu\,a_{t-1}$).
- **F4 — Regime of $p$ vs. $n$. ✅ DECIDED (D-004, 2026-06-03): Janson regime ($np\to\infty$,
  $np^r\to0$).** Scale $p_n=\beta\,n^{-\alpha}$ with $\alpha\in(1/r,1)$ (per §4; e.g. $\alpha=0.7$ for
  $r=2$), so the JŁTV sharp-threshold theory (§4) is the benchmark and finite-size scaling is
  well-defined. *Rejected:* the bounded-mean-degree branching/configuration regime ($np=$ const, using
  the sparse Watts / Amini–Cont–Minca threshold) — it would abandon the Janson benchmark the project is
  built on, muddy the finite-size scaling, and preclude extending Janson's theorems. **Kept** as the
  natural home only if the project later pivots to a configuration model with empirical degrees (Q2).
