# Empirical Validation of the Two-Channel Bootstrap Percolation Critical Scaling Law

**Audit Context:**
- **Project Scope:** Affects Q1 / scaling conjecture **D-012** under the Tiered Stance (**D-009**).
- **Data Generation Commit:** `ce198a07b73d89accacdb95e397056dd87aa6cd2`
- **Analysis Runtime Commit:** `283776fd630d22dbc63c640d836cb575c6c3ed42`
- **Base Seed:** `20260611` (generated on 2026-06-11)
- **Simulation Engine:** C++ core engine (passed cross-language verification under **S-021**).

---

## 1. Introduction and Theoretical Background

This research note documents the numerical validation of the conjectured scaling law for the critical seed size in the two-channel bootstrap percolation model. The model couples a local-threshold capital-buffer solvency rule (Janson solvency channel) with a self-reinforcing, confidence-driven global panic field (fear channel).

### 1.1 Model Summary
We analyze the process on an Erdős–Rényi random graph $G(n,p)$ where each node $i$ is either solvent or failed (absorbing). 
1. **Solvency Channel:** A solvent node $i$ fails if it has at least $r \ge 2$ failed neighbors.
2. **Fear Channel:** In round $t$, a solvent node $i$ fails with probability $f_i \, g_t$, where $g_t = a_{t-1}/n$ is the global fear field (fraction of nodes failed in the previous round), and $f_i \sim \text{Beta}(\alpha, \beta)$ is the individual susceptibility drawn at $t=0$ with mean $E[f] = \mu$ and concentration $\kappa$.

### 1.2 Scaling Law Conjecture
In the thermodynamic limit ($n \to \infty$), the generation sizes concentrate around their mean-field expectations. Setting the self-consistent Poisson-combined map $H(\varphi) = \frac{a}{n} + \frac{(np\varphi)^r}{r!} + \mu\varphi$ equal to $\varphi$ (yielding the fixed-point equation $(1-\mu)\varphi \approx \frac{a}{n} + \frac{(np\varphi)^r}{r!}$) and its derivative to $1$ under the saddle-node tangency condition yields the critical seed size scaling relation:
$$a_c(\mu) = a_c(0)(1-\mu)^{r/(r-1)}$$
where $a_c(0)$ is the standard Janson et al. (2012) bootstrap percolation threshold at $\mu = 0$:
$$a_c(0) = \left(1-\frac{1}{r}\right) \left(\frac{(r-1)!}{n p^{r}}\right)^{1/(r-1)}$$

This note evaluates whether the empirical threshold scaling ratio $\text{ratio}_{\text{emp}} = a_{\text{emp}}(\mu)/a_{\text{emp}}(0)$ complies with the theoretical ratio $\text{ratio}_{\text{theory}} = (1-\mu)^{r/(r-1)}$.

---

## 2. Simulation Setup

We perform sweeps using the high-performance C++ simulation engine. The parameters are configured as follows:
* **System Size ($N$):** $1000$
* **Edge Probability ($p$):** $0.008$ (yielding target mean degree $np = 8.0$)
* **Fear Heterogeneity ($\kappa$):** $50.0$
* **Systemic-Event Threshold ($\theta$):** $0.5$ (in the bimodal valley)
* **Fear Grid ($\mu$):** $\mu \in [0.0, 0.9]$ in steps of $0.05$ (19 points)
* **Seed Grid Multiples ($m$):** `[0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]` (10 points)
* **Realizations per Cell:** 500

For each parameter cell $(\mu, m)$, the seed size is scaled relative to the Janson baseline $a_c(0)$ as $a = \max(r, \text{round}(m \cdot a_c(0)))$. The empirical threshold $a_{\text{emp}}(\mu)$ is estimated by linear interpolation of the systemic probability $P(\text{systemic}) = P(|A^*|/n \ge \theta)$ across the seed size grid to locate the $0.5$ crossing point.

---

## 3. Quantitative Validation Results

