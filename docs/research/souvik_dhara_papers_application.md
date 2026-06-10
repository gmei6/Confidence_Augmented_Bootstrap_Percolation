# Application of Souvik Dhara's Research to the Two-Channel Cascade Model

This document provides a comprehensive analysis of how three foundational papers co-authored by Prof. Souvik Dhara apply to the **Two-Channel Cascade Model of Bank Failure**. It details the mathematical frameworks, core equations, and actionable implementation guidelines for both our baseline $G(n,p)$ simulations and future scale-free configuration model extensions.

---

## 1. Multiscale Genesis of a Tiny Giant for Percolation on Scale-Free Random Graphs (2024)
*Shankar Bhamidi, Souvik Dhara, Remco van der Hofstad*

### 1.1 Key Mathematical Framework
This paper analyzes critical percolation on scale-free random graphs (Norros–Reittu, Chung–Lu, and generalized random graphs) with power-law degree exponent $\tau \in (2,3)$. Because the variance of the degree distribution is infinite in this regime, the phase transition behaves differently than in standard Erdős–Rényi models.

> [!WARNING]
> **Notation Overloading Warning:**
> The symbols $\alpha$ and $\beta$ are heavily overloaded in this project:
> 1. **Janson scaling regime:** $p_n = \beta_{\mathrm{J}} n^{-\alpha_{\mathrm{J}}}$.
> 2. **Beta susceptibility distribution:** $f_i \sim \text{Beta}(\alpha_{\mathrm{Beta}}, \beta_{\mathrm{Beta}})$.
> 3. **Bhamidi et al. (2024) exponents:** weight scaling exponent $\alpha = 1/(\tau-1)$ and component scaling exponent $\beta = \frac{\tau^2-4\tau+5}{2(\tau-1)}$.
> In this section, $\alpha$ and $\beta$ refer strictly to the paper's exponents (case 3), unless subscripted otherwise.

* **Vertex Weight Parameterization:** Vertices are assigned weights $w_i = c_{\mathrm{F}} \xi_i$ (Bhamidi et al. 2024, Eq. 2.1), where $\xi_i = (i/n)^{-\alpha}$ is a rank-dependent scaling factor (or drawn from a power law with tail exponent $\tau$), $c_{\mathrm{F}} > 0$ is a scaling constant, and $\alpha = 1/(\tau-1)$. This formulation ensures that the maximum weight scales as $w_{\max} = \Theta(n^\alpha)$ while the mean vertex weight $\mu_{\mathrm{W}} = \mathbb{E}[W]$ remains a bounded, $O(1)$ constant.
* **Critical Scaling Window:** The critical edge-retention probability $\pi_n$ scales as:
  $$\pi_n(\lambda) = \lambda n^{-\eta_s} \quad \text{where} \quad \eta_s = \frac{3-\tau}{2} \quad \text{(Bhamidi et al. 2024, Eq. 2.8)}$$
  The critical window is a bounded interval $\lambda \in (0, \lambda_c)$.
* **Component Size Scaling:** Inside this window, the largest components scale as $n^\beta$ with:
  $$\beta = \frac{\tau^2 - 4\tau + 5}{2(\tau - 1)} \in \left[\sqrt{2}-1, 0.5\right) \quad \text{(Bhamidi et al. 2024, Theorem 2.3)}$$
* **The Critical Threshold ($\lambda_c$):** The critical value $\lambda_c$ is explicitly defined as:
  $$\lambda_c := \sqrt{\frac{\eta}{4B_{\alpha}}} = \frac{c_{\mathrm{F}}^{-1/\alpha}}{2} \sqrt{\frac{(3-\tau)\mu_{\mathrm{W}}^{1/\alpha}}{A_{\alpha}}} \quad \text{(Bhamidi et al. 2024, Eq. 2.10)}$$
  where:
  - $\alpha = 1/(\tau-1)$ is the scale of the maximum weight.
  - $\eta = \frac{3-\tau}{\tau-1}$ is the window scaling exponent.
  - $A_{\alpha} := \int_0^{\infty} \frac{1 - e^{-z}}{z^{1/\alpha}} dz$ and $B_{\alpha} := \frac{\alpha c_{\mathrm{F}}^{2/\alpha} A_{\alpha}}{\mu_{\mathrm{W}}^{1/\alpha}}$ (Bhamidi et al. 2024, Eq. 2.11).
  > [!NOTE]
  > Eq. (2.11) in the original paper contains a minor typo where $\alpha$ is placed in the denominator of $B_{\alpha}$; consistency with the expanded form in Eq. (2.10) requires $\alpha$ to be in the numerator as written above.
  > [!IMPORTANT]
  > The term $\mu_{\mathrm{W}}$ represents the mean vertex weight of the random graph. This must not be conflated with the cascade model's mean individual fear parameter $\mu = \mathbb{E}[f]$, which is a property of the node susceptibility distribution.
