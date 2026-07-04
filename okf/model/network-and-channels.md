---
mutability: frozen
type: concept
---

# §3 — Model Specification (3.1–3.4: network, channels, dynamics)

Precise definition. Change only via the Decision Log.

### 3.1 Network & states
- Interbank network: Erdős–Rényi random graph $G(n,p)$.
- Each bank is **solvent** or **failed**. Failure is **absorbing** (a failed bank stays failed), so
  the failed set grows monotonically.
- Seed: at $t=0$, a set of $a$ banks is failed (chosen at random by default; high-degree targeting
  is a variant — but see §3.6, on $G(n,p)$ targeting ≈ random).
- $A(t)$ = number of failed banks after round $t$. $a_t := A(t) - A(t-1)$ = **new** failures in
  round $t$, with $A(-1):=0$ so $a_0 = a$.

### 3.2 Channel 1 — Solvency (Janson local rule)
A solvent bank $i$ fails if at least $r$ of its neighbors have already failed:
$$\bigl|\{\, j \in N(i) : j \text{ failed} \,\}\bigr| \ge r.$$
Threshold $r$ is the capital-buffer depth. Use $r \ge 2$ (the $r=1$ case is qualitatively
different). This channel is **super-linear near zero** for $r \ge 2$ (it contributes nothing to the
linearization at the all-solvent state) — this is *why* Janson's threshold has the
$(np^r)^{-1/(r-1)}$ form. Keep this fact in mind for all mean-field / spectral reasoning.

### 3.3 Channel 2 — Fear (global, self-referential, heterogeneous)
- **Global fear field** $g_t \in [0,1]$ = fraction of banks that failed in the *previous* round:
  $$g_t := \frac{a_{t-1}}{n}\quad\text{(incremental — current default; see fork F1 in §3.6).}$$
- **Individual fear** $f_i \in [0,1]$, drawn **once** at $t=0$ from $\text{Beta}(\alpha,\beta)$ with
  $\alpha=\mu\kappa,\ \beta=(1-\mu)\kappa$, so $E[f]=\mu$ **exactly** (fork F3 resolved → Beta; see
  D-002 and §3.5). Concentration $\kappa$ sets the heterogeneity independently of the mean.
- A solvent bank $i$ fails through the fear channel in round $t$ with probability $f_i\, g_t$
  (a valid probability since $f_i, g_t \in [0,1]$).

**Key structural fact (most important consequence in the whole project):** because $f_i \in [0,1]$
forces $\mu < 1$, the **fear-only per-round reproduction number is $R_{\text{fear}} \approx \mu < 1$.**
Fear is a **subcritical amplifier**: it cannot ignite a cascade on its own; it can only amplify one
that the solvency channel has already started. At $t=1$, $g_1 = a/n \approx 0$ for any sub-linear
seed, so fear is essentially *off* until the solvency channel first produces a macroscopic round.
**This is the project's central risk** (see §7) and shapes the analytical check (see §4).

### 3.4 Dynamics & stopping rule
- Each round, **simultaneously**, every solvent bank fails if **Channel 1 is satisfied OR** an
  independent **Bernoulli$(f_i\, g_t)$** draw succeeds.
- The process **halts** at the first round with no new failures ($a_t = 0$). Fear is then zero by
  construction ($g_{t+1} = 0$), so the absorbing state is genuine.
- Record the final failed fraction $|A^*|/n$.