### 3.1 Metric Definitions
* **`diff` (Signed Error):** $\text{ratio}_{\text{emp}} - \text{ratio}_{\text{theory}}$
* **`max_diff` (Max Absolute Error):** $\max | \text{ratio}_{\text{emp}} - \text{ratio}_{\text{theory}} |$ over non-clamped rows.
* **`mean_diff` (Mean Absolute Error):** $\text{mean} | \text{ratio}_{\text{emp}} - \text{ratio}_{\text{theory}} |$ over non-clamped rows, including the $\mu=0.0$ anchor (where $\text{diff} \equiv 0.0$).
* **`predicted_ac`:** Descriptive asymptotic theoretical threshold $a_c(\mu) = a_c(0)(1-\mu)^{r/(r-1)}$. This is not a prediction of the finite empirical threshold $a_{\text{emp}}(\mu)$ because it sits systematically lower due to finite-size offsets.
* **`is_clamped`:** Set to `True` if $a_{\text{emp}} \le \text{min}(simulated\ seed\ sizes)$. Clamped rows are excluded from the summary statistics (`max_diff`, `mean_diff`).

### 3.2 Solvency Depth $r = 2$
* **Baseline Empirical Threshold $a_{\text{emp}}(0)$:** $11.630$ (vs. asymptotic theoretical $a_c(0) = 7.813$)
* **Mean Absolute Error (`mean_diff`):** $0.114$
* **Maximum Absolute Error (`max_diff`):** $0.189$ (occurring at $\mu = 0.65$)
* **Clamping Status:** Clamped at $\mu = 0.90$ (where $a_{\text{emp}} = 2.0$)

| $\mu$ | $a_{\text{emp}}$ | $\text{ratio}_{\text{emp}}$ | $\text{ratio}_{\text{theory}}$ | $\text{diff}$ (signed) | $a_c(\mu)$ (Asymptotic) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 0.00 | 11.6301 | 1.0000 | 1.0000 | 0.0000 | 7.8125 | Valid |
| 0.05 | 10.7795 | 0.9269 | 0.9025 | 0.0244 | 7.0508 | Valid |
| 0.10 | 9.8741 | 0.8490 | 0.8100 | 0.0390 | 6.3281 | Valid |
| 0.15 | 9.2286 | 0.7935 | 0.7225 | 0.0710 | 5.6445 | Valid |
| 0.20 | 8.0938 | 0.6959 | 0.6400 | 0.0559 | 5.0000 | Valid |
| 0.25 | 7.4634 | 0.6417 | 0.5625 | 0.0792 | 4.3945 | Valid |
| 0.30 | 6.8846 | 0.5920 | 0.4900 | 0.1020 | 3.8281 | Valid |
| 0.35 | 6.2353 | 0.5361 | 0.4225 | 0.1136 | 3.3008 | Valid |
| 0.40 | 5.4881 | 0.4719 | 0.3600 | 0.1119 | 2.8125 | Valid |
| 0.45 | 4.9018 | 0.4215 | 0.3025 | 0.1190 | 2.3633 | Valid |
| 0.50 | 4.6993 | 0.4041 | 0.2500 | 0.1541 | 1.9531 | Valid |
| 0.55 | 4.2994 | 0.3697 | 0.2025 | 0.1672 | 1.5820 | Valid |
| 0.60 | 3.7578 | 0.3231 | 0.1600 | 0.1631 | 1.2500 | Valid |
| 0.65 | 3.6222 | 0.3115 | 0.1225 | 0.1890 | 0.9570 | Valid |
| 0.70 | 2.8284 | 0.2432 | 0.0900 | 0.1532 | 0.7031 | Valid |
| 0.75 | 2.6000 | 0.2236 | 0.0625 | 0.1611 | 0.4883 | Valid |
| 0.80 | 2.4865 | 0.2138 | 0.0400 | 0.1738 | 0.3125 | Valid |
| 0.85 | 2.2560 | 0.1940 | 0.0225 | 0.1715 | 0.1758 | Valid |
| 0.90 | 2.0000 | — | 0.0100 | — | 0.0781 | Clamped |

### 3.3 Solvency Depth $r = 3$
* **Baseline Empirical Threshold $a_{\text{emp}}(0)$:** $60.498$ (vs. asymptotic theoretical $a_c(0) = 41.667$)
* **Mean Absolute Error (`mean_diff`):** $0.026$
* **Maximum Absolute Error (`max_diff`):** $0.069$ (occurring at $\mu = 0.80$)
* **Clamping Status:** Clamped at $\mu \ge 0.85$ (where $a_{\text{emp}} = 8.0$)