* **Two-Step Connectivity:** Macro-hubs (vertices of weight $n^\alpha$) connect via two-hop paths through intermediate meso-hubs (vertices of weight $n^\rho$ with $\rho = (\tau-2)/(\tau-1)$) with a Poisson number of connections:
  $$\lambda_{ij} := \lambda^2 \int_0^\infty (1 - e^{-c_{\mathrm{F}} \xi_i x^{-\alpha}})(1 - e^{-c_{\mathrm{F}} \xi_j x^{-\alpha}}) dx \quad \text{(Bhamidi et al. 2024, Eq. 2.14)}$$
* **The Tiny Giant:** When $\lambda > \lambda_c$, a unique, concentrated giant component of size $\Theta(\sqrt{n})$ suddenly emerges (Bhamidi et al. 2024, Theorem 2.6).

### 1.2 Translation to the Cascade Model
* **The Cascade Takeoff Analogy:**
  The sudden emergence of the tiny giant is a conceptual analogue for the systemic-cascade takeoff. However, there is a fundamental difference in the transition: the paper characterizes the "sudden emergence" of a unique giant component of size $\Theta(\sqrt{n})$ for $\lambda > \lambda_c$, whereas the solvency-fear cascade model exhibits a discontinuous (first-order) phase transition (the Janson dichotomy) due to the local solvency threshold $r \ge 2$.
* **First-Order Cascade Transition in the Scale-Free Regime:**
  The discontinuous (first-order) nature of the cascade transition is robust even in the infinite-variance $\tau \in (2,3)$ regime. The hubs of the "tiny giant" core do not smooth out the transition; instead, they act as a concentrated internal seed that localizes failures and ignites the network, causing a first-order collapse at a significantly lower connectivity threshold.
* **Sublinear Tiny Giant vs. Macroscopic Cascade:**
  The "tiny giant" component is of size $\Theta(\sqrt{n})$, which is sub-macroscopic ($o(n)$) in the thermodynamic limit. In contrast, our cascade model defines a systemic event macroscopically as $|A^*|/n \ge \theta$ where $\theta \in [0.2, 0.8]$ (a linear fraction $\Theta(n)$). Janson's sub-macroscopic step-clock collapse assumption holds during the early critical stages but breaks down once the cascade reaches macroscopic size.
* **Transition-Width Exponent $\nu$ and $\mu$-Invariance (Q3 / Baseline):**
  For our baseline $G(n,p)$ model, the transition-width exponent $\nu$ belongs to the Erdős–Rényi Janson regime ($r \ge 2$). Under connectivity scaling $p_n = \beta_{\mathrm{J}} n^{-\alpha_{\mathrm{J}}}$, the transition width is set by the fluctuations of the active set size at the critical step $t_c \sim n^{\frac{r\alpha_{\mathrm{J}}-1}{r-1}}$, scaling as $t_c^{1/2}$. This translates to an absolute seed fraction transition width of:
  $$\Delta (a/n) \sim n^{-\frac{2r-1-r\alpha_{\mathrm{J}}}{2(r-1)}}$$
  For our parameters $r=2$ and $\alpha_{\mathrm{J}}=0.7$, the critical step scales as $t_c \sim n^{0.4}$, and the absolute seed fraction transition width scales as $n^{-0.8}$ (implying an absolute exponent $\nu_{\mathrm{abs}} = 1.25$).
  
  In terms of the *relative* transition width (relative to the critical seed size $a_c/n \sim n^{-0.6}$), the scaling is:
  $$\Delta(a)/a_c \sim \Delta(a/n)/(a_c/n) \sim n^{-0.8}/n^{-0.6} = n^{-0.2}$$
  which yields a relative exponent $\nu_{\mathrm{rel}} = 5.0$. We formulate these as conjectural predictions to be simulation-tested in Week 6-7.

  > [!NOTE]
  > **Mathematical Exponent Invariance and Crossover Regime:**
  > Under our rescaled model (Decision D-012), the rescaled Janson equation becomes $(1-\mu)\varphi \approx \frac{a}{n} + \frac{(np\varphi)^r}{r!}$, which is isomorphic to the pure Janson model with rescaled parameters $a_{\text{eff}} = a/(1-\mu)$ and $p_{\text{eff}} = p (1-\mu)^{-1/r}$. Because the Janson exponent $\alpha_{\mathrm{J}}$ is unchanged, the scaling of the bottleneck step size $t_c$ and the transition-width exponents are mathematically invariant to $\mu \in [0, 1)$. However, this requires $n p_{\text{eff}}^r \to 0$ to hold, which translates to the constraint $1-\mu \gg n^{1 - r\alpha_{\mathrm{J}}}$. For $r=2, \alpha_{\mathrm{J}}=0.7$, the regime breaks down when $1-\mu \le O(n^{-0.4})$, creating a finite-size scaling crossover region where Janson invariants break down.

