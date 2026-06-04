# Fork F2 — Theoretical Analysis: The $m$/$k$ Fear-Marks Mechanism

> **Research Agent Report** — 2026-06-04  
> **Reporting contract:** [Research Files Updated, Theoretical Risks Identified, Benchmark Comparisons]  
> **Status:** This file is the sole output. No implementation, configuration, or test files were modified.

---

## Executive Summary

The F2 "fear marks" mechanism proposes replacing the current direct-failure fear channel (Bernoulli($f_i g_t$)) with a mark-accumulation rule: when fear is activated for bank $i$, $m$ marks are added to $i$'s counter, lasting $k$ rounds, and a bank fails via the solvency channel when its **failed neighbors plus accumulated marks** reach the threshold $r$. This analysis concludes that **F2 marks should be dropped from the MVP** (option (a) in §3.6). The mechanism:

1. **Breaks** the clean channel separation that the entire analytical framework depends on.
2. **Destroys** the subcritical amplifier property ($R_{\text{fear}} \approx \mu < 1$) in parameter regimes where $m \ge r$ or where mark accumulation from repeated fear activations crosses the solvency threshold.
3. **Makes** the mean-field tangency analysis substantially less tractable (the combined map becomes a coupled system with $k$-step memory).
4. **Adds** a second persistence channel (mark lifetime $k$) that interacts problematically with the D-006 window-length $X$, creating a dual-memory system with little additional physical insight.
5. **Does not** add genuinely new physics beyond what the current model + D-006 window-length already captures — the "fear amplifies solvency" story is already told by the OR rule and the subcritical amplifier.

**Recommendation:** Drop $m$/$k$ marks for the MVP (D-005/D-006 already provide a clean persistence handle). If ever revisited, treat as a **separate model variant** with its own mean-field derivation, not a parameter extension of the current model.

---

## §1 — Mechanism Comparison: Direct Failure vs. Fear Marks

### 1.1 The Current Model (§3.3)

In the decided model, the two channels are **structurally independent and combined by OR**:

$$
\text{Bank } i \text{ fails at round } t \iff \underbrace{|\{j \in N(i) : j \text{ failed}\}| \ge r}_{\text{Channel 1: Solvency}} \;\;\text{OR}\;\; \underbrace{\text{Bernoulli}(f_i \, g_t) = 1}_{\text{Channel 2: Fear (direct)}}
$$

Key properties:
- **Channel separation:** Fear and solvency are independent failure modes. A bank can fail by fear alone (with probability $f_i g_t$) or by solvency alone (with $r$ failed neighbors), or by either.
- **Fear is memoryless within a round:** The Bernoulli draw depends only on the current global field $g_t$ and the bank's fixed susceptibility $f_i$. No state accumulates on the bank from fear.
- **Linearity of fear at the all-solvent state:** Expected fear-failures in round $t$ are $\approx \mu \cdot a_{t-1}$ (since $g_t = a_{t-1}/n$ and $\sum_i f_i \approx \mu n$), giving $R_{\text{fear}} \approx \mu < 1$.

### 1.2 The F2 Marks Model (proposed)

Under F2, fear no longer fails banks directly. Instead:

$$
\text{If Bernoulli}(f_i \, g_t) = 1 \text{ for bank } i, \text{ then } m \text{ marks are added to bank } i\text{'s mark counter.}
$$

Each mark **decays** (disappears) after $k$ rounds. A bank's **effective load** at time $t$ is:

$$
L_i(t) = |\{j \in N(i) : j \text{ failed}\}| + M_i(t)
$$

where $M_i(t)$ is the total number of active marks on bank $i$. Bank $i$ fails when:

$$
L_i(t) \ge r
$$

Key structural changes:
- **Channel unification:** Fear no longer operates independently — it feeds into the solvency channel. The two channels are **coupled through the mark mechanism**.
- **Fear is now stateful:** Bank $i$ carries a mark history $M_i(t)$ that depends on all fear activations in the past $k$ rounds.
- **Fear cannot fail a bank alone (if $m < r$):** A single fear activation adds $m$ marks. If $m < r$, a bank needs either multiple fear activations or some failed neighbors. If $m \ge r$, a single fear activation can fail a bank — recovering the direct-failure behavior but with added complexity.
- **The failure criterion is no longer OR — it is a threshold on a combined sum.** This is a fundamentally different dynamical rule.

### 1.3 Mathematical Differences (Summary Table)

| Property | Current Model (§3.3) | F2 Marks |
|---|---|---|
| Failure rule | OR of two independent channels | Threshold on combined load |
| Fear's effect | Immediate failure (Bernoulli) | Marks that **count toward** the solvency threshold |
| State per bank | $f_i$ (fixed), failed/solvent (absorbing) | $f_i$ (fixed), $M_i(t)$ (mark history), failed/solvent |
| Memory | None beyond $g_t$ (current) / $X$-window (D-006) | $k$-round mark persistence **per bank** |
| Fear-only $R_0$ | $\mu$ (subcritical) | Depends on $m$, $k$, $r$ — see §3 |
| Channel interaction | Additive at the probability level | Multiplicative at the threshold level |
| Mean-field map | Separable (solvency + fear terms) | Coupled (marks alter the solvency activation function) |

---

## §2 — Janson Regime Interaction

### 2.1 The Janson Sharp Threshold (Background)

In the Janson regime ($np \to \infty$, $np^r \to 0$), the critical seed for pure bootstrap percolation ($\mu = 0$) is:

$$
a_c = \frac{r-1}{r} \cdot t_c, \qquad t_c = \left(\frac{(r-1)!}{np^r}\right)^{1/(r-1)}
$$

The **dichotomy** is: seeds below $a_c$ produce $o(n)$ failures; seeds above $a_c$ produce $n - o(n)$ failures. The mechanism behind this sharp threshold is the super-linearity of the solvency channel near zero: the probability of failing via solvency scales as $(c\varphi)^r / r!$ where $c = np$ and $\varphi$ is the failed fraction — for $r \ge 2$, this vanishes faster than linearly as $\varphi \to 0$.

### 2.2 How Marks Would Interact with the Threshold

Under the marks mechanism, a bank with $M_i(t)$ active marks needs only $r - M_i(t)$ failed neighbors to fail via solvency. This **effectively reduces the local threshold** for marked banks:

$$
r_{\text{eff},i}(t) = \max(0, \; r - M_i(t))
$$

**This is the central mathematical consequence.** The population of solvent banks is no longer homogeneous in their solvency threshold — fear creates a distribution of effective thresholds.

#### Case: $m \ge r$ (single activation can fail)

If $m \ge r$, a single fear activation immediately brings $L_i(t) \ge r$ (assuming no failed neighbors are needed). In this regime, the marks mechanism is **strictly more powerful** than direct failure, because the marks also persist for $k$ rounds, meaning a marked bank that doesn't fail this round carries the marks forward, potentially pushing unmarked neighbors over their thresholds in subsequent rounds through the solvency channel.

#### Case: $m < r$ (marks alone insufficient)

A single fear activation adds $m < r$ marks. The bank needs either:
- Additional fear activations in subsequent rounds (total marks $\ge r$), or
- Failed neighbors to close the gap ($r - M_i(t)$ failed neighbors suffice).

The **effective threshold** for marked banks drops to $r - m$ (after one activation) or lower (after multiple activations). This modifies the Janson scaling:

- For the sub-population of banks with $m$ marks, the critical quantity becomes $(np^{r-m})$ instead of $(np^r)$.
- Since $np^{r-m} \gg np^r$ in the Janson regime (because $np \to \infty$ and $p \ll n^{-1/r}$), marked banks face a **much easier** solvency criterion.

### 2.3 Impact on $a_c$ and the Dichotomy

The effect on the critical seed depends on the **density of marked banks**. Let $\rho_m(t)$ be the fraction of solvent banks carrying $\ge m$ marks at time $t$. These banks have effective threshold $r' = r - m$, for which the relevant Janson quantity is $np^{r'} = np^{r-m}$.