| $\mu$ | $a_{\text{emp}}$ | $\text{ratio}_{\text{emp}}$ | $\text{ratio}_{\text{theory}}$ | $\text{diff}$ (signed) | $a_c(\mu)$ (Asymptotic) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 0.00 | 60.4981 | 1.0000 | 1.0000 | 0.0000 | 41.6667 | Valid |
| 0.05 | 55.4333 | 0.9163 | 0.9259 | -0.0097 | 38.5811 | Valid |
| 0.10 | 51.7316 | 0.8551 | 0.8538 | 0.0013 | 35.5756 | Valid |
| 0.15 | 47.2437 | 0.7809 | 0.7837 | -0.0027 | 32.6526 | Valid |
| 0.20 | 44.0093 | 0.7274 | 0.7155 | 0.0119 | 29.8142 | Valid |
| 0.25 | 39.3243 | 0.6500 | 0.6495 | 0.0005 | 27.0633 | Valid |
| 0.30 | 36.3791 | 0.6013 | 0.5857 | 0.0157 | 24.4026 | Valid |
| 0.35 | 32.6684 | 0.5400 | 0.5240 | 0.0159 | 21.8353 | Valid |
| 0.40 | 29.5714 | 0.4888 | 0.4648 | 0.0240 | 19.3649 | Valid |
| 0.45 | 26.4272 | 0.4368 | 0.4079 | 0.0289 | 16.9955 | Valid |
| 0.50 | 23.2414 | 0.3842 | 0.3536 | 0.0306 | 14.7314 | Valid |
| 0.55 | 20.4286 | 0.3377 | 0.3019 | 0.0358 | 12.5779 | Valid |
| 0.60 | 17.8186 | 0.2945 | 0.2530 | 0.0415 | 10.5409 | Valid |
| 0.65 | 14.8621 | 0.2457 | 0.2071 | 0.0386 | 8.6276 | Valid |
| 0.70 | 12.9418 | 0.2139 | 0.1643 | 0.0496 | 6.8465 | Valid |
| 0.75 | 11.2958 | 0.1867 | 0.1250 | 0.0617 | 5.2083 | Valid |
| 0.80 | 9.5667 | 0.1581 | 0.0894 | 0.0687 | 3.7268 | Valid |
| 0.85 | 8.0000 | — | 0.0581 | — | 2.4206 | Clamped |
| 0.90 | 8.0000 | — | 0.0316 | — | 1.3176 | Clamped |

### 3.4 Solvency Depth $r = 4$
* **Baseline Empirical Threshold $a_{\text{emp}}(0)$:** $137.867$ (vs. asymptotic theoretical $a_c(0) = 85.178$)
* **Mean Absolute Error (`mean_diff`):** $0.020$
* **Maximum Absolute Error (`max_diff`):** $0.048$ (occurring at $\mu = 0.85$)
* **Clamping Status:** Clamped at $\mu = 0.90$ (where $a_{\text{emp}} = 17.0$)

| $\mu$ | $a_{\text{emp}}$ | $\text{ratio}_{\text{emp}}$ | $\text{ratio}_{\text{theory}}$ | $\text{diff}$ (signed) | $a_c(\mu)$ (Asymptotic) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 0.00 | 137.8667 | 1.0000 | 1.0000 | 0.0000 | 85.1775 | Valid |
| 0.05 | 129.1376 | 0.9367 | 0.9339 | 0.0028 | 79.5469 | Valid |
| 0.10 | 120.8817 | 0.8768 | 0.8689 | 0.0079 | 74.0142 | Valid |
| 0.15 | 111.8656 | 0.8114 | 0.8052 | 0.0062 | 68.5831 | Valid |
| 0.20 | 104.9964 | 0.7616 | 0.7427 | 0.0189 | 63.2574 | Valid |
| 0.25 | 94.8037 | 0.6876 | 0.6814 | 0.0062 | 58.0417 | Valid |
| 0.30 | 87.2578 | 0.6329 | 0.6215 | 0.0114 | 52.9406 | Valid |
| 0.35 | 78.9803 | 0.5729 | 0.5631 | 0.0098 | 47.9597 | Valid |
| 0.40 | 73.3412 | 0.5320 | 0.5061 | 0.0259 | 43.1049 | Valid |
| 0.45 | 63.6238 | 0.4615 | 0.4506 | 0.0109 | 38.3833 | Valid |
| 0.50 | 57.3750 | 0.4162 | 0.3969 | 0.0193 | 33.8027 | Valid |
| 0.55 | 50.7783 | 0.3683 | 0.3448 | 0.0235 | 29.3726 | Valid |
| 0.60 | 43.6615 | 0.3167 | 0.2947 | 0.0220 | 25.1037 | Valid |
| 0.65 | 39.4967 | 0.2865 | 0.2467 | 0.0398 | 21.0095 | Valid |
| 0.70 | 31.6758 | 0.2298 | 0.2008 | 0.0289 | 17.1062 | Valid |
| 0.75 | 26.5094 | 0.1923 | 0.1575 | 0.0348 | 13.4146 | Valid |
| 0.80 | 22.5617 | 0.1636 | 0.1170 | 0.0467 | 9.9624 | Valid |
| 0.85 | 17.6483 | 0.1280 | 0.0797 | 0.0483 | 6.7886 | Valid |
| 0.90 | 17.0000 | — | 0.0464 | — | 3.9536 | Clamped |

