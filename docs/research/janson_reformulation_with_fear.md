# Mathematical Reformulation of Janson's Section 2 with the Fear Channel

This document provides a mathematically rigorous reformulation of Section 2 ("A useful reformulation") of Janson, Łuczak, Turova, and Vallier (JŁTV 2012) to incorporate the self-reinforcing, confidence-driven global fear channel.

---

## 1. Introduction and Terminology

To analyze the two-channel bootstrap percolation process on $G(n,p)$, we adapt Janson's sequential edge-exposure formulation. We track the state of the interbank network, where each bank $i \in V_n$ is either *solvent* or *failed* (absorbing). The process is driven by two competing channels:
1. **Solvency Channel (Local):** A solvent bank fails if it has at least $r \geq 2$ failed neighbors in the graph.
2. **Fear Channel (Global):** A solvent bank fails with a probability proportional to the realized rate of failures in the previous generation, scaled by the bank's individual susceptibility $f_i \sim \text{Beta}(\alpha, \beta)$ drawn once at $t=0$.

Janson's original reformulation changes the time scale by exposing edges from one active, unused vertex at a time, discarding the concept of rounds (generations) to enable clean martingale analysis. Because the fear channel is intrinsically round-based, we reconcile the two models by recovering generations from Janson's queue using a First-In, First-Out (FIFO) processing order. We specialize this mathematical analysis to the core theoretical model where the memory window length is $window\_len = 1$ ($g_t = a_{t-1}/n$). Overlapping memory windows of length $X > 1$ (permitted under Decision D-006) would introduce complex dynamic dependencies that violate Janson's clean queue-like generational separation, though the limiting results are expected to be robust to this extension.

---

## 2. Sequential Edge-Exposure with FIFO Generational Tracking

We construct the graph sequentially on a "need-to-know" basis. Let $u_t$ denote the vertex processed at Janson time step $t$. We maintain three sets of vertices:
*   $\mathcal{A}(t)$: The set of *active* (solvency- or fear-activated) vertices up to step $t$.
*   $Z(t) = \{u_1, \ldots, u_t\}$: The set of *used/processed* vertices up to step $t$, with $Z(0) = \emptyset$.
*   $\mathcal{G}_k$: The queue of active vertices belonging to generation $k$.

To preserve the generational boundaries, we enforce a strict **FIFO processing order** on the queue. Let $T_k$ denote the cumulative number of active vertices processed up to the end of generation $k$.

### Base Case ($k = 0$)
Let $\mathcal{A}(0) = \{u_1, \ldots, u_a\}$ be the initial random seed set of size $a_0 = a$.
*   The cumulative count at generation 0 is $T_0 := a$.
*   The used set at step $T_0$ is $Z(T_0) = \mathcal{A}(0)$.
*   The queue of vertices processed in generation 0 is $\mathcal{G}_0 = \mathcal{A}(0)$.

### Recurrence ($k \geq 1$)
For generation $k \geq 1$:
*   The size of generation $k$ is $a_k := T_k - T_{k-1}$ (where $T_{-1} = 0$).
*   The set of vertices processed in generation $k$ is:
    $$\mathcal{G}_k := \{u_t : T_{k-1} < t \leq T_k\}.$$
*   We define the generation tracker function $k(t)$ for any step $t \in \{1, 2, \dots, T_K\}$ as the unique generation index satisfying:
    $$T_{k(t)-1} < t \leq T_{k(t)} \quad (\text{with } k(t) = 0 \text{ for } t \leq T_0).$$

> **Boundary Case:** For steps $t > T_K$ (after the cascade halts at generation $K$ where $a_K = 0$), we set $k(t) = K$ and define the fear fields $g_j = 0$ for all $j > K$.