### 1.3 Interface with the Asymptotic Decoupling Conjecture
Dhara's work on critical scaling limits relies on analyzing percolation via local tree-like neighborhoods. This directly interfaces with our project's **Asymptotic Decoupling Conjecture** (empirically validated in Session 19). The decoupling conjecture states that the individual node activation times $Y_i'$ are asymptotically decoupled into *independent random variables* $Y_i = \min(Y_i^{\text{solv}}, Y_i^{\text{fear}})$, where the fear clocks become independent geometric clocks $Y_i^{\text{fear}} \sim \text{Geom}(f_i/n)$ due to the concentration of generation sizes. In the critical phase, the network is locally tree-like, which mathematically justifies the independence of individual fear activation trials and enables branching-process approximations of the early cascade phase.

> [!NOTE]
> **Janson vs. Bounded-Degree Regime for Fear Heterogeneity:**
> In our baseline Janson regime ($np \to \infty$), the ratio of the second-order fear term to the leading solvency term scales as $O((np)^{-r/(r-1)}) \to 0$, which means that fear heterogeneity (variance) only enters at second order, and the threshold is dominated strictly by $\mu$. However, in a sparse configuration model (Q2 pivot) with bounded mean degree ($np = O(1)$), the solvency and fear variance terms are of the same order, meaning fear heterogeneity will shift the takeoff boundary at first order.

---

## 2. Global Lower Mass-Bound for Critical Configuration Models in the Heavy-Tailed Regime (2022)
*Shankar Bhamidi, Souvik Dhara, Remco van der Hofstad, Sanchayan Sen*

### 2.1 Key Mathematical Framework
This paper analyzes critical configuration models with power-law exponent $\tau \in (3,4)$ (finite variance, infinite third moment). It proves that critical components satisfy the **global lower mass-bound property**, meaning that the vertex count in any small neighborhood of a critical component is well-distributed (no "light spots").

* **Criticality Window Condition:** The configuration model is positioned within the critical window of the phase transition when the branching ratio parameter satisfies:
  $$\nu_n = \frac{\sum_{i \in [n]} d_i(d_i - 1)}{\sum_{i \in [n]} d_i} = 1 + \lambda n^{-\eta_{\tau\in(3,4)}} + o(n^{-\eta_{\tau\in(3,4)}}) \quad \text{(Bhamidi et al. 2022, Eq. 1.2)}$$
  where $\eta_{\tau\in(3,4)} = (\tau-3)/(\tau-1)$.
  > [!IMPORTANT]
  > **Exponents and Threshold Mismatch:**
  > The branching parameter condition $\nu_n = 1$ characterizes the critical window for standard percolation ($r=1$). For bootstrap percolation / our cascade model ($r \ge 2$), the transition is first-order (discontinuous) and occurs at a much higher threshold where the branching parameter $\nu_n$ is strictly greater than 1 (and can be arbitrarily large). The branching parameter $\nu_n$ must not be confused with the critical transition-width exponent $\nu$ used in Janson sweeps.
* **GHP Convergence:** Proving this mass-bound allows the authors to establish convergence in the Gromov-Hausdorff-Prokhorov (GHP) topology, yielding scaling limits for global functionals such as the diameter:
  $$\text{diam}(\mathscr{C}_{(i)}) \sim n^{\eta_{\tau\in(3,4)}} \quad \text{(Bhamidi et al. 2022, Theorem 1.2)}$$

### 2.2 Translation to the Cascade Model
* **Degree Sequence Configuration (Q2):**
  If we implement the configuration-model pivot, we can adopt their exact moment assumptions (Assumption 1.1) and size-biased tail bounds (Assumption 1.3) to generate a mathematically valid critical network.