---

## 4. Discussion of Analytical Caveats

### 4.1 Coarse Seed Grid Quantization
The seed sizes swept in simulation are discrete integers. The grid is spaced in intervals of $\Delta a = 0.2 \times a_c(0)$, meaning that for a given $\mu$, the $0.5$ crossing is linearly interpolated across adjacent grid multiples. When the empirical critical seed is small (especially in the $r=2$ sweep), the step size $\Delta a \approx 1.5$ is large relative to the threshold itself, making the interpolation highly sensitive to realization-level statistical noise. 

### 4.2 Data-Driven Clamping Floor Constraint
In `analysis.py`, clamping is evaluated purely via a data-driven rule:
$$\text{is\_clamped} = a_{\text{emp}} \le \min(\text{simulated seed sizes})$$
By the runner's grid construction, the minimum simulated seed size is $a_{\text{min}} = \max(r, \text{round}(m_{\text{min}} \times a_c(0)))$, with $m_{\text{min}} = 0.2$. Consequently, the minimum possible seed sizes are:
* For $r=2$: $\max(2, \text{round}(0.2 \times 7.8125)) = 2.0$
* For $r=3$: $\max(3, \text{round}(0.2 \times 41.6667)) = 8.0$
* For $r=4$: $\max(4, \text{round}(0.2 \times 85.1775)) = 17.0$

When $\mu \to 1.0$, the theoretical critical seed size $a_c(\mu)$ decays to zero. However, because the seed size is bounded from below by these grid constraints, the empirical crossing cannot cross the floor and is clamped. Clamped rows are successfully masked out of the summary statistics to preserve validation integrity.

### 4.3 Finite-Size Baseline Offset
At $N=1000$, a significant offset exists between the finite-system empirical threshold $a_{\text{emp}}(0)$ and the asymptotic theoretical limit $a_c(0)$. As documented in the project tracker (S-006/S-007), this offset is a finite-size effect set by the absolute magnitude of $a_c(0)$: as $a_c(0)$ increases (either via system size or graph connectivity), the transition sharpens and the ratio $a_{\text{emp}}(0)/a_c(0) \to 1$.

At the current scale, the empirical baseline thresholds sit systematically higher, forming a non-monotonic band of **$45\%$ to $62\%$ upward shift**:
* For $r=3$: $a_{\text{emp}}(0) / a_c(0) = 60.498 / 41.667 \approx 1.45$ ($45\%$ offset)
* For $r=2$: $a_{\text{emp}}(0) / a_c(0) = 11.630 / 7.813 \approx 1.49$ ($49\%$ offset)
* For $r=4$: $a_{\text{emp}}(0) / a_c(0) = 137.867 / 85.178 \approx 1.62$ ($62\%$ offset)

This shows that `predicted_ac` is a descriptive asymptotic benchmark rather than a predictive estimator of $a_{\text{emp}}(\mu)$ in finite systems.