> **Pathwise Equivalence Theorem:** Under a FIFO queue order, a pathwise equality holds on every realization of the random graph and uniform fear parameters $U_{i,j}$: the set of vertices in generation $k$ in the sequential process ($\mathcal{G}_k$) is identical to the set of new failures in round $k$ of the simultaneous (synchronous) reference engine.
> 
> *Proof:* Let $\mathcal{A}_{\text{sync}}(k)$ be the set of failed vertices at the end of round $k$ in the synchronous model, and let $a_k^{\text{sync}} := |\mathcal{A}_{\text{sync}}(k) \setminus \mathcal{A}_{\text{sync}}(k-1)|$ be the number of new failures in round $k$ (with $\mathcal{A}_{\text{sync}}(-1) := \emptyset$ and $a_0^{\text{sync}} = a$). 
> Let $T_k = \sum_{j=0}^k a_j$, where $a_j = |\mathcal{G}_j|$ is the size of generation $j$ in the sequential process. 
> 
> We prove by induction on $k \geq 0$ that:
> 1. The used/processed set at step $T_k$ equals the synchronous failed set up to round $k$: $Z(T_k) = \mathcal{A}_{\text{sync}}(k)$.
> 2. The generation sizes match: $a_k = a_k^{\text{sync}}$.
> 3. The active set at step $T_k$ equals the synchronous failed set up to round $k+1$: $\mathcal{A}(T_k) = \mathcal{A}_{\text{sync}}(k+1)$.
> 
> **Base Case ($k = 0$):**
> *   By definition, $T_0 = a$. The seed vertices are processed in steps $1, \dots, T_0$, so the used set is $Z(T_0) = \mathcal{A}(0) = \mathcal{A}_{\text{sync}}(0)$. Thus, $a_0 = a = a_0^{\text{sync}}$, verifying claims (1) and (2).
> *   During these steps, the solvency mark counter $M_i(T_0) = \sum_{s=1}^{T_0} I_i(s)$ represents the number of neighbors node $i$ has in the seed set $\mathcal{A}_{\text{sync}}(0)$. A solvent node $i \notin \mathcal{A}_{\text{sync}}(0)$ is solvency-activated in generation 1 if $M_i(T_0) \geq r$, which is the exact solvency condition for round 1 in the synchronous model:
>     $$\mathcal{S}(1) = \{i \notin \mathcal{A}_{\text{sync}}(0) : M_i(T_0) \geq r\}.$$
> *   The fear field at step $T_0$ is $g_1 = a_0/n = a_0^{\text{sync}}/n$. A solvent node $i \notin \mathcal{A}_{\text{sync}}(0) \cup \mathcal{S}(1)$ is fear-activated if $U_{i,1} < f_i g_1$, which is the exact fear activation condition for round 1 in the synchronous model:
>     $$\mathcal{F}(1) = \{i \notin \mathcal{A}_{\text{sync}}(0) \cup \mathcal{S}(1) : U_{i,1} < f_i g_1\}.$$
> *   Thus, the new active set $\mathcal{G}_1 = \mathcal{S}(1) \cup \mathcal{F}(1)$ contains exactly the new failures in round 1 of the synchronous process. The total active set is:
>     $$\mathcal{A}(T_0) = \mathcal{A}(0) \cup \mathcal{G}_1 = \mathcal{A}_{\text{sync}}(0) \cup (\mathcal{A}_{\text{sync}}(1) \setminus \mathcal{A}_{\text{sync}}(0)) = \mathcal{A}_{\text{sync}}(1),$$
>     verifying claim (3).
> 
> **Inductive Step:**
> Assume the inductive hypothesis holds for $k-1$. That is:
> $$Z(T_{k-1}) = \mathcal{A}_{\text{sync}}(k-1), \quad a_{k-1} = a_{k-1}^{\text{sync}}, \quad \mathcal{A}(T_{k-1}) = \mathcal{A}_{\text{sync}}(k).$$
> *   In generation $k$, the FIFO queue order ensures that we process the vertices of generation $k$ in steps $t \in (T_{k-1}, T_k]$, where $T_k = T_{k-1} + a_k$. The queue processed in generation $k$ is:
>     $$\mathcal{G}_k = \mathcal{A}(T_{k-1}) \setminus Z(T_{k-1}) = \mathcal{A}_{\text{sync}}(k) \setminus \mathcal{A}_{\text{sync}}(k-1).$$
>     The used set at step $T_k$ becomes:
>     $$Z(T_k) = Z(T_{k-1}) \cup \mathcal{G}_k = \mathcal{A}_{\text{sync}}(k-1) \cup (\mathcal{A}_{\text{sync}}(k) \setminus \mathcal{A}_{\text{sync}}(k-1)) = \mathcal{A}_{\text{sync}}(k),$$
>     verifying claim (1).
> *   At step $T_k$, all vertices of $\mathcal{A}_{\text{sync}}(k)$ have been processed. The solvency counter $M_i(T_k)$ represents the number of neighbors node $i$ has in $\mathcal{A}_{\text{sync}}(k)$. A solvent node $i \notin \mathcal{A}_{\text{sync}}(k)$ is solvency-activated in generation $k+1$ if $M_i(T_k) \geq r$:
>     $$\mathcal{S}(k+1) = \{i \notin \mathcal{A}_{\text{sync}}(k) : M_i(T_k) \geq r\}.$$
> *   The fear field at step $T_k$ is $g_{k+1} = a_k/n = a_k^{\text{sync}}/n$. A solvent node $i \notin \mathcal{A}_{\text{sync}}(k) \cup \mathcal{S}(k+1)$ is fear-activated if $U_{i,k+1} < f_i g_{k+1}$:
>     $$\mathcal{F}(k+1) = \{i \notin \mathcal{A}_{\text{sync}}(k) \cup \mathcal{S}(k+1) : U_{i,k+1} < f_i g_{k+1}\}.$$
> *   The new queue $\mathcal{G}_{k+1} = \mathcal{S}(k+1) \cup \mathcal{F}(k+1)$ contains exactly the new failures in round $k+1$ of the synchronous process. Thus, $a_{k+1} = a_{k+1}^{\text{sync}}$, verifying claim (2).
> *   The active set at step $T_k$ is:
>     $$\mathcal{A}(T_k) = \mathcal{A}(T_{k-1}) \cup \mathcal{G}_{k+1} = \mathcal{A}_{\text{sync}}(k) \cup (\mathcal{A}_{\text{sync}}(k+1) \setminus \mathcal{A}_{\text{sync}}(k)) = \mathcal{A}_{\text{sync}}(k+1),$$
>     verifying claim (3).
> 
> By induction, the pathwise equivalence holds for all generations $k \geq 0$. $\square$
> 
> *FIFO Note:* While the generational FIFO ordering is necessary to prevent causal violations between rounds, the specific ordering of vertex exposure *within* a single generation does not affect the final set of activations or the sizes of subsequent generations.

