# Q1 Rigor Assessment: Mathematical Tractability of extending Janson's Theorems

This document assesses the feasibility of establishing a fully rigorous mathematical theory for the two-channel cascade model of bank failure (local solvency channel + self-reinforcing global fear channel) on an Erdős–Rényi random graph $G(n,p)$, scaling under the Janson regime ($np \to \infty$ and $np^r \to 0$ as $n \to \infty$).

## 1. Janson's Proof Machinery (JŁTV 2012)
Janson, Łuczak, Turova, and Vallier (JŁTV 2012) analyze bootstrap percolation on $G(n,p)$ using three key pillars:
1. **Branching Process Coupling**: In the early stages of percolation (when the number of failed nodes is $o(n)$), the transmission of failures through the local network behaves like a branching process. On a sparse random graph $G(n,p)$, the local neighborhood of a node is tree-like with high probability.
2. **Martingale Concentration**: They construct an exposure process where edges are revealed step-by-step. They define a continuous-time version of the process where each edge has an independent exponential lifetime. This allows them to prove that the trajectory of active nodes concentrates tightly around its deterministic mean-field limit.
3. **Saddle-Node Phase Transition**: The critical seed size $a_c$ is derived as the point where the mean-field recursion function is tangent to the identity line. Below this, the process is subcritical and terminates with $A^* = o(n)$ failures. Above it, a cascade occurs, leading to $n - o(n)$ failures.

## 2. Key Theoretical Bottlenecks with the Fear Channel
The introduction of the self-reinforcing global fear channel ($g_t = a_{t-1}/n$, with individual susceptibilities $f_i \sim \text{Beta}(\alpha, \beta)$) breaks several of the core assumptions in the JŁTV proofs:
- **Loss of Locality / Global Coupling**: In bootstrap percolation, a node's state depends *only* on the states of its neighbors (a local rule). Martingale concentration is proved by exposing edges. However, the fear probability $f_i g_t$ depends on $a_{t-1}$, which is the *global count* of failures in the previous round. This means the failure probability of any node depends on the global history of the process, which destroys the tree-like independence of branchings and the standard edge-exposure martingale filtration.
- **Heterogeneous Random Fields**: The individual fear thresholds $f_i$ introduce a second layer of randomness. A proof must show concentration not only over graph realizations (as $n \to \infty$) but also over the realization of the fear parameters drawn from the Beta distribution.
- **Simultaneous Round Update & Discrete Time**: The fear channel probability is defined dynamically based on discrete rounds ($a_{t-1}$). Translating this to continuous time (which JŁTV use heavily for their martingale analysis) is highly non-trivial because the fear field is transient and depends on the instantaneous rate of failures, requiring a memory kernel.

## 3. Plausibly Provable Results (Undergraduate Research Scope)
While a full sharpness proof for the combined model is likely out of scope for a 10-week project without measure-theoretic probability coursework, several intermediate results are mathematically tractable:
- **Heuristic Mean-Field Critical Scaling (The $(1-\mu)^{r/(r-1)}$ Scaling Law)**:
  We can derive the critical seed size scaling analytically using self-consistent equations. 
  Let the final failed fraction be $\varphi = |A^*|/n$. The solvency failure probability for small $\varphi$ is $P_{\text{solv}}(\varphi) \approx \frac{(np\varphi)^r}{r!}$.
  The fear failure probability for small $\varphi$ is $1 - E[e^{-f \varphi}] \approx \mu \varphi$.
  Thus, the self-consistent equation for the final failed fraction is:
  $$\varphi \approx \frac{a}{n} + \frac{(np\varphi)^r}{r!} + \mu \varphi \implies \varphi(1-\mu) \approx \frac{a}{n} + \frac{(np\varphi)^r}{r!}$$
  Finding the saddle-node tangency of this map yields the critical seed size $a_c(\mu)$:
  $$a_c(\mu) = (1-\mu)^{r/(r-1)} a_c(0)$$
  For $r=2$, this predicts $a_c(\mu) = (1-\mu)^2 a_c(0)$. This is a clean, highly non-trivial scaling law that can be stated as a conjecture and verified via simulation.
- **Subcriticality of Fear-Only Channel**: 
  We can rigorously prove that if $p=0$ (no solvency channel), the fear-only process is a subcritical branching process with expected offspring $\mu < 1$, which terminates in $o(n)$ steps with $A^* = O(a)$ with high probability.
- **Bounded Amplification**: 
  We can prove that for any graph, the total number of failures in the two-channel model is stochastically dominated by a process where each solvency failure generates a geometric number of fear offspring with mean $\mu$, yielding a total cascade size bounded by a factor of $1/(1-\mu)$ times the solvency-only cascade size in the subcritical regime.

## 4. Recommended Stance for §2
We recommend falling back to **"Heuristic Mean-Field Validated by Simulation"** as the primary stance, but with a **structured tiered approach**:
1. **Rigorously Prove**: The subcriticality and bounded amplification of the fear-only channel ($p=0$ and the general dominance bound).
2. **Conjecture with Mean-Field Analysis**: The $(1-\mu)^{r/(r-1)}$ scaling law for the critical seed $a_c(\mu)$, showing the derivation.
3. **Verify via Simulation**: The phase boundary, bimodality, and the scaling exponents.

This draws a clean line that keeps the project mathematically honest, achieves a publication-grade analytical insight (the scaling law), and avoids getting bogged down in a multi-month martingale proof.