### 4.4 The Cancellation of the Finite-Size Factor $K$
To understand why the relative scaling law holds when predicted thresholds are off by ~49%, we can model the finite empirical threshold as:
$$a_{\text{emp}}(\mu) \approx K(\mu, n) \cdot a_c(\mu)$$
where $K(\mu, n)$ is a finite-size inflation factor. Taking the relative empirical ratio gives:
$$\text{ratio}_{\text{emp}} = \frac{a_{\text{emp}}(\mu)}{a_{\text{emp}}(0)} \approx \left[ \frac{K(\mu, n)}{K(0, n)} \right] (1-\mu)^{r/(r-1)}$$
For large $a_c(0)$ configurations (such as $r=3$ and $r=4$), the inflation factor $K(\mu, n)$ is approximately independent of the fear level $\mu$. The coefficient ratio $K(\mu, n)/K(0, n)$ thus collapses to $1$, allowing the finite-size correction to cancel out. This explains why the relative scaling ratio validates with exceptional accuracy despite substantial absolute offsets.

### 4.5 Systematic Positive Bias for $r=2$
The solvency depth $r=2$ exhibits a systematic positive bias across the entire sweep range where the empirical ratio decays slower than $(1-\mu)^2$:
* The positive bias is present even at low fear levels (e.g., $\text{diff} = +0.071$ at $\mu=0.15$ where $a_{\text{emp}} \approx 9.2$, far above the grid floor of 2).
* The maximum absolute difference ($\text{max\_diff} = 0.189$) occurs in the middle of the sweep at $\mu=0.65$ (where $a_{\text{emp}} \approx 3.6$), rather than near the high-$\mu$ floor boundary.
* Since the seed size gets very small at high $\mu$, the $r=2$ system operates in a regime where the finite-size inflation factor $K(\mu, n)$ is highly sensitive to the absolute scale. The inflation $K(\mu,n)$ grows as the threshold drops, meaning $K(\mu,n) > K(0,n)$, which prevents the cancellation of the finite-size factor and causes the positive ratio bias.
* The same bias exists for $r=3$ and $r=4$ but is small and well-controlled (maximum absolute differences of $0.069$ and $0.048$, respectively), showing that it is a genuine caveat specifically for the small-$a_c(0)$ regime of $r=2$.

---

## 5. Convergence Analysis and Future Work

### 5.1 Convergence and Exceptions
The relative scaling ratio validation confirms the scaling model with exceptional accuracy for higher-order configurations:
* **$r=3$ Compliance:** Mean absolute error of $2.6\%$, with the scaling ratio closely tracking the $(1-\mu)^{1.5}$ profile.
* **$r=4$ Compliance:** Mean absolute error of $2.0\%$, tracking the $(1-\mu)^{1.33}$ profile.

The solvency depth $r=2$ is the exception, exhibiting a mean absolute error of $11.4\%$. 

### 5.2 Exponent Sensitivity and Discretization
Because $a_c(0)$ is very small for $r=2$ ($7.81$), the absolute values of the seeds are small (varying between 2 and 12). Discretization to integer steps represents a massive relative step size, causing high sensitivity to finite-size corrections. Furthermore, the sensitivity to errors in the effective decay base is amplified most strongly by the exponent $r/(r-1) = 2$ (compared to $1.5$ for $r=3$ and $1.33$ for $r=4$).

### 5.3 Proposed Future Experiments
To resolve whether this systematic bias is purely a finite-size convergence delay or a fundamental limitation of the $r=2$ mean-field model, we propose the following sweeps:
1. **Larger System Sizes ($N$):** Perform sweeps at $N=5000$ and $N=10000$.
2. **Mandatory $p$-scaling:** In accordance with the Janson connectivity scaling regime (Decision **D-004**), the edge probability must scale as:
   $$p_n = \beta n^{-\alpha} \quad (\text{with } \alpha = 0.7 \text{ for } r=2)$$
   where the scaling coefficient $\beta$ is fixed at a reference system size (e.g. $N_{\text{ref}} = 1000$ so $\beta = 0.008 / 1000^{-0.7} \approx 1.007140$). This scaling guarantees that the mean degree $np$ grows as $n^{0.3}$ and the baseline critical seed size $a_c(0) \propto n^{0.4}$ increases with $n$ (from $7.81$ at $N=1000$ to $14.87$ at $N=5000$ and $19.62$ at $N=10000$). Holding $p$ fixed would instead cause $a_c(0)$ to decrease (from $7.81$ down to $1.56$ at $N=5000$), compounding the floor constraint.
3. **Finer Seed Grids:** Sweep with a finer multiples grid near the floor (e.g., spacing of $0.05$ or $0.10$ rather than $0.20$) to refine crossing interpolation and reduce quantization noise.