---

## 3. Dynamic Fear Field and Uniform Coupling

Let $M_i(t)$ be the solvency mark counter representing the number of neighbors of node $i$ that have been processed up to step $t$:
$$M_i(t) := \sum_{s=1}^t I_i(s),$$
where $I_i(s) \sim \text{Be}(p)$ is the indicator that there is an edge between processed vertex $u_s$ and node $i$. For any node $i \notin Z(t)$, $M_i(t)$ is distributed as $\text{Bin}(t, p)$.

### Global Fear Field
At the generational boundary step $T_{k-1}$, the incremental fear field is determined by the size of the completed generation $k-1$:
$$g_k := \frac{a_{k-1}}{n} = \frac{T_{k-1} - T_{k-2}}{n}.$$

### Uniform Coupling
To define the coupled indicators rigorously on a single probability space:
*   **Base Case Definition:** We define $\mathcal{A}(T_{-1}) := \mathcal{A}(0) = \{u_1, \ldots, u_a\}$ to initialize the recurrences at $k=1$.
1.  Draw individual susceptibility parameters $f_i \sim \text{Beta}(\alpha, \beta)$ once at $t=0$ for all $i \in V_n$, where $\alpha = \mu \kappa$ and $\beta = (1-\mu)\kappa$. At the boundaries $\mu=0$ and $\mu=1$, $f_i$ is a point mass at $0$ and $1$, respectively.
2.  Pre-draw $U_{i,j} \sim \text{Unif}[0,1]$ i.i.d. for all $i \in V_n$ and generations $j \geq 1$.
3.  Define the fear activation indicator of node $i$ at generation $j$ as:
    $$I_i^{\text{fear}}(j) := \mathbf{1}[U_{i,j} < f_i g_j].$$
4.  The set of fear-activated nodes at the transition of generation $k$ is:
    $$\mathcal{F}(k) := \{i \notin \mathcal{A}(T_{k-2}) \cup \mathcal{S}(k) : I_i^{\text{fear}}(k) = 1\},$$
    where the solvency-activated set is:
    $$\mathcal{S}(k) := \{i \notin \mathcal{A}(T_{k-2}) : M_i(T_{k-1}) \geq r\}.$$
*   **Generation Queue:** For $k \geq 1$, the queue of nodes processed in generation $k$ is exactly $\mathcal{G}_k = \mathcal{S}(k) \cup \mathcal{F}(k)$.

---

## 4. Reconciled Node Activation Times

To avoid mixing step-level solvency clocks and generation-level fear clocks, we first determine the activation **generation** $K_i'$ for each node $i \notin \mathcal{A}(0)$:
$$K_i' := \min \left\{ k \geq 1 : M_i(T_{k-1}) \geq r \text{ or } \exists j \leq k \text{ s.t. } I_i^{\text{fear}}(j) = 1 \right\}.$$