* **Topology-Free Coupling vs. Diameter Decoupling:**
  Although critical component diameters scale as $n^{\eta_{\tau\in(3,4)}}$ in the underlying network, the global fear channel introduces a completely topology-free coupling ($g_t = a_{t-1}/n$) that acts as a global shortcut across disconnected components once the cascade reaches macroscopic size ($a_{t-1} = \Theta(n)$). During the early critical takeoff phase when $a_{t-1} = o(n)$, the local component topology and diameter remain major bottlenecks, because the probability of depositing $r$ independent fear failures in a small component of size $K$ is vanishingly small ($O(K^r (a_{t-1}/n)^r)$).
* **Universality Class Framing:**
  Helps us partition our configuration-model cascade results into two distinct heavy-tailed universality classes:
  1. $\tau \in (3,4)$: Finite variance, where critical component diameters grow as $n^{\eta_{\tau\in(3,4)}}$.
  2. $\tau \in (2,3)$: Infinite variance, where typical distances collapse to the ultra-small-world scale $O(\log\log n)$ due to the tiny-giant core.

---

## 3. On $s$-to-$q$ Norms of Random Matrices with Nonnegative Entries (2023)
*Souvik Dhara, Debankur Mukherjee, Kavita Ramanan*

> [!WARNING]
> **Severe Notation Collision Warning:**
> The paper defines the $r$-to-$p$ operator norm (Dhara et al. 2023, Eq. 1.1). We rename the paper's exponents $r \to s$ and $p \to q$ to prevent extreme confusion with the cascade model's solvency threshold $r$ and the graph edge-probability $p$.

> [!IMPORTANT]
> **Developer Implementation Guidelines:**
> To prevent catastrophic logic bugs, all code comments, implementation files, and tests must strictly use the $(s, q)$ norm notation, avoiding the paper's original $(r, p)$ notation. The letters $r$ and $p$ are reserved exclusively for the solvency threshold and the graph edge-probability, respectively. Additionally, do not confuse the configuration model's branching parameter `nu_n` (or `branching_ratio`) with the transition-width scaling exponent `nu` (or `width_exponent`) in code or configurations.

### 3.1 Key Mathematical Framework
This paper studies the $s \to q$ operator norm of symmetric nonnegative random matrices $A_n$ (for $1 < q \le s < \infty$):
$$\|A_n\|_{s \to q} := \sup_{\|\mathbf{x}\|_s \le 1} \|A_n \mathbf{x}\|_q \quad \text{(Dhara et al. 2023, Eq. 1.1)}$$
* **$\ell_\infty$ Maximizer Bound:** The unique positive maximizing vector $\mathbf{v}_n$ concentrates around the uniform vector:
  $$\|\mathbf{v}_n - n^{-1/s}\mathbf{1}\|_{\infty} \le \frac{6q}{s-q} n^{-\frac{1}{s}} \sqrt{\frac{\log n}{n\mu_{\mathrm{A}, n}} \times \frac{\sigma_{\mathrm{A}, n}^2}{\mu_{\mathrm{A}, n}}} \quad \text{(Dhara et al. 2023, Theorem 2.6(a))}$$
  where $\mu_{\mathrm{A}, n}$ is the mean of the random matrix entries, and $\sigma_{\mathrm{A}, n}^2$ is their variance.
  > [!NOTE]
  > We denote the mean matrix entry as $\mu_{\mathrm{A}, n}$ to avoid conflation with the cascade model's mean individual fear $\mu$.
  > [!WARNING]
  > **Concentration Breakdown and Hub Localization:**
  > The concentration of the maximizing vector $\mathbf{v}_n$ around the uniform vector requires a bounded variance-to-mean ratio (Fano factor) of the matrix entries. In scale-free graphs with $\tau \in (2,3)$ (Q2 pivot), the degree variance diverges as $n \to \infty$, causing the Fano factor to blow up and the maximizing vector to localize on high-degree hubs, violating the uniform vector concentration assumption. For $\tau \in [3,4)$, the degree variance is finite, but the third moment diverges.

### 3.2 Translation to the Cascade Model
* **Honesty Guardrail: Mean-Field Reduction Justification:**
  In our $G(n,p)$ baseline, the fear channel is a **global feedback field** ($g_t = a_{t-1}/n$). Because the fear channel is global and completely independent of the interbank network's edges, its mean-field reduction is justified by the law of large numbers on the independent node draws, not by the spectral properties or operator norms of the adjacency matrix $A_n$. The $\ell_\infty$ maximizer bound on the adjacency matrix is a conceptual framework showing that localized states are suppressed in homogeneous graphs, rather than a direct mathematical proof for the fear channel.