In the Janson regime:
- $np^r \to 0$ (the original threshold is hard to cross)
- $np^{r-m} \to \infty$ for $m \ge 1$ and $r - m \ge 1$ (the reduced threshold is **trivially easy** to cross)
- $np^{r-m} \to \infty$ even for $m = 1$: $np^{r-1} = np^r / p \to 0 / p$, but $p \to 0$ so this ratio diverges — indeed $np^{r-1} = (np^r) \cdot (1/p) \to 0 \cdot \infty$, and more precisely with $p = \beta n^{-\alpha}$, $\alpha \in (1/r, 1)$: $np^{r-1} = \beta^{r-1} n^{1-(r-1)\alpha}$, and $1-(r-1)\alpha > 1 - (r-1) \cdot 1 = 2 - r$. For $r = 2$: $np = \beta n^{1-\alpha} \to \infty$ (the reduced threshold for a marked bank is $r-1 = 1$, i.e., a single failed neighbor suffices — and the mean degree diverges, so this is trivially satisfied).

**Key finding:** In the Janson regime, even $m = 1$ mark effectively **removes** the solvency barrier for the marked bank, because the reduced threshold $r - 1$ is in the regime where $np^{r-1} \to \infty$ (i.e., above the upper boundary of the Janson window). A bank with a single mark is, for Janson-scaling purposes, essentially certain to fail via the solvency channel as soon as any of its (divergingly many) neighbors has failed.

> **Implication:** If a non-negligible fraction of banks acquire even one mark, the solvency channel becomes trivially activated for them, and the cascade dynamic degenerates. The marks mechanism is **far too powerful** in the Janson regime — it doesn't gently "amplify" solvency; it **eliminates** the solvency barrier for any marked bank.

### 2.4 The Dichotomy Under Marks

The Janson dichotomy ($o(n)$ vs. $n - o(n)$) relies on the solvency channel being the sole failure mechanism with its super-linear activation curve. Under marks:

- The marked sub-population faces a threshold that is trivially easy in the Janson regime.
- The unmarked sub-population still faces the original $r$-threshold.
- The cascade dynamic becomes a **two-population** process: easy-to-fail (marked) and hard-to-fail (unmarked), with the marked population feeding failures back into both populations.

If $\rho_m$ (the fraction marked) exceeds $O(np^{-1}) = O(n^{\alpha-1})$ (a vanishing but non-trivial fraction), the cascade through the marked sub-population alone may suffice for percolation. This could **lower $a_c$ discontinuously** (not just shift it) and potentially **break the sharp-threshold structure** by creating a regime where partial cascades stabilize at the boundary between the two sub-populations.

---

## §3 — Subcritical Amplifier Property

### 3.1 Current Model: Fear is Subcritical ($R_{\text{fear}} \approx \mu < 1$)

The most important structural property of the current model is that fear cannot ignite a cascade on its own. At the all-solvent fixed point:

- One failure at time $t-1$ produces $a_{t-1} = 1$, so $g_t = 1/n$.
- Expected fear-induced failures: $\sum_i f_i \cdot g_t \approx \mu n \cdot (1/n) = \mu$.
- Since $\mu < 1$ (because $f_i \in [0,1]$ and $E[f] = \mu$), each fear-failure produces on average $\mu < 1$ further fear-failures.
- The fear chain is **geometrically decaying** — total fear-offspring from one seed failure $\approx \mu / (1 - \mu)$.

This means:
1. **The all-solvent state is linearly stable** (the linearized map has spectral radius $\mu < 1$, since solvency contributes nothing to the linearization for $r \ge 2$).
2. **A finite critical seed is needed** to cross the nonlinear solvency barrier — the §4 saddle-node tangency.
3. **Fear amplifies but does not initiate** — it multiplies the solvency cascade by a bounded factor $\approx 1/(1-\mu)$.

### 3.2 Under F2 Marks: Subcriticality Analysis

Under the marks mechanism, fear does not directly cause failures. Instead, it produces marks. The question is whether marks can accumulate to create supercritical feedback.