The sequential activation step $Y_i'$ is then defined unambiguously by resolving precedence:
*   **Solvency Precedence:** If the solvency counter $M_i(T_{K_i'-1}) \geq r$ (meaning the node accumulated at least $r$ marks from neighbor exposures during generation $K_i'-1$), its activation step is:
    $$Y_i' = \min \{ t \in (T_{K_i'-2}, T_{K_i'-1}] : M_i(t) \geq r \}.$$
*   **Fear Activation:** If $M_i(T_{K_i'-1}) < r$ (which implies $I_i^{\text{fear}}(K_i') = 1$ since the node activated in generation $K_i'$), its activation step is:
    $$Y_i' = T_{K_i'-1}.$$

> **Temporal Mapping Note:** A node belongs to generation $k$ because it is activated by the exposures of generation $k-1$ or the fear field $g_k$ (which depends on the size of generation $k-1$). Hence, its activation step $Y_i'$ falls in the step interval $(T_{k-2}, T_{k-1}]$ when generation $k-1$ is processed.

The active set at step $T_k$ is the union of all processed vertices up to generation $k$ and the queued vertices for generation $k+1$:
$$\mathcal{A}(T_k) = \mathcal{A}(T_{k-1}) \cup \mathcal{S}(k+1) \cup \mathcal{F}(k+1) = \bigcup_{j=0}^{k+1} \mathcal{G}_j.$$

The process halts at generation $K$ where the queue is empty:
$$K := \min\{k \geq 0 : a_k = 0\} \implies T_K = T_{K-1}.$$
The final active set size is $A^* = T_K$.

---

## 5. Asymptotic Decoupling and the Independent Limit

At finite $n$, the variables $Y_1', \dots, Y_{n-a}'$ are coupled because the fear fields $g_j$ depend on the sizes of previous generations.

### Asymptotic Decoupling Conjecture
We conjecture that in the thermodynamic limit ($n \to \infty$), the sequence of generation sizes $(a_k)_{k \geq 0}$ concentrates tightly around its deterministic mean-field trajectory. Consequently, the fear fields $g_j$ behave as deterministic constants.

### Geometric-Fear Clock Collapse
Under this concentration conjecture, assuming the generation sizes are sub-macroscopic ($a_k = o(n)$ w.h.p., which holds near the critical phase boundary), the sum of fear fields up to generation $k(t)$ collapses directly to Janson's step clock:
$$\sum_{j=1}^{k(t)} g_j = \sum_{j=1}^{k(t)} \frac{a_{j-1}}{n} = \frac{T_{k(t)-1}}{n} \approx \frac{t}{n}.$$

For a node $i$ with susceptibility $f_i$, the conditional survival probability factors asymptotically as $n \to \infty$:
$$P\left(Y_i' > t \mid g_1, \dots, g_{k(t)}, f_i\right) \to P(Y_i^{\text{solv}} > t \mid f_i) \prod_{j=1}^{k(t)} (1 - f_i g_j)$$
At finite $n$, this factorization holds exactly if we condition on the fear field $(g_j^{(-i)})_{j \geq 1}$ of the **leave-one-out system** run on the subgraph $G \setminus \{i\}$ (with node $i$ completely removed from the network from the start). Because $i$ is absent in this system, the trajectory of $g_j^{(-i)}$ is strictly independent of $i$'s susceptibility $f_i$, private fear parameters, and incident edges.
On the survival event $\{Y_i' > t\}$, node $i$ has not activated up to step $t$. Consequently, the active and used sets of the actual system are pathwise identical to those of the leave-one-out system up to step $t$, meaning $g_j = g_j^{(-i)}$ holds *exactly* for all $j \le k(t)$.
$$P\left(Y_i' > t \mid g_1^{(-i)}, \dots, g_{k(t)}^{(-i)}, f_i\right) = P(Y_i^{\text{solv}} > t \mid f_i) \prod_{j=1}^{k(t)} (1 - f_i g_j^{(-i)})$$
Using the logarithmic expansion of the product under the leave-one-out field:
$$\sum_{j=1}^{k(t)} \log \left(1 - f_i g_j^{(-i)}\right) \approx -f_i \sum_{j=1}^{k(t)} g_j^{(-i)} \approx -f_i \frac{t}{n} \approx t \log\left(1 - \frac{f_i}{n}\right)$$
This yields the asymptotic decoupling:
$$P\left(Y_i' > t \mid g_1, \dots, g_{k(t)}, f_i\right) \approx P\left(\text{Bin}(t, p) < r\right) \left(1 - \frac{f_i}{n}\right)^t.$$

This decouples the activation times into independent variables $Y_i = \min(Y_i^{\text{solv}}, Y_i^{\text{fear}})$, where $Y_i^{\text{fear}} \sim \text{Geom}(f_i/n)$ is an independent geometric clock.

> **Step-vs-Generation Clock Note:** In the coupled sequential process, fear activations are tested once per generation at the boundaries $T_{k-1}$, whereas the decoupled geometric clock tests fear step-by-step. By Bernoulli's inequality, $(1 - f_i/n)^{a_{j-1}} > 1 - f_i a_{j-1}/n$ for generation size $a_{j-1} > 1$, meaning the step-level geometric clock exhibits a minor finite-$n$ survival probability upward bias relative to the generational clock. However, in the thermodynamic limit where generation sizes are sub-macroscopic ($a_k = o(n)$ w.h.p.), this clock mismatch collapses, and the geometric clock represents the exact asymptotic limit.

### 5.1 Joint Decoupling: Exact Conditional Factorisation

The leave-one-out argument above establishes the marginal survival probability for a single node. We now extend it to the joint survival of multiple nodes, showing that the $Y_i'$ are **exactly conditionally independent given the fear field** — an exact finite-$n$ result requiring no asymptotic assumptions (Tier 1).

#### Exact Joint-Survival Identity

For distinct non-seed nodes $i, j \in V_n \setminus \mathcal{A}(0)$ and any step $t$, define the **leave-$\{i,j\}$-out system**: the FIFO sequential process run on $G \setminus \{i,j\}$ (with both nodes completely removed from the network from the start), producing fear fields $g_k^{(-i,-j)} = a_{k-1}^{(-i,-j)}/n$. 

We couple the two systems on a common probability space by sharing all pre-drawn Bernoulli edge indicators $\{I_\ell(s)\}_{\ell \in V_n, s \geq 1}$ (representing potential network connections) and all fear uniform draws $\{U_{\ell,k}\}_{\ell \in V_n, k \geq 1}$, restricting the leave-$\{i,j\}$-out system to the sub-collection indexed by $V_n \setminus \{i,j\}$.

The unconditional joint survival probability admits the exact finite-$n$ representation:
$$P(Y_i' > t,\; Y_j' > t) = \mathbb{E}\!\left[\,P(Y_i' > t \mid \mathbf{g}^{(-i,-j)}, f_i)\;\cdot\;P(Y_j' > t \mid \mathbf{g}^{(-i,-j)}, f_j)\,\right]$$

where the expectation is over the random leave-out field $\mathbf{g}^{(-i,-j)}$ and the individual susceptibilities $f_i, f_j$. Each factor has the closed form:
$$P(Y_\ell' > t \mid \mathbf{g}^{(-i,-j)}, f_\ell) = P(\text{Bin}(t,p) < r) \prod_{k=1}^{k(t)} \bigl(1 - f_\ell\, g_k^{(-i,-j)}\bigr) \quad \text{for } \ell \in \{i,j\}.$$

Here, the solvency term $P(\text{Bin}(t,p) < r)$ is a marginal probability over node $\ell$'s solvency-edge indicators $\{I_\ell(s)\}_{s=1}^t$, which are independent of the leave-$\{i,j\}$-out field and the susceptibility $f_\ell$. These solvency edges are marginalized out and are not part of the conditioning sigma-algebra.

This identity is the composition of two exact results: a **pathwise equivalence** on the joint survival event, and a **conditional factorisation** from the independence of private randomness.

#### Pathwise Equivalence on Joint Survival

**Lemma.** On the event $\{Y_i' > t\} \cap \{Y_j' > t\}$, the real cascade agrees pathwise with the leave-$\{i,j\}$-out cascade:
$$g_k = g_k^{(-i,-j)} \quad \text{for all } k \leq k(t).$$

*Proof.* By induction on generation $k$. Since $\{Y_i' > t\} \cap \{Y_j' > t\}$ guarantees that neither $i$ nor $j$ has activated up to step $t$, they cannot have activated by solvency or fear up to generation $k(t)$ (since $T_{k(t)} \leq t$).

For the base case $k=1$, since neither $i$ nor $j$ is in the seed set $\mathcal{A}(0)$ (which is required by $i, j \notin \mathcal{A}(0)$), we have $a_0 = a_0^{(-i,-j)}$ and $g_1 = g_1^{(-i,-j)}$.

For the inductive step, suppose the cascades agree through generation $k-1$: the set of processed vertices matches ($Z(T_{k-1}) = Z^{(-i,-j)}(T_{k-1})$) and all generation sizes match. In generation $k$:
- **Solvency.** For any $\ell \neq i, j$: the solvency counter $M_\ell(T_{k-1})$ counts exposed edges from $Z(T_{k-1})$ to $\ell$. Under our coupling, the edge indicators $I_\ell(s)$ are identical across both systems for all $s \le T_{k-1}$. Since $Z(T_{k-1}) = Z^{(-i,-j)}(T_{k-1})$ by the inductive hypothesis, and neither $i$ nor $j$ is in $Z(T_{k-1})$, the mark counts are pathwise identical: $M_\ell(T_{k-1}) = M_\ell^{(-i,-j)}(T_{k-1})$. Since $t \ge T_{k(t)} \ge T_k$, the survival event guarantees $i, j \notin \mathcal{S}(k)$, so the set of newly solvency-activated nodes satisfies $\mathcal{S}^{(-i,-j)}(k) = \mathcal{S}(k)$.
- **Fear.** The field $g_k = g_k^{(-i,-j)}$ by the inductive hypothesis. For any $\ell \neq i, j$: under the coupling, the uniform draw $U_{\ell,k}$ is identical in both systems. Thus, the fear indicator $I_\ell^{\text{fear}}(k) = \mathbf{1}[U_{\ell,k} < f_\ell g_k]$ is pathwise identical. The survival event guarantees $i, j \notin \mathcal{F}(k)$, so the set of newly fear-activated nodes satisfies $\mathcal{F}^{(-i,-j)}(k) = \mathcal{F}(k)$.

Therefore, the active queue members in generation $k$ are identical ($\mathcal{G}_k^{(-i,-j)} = \mathcal{G}_k$), giving $a_k^{(-i,-j)} = a_k$ and $g_{k+1}^{(-i,-j)} = g_{k+1}$. $\square$

**Converse (event equivalence).** The event $\{Y_i' > t,\; Y_j' > t\}$ in the real system is identical to $\{i \text{ survives vs. leave-}\{i,j\}\text{-out}\} \cap \{j \text{ survives vs. leave-}\{i,j\}\text{-out}\}$. 

The forward direction follows directly from the pathwise equivalence lemma above. For the reverse direction: suppose both nodes survive up to step $t$ in the leave-$\{i,j\}$-out cascade. We prove by induction on $k \leq k(t)$ that the real cascade matches the leave-out cascade pathwise: since neither node has activated in either system, the solvency counts and fear activations remain identical at each step, ensuring no discrepancy can arise. Since they survive in the leave-$\{i,j\}$-out cascade, they must also survive in the pathwise-identical real cascade. $\square$

#### Conditional Factorisation

Since $i$ and $j$ are absent from the leave-$\{i,j\}$-out system, the fields $\mathbf{g}^{(-i,-j)}$ are **strictly independent** of the private susceptibilities $f_i, f_j$, the uniforms $\{U_{i,k}\}_{k \geq 1}, \{U_{j,k}\}_{k \geq 1}$, and the solvency edge indicators $\{I_i(s)\}_{s \geq 1}, \{I_j(s)\}_{s \geq 1}$.

Conditional on $\mathbf{g}^{(-i,-j)}$ and $(f_i, f_j)$, node $i$'s survival depends only on $\{I_i(s)\}_{s=1}^t$ and $\{U_{i,k}\}_{k=1}^{k(t)}$; node $j$'s survival depends only on $\{I_j(s)\}_{s=1}^t$ and $\{U_{j,k}\}_{k=1}^{k(t)}$. These are disjoint collections of mutually independent random variables (by the Uniform Coupling, §3). Therefore:
$$P(Y_i' > t,\; Y_j' > t \mid \mathbf{g}^{(-i,-j)}, f_i, f_j) = P(Y_i' > t \mid \mathbf{g}^{(-i,-j)}, f_i) \cdot P(Y_j' > t \mid \mathbf{g}^{(-i,-j)}, f_j). \qquad \square$$

#### Generalisation to $m$-Tuples

The argument extends immediately. For any fixed $m$ and any subset of non-seed nodes $S = \{i_1, \ldots, i_m\} \subseteq V_n \setminus \mathcal{A}(0)$, define the leave-$S$-out system on $G \setminus S$, coupled by restricting the edge exposures and uniform draws to $V_n \setminus S$. The following invariants hold exactly for any finite $n > |S| + a$:

**(I1) Pathwise equivalence on joint survival.** On the joint survival event $\bigcap_{i \in S} \{Y_i' > t\}$:
$$g_k = g_k^{(-S)} \quad \text{for all } k \leq k(t).$$

**(I2) Independence from $S$-private randomness.** The leave-$S$-out trajectory $\mathbf{g}^{(-S)}$ is independent of $\{f_i, U_{i,k}, I_i(s) : i \in S,\; k \geq 1,\; s \geq 1\}$.

**(I3) Conditional factorisation.**
$$P\!\left(\bigcap_{i \in S} \{Y_i' > t\} \;\middle|\; \mathbf{g}^{(-S)}, (f_i)_{i \in S}\right) = \prod_{i \in S} P\!\left(Y_i' > t \;\middle|\; \mathbf{g}^{(-S)}, f_i\right).$$

*Proof.* Identical to the pairwise case. Under the coupled probability space, no node in $S$ activates, so the real cascade restricted to $V_n \setminus S$ is pathwise identical to the leave-$S$-out cascade (I1). The leave-$S$-out fields are independent of all $S$-private randomness (I2) since $S$ is absent from the system. Conditional on $\mathbf{g}^{(-S)}$ and the susceptibilities, each node's survival depends on its own disjoint set of independent random variables (I3). $\square$

#### Structural Consequence: Common-Noise Conditional i.i.d.

Invariant (I3) establishes that the activation times $Y_i'$ are **conditionally i.i.d. given the fear field**. The fear field acts as a latent common factor: once it is fixed, all inter-node dependence vanishes. By vertex-exchangeability of $G(n,p)$ and the i.i.d. draws of $f_i$, the conditional marginal distributions are identical across non-seed nodes. This "common-noise" structure is exact at finite $n$ and holds for any fixed $m$.

Note that the conditioning field $\mathbf{g}^{(-S)}$ depends on the specific choice of subset $S$. Therefore, while any fixed $m$-tuple is conditionally independent given its own leave-$S$-out field, establishing a single, universal conditioning field for the entire population requires the Tier 2 leave-out field equivalence (i.e., that all $\mathbf{g}^{(-S)}$ concentrate around the same deterministic limit). Additionally, seed nodes $\mathcal{A}(0)$ do not participate in this conditional i.i.d. structure, as they are deterministically activated at step 0.

#### Gap to Unconditional Independence (Tier 2)

The exact joint-survival identity expresses $P(Y_i' > t,\; Y_j' > t)$ as an expectation over the random leave-out field. For this to equal $P(Y_i' > t) \cdot P(Y_j' > t)$, two additional ingredients are needed:

1. **Fear-field concentration.** The random variable $\mathbb{E}_f[P(Y_i' > t \mid \mathbf{g}^{(-i,-j)}, f)]$ (viewed as a function of the random field $\mathbf{g}^{(-i,-j)}$) must concentrate around its mean. Without concentration, the expectation of the product does not factorize, as the shared random field introduces residual positive correlation.
2. **Leave-out field equivalence.** The marginal $P(Y_i' > t)$ uses the leave-$i$-out field $\mathbf{g}^{(-i)}$, while the joint probability uses the leave-$\{i,j\}$-out field $\mathbf{g}^{(-i,-j)}$. These fields must converge to the same deterministic limit as $n \to \infty$.

Both are aspects of the **Asymptotic Decoupling Conjecture** (Tier 2). However, the conditional factorisation has sharpened the conjecture from a diffuse "activation times decouple" statement into a precise concentration question about a single well-defined random object — the fear-field trajectory.

> **Pathway to the variance bound (companion_mapping row 14).** The conditional factorisation suggests that pairwise covariances satisfy:
> $$\text{Cov}\bigl(\mathbf{1}\{Y_i' > t\},\; \mathbf{1}\{Y_j' > t\}\bigr) = \text{Var}_{\mathbf{g}^{(-i,-j)}}\!\bigl(\mathbb{E}_f[h(t, \mathbf{g}^{(-i,-j)}, f)]\bigr) + \text{Error}_{\text{field}},$$
> where $h(t, \mathbf{g}, f) := P(\text{Bin}(t,p) < r) \prod_k (1 - f g_k)$, and the error term accounts for the field mismatch between the leave-$\{i,j\}$-out field $\mathbf{g}^{(-i,-j)}$ and the individual leave-one-out fields $\mathbf{g}^{(-i)}, \mathbf{g}^{(-j)}$ used in the marginals. The variance bound $\text{Var}(S(t))$ thus reduces to the same fear-field concentration targeted by the Asymptotic Decoupling Conjecture. Conditional on concentration, Janson's binomial variance bound (row 14) is recovered.

### Expectation Over Populations and Jensen's Inequality
Aggregating survival across the population yields:
$$P(Y_1 > t) = P\left(\text{Bin}(t, p) < r\right) \mathbb{E}_f \left[ \left(1 - \frac{f}{n}\right)^t \right].$$

By Jensen's inequality, $\mathbb{E}_f[(1-f/n)^t] \ge (1-\mu/n)^t$ since $(1-f/n)^t$ is convex in $f$. We resolve the gap near the phase transition boundary (where the critical step $t_c = o(n)$ implies the failed fraction $\varphi = t/n \to 0$ as $n \to \infty$; note that the scaling exponent $\alpha < 1$ in the Janson connectivity regime $p_n = \beta n^{-\alpha}$ guarantees $t_c \sim n^{(r\alpha - 1)/(r-1)} = o(n)$) by expanding the expectation:
$$\mathbb{E}_f \left[ \left(1 - \frac{f}{n}\right)^t \right] \approx \mathbb{E}_f \left[ e^{-f \varphi} \right] \approx \mathbb{E}_f \left[ 1 - f \varphi + \frac{1}{2} f^2 \varphi^2 \right] = 1 - \mu \varphi + \frac{1}{2} \mathbb{E}[f^2] \varphi^2 \approx e^{-\mu \varphi + \frac{1}{2} \text{Var}(f) \varphi^2}.$$

This shows that near the threshold, the heterogeneity of $f$ enters only through the second-order fear term $\frac{1}{2}\mathbb{E}[f^2]\varphi^2$. The deviation from the homogeneous case is proportional to the variance since $\mathbb{E}[f^2] = \mu^2 + \text{Var}(f)$. Near the critical boundary, the first-order mean individual fear $\mu = \mathbb{E}[f]$ dominates the phase transition to leading order.

*Solvency vs. Second-Order Fear Domination:* Note that while the second-order fear term scales as $\varphi^2$ and has the same power as the solvency term $\frac{(np\varphi)^2}{2}$ for $r=2$, in the connectivity regime $\alpha < 1$ the mean degree $np \to \infty$ as $n \to \infty$. Quantitatively, at the critical threshold, the leading first-order terms scale as $(np)^{-r/(r-1)}$ while the second-order fear correction scales as $(np)^{-2r/(r-1)}$. Since $np \to \infty$, the ratio of the second-order fear correction to the leading solvency terms is:
$$\frac{O((np)^{-2r/(r-1)})}{O((np)^{-r/(r-1)})} = O((np)^{-r/(r-1)}) \to 0 \quad \text{as } n \to \infty$$
Thus, for $r=2$, the solvency term dominates the second-order fear term in the thermodynamic limit. For $r > 2$, the solvency term $\frac{(np\varphi)^r}{r!}$ dominates the second-order fear term because the fear channel's higher-order terms are concave near the origin, meaning only the convex solvency $\varphi^r$ term can drive the saddle-node bifurcation. Thus, for all $r \ge 2$, only the mean individual fear $\mu = \mathbb{E}[f]$ determines the critical saddle-node boundary to first order.

### Bridge to Janson Tangency Machinery
Using independent $Y_i$ variables, we analyze the drift of the active set size $U(t) = A(t) - t$:
$$\mathbb{E}[A(t)] \approx a + (n-a) P\left(Y_1 \leq t\right) = a + (n-a) \left( 1 - P\left(\text{Bin}(t, p) < r\right) \mathbb{E}_f\left[\left(1 - \frac{f}{n}\right)^t\right] \right).$$

Setting the mean-field drift to zero ($\mathbb{E}[A(t)] = t$) and denoting $\varphi = t/n$ yields the self-consistent equation:
$$\varphi \approx \frac{a}{n} + \left(1 - \frac{a}{n}\right) \left( 1 - P\left(\text{Bin}(t, p) < r\right) e^{-\mu \varphi} \right).$$

Using $P(\text{Bin}(t, p) < r) \approx 1 - \frac{(np\varphi)^r}{r!}$ and approximating $e^{-\mu \varphi} \approx 1 - \mu\varphi$ yields:
$$\varphi \approx \frac{a}{n} + \frac{(np\varphi)^r}{r!} + \mu\varphi \implies (1-\mu)\varphi \approx \frac{a}{n} + \frac{(np\varphi)^r}{r!}.$$

Finding the saddle-node tangency of this map (setting the map equal to $\varphi$ and its derivative to $1$) yields the critical seed size scaling law:
$$a_c(\mu) = (1-\mu)^{r/(r-1)} a_c(0).$$

---

## 6. Limiting Cases and Reductions

We verify that the reformulated model reduces to the correct boundaries:

### Case 1: Pure Bootstrap Percolation ($\mu = 0$)
When $\mu = 0$, the individual fear draws $f_i$ collapse to point masses at $0$. This implies $I_i^{\text{fear}}(j) = 0$ for all $i$ and $j$.
*   The activation generation reduces to $K_i' = \min \{ k \geq 1 : M_i(T_{k-1}) \geq r \}$, and $Y_i' = \min \{ t \geq 1 : M_i(t) \geq r \} = Y_i$.
*   The active set recurrence becomes $\mathcal{A}(T_k) = \mathcal{A}(T_{k-1}) \cup \mathcal{S}(k+1)$.
*   This matches Janson's original equations (2.1)–(2.13) exactly.

### Case 2: Pure Fear-Only Branching ($p = 0$)
When $p = 0$, $M_i(t) = 0$ for all $t$, meaning solvency activations cannot occur ($\mathcal{S}(k) = \emptyset$).
*   The activation generation reduces to $K_i' = \min \{ k \geq 1 : \exists j \leq k \text{ s.t. } I_i^{\text{fear}}(j) = 1 \}$, and $Y_i' = T_{K_i'-1}$.
*   The queue sizes are governed solely by fear draws $a_k = |\mathcal{F}(k)|$.
*   Since $g_k = a_{k-1}/n$, this process behaves asymptotically like a branching process where each active node in generation $k-1$ infects each solvent node independently with probability $f_i / n$. The expected offspring per failure is $\mathbb{E}[f] = \mu$. Since $\mu < 1$, the population size is pathwise dominated by a subcritical Galton-Watson branching process which terminates in $o(n)$ steps with $A^* = O(a)$ failures w.h.p.
