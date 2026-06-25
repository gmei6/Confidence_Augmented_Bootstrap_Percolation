# Companion Mapping: Janson §2 ("A Useful Reformulation") ↔ Two-Channel Reformulation

**Affects:** Q1 (analytical scope / Tiered Stance, D-009). **Status:** living document, Phase 1 (correspondence table) complete; Phases 2–4 (break-point narrative, rigor ledger, notation appendix) outstanding — see Open Items below.

**Purpose:** Walk through Janson, Łuczak, Turova & Vallier's (2012) Section 2 equation-by-equation and state, for each object, whether our two-channel reformulation (`docs/research/janson_reformulation_with_fear.md`) carries it over **unchanged**, **modifies** it with a stated reason, or required **new machinery**. This makes the Tiered Stance (D-009) legible at the resolution an advisor working directly in this literature will want, and is meant to double as scaffolding for the Wk-10 write-up.

**Sources:**
- Janson, Łuczak, Turova & Vallier, *Ann. Appl. Probab.* 22(5), 1989–2047 (arXiv:1012.3535) — extracted in full at `docs/research/janson_paper/BOOTSTRAP_PERCOLATION_ON_THE_RANDOM_GRAPH.md`; §2 spans lines 60–129, equations (2.1)–(2.13).
- Our reformulation: `docs/research/janson_reformulation_with_fear.md`.
- Background notes: `docs/research/understanding_janson/section_2.md`.

---

## Correspondence Table

| # | Janson §2 (JŁTV) | Statement | Our Analog (`janson_reformulation_with_fear.md`) | Status | Reason |
|---|---|---|---|---|---|
| 1 | Prose, lines 62–68 (before 2.1) | Sequential node-by-node edge exposure; "forget the generations." | §2, FIFO generational queue ($\mathcal{G}_k$, $T_k$) | **Modified** | Janson explicitly discards rounds for clean martingale analysis. We must restore them via a FIFO queue, since the fear field $g_k$ is intrinsically round-indexed. Justified rigorously by the Pathwise Equivalence Theorem (§2), not just asserted. |
| 2 | (2.1)–(2.2) | $T:=\min\{t\ge0:\mathcal{A}(t)\setminus Z(t)=\emptyset\}=\min\{t\ge0:A(t)\le t\}$ | §4: $K:=\min\{k\ge0:a_k=0\}\implies T_K=T_{K-1}$ | **Modified (re-indexed)** | Same stopping logic ("queue empties"), restated at the generation level since we now track two clocks (step $t$, generation $k$). |
| 3 | (2.3) | $A^*:=A(T)=\lvert\mathcal{A}(T)\rvert=\lvert Z(T)\rvert=T$ | §4: $A^*=T_K$ | **Unchanged** | Pure outcome-level definition; doesn't depend on which channel produced a given failure, so it transfers untouched. |
| 4 | (2.4) | $M_i(t)=\sum_{s=1}^tI_i(s)$, $I_i(s)$ i.i.d. $\mathrm{Be}(p)$ | §3: "$M_i(t):=\sum_{s=1}^tI_i(s)$" | **Unchanged (verbatim)** | The solvency channel is untouched by the fear extension; reused exactly, including $M_i(t)\sim\mathrm{Bin}(t,p)$. |
| 5 | Prose, line 86 (the "redundant variables" extension) | Extend $I_i(s)$ to all $i\in V_n,\,s\ge1$ on one probability space, with a fallback vertex-selection rule. | §3 "Uniform Coupling," steps 1–4 | **Modified** | Same purpose, but must additionally pre-draw $f_i\sim\mathrm{Beta}(\alpha,\beta)$ and i.i.d. $U_{i,j}$ to extend the *fear* indicator $I_i^{\text{fear}}(j)$ the same way Janson extends $I_i(s)$. |
| 6 | (2.5) | $Y_i:=\min\{t:M_i(t)\ge r\}$ | §4: $K_i'$ (activation generation) and $Y_i'$ via an explicit precedence rule | **Modified** | Janson has one channel, one clock — no reconciliation needed. We must explicitly arbitrate between a step-indexed solvency clock and a generation-indexed fear clock. |
| 7 | (2.6) | $\mathcal{A}(t)=\mathcal{A}(0)\cup\{i\notin\mathcal{A}(0):Y_i\le t\}$ | §4: $\mathcal{A}(T_k)=\mathcal{A}(T_{k-1})\cup\mathcal{S}(k+1)\cup\mathcal{F}(k+1)$ | **Modified** | The update now unions *two* disjoint activation mechanisms ($\mathcal{S}$ solvency, $\mathcal{F}$ fear) instead of one criterion $\{Y_i\le t\}$. |
| 8 | (2.7) | $Y_i\sim\mathrm{NegBin}(r,p)$, and **i.i.d.** across $i$ | §5 marginal identity + §5.1 conditional factorisation (I1)–(I3) | **Partially resolved** | **Central break point, now sharpened.** The $Y_i'$ are **conditionally i.i.d. given the fear field** — proven exactly at finite $n$ for any $m$-tuple via the leave-$m$-out construction (Tier 1). Unconditional i.i.d. remains Tier 2: it requires (a) fear-field concentration and (b) leave-out field equivalence (both aspects of the Asymptotic Decoupling Conjecture, now formulated as a precise concentration question about the fear-field trajectory). |
| 9 | (2.8) | $S(t):=\sum_{i\notin\mathcal{A}(0)}\mathbf{1}\{Y_i\le t\}$ | Not explicitly named; implicit in the $\mathbb{E}[A(t)]$ derivation (§5) | **Gap — not yet made explicit** | Same counting-process role, but since the underlying indicators aren't exactly independent, $S(t)$ itself has no rigorously characterized law in our model — only its *mean* is derived. Should be defined explicitly even if only its mean is tractable. |
| 10 | (2.9) | $A(t)=A(0)+S(t)$ | §5: $\mathbb{E}[A(t)]\approx a+(n-a)P(Y_1\le t)$ | **Modified** | Same decomposition (seed + new activations), but only holds *in expectation* — Janson's version is a pathwise identity, ours is not. |
| 11 | (2.10) | $S(t)\sim\mathrm{Bin}(n-a,\pi(t))$ | — | **Gap — not derived** | No distributional claim exists for $S(t)$ in the combined model, only the mean-field map. |
| 12 | (2.11) | $\pi(t):=P(Y_1\le t)=P(\mathrm{Bin}(t,p)\ge r)$ | §5: $P(Y_1\le t)=1-P(\mathrm{Bin}(t,p)<r)\,\mathbb{E}_f[(1-f/n)^t]$ | **Modified** | Direct generalization, augmented by the fear-survival factor averaged over the $f$-population. Reduces exactly to Janson's $\pi(t)$ at $\mu=0$ (§6 limiting case — confirms the generalization is honest). |
| 13 | (2.12) | $\mathbb{E}S(t)=(n-a)\pi(t)$ | §5, line 172: $\mathbb{E}[A(t)]\approx a+(n-a)P(Y_1\le t)$ | **Modified** | Structurally identical, using the generalized $\pi(t)$ from row 12. |
| 14 | (2.13) | $\mathrm{Var}\,S(t)=(n-a)\pi(t)(1-\pi(t))\le\mathbb{E}S(t)\le n\pi(t)$ | §5.1 covariance via conditional factorisation | **Reduced to concentration — Tier 2** | The conditional factorisation (§5.1) suggests that pairwise covariances are controlled by the variance of the conditional survival probability viewed as a function of the random fear field. The variance bound thus reduces to fear-field concentration — the same object targeted by the Asymptotic Decoupling Conjecture. No longer an unstructured gap: conditional on concentration, Janson's binomial variance bound is recovered. |
| 15 | All of §2 (validation) | — | §6: $\mu=0$ reduces exactly to (2.1)–(2.13); $p=0$ reduces to a subcritical Galton-Watson branching process | **Unchanged (sanity check)** | Confirms every "Modified" row above is an honest generalization, not a silent redefinition — switching fear off recovers Janson exactly. |

