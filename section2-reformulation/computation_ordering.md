# Computation Ordering: S(k) and F(k)

> **Note:** `index.html` now defines $\mathcal{S}(k)$ and $\mathcal{F}(k)$ using the background set
> $B_k := \bigcup_{j < k} \mathcal{G}_j$, which makes the exclusion set self-evident. The index-lag
> question this document was written to answer no longer arises in the primary notation. The
> $T_k$-indexed walkthrough below remains valid as the sequential bridge: $B_k = Z(T_{k-1}) =
> \mathcal{A}(T_{k-2})$.

**Question:** Why does the exclusion in $\mathcal{S}(k)$ and $\mathcal{F}(k)$ use $\mathcal{A}(T_{k-2})$ rather than $\mathcal{A}(T_{k-1})$?

**Short answer:** $\mathcal{A}(T_{k-1})$ does not exist yet. It is the *output* of computing $\mathcal{S}(k)$ and $\mathcal{F}(k)$:

$$\mathcal{A}(T_{k-1}) := \mathcal{A}(T_{k-2}) \cup \mathcal{S}(k) \cup \mathcal{F}(k)$$

Using $\mathcal{A}(T_{k-1})$ as the exclusion set would be circular.

---

## General Computation Ordering

```mermaid
flowchart TD
    A["A(T_k-2) = Z(T_k-1) is known\n= all nodes processed through gen k-1\n= A_sync(k-1)"]
    B["Process G_k-1 sequentially\nsteps T_k-2+1 through T_k-1\nUpdate solvency marks M_i(t) for each node exposed"]
    C["Reach boundary T_k-1\nCompute fear field: g_k = a_k-1 / n"]
    D["Solvency scan:\nS(k) = nodes NOT in A(T_k-2) with M_i(T_k-1) >= r"]
    E["Fear scan:\nF(k) = nodes NOT in A(T_k-2) or S(k)\nwith U_ik < f_i * g_k"]
    F["Generation k defined:\nG_k = S(k) union F(k)"]
    G["Active set updated:\nA(T_k-1) := A(T_k-2) union G_k    ← created here, not before"]
    H["Process G_k in steps T_k-1+1 through T_k\nthen repeat for generation k+1"]

    A --> B --> C --> D --> E --> F --> G --> H

```

The exclusion set for both scans is $\mathcal{A}(T_{k-2})$, which equals $Z(T_{k-1})$ — nodes already consumed by the process. The nodes the user was worried about, $\mathcal{G}_k = \mathcal{A}(T_{k-1}) \setminus \mathcal{A}(T_{k-2})$, are not pre-existing; box **G** is where they first appear.

---

## First Generation (k = 1): Concrete Walk-through

For $k = 1$ the indices collapse to:

| General | k = 1 | Meaning |
|---|---|---|
| $\mathcal{A}(T_{k-2})$ | $\mathcal{A}(T_{-1}) = \mathcal{A}(0) = \mathcal{G}_0$ | the seed set |
| $T_{k-1}$ | $T_0 = a$ | last step of processing the seed |
| $g_k$ | $g_1 = a/n$ | fear field from the seed |
| Exclusion | $i \notin \mathcal{G}_0$ | not already in the seed |

**Setup:** $n = 8$, seed $\mathcal{G}_0 = \{1, 2\}$ so $a = 2$, threshold $r = 2$.

Edges touching seed nodes: $3\text{-}1,\ 3\text{-}2,\ 4\text{-}1,\ 4\text{-}2,\ 5\text{-}1,\ 6\text{-}2,\ 7\text{-}2$.

Pre-drawn fear susceptibilities: $f_5 = 0.40,\ f_6 = 0.70,\ f_7 = 0.20,\ f_3 = f_4 = f_8 = 0$.

Pre-drawn fear uniforms: $U_{5,1} = 0.05,\ U_{6,1} = 0.20,\ U_{7,1} = 0.08$.

```mermaid
flowchart TD
    SEED["t = 0  |  Seed established\nA(T_-1) = A(0) = G0 = {1, 2}\nAll other mark counts M_i = 0\nExclusion set = {1, 2}"]

    T1["t = 1  |  Process node 1\nNeighbors: {3, 4, 5}\nM_3: 0 -> 1    M_4: 0 -> 1    M_5: 0 -> 1"]

    T2["t = 2 = T_0  |  Process node 2\nNeighbors: {3, 4, 6, 7}\nM_3: 1 -> 2    M_4: 1 -> 2    M_6: 0 -> 1    M_7: 0 -> 1\nSeed fully processed. Z(T_0) = {1, 2} = A(T_-1). ✓"]

    BOUND["Boundary T_0 = 2\ng_1 = a/n = 2/8 = 0.25"]

    SOL["Solvency scan over nodes NOT in {1, 2}:\nM_3(T_0) = 2 >= 2  ✓\nM_4(T_0) = 2 >= 2  ✓\nM_5(T_0) = 1 < 2   ✗\nM_6(T_0) = 1 < 2   ✗\nM_7(T_0) = 1 < 2   ✗\nS(1) = {3, 4}"]

    FEAR["Fear scan over nodes NOT in {1, 2, 3, 4}:\nNode 5:  U_5,1 = 0.05  vs  f_5 * g_1 = 0.40 * 0.25 = 0.10  → 0.05 < 0.10  ✓\nNode 6:  U_6,1 = 0.20  vs  f_6 * g_1 = 0.70 * 0.25 = 0.175 → 0.20 > 0.175 ✗\nNode 7:  U_7,1 = 0.08  vs  f_7 * g_1 = 0.20 * 0.25 = 0.05  → 0.08 > 0.05  ✗\nF(1) = {5}"]

    GEN1["G_1 = S(1) ∪ F(1) = {3, 4, 5}"]

    UPDATE["A(T_0) := A(T_-1) ∪ G_1\n= {1, 2} ∪ {3, 4, 5} = {1, 2, 3, 4, 5}\nNow process G_1 in steps t = 3, 4, 5  (generation 2 computation begins)"]

    SEED --> T1 --> T2 --> BOUND --> SOL --> FEAR --> GEN1 --> UPDATE

```

---

## Why A(T_{k-1}) Cannot Be the Exclusion Set

After the walk-through above, $\mathcal{A}(T_0) = \{1,2,3,4,5\}$. This is $\mathcal{A}(T_{k-1})$ for $k=1$.

If we had written the definition as $\mathcal{S}(1) := \{i \notin \mathcal{A}(T_0) : \ldots\}$, we would need to know that $\{3,4,5\} \subset \mathcal{A}(T_0)$ *before* computing $\mathcal{S}(1)$ — but $\{3,4,5\} = \mathcal{G}_1$ is produced *by* computing $\mathcal{S}(1)$ and $\mathcal{F}(1)$. The definition would depend on its own output.

The correct exclusion is $\mathcal{A}(T_{k-2})$ because it is the set of already-processed nodes at the moment the boundary scan runs — a fully determined object with no dependency on the current generation's output.