* **Detecting Localization on Hubs:**
  On scale-free configuration models, the maximizing vector of the adjacency matrix localizes on the hubs. This describes how targeted seeding of hubs shifts the cascade takeoff boundary.
* **Solvency Channel Non-linear Dynamics:**
  For a solvency threshold $r \ge 2$, the local solvency channel is super-linear near zero, meaning its derivative at the origin is 0. The takeoff threshold corresponds to a saddle-node bifurcation of the non-linear map $\boldsymbol{\varphi}(t+1) = T(\boldsymbol{\varphi}(t)) = \Psi_{\mathrm{solv}}(A\boldsymbol{\varphi}(t))$.
  
  The Euler-Lagrange equations for the $s \to q$ norm involve nested applications of $A$ (i.e. $A^T \Psi_q(A\mathbf{v})$), whereas the cascade map involves only a single application of $A$ (i.e. $\Psi_{\mathrm{solv}}(A\boldsymbol{\varphi})$). Thus, the $s \to q$ norm framework serves as a **conceptual parallel** for analyzing non-linear fixed-point stability on graphs, rather than a direct algebraic mapping. Note that mapping the solvency takeoff fixed-point equation to this framework puts us in an endpoint/boundary case (specifically $s=1, q=2$ via the dual norm $\|A\|_{1 \to 2}$ mapping, violating $1 < q \le s < \infty$) where the paper's strict theorem assumptions do not directly hold, requiring caution when applying the results.

  > [!NOTE]
  > **Nonlinear Operator Norm Localization ($s=1, q=2$):**
  > In the $1 \to 2$ operator norm ($s=1, q=2$) endpoint regime, the maximizing vector does not concentrate around the uniform vector; instead, it localizes entirely on the highest-degree hubs (columns of $A$ with maximum $\ell_2$ norm). This hub localization mathematically explains why targeted seeding of hubs is highly effective and how the transition boundary shifts under degree heterogeneity.

---

## 4. Edge Cases and Technical Constraints

* **Hub Failure Probability Saturation:**
  Under the decided baseline model, the fear failure probability $f_i g_t$ is strictly bounded in $[0, 1]$ since both $f_i$ and $g_t$ are bounded in $[0, 1]$. Saturation (activation probability exceeding $1.0$) is only a concern for future degree-dependent extensions (e.g. scaling by degree $d_i$ as $f_i d_i g_t$). In such extensions, the probability must be explicitly clamped via $\min(f_i d_i g_t, 1.0)$ in simulations.
  
  > [!NOTE]
  > **Nonlinearity under Degree Clamping:**
  > Clamping the probability via $\min(f_i d_i g_t, 1.0)$ introduces a sharp, non-differentiable nonlinearity. This breaks the smooth analytical saddle-node bifurcation equations at the hubs, making the takeoff boundary highly sensitive to the exact degree distribution of the hubs.
* **High-Fear Regime and Physical Seed Clamping ($a < r$):**
  The analytical scaling law $a_c(\mu) = a_c(0)(1-\mu)^{r/(r-1)}$ (Decision D-012) predicts that $a_c(\mu) \to 0$ as $\mu \to 1^-$. However, in any physical simulation, the seed size $a$ must be an integer and is bounded by $a \ge r$ to activate the solvency channel directly under critical connectivity. When $\mu$ is high enough that the theoretical threshold $a_c(\mu) < r$, the takeoff physics undergoes a qualitative change: takeoff is no longer a simple saddle-node bifurcation of the deterministic mean-field map from $a \ge r$. Instead, it is governed by the probability that a subcritical fear-only branching process (with offspring number $\mu < 1$, starting from a small seed $a < r$) survives long enough to generate at least $r$ total failures to activate the solvency channel.
* **Numerical Boundary Guards for Beta Distribution:**
  When generating $f_i \sim \text{Beta}(\alpha, \beta)$ under extreme parameters (e.g. $\mu \to 0$ or $\mu \to 1$), the parameters can cause numerical issues or degeneracies. In our C++ and Python engines, write-guards must clamp parameters or handle these degenerate cases cleanly (as logged in `docs/LESSONS_LEARNED.md`).
* **Sub-macroscopic Transition Limit:**
  Janson's martingale method relies on sub-macroscopic generation sizes ($o(n)$). When the cascade transitions to a macroscopic systemic event ($\Theta(n)$), these assumptions break down. Analytical limits must not extrapolate the sub-macroscopic clock collapse into the macroscopic cascade phase.
