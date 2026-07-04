---
mutability: frozen
type: concept
---

# §3 — Model Specification (3.5: notation & parameters)

### 3.5 Notation & parameters

> **Notation reconciliation (resolves an inconsistency in the original summary):** the summary's
> fear-channel definition used $f_i, g_t$ while its parameter table and dynamics used
> $\upsilon_i, \tau_t$ for the *same* objects (the mentor review also uses $\upsilon, \tau$). **This
> tracker standardizes on $f$ (individual fear) and $g$ (global fear field).** Mapping for reading
> the review: $\upsilon_i \equiv f_i$, $\tau_t \equiv g_t$, $E[\upsilon] \equiv \mu$.

**True parameters (knobs you set):**

| Symbol | Meaning | Notes / working regime |
|---|---|---|
| $n$ | number of banks (system size) | finite-size set: 1000, 2000, 5000, (10000 for exponent fit) |
| $p$ | edge probability (connectivity) | **scale with $n$** — see §4. Working mean degree $np$ ≈ 8–10 |
| $r$ | failed neighbors for solvency failure | **short discrete list** {2, 3, 4}; not a continuous axis |
| $\mu$ | mean individual fear $E[f]$ | the continuous sweep axis, $\mu \in [0,1]$ (~30 pts) |
| $\sigma$ | fear heterogeneity (sd of $f$) | via Beta concentration $\kappa$: $\sigma^2=\mu(1-\mu)/(\kappa+1)$. Enters only at 2nd order — **fix $\kappa$ for main diagram**, separate $\kappa$-sweep |
| $a$ | seed size (initial shock) | set as a multiple of per-$n$ $a_c$, e.g. $0.8a_c$, $1.2a_c$ |
| $\theta$ | systemic-event threshold | pick in the bimodal trough (0.5); show robustness for $\theta\in[0.2,0.8]$ |

**State variables (NOT parameters — recomputed each round / drawn once):**
$A(t)$, $a_t$ (dynamic counts); $g_t$ (recomputed every round); $f_i$ (per-bank draw at $t=0$).