---

## What This Surfaces

- **Rows 1–7, 12–13, 15** are solid: either unchanged or modified-with-proof (row 1 is covered by the Pathwise Equivalence Theorem; row 15 validates the rest).
- **Row 8 is the crux — now partially resolved.** Janson's i.i.d. structure is what the fear channel breaks, but §5.1 proves that the $Y_i'$ are **conditionally i.i.d. given the fear field** (Tier 1, exact at finite $n$). Unconditional i.i.d. is sharpened from a diffuse conjecture into a precise fear-field concentration question (Tier 2).
- **Row 14 is reduced to the same concentration question** as row 8. The conditional factorisation provides a structural pathway: pairwise covariances are controlled by the variance of the conditional survival probability viewed as a function of the random fear field. This is no longer an unstructured gap.
- **Rows 9 and 11 remain open gaps**, not yet attempted.

## Open Items (next passes on this document)

1. **Notation reconciliation appendix** — side-by-side glossary of Janson's symbols vs. ours (most already share notation by design, but $\bar{\mathcal{A}}(t)$, $Z(t)$ vs. $\mathcal{G}_k$ deserve an explicit note).
2. **Rigor ledger** — tag each row with its Tiered-Stance tier (proven lemma / conjecture+mean-field / simulation-only) for a single-glance summary.
3. **Expanded break-point narrative** — a few paragraphs unpacking row 8 in full (why locality is what Janson's proof needs, and exactly how the leave-one-out trick repairs it asymptotically but not exactly).
4. **Row 14 variance bound** is structurally resolved conditional on the Asymptotic Decoupling Conjecture (see §5.1). Whether to pursue a direct proof of fear-field concentration (which would promote both row 8 and row 14 to Tier 1) remains a stretch-item decision for the final write-up.