**Linearization at the all-solvent state:**

Starting from the all-solvent state with a single failure, consider the chain of events:

1. $a_0 = 1$ (one seed failure), so $g_1 = 1/n$.
2. Each solvent bank $i$ activates fear with probability $f_i \cdot g_1 \approx f_i / n$. Expected number of banks receiving marks: $\sum_i f_i / n \approx \mu$.
3. Each marked bank receives $m$ marks. But **marks do not cause failure** — they lower the effective threshold.
4. A marked bank with $m$ marks needs $r - m$ failed neighbors to fail via solvency. At $\varphi \approx 1/n$, the probability of having $r - m$ failed neighbors is $\approx (c/n)^{r-m} / (r-m)! = (np \cdot 1/n)^{r-m} / (r-m)!$, which for $r - m \ge 2$ is super-linear in $\varphi$ and hence $\approx 0$.
5. For $r - m = 1$: probability of at least one failed neighbor $\approx c \cdot \varphi = np/n \approx p \to 0$.
6. For $r - m = 0$ (i.e., $m \ge r$): the bank fails immediately upon receiving marks.

**Conclusion on linearization:**

- **If $m < r - 1$:** The marked banks still face a super-linear (though reduced) solvency barrier. At the linearization level, marks produce **zero** additional failures. The all-solvent state remains linearly stable (in fact, with spectral radius 0, not just $< 1$). Fear marks are **strictly weaker** than direct failure near the all-solvent state.
- **If $m = r - 1$:** Marked banks need one failed neighbor. The linearized reproduction number from the fear-mark channel is $\approx \mu \cdot p \to 0$. Still subcritical (and weaker than the current model's $\mu$).
- **If $m \ge r$:** Marked banks fail immediately. The linearized reproduction number is $\mu$ (same as the current model, since each activation triggers immediate failure). But with the additional wrinkle that marks **persist for $k$ rounds**, creating an accumulation effect not present in the current model.

### 3.3 The Accumulation Problem

Even when $m < r$, marks from **multiple rounds** can accumulate. A bank that receives fear marks in rounds $t_1, t_2, \ldots$ accumulates $m$ marks per activation, each lasting $k$ rounds. If a bank receives marks in $\lceil r/m \rceil$ rounds within a $k$-round window, its mark count reaches $r$ and it fails without any failed neighbors.

The expected number of fear activations for bank $i$ in a $k$-round window with field strength $g$ is:

$$
\text{E}[\text{activations in } k \text{ rounds}] = k \cdot f_i \cdot g
$$

For bank $i$ to accumulate $r$ marks from fear alone (needing $\lceil r/m \rceil$ activations), we need:

$$
k \cdot f_i \cdot g \ge \lceil r/m \rceil
$$

This is a **threshold on the sustained fear field**: if $g$ stays above $\lceil r/m \rceil / (k \cdot f_i)$ for $k$ rounds, bank $i$ fails by marks alone.

For highly susceptible banks ($f_i \approx 1$) with large $k$:

$$
g \ge \frac{\lceil r/m \rceil}{k}
$$

With $k$ large and $m$ not too small, this threshold can be quite low. For example, $r = 2$, $m = 1$, $k = 5$: a bank with $f_i = 1$ fails by marks alone if $g \ge 2/5 = 0.4$ — i.e., if 40% of banks failed in each of the past 5 rounds, which is deep in the cascade, not near the boundary. But for $r = 2$, $m = 1$, $k = 20$: the threshold drops to $g \ge 0.1$.

**This introduces a potential feedback loop not present in the current model**: fear marks accumulate → some banks fail → $g$ increases → more marks accumulate → more banks fail. Whether this loop is supercritical depends on the parameters $m$, $k$, and the distribution of $f_i$.

### 3.4 Verdict on Subcriticality

- **Near the all-solvent state ($\varphi \ll 1$):** The marks mechanism is **weakly subcritical** (in fact weaker than the current model for $m < r$, since marks do not directly cause failures). The $R_{\text{fear}} \approx \mu < 1$ property holds in a degenerate sense (the contribution is $\ll \mu$).
- **At moderate cascade fractions ($\varphi = O(1)$):** The marks mechanism becomes **potentially supercritical** through accumulation, especially for large $k$ and when $m \cdot k \ge r$. The effective reproduction number through the mark channel scales as $\mu \cdot k \cdot m$ for the fraction of banks that accumulate enough marks, which can exceed 1.
- **The qualitative picture changes:** In the current model, fear is a simple subcritical multiplier at all cascade stages. Under marks, fear is **negligible near zero** but potentially **supercritical at intermediate densities** — a qualitatively different amplification profile that could create new fixed points or bifurcations in the mean-field map.

---

## §4 — Mean-Field Tangency Analysis Under F2

### 4.1 Current Mean-Field Map (§4)

The current analytical benchmark uses a combined mean-field map $\Phi(\varphi)$ for the failed fraction $\varphi$:

$$
\Phi(\varphi) = 1 - \exp\left(-\frac{(c\varphi)^r}{r!}\right) + \mu \cdot \varphi - \text{(overlap correction)}
$$

More precisely (separating channels): the probability that a solvent bank fails in one round is:

$$
P(\text{fail}) = 1 - [1 - P_{\text{solv}}(\varphi)] \cdot [1 - P_{\text{fear}}(\varphi)]
$$

where:
- $P_{\text{solv}}(\varphi) \approx (c\varphi)^r / r!$ (Poisson approximation for $\ge r$ failed neighbors)
- $P_{\text{fear}}(\varphi) \approx \mu \cdot \varphi$ (fear failures proportional to the failed fraction)

The **tangency condition** (saddle-node bifurcation) finds the critical seed where $\Phi(\varphi) = \varphi$ and $\Phi'(\varphi) = 1$ simultaneously, producing the mean-field $a_c(\mu)$. This is a **scalar** fixed-point problem — highly tractable.

### 4.2 Mean-Field Map Under F2 Marks

Under marks, the map becomes a **coupled system** because the mark state is history-dependent:

Let $\varphi_t$ = failed fraction, $\rho_j(t)$ = fraction of solvent banks with exactly $j$ accumulated marks ($j = 0, 1, \ldots$). The state is now the vector $(\varphi_t, \rho_0(t), \rho_1(t), \ldots, \rho_{r-1}(t))$.

The solvency activation probability for a bank with $j$ marks is:

$$
P_{\text{solv}}^{(j)}(\varphi) \approx \frac{(c\varphi)^{r-j}}{(r-j)!} \quad \text{for } j < r, \qquad P_{\text{solv}}^{(j)} = 1 \quad \text{for } j \ge r
$$

The mark dynamics (mean-field):
- In each round, a solvent bank with $j$ marks receives $m$ new marks with probability $f_i \cdot g_t$.
- Marks older than $k$ rounds decay.

The mean-field map becomes:

$$
\Delta \varphi_{t+1} = \sum_{j=0}^{r} \rho_j(t) \cdot P_{\text{solv}}^{(j)}(\varphi_t)
$$

with $\rho_j(t)$ evolving according to a $k$-step recurrence that tracks mark ages.

**This is a $(k \cdot r)$-dimensional dynamical system**, not a scalar map. Key consequences:

1. **The tangency analysis is no longer a 1-D saddle-node.** It becomes a higher-dimensional bifurcation problem, likely requiring numerical continuation methods rather than the closed-form tangency condition.
2. **The sharp dichotomy may not survive** in the mean-field, because the multi-dimensional system can have stable intermediate fixed points (partial cascades that stabilize when the marked sub-population is exhausted).
3. **Analytical tractability is severely reduced.** The current §4 approach — solve $\Phi(\varphi) = \varphi$ and $\Phi'(\varphi) = 1$ simultaneously — does not generalize straightforwardly.

### 4.3 Special Cases with Partial Tractability

- **$k = 1$ (marks decay immediately):** Marks do not persist. A bank that receives marks this round either fails (if combined with enough failed neighbors) or the marks vanish. This is a **weaker** version of the current model (fear provides a "bonus" toward the solvency threshold for one round, rather than directly failing the bank). The map remains scalar but with a modified activation function — somewhat tractable, but strictly less powerful than the current model.
- **$m \ge r$ (single activation suffices):** Marks immediately fail the bank, so the mark mechanism is equivalent to direct failure (the current model) plus residual marks that persist for $k$ rounds on already-failed banks (irrelevant, since failure is absorbing). In this case, the map is again scalar and $\approx$ the current model — but then $m \ge r$ adds nothing over §3.3.
- **$m = 1, k = 1$ (minimal marks):** Each fear activation adds 1 mark lasting 1 round. This is the weakest marks variant: a marked bank needs $r - 1$ failed neighbors instead of $r$. The map is scalar with a modified solvency term. This is tractable but the effect is weak and redundant.

---

## §5 — Mark Decay and Memory Interaction

### 5.1 The D-006 Window-Length $X$

The decided model (D-006) already has a memory handle: the fear field is computed over a window of $X$ past rounds:

$$
g_t = \frac{1}{n} \sum_{j=1}^{X} w_j \, a_{t-j}, \qquad \sum_j w_j = 1
$$

This creates a **global** memory: the fear field $g_t$ remembers the past $X$ rounds of system-wide failure rates.

### 5.2 The F2 Mark Lifetime $k$

The marks mechanism introduces a **local** (per-bank) memory: each bank remembers whether it was fear-activated in the past $k$ rounds, via the accumulated marks.

### 5.3 Interaction Analysis

With both $X > 1$ and $k > 1$, the system has **two independent memory channels**:

1. **Global memory** (window $X$): the fear field $g_t$ is a weighted average of past failure rates. This affects the probability of new fear activations system-wide.
2. **Local memory** (mark lifetime $k$): each bank accumulates marks that lower its effective solvency threshold. This affects the vulnerability of individual banks to the solvency channel.

The interaction creates a **compound feedback loop**:
- High past failure rates (within the $X$-window) → high $g_t$ → more fear activations → more marks → lower effective thresholds → more solvency failures → higher future failure rates → higher $g_{t+1}$...

This loop has two timescales ($X$ for the global field, $k$ for mark persistence) and can produce complex transient dynamics:

| Regime | Behavior |
|---|---|
| $k \ll X$ | Marks decay before the field has memory of them. Marks are a fast perturbation on a slow field. |
| $k \gg X$ | Marks persist long after the field has forgotten the failures that caused them. Banks remain "pre-stressed" even when the fear field drops to zero. This can restart cascades from a quiet state. |
| $k \approx X$ | Resonance possible — marks and field memory reinforce on the same timescale. |

### 5.4 The $k > X$ Problem (Latent Mark Restart)

Consider a scenario where $k > X$: a burst of failures at time $t_0$ causes fear activations, depositing marks. The field $g_t$ returns to $\approx 0$ after $X$ rounds of quiet. But marks persist for $k > X$ rounds. If those marked banks subsequently acquire new failed neighbors (from slow solvency propagation), they fail because their effective threshold is reduced — producing new failures, which re-ignite the fear field.

**This violates the §3.4 absorbing-state property** in spirit: the halting rule says "halt when the window is empty" ($X$ consecutive quiet rounds), but marks from before the quiet period are still active. The system could halt and then restart if we were running a continuous-time version, or it could produce a "false quiet" followed by a delayed burst.

> **Risk:** The interaction between $k$ and $X$ creates edge cases where the stopping rule must be modified (halt only when both the window is empty AND no marks remain), complicating the dynamics without adding clear physical insight.

---

## §6 — Theoretical Risks and Edge Cases

### Risk 1: $m \ge r$ Collapses to the Current Model (Low Severity, High Likelihood)

If $m \ge r$, a single fear activation immediately produces enough marks to fail the bank. This is strictly equivalent to direct failure (the current model) for the purpose of cascade dynamics. The only difference is that marks persist on already-failed banks, which is irrelevant due to absorbing failure. **Setting $m \ge r$ adds complexity without new behavior.**

### Risk 2: Marks Change the Universality Class (High Severity, Medium Likelihood)

The Janson sharp-threshold dichotomy ($o(n)$ vs. $n - o(n)$, with no intermediate stable state) relies on the solvency channel being the sole failure mechanism with a uniform threshold $r$. Marks create a **heterogeneous effective threshold** ($r_{\text{eff}} = r - M_i(t)$ varies across banks and across time). This heterogeneity is qualitatively similar to having a threshold distribution rather than a fixed $r$ — which is the setup of **Watts (2002)** and **Gleeson-Cahalane (2007)**, not Janson.

In the Watts/Gleeson regime, the cascade condition involves the fraction of "vulnerable" nodes (those with low enough threshold to be activated early), and the dichotomy can be replaced by a **continuous transition** or a **cascade window** in $p$-space. Introducing marks into the Janson regime could shift the model's behavior toward the Watts universality class, undermining the §4 benchmark and the entire Janson-extension research direction (Q1/D-004).

### Risk 3: Parameter Space Explosion (Medium Severity, High Likelihood)

The current model has the parameter set $(n, p, r, \mu, \kappa, a, \theta)$ with the phase diagram in $(r, \mu)$ space. Adding $m$ and $k$ creates a 2-parameter family of marks mechanisms, and the "interesting" behavior likely depends on the ratios $m/r$ and $k/X$. The phase diagram becomes $(r, \mu, m, k)$-dimensional — far too many axes for a clean deliverable within 10 weeks.

### Risk 4: Marks Introduce Partial Cascades (Medium Severity, Medium Likelihood)

In the current model, the Janson dichotomy ensures cascades are all-or-nothing. Under marks, the sub-population of marked banks (with reduced threshold) could percolate while the unmarked population does not, producing a **stable intermediate cascade size**. This would show up as a unimodal peak in the $|A^*|/n$ histogram at some intermediate value — breaking the bimodality that justifies the systemic-event threshold $\theta$.

### Risk 5: The $k > 1$ Memory Violates the Halting Rule (Low Severity, Medium Likelihood)

As discussed in §5.4, marks persisting beyond the window length $X$ create a tension with the halting rule. Either:
- The halting rule must be extended to wait for all marks to decay ($X + k$ consecutive quiet rounds in the worst case), or
- The halting rule stays at $X$ quiet rounds but the system retains "hidden" stress (marks) that could trigger a delayed cascade if slightly perturbed.

This is not a mathematical inconsistency, but it adds operational complexity and makes the absorbing-state argument less clean.

### Risk 6: Empirical Indistinguishability (Medium Severity, High Likelihood)

The marks mechanism (for $m < r$ and moderate $k$) primarily affects the cascade at intermediate densities, where fear amplifies solvency propagation. The D-006 window-length $X$ already provides a handle on fear persistence at the global level. It is plausible that the $(r, \mu)$ phase diagram under marks (with appropriate $m, k$) is statistically indistinguishable from the current model with an adjusted $\mu_{\text{eff}}$ or $X_{\text{eff}}$ — meaning marks add complexity without empirically distinguishable signatures.

---

## §7 — Benchmark Comparisons

### 7.1 Current Model vs. F2 Marks: Summary Table

| Criterion | Current (§3.3) | F2 Marks ($m < r$) | F2 Marks ($m \ge r$) |
|---|---|---|---|
| Analytical tractability | **High** — scalar mean-field map, tangency condition, clean $a_c(\mu)$ | **Low** — coupled $O(kr)$-dim system | **Medium** — reduces to current model |
| Subcritical amplifier ($R \approx \mu$) | **Yes**, cleanly | Weaker near zero; **possibly supercritical** at intermediate $\varphi$ | **Yes** (equivalent to current) |
| Janson dichotomy preserved | **Yes** — solvency channel unmodified | **Questionable** — heterogeneous effective $r$ | **Yes** (equivalent) |
| D-006 compatibility | **Clean** — single global memory | **Problematic** — dual memory ($X$ + $k$) | **Clean** (marks irrelevant) |
| New physics beyond current + D-006 | N/A (baseline) | **Marginal** — similar "fear amplifies solvency" | **None** |
| Parameter count | $(n, p, r, \mu, \kappa, a)$ | $(n, p, r, \mu, \kappa, a, m, k)$ | Same as current |
| Implementation complexity | **Low** — Bernoulli draw | **High** — per-bank mark tracking with $k$-round decay | **Medium** (effectively Bernoulli) |
| Risk to MVP timeline | **None** (decided model) | **High** — new analytics, new code path, new parameter sweeps | **None** (no new behavior) |

### 7.2 Comparison with the D-006 Window-Length

The D-006 window-length $X$ already provides a **global** persistence mechanism for fear that:
- Is analytically tractable (the $z$-transform / characteristic polynomial analysis in D-006 confirms subcriticality for all $X$).
- Does not modify the solvency channel or create heterogeneous thresholds.
- Does not require per-bank state tracking.
- Has been empirically validated (pilot shows boundary invariance in $X$ within $\pm 0.03$).

The F2 marks mechanism can be understood as a **local** persistence mechanism — fear "sticks" to individual banks rather than affecting the global field. But this local persistence:
- Breaks the clean channel separation.
- Creates heterogeneous effective thresholds (analytically hard, possibly universality-changing).
- Adds little that $X$ does not already capture (both are "fear has a lingering effect").

---

## §8 — Recommendation

### Drop F2 marks for the MVP (option (a) in §3.6).

**Rationale:**

1. **No new physics.** The marks mechanism's primary effect — "fear amplifies solvency" — is already captured by the current model's OR rule (fear independently causes failures, which feed back into the solvency channel via increased failed neighbors). The marks formulation couples the channels through a shared threshold, which changes the mechanism but not the qualitative story.

2. **D-006 already covers persistence.** The window-length $X$ provides a clean, analytically tractable handle on fear persistence without touching the solvency channel. The pilot (D-006) confirms it is empirically robust.

3. **Analytical intractability.** The marks mechanism destroys the scalar mean-field map and the clean tangency analysis (§4). The advisor's steer toward a theoretical result (Q1) makes this a dealbreaker — the project cannot extend Janson's theorems if the mean-field map is a $kr$-dimensional coupled system.

4. **Janson regime incompatibility.** Even $m = 1$ mark effectively eliminates the solvency barrier for marked banks in the Janson regime (§2.3), because $np^{r-1} \to \infty$. This is not a gentle amplification — it's a qualitative regime change that could break the sharp-threshold structure.

5. **Scope.** Two new parameters ($m, k$), a new per-bank state variable ($M_i(t)$), mark-decay bookkeeping, halting-rule modifications, and a higher-dimensional phase diagram are a substantial scope expansion incompatible with the 10-week timeline and the MVP-first roadmap (§6).

### If ever revisited (post-MVP, separate model variant):

- Treat as a **distinct model** ("threshold-coupled two-channel cascade") with its own mean-field derivation.
- Focus on the $m = 1$, $k = 1$ case for minimal added complexity.
- Compare against the decided model's $(r, \mu)$ phase diagram to identify whether marks produce any empirically distinguishable signature.
- Be explicit about the universality-class question: is the marks model in the Janson class or the Watts class?

---

## Reporting Contract

| Item | Status |
|---|---|
| **Research Files Updated** | `docs/research/f2_theoretical_analysis.md` (this file) — new |
| **Theoretical Risks Identified** | 6 risks identified (§6): (1) $m \ge r$ collapse, (2) universality class change, (3) parameter explosion, (4) partial cascades / broken bimodality, (5) halting rule violation with $k > X$, (6) empirical indistinguishability from current model |
| **Benchmark Comparisons** | §7: current model vs. F2 marks (both $m < r$ and $m \ge r$) across 8 criteria; §7.2: F2 marks vs. D-006 window-length |

---

*End of analysis.*
