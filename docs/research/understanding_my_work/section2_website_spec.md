# Build Spec: "Two-Channel Reformulation of Janson §2" — Static Web Page

**Prepared for:** Google AI Lab  
**Project:** TwoCascade — A Two-Channel Cascade Model of Bank Failure  
**Author:** Gary Mei (Georgia Tech ISyE)  
**Date:** 2026-06-29  

---

## 1. What This Page Is

A single static web page that presents a mathematically rigorous, self-contained rewrite of
Section 2 ("A Useful Reformulation") from Janson, Łuczak, Turova & Vallier (2012) — adapted to
incorporate a second, global "fear" failure channel. The page is for the author's own study and
reference. It presents the **author's two-channel model as the primary object** (not a side-by-side
comparison), with two optional overlay modes toggled by the reader.

**What this page must NOT do:**
- Call any external API (no Gemini API, no OpenAI, no anything)
- Require a server or build step
- Use any JavaScript framework (React, Vue, etc.)

---

## 2. Technical Requirements (non-negotiable)

| Requirement | Detail |
|---|---|
| **Deliverable** | A downloadable `.zip` file containing all assets |
| **Static only** | Pure HTML + CSS + JS — opens directly in a browser from disk (`file://`) |
| **No API calls** | Zero network requests except MathJax CDN (see below) |
| **Math rendering** | MathJax 3.x, loaded from `https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js` |
| **No frameworks** | Plain JS (ES6 ok). No jQuery, React, Vue, etc. |
| **File structure** | Modular — see §3 |
| **Browser support** | Chrome/Firefox/Safari latest. No IE. |

### MathJax configuration (copy this exactly)

```html
<script>
MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']],
    tags: 'ams'
  },
  chtml: { scale: 0.95 }
};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js" async></script>
```

---

## 3. File Structure

```
section2-reformulation/
├── index.html      ← page structure and all mathematical content (inline)
├── style.css       ← all visual styling, including toggle-activated states
└── script.js       ← toggle logic only (~30 lines)
```

**Rationale for keeping content in `index.html`:** MathJax must parse LaTeX that lives in the
DOM at load time. Putting math in a separate JS data file requires manual typesetting calls and
breaks the clean load order. All math stays in HTML; all presentation is in CSS; all behavior is
in JS. Strict separation of concerns within this constraint.

---

## 4. The Toggle System

Two independent toggles appear in a fixed control bar at the top of the page.

### Toggle A — Annotation Mode

| State | Behavior |
|---|---|
| **OFF (default)** | Clean unified narrative. No colors, no status chips. Reads like a math paper. |
| **ON** | Each content block gains a colored left border and a status chip in its top-right corner, categorized by the block's mathematical status relative to Janson's original. |

**Implementation:** Toggle adds/removes the class `annotated` on `<body>`. All annotation
styling is gated behind `body.annotated` in `style.css`, so zero JS is needed beyond the class
toggle. MathJax does not need to re-render.

### Toggle B — Audience Mode

| State | Behavior |
|---|---|
| **OFF (default — "raw")** | Open-gap and conjecture blocks show direct labels: *"OPEN GAP — not yet attempted"* |
| **ON ("advisor")** | Same blocks show positioned academic language: *"Tier 2 — scope decision: pursue direct fear-field concentration proof or defer to write-up (open Q)"* |

**Implementation:** Toggle adds/removes the class `advisor-mode` on `<body>`. Each gap/conjecture
block contains two sibling `<span>` elements: `.label-raw` and `.label-advisor`. CSS hides the
inactive one based on body class.

### Control bar HTML (reference implementation)

```html
<div id="control-bar">
  <label class="toggle-wrap">
    <span class="toggle-label">Annotation Mode</span>
    <input type="checkbox" id="toggle-annotation">
    <span class="toggle-slider"></span>
  </label>
  <label class="toggle-wrap">
    <span class="toggle-label">Advisor Mode</span>
    <input type="checkbox" id="toggle-audience">
    <span class="toggle-slider"></span>
  </label>
</div>
```

```js
// script.js — complete toggle logic
document.getElementById('toggle-annotation').addEventListener('change', e => {
  document.body.classList.toggle('annotated', e.target.checked);
});
document.getElementById('toggle-audience').addEventListener('change', e => {
  document.body.classList.toggle('advisor-mode', e.target.checked);
});
```

---

## 5. Status Taxonomy

Every content block in the page carries a `data-status` attribute. The six valid values and
their visual treatment (active only when `body.annotated`):

| `data-status` | Chip label | Left border color | Background tint | Meaning |
|---|---|---|---|---|
| `unchanged` | UNCHANGED | `#6b7280` (gray) | `#f9fafb` | Carried over from Janson verbatim |
| `modified` | MODIFIED | `#d97706` (amber) | `#fffbeb` | Janson object adapted with stated reason |
| `new` | NEW MACHINERY | `#2563eb` (blue) | `#eff6ff` | Entirely new construct with no Janson analog |
| `tier1` | TIER 1 — PROVED | `#059669` (green) | `#f0fdf4` | Exact finite-$n$ result, proven rigorously |
| `tier2` | TIER 2 — CONJECTURE | `#7c3aed` (purple) | `#faf5ff` | Mean-field conjecture, simulation-validated |
| `gap` | OPEN GAP | `#dc2626` (red) | `#fef2f2` | Not yet derived; structure only |

### Block HTML pattern

```html
<div class="math-block" data-status="modified">
  <span class="status-chip"></span>  <!-- chip text injected by CSS attr() or JS -->
  <!-- mathematical content here -->
  <!-- for gap/tier2 blocks also include: -->
  <p class="audience-label">
    <span class="label-raw">OPEN GAP — not yet attempted.</span>
    <span class="label-advisor">Tier 2 — scope decision: pursue direct fear-field 
      concentration proof or bound in write-up (open Q, §9 Q1).</span>
  </p>
</div>
```

Chip text can be injected via a small JS loop at load that reads `data-status` and sets
`innerText` on `.status-chip`, or via CSS `content: attr(data-status)` with a lookup table
— either approach is fine.

---

## 6. Page Layout

```
┌─────────────────────────────────────────────────────┐
│  [sticky control bar — Annotation toggle | Audience toggle]  │
├─────────────────────────────────────────────────────┤
│  Page title + one-paragraph purpose statement        │
│  Key: how to read the status chips (shown/hidden     │
│       based on annotation toggle)                    │
├─────────────────────────────────────────────────────┤
│  §1  FIFO Generational Tracking                      │
│  §2  Dynamic Fear Field & Uniform Coupling           │
│  §3  Reconciled Node Activation Times                │
│  §4  Asymptotic Decoupling & Independent Limit       │
│     §4.1  Geometric-Fear Clock Collapse              │
│     §4.2  Joint Decoupling (Exact, Tier 1)           │
│     §4.3  Gap to Unconditional Independence          │
│     §4.4  Bridge to Janson Tangency                  │
│  §5  Limiting Cases & Reductions                     │
│  Appendix  Companion Mapping Table                   │
└─────────────────────────────────────────────────────┘
```

Navigation: a small sticky sidebar TOC (desktop) or a `<details>` TOC (mobile) with anchor
links to each section.

Typography: serif body (e.g. `Georgia` or system-serif), `font-size: 1.05rem`,
`line-height: 1.75`, `max-width: 780px`, centered. This matches the feel of a math paper.

---

## 7. Section-by-Section Content Specification

Each subsection below lists: the **source** (which document to pull from), the **equations**
to include, and the **`data-status`** for each block.

> **Source documents** (provided separately):
> - `janson_reformulation_with_fear.md` — the primary source for all mathematical content
> - `companion_mapping.md` — drives status labels and the Appendix table
> - `rewrite_section2.txt` — supplementary context for the narrative prose

---

### §1 — Sequential Edge-Exposure with FIFO Generational Tracking

**Source:** `janson_reformulation_with_fear.md` §2  
**Companion mapping rows:** 1

**Opening prose block** `[data-status="modified"]`  
Explain that Janson's original §2 explicitly discards generations for clean martingale analysis.
This model restores them via a FIFO queue because the fear field $g_k$ is intrinsically
round-indexed. State that the equivalence between the two orderings is not asserted but proved
(see Pathwise Equivalence Theorem below).

**Definitions block** `[data-status="modified"]`  
Define the three tracking sets:
- $\mathcal{A}(t)$: active vertices at step $t$
- $Z(t) = \{u_1, \ldots, u_t\}$: used/processed vertices, $Z(0) = \emptyset$
- $\mathcal{G}_k$: queue of active vertices belonging to generation $k$

**Base case block** `[data-status="modified"]`  
State $\mathcal{A}(0) = \{u_1, \ldots, u_a\}$, $a_0 = a$, $T_0 := a$, $Z(T_0) = \mathcal{A}(0)$,
$\mathcal{G}_0 = \mathcal{A}(0)$.

**Recurrence block** `[data-status="modified"]`  
State $a_k := T_k - T_{k-1}$ ($T_{-1} = 0$), and:
$$\mathcal{G}_k := \{u_t : T_{k-1} < t \leq T_k\}$$
Define the generation tracker $k(t)$ as the unique index satisfying:
$$T_{k(t)-1} < t \leq T_{k(t)} \quad (k(t) = 0 \text{ for } t \leq T_0)$$

**Pathwise Equivalence Theorem block** `[data-status="tier1"]`  
Full theorem statement and proof by induction (three claims: $Z(T_k) = \mathcal{A}_{\text{sync}}(k)$,
$a_k = a_k^{\text{sync}}$, $\mathcal{A}(T_k) = \mathcal{A}_{\text{sync}}(k+1)$).  
Pull from `janson_reformulation_with_fear.md` §2 blockquote verbatim.  
Include the FIFO Note at the end.

---

### §2 — Dynamic Fear Field & Uniform Coupling

**Source:** `janson_reformulation_with_fear.md` §3  
**Companion mapping rows:** 4, 5

**Solvency mark counter block** `[data-status="unchanged"]`  
$$M_i(t) := \sum_{s=1}^t I_i(s), \quad I_i(s) \sim \mathrm{Be}(p) \text{ i.i.d.}$$
State that $M_i(t) \sim \mathrm{Bin}(t, p)$ for $i \notin Z(t)$. Note explicitly: *"The solvency
channel is carried over from Janson verbatim. This block is unchanged."*

**Global fear field block** `[data-status="new"]`  
$$g_k := \frac{a_{k-1}}{n} = \frac{T_{k-1} - T_{k-2}}{n}$$
Determined at the generational boundary step $T_{k-1}$.

**Uniform Coupling block** `[data-status="modified"]`  
Four steps:
1. Draw $f_i \sim \mathrm{Beta}(\alpha, \beta)$ once at $t=0$, $\alpha = \mu\kappa$, $\beta = (1-\mu)\kappa$.  
   Boundary cases: $\mu=0$ → point mass at $0$; $\mu=1$ → point mass at $1$.
2. Pre-draw $U_{i,j} \sim \mathrm{Unif}[0,1]$ i.i.d. for all $i \in V_n$, $j \geq 1$.
3. Fear indicator:
   $$I_i^{\text{fear}}(j) := \mathbf{1}[U_{i,j} < f_i g_j]$$
4. Fear-activated set:
   $$\mathcal{F}(k) := \{i \notin \mathcal{A}(T_{k-2}) \cup \mathcal{S}(k) : I_i^{\text{fear}}(k) = 1\}$$
   Solvency-activated set:
   $$\mathcal{S}(k) := \{i \notin \mathcal{A}(T_{k-2}) : M_i(T_{k-1}) \geq r\}$$
   Generation queue: $\mathcal{G}_k = \mathcal{S}(k) \cup \mathcal{F}(k)$.

Note: step 2 extends $I_i(s)$ to all $(i, s)$ pairs the same way Janson does in his "redundant
variables" extension, but additionally requires pre-drawing $f_i$ and $U_{i,j}$ for the fear
channel.

---

### §3 — Reconciled Node Activation Times

**Source:** `janson_reformulation_with_fear.md` §4  
**Companion mapping rows:** 2, 3, 6, 7

**Activation generation block** `[data-status="modified"]`  
$$K_i' := \min \left\{ k \geq 1 : M_i(T_{k-1}) \geq r \;\text{or}\; \exists j \leq k \text{ s.t. } I_i^{\text{fear}}(j) = 1 \right\}$$

**Activation step block** `[data-status="modified"]`  
Two cases with explicit precedence:
- *Solvency precedence* (if $M_i(T_{K_i'-1}) \geq r$):
  $$Y_i' = \min \{ t \in (T_{K_i'-2},\, T_{K_i'-1}] : M_i(t) \geq r \}$$
- *Fear activation* (if $M_i(T_{K_i'-1}) < r$):
  $$Y_i' = T_{K_i'-1}$$

Include the "Temporal Mapping Note" as a callout: node belonging to generation $k$ because
it is activated by exposures of generation $k-1$.

**Active set recurrence block** `[data-status="modified"]`  
$$\mathcal{A}(T_k) = \mathcal{A}(T_{k-1}) \cup \mathcal{S}(k+1) \cup \mathcal{F}(k+1) = \bigcup_{j=0}^{k+1} \mathcal{G}_j$$

**Stopping condition block** `[data-status="modified"]`  
$$K := \min\{k \geq 0 : a_k = 0\} \implies T_K = T_{K-1}$$

**Final active set block** `[data-status="unchanged"]`  
$$A^* = T_K$$
Structurally identical to Janson's $A^* = T$.

---

### §4 — Asymptotic Decoupling & the Independent Limit

**Source:** `janson_reformulation_with_fear.md` §5  
**Companion mapping rows:** 8, 9, 10, 11, 12, 13, 14

**Coupling preamble block** `[data-status="modified"]`  
Brief prose: at finite $n$, the $Y_i'$ are coupled because $g_j$ depends on generation sizes.
The goal of this section is to characterize the approach to independence as $n \to \infty$.

---

#### §4.1 — Geometric-Fear Clock Collapse

**Source:** `janson_reformulation_with_fear.md` §5 (main body, before §5.1)

**Concentration conjecture block** `[data-status="tier2"]`  
State the Asymptotic Decoupling Conjecture: generation sizes $(a_k)$ concentrate tightly around
the deterministic mean-field trajectory, making fear fields $g_j$ asymptotically deterministic.

*Audience labels for this block:*
- Raw: *"TIER 2 CONJECTURE — simulation-validated but not yet proved."*
- Advisor: *"Tier 2 — Asymptotic Decoupling Conjecture: requires fear-field concentration;
  simulation confirms phase-boundary invariance within ±0.03."*

**Clock collapse block** `[data-status="tier2"]`  
Under the concentration conjecture and $a_k = o(n)$ w.h.p.:
$$\sum_{j=1}^{k(t)} g_j = \sum_{j=1}^{k(t)} \frac{a_{j-1}}{n} = \frac{T_{k(t)-1}}{n} \approx \frac{t}{n}$$

**Marginal survival factorization block** `[data-status="tier2"]`  
Conditional survival probability:
$$P\!\left(Y_i' > t \mid g_1, \ldots, g_{k(t)}, f_i\right)
  \to P(Y_i^{\text{solv}} > t \mid f_i) \prod_{j=1}^{k(t)} (1 - f_i g_j)$$

Under the leave-one-out field (exact at finite $n$, then with the log expansion and clock
collapse approximation):
$$P\!\left(Y_i' > t \mid g_1, \ldots, g_{k(t)}, f_i\right)
  \approx P\!\left(\mathrm{Bin}(t,p) < r\right) \left(1 - \frac{f_i}{n}\right)^t$$

Include the "Step-vs-Generation Clock Note" callout explaining the minor finite-$n$ survival
probability upward bias and why it collapses in the thermodynamic limit.

---

#### §4.2 — Joint Decoupling: Exact Conditional Factorisation (Tier 1)

**Source:** `janson_reformulation_with_fear.md` §5.1  
**Companion mapping row:** 8 (Tier 1 component)

**Setup block** `[data-status="tier1"]`  
Define the leave-$\{i,j\}$-out system on $G \setminus \{i,j\}$. State the coupled probability
space construction. State the exact finite-$n$ joint-survival identity:
$$P(Y_i' > t,\; Y_j' > t) = \mathbb{E}\!\left[P(Y_i' > t \mid \mathbf{g}^{(-i,-j)}, f_i)
  \cdot P(Y_j' > t \mid \mathbf{g}^{(-i,-j)}, f_j)\right]$$

**Pathwise Equivalence Lemma block** `[data-status="tier1"]`  
Lemma statement and proof by induction: on $\{Y_i' > t\} \cap \{Y_j' > t\}$,
$g_k = g_k^{(-i,-j)}$ for all $k \leq k(t)$.  
Include the Converse (event equivalence).

**Conditional Factorisation block** `[data-status="tier1"]`  
$$P(Y_i' > t,\; Y_j' > t \mid \mathbf{g}^{(-i,-j)}, f_i, f_j)
  = P(Y_i' > t \mid \mathbf{g}^{(-i,-j)}, f_i) \cdot P(Y_j' > t \mid \mathbf{g}^{(-i,-j)}, f_j)$$

**Generalisation to $m$-tuples block** `[data-status="tier1"]`  
State invariants (I1) pathwise equivalence, (I2) independence from $S$-private randomness,
(I3) conditional factorisation for any subset $S$ of fixed size $m$. State the proof is
identical to the pairwise case.

**Structural consequence block** `[data-status="tier1"]`  
State the common-noise conditional i.i.d. result: $Y_i'$ are conditionally i.i.d. given the
fear field; the fear field acts as a latent common factor; all inter-node dependence vanishes
conditional on it.

---

#### §4.3 — Gap to Unconditional Independence (Tier 2)

**Source:** `janson_reformulation_with_fear.md` §5.1 "Gap to Unconditional Independence"  
**Companion mapping rows:** 8 (Tier 2 component), 14

**Gap statement block** `[data-status="tier2"]`  
State the two ingredients still needed for unconditional i.i.d.:
1. Fear-field concentration: $\mathbb{E}_f[P(Y_i' > t \mid \mathbf{g}^{(-i,-j)}, f)]$ concentrates around its mean.
2. Leave-out field equivalence: $\mathbf{g}^{(-i)}$ and $\mathbf{g}^{(-i,-j)}$ converge to the same deterministic limit.

*Audience labels:*
- Raw: *"OPEN GAP — concentration proof not yet attempted."*
- Advisor: *"Tier 2 — both sub-questions are aspects of the Asymptotic Decoupling Conjecture.
  The conditional factorisation has sharpened a diffuse conjecture into a precise concentration
  question about the fear-field trajectory."*

**Variance bound pathway block** `[data-status="tier2"]`  
State the covariance decomposition:
$$\mathrm{Cov}\!\left(\mathbf{1}\{Y_i' > t\},\, \mathbf{1}\{Y_j' > t\}\right)
  = \mathrm{Var}_{\mathbf{g}^{(-i,-j)}}\!\left(\mathbb{E}_f[h(t, \mathbf{g}^{(-i,-j)}, f)]\right)
  + \mathrm{Error}_{\text{field}}$$
where $h(t, \mathbf{g}, f) := P(\mathrm{Bin}(t,p) < r) \prod_k (1 - f g_k)$. State: conditional
on concentration, Janson's binomial variance bound (row 14) is recovered.

**S(t) definition gap block** `[data-status="gap"]`  
State explicitly that Janson defines $S(t) := \sum_{i \notin \mathcal{A}(0)} \mathbf{1}\{Y_i \leq t\}$
as a named counting process central to his §2 analysis. In the two-channel model, the analog
exists but its law is not yet characterized — only its mean is derived.

*Audience labels:*
- Raw: *"OPEN GAP — S(t) counting process not yet given a distributional characterization."*
- Advisor: *"Tier 2 — distributional characterization of $S(t)$ deferred; only its mean is
  tractable without concentration. Scope decision for the write-up."*

**Bin distribution gap block** `[data-status="gap"]`  
State that Janson has $S(t) \sim \mathrm{Bin}(n-a, \pi(t))$ from the i.i.d. structure. No
distributional analog exists in the two-channel model (only the mean-field map).

*Audience labels:*
- Raw: *"OPEN GAP — distributional law of S(t) not derived; blocked on Tier 2 concentration."*
- Advisor: *"Tier 2 — follows directly from concentration; not pursued independently."*

---

#### §4.4 — Bridge to Janson Tangency Machinery

**Source:** `janson_reformulation_with_fear.md` §5 "Expectation Over Populations" and "Bridge"

**Jensen's inequality block** `[data-status="modified"]`  
$$P(Y_1 > t) = P\!\left(\mathrm{Bin}(t, p) < r\right) \mathbb{E}_f\!\left[\left(1 - \frac{f}{n}\right)^t\right]$$
Expand via Jensen and the $\varphi = t/n \to 0$ regime near threshold:
$$\mathbb{E}_f\!\left[\left(1 - \frac{f}{n}\right)^t\right] \approx e^{-\mu\varphi + \frac{1}{2}\mathrm{Var}(f)\varphi^2}$$
State the consequence: heterogeneity of $f$ enters only through the second-order fear term;
$\mu = \mathbb{E}[f]$ dominates to first order.

**Self-consistent equation block** `[data-status="modified"]`  
$$\mathbb{E}[A(t)] \approx a + (n-a)\left(1 - P\!\left(\mathrm{Bin}(t,p) < r\right) e^{-\mu\varphi}\right)$$
Setting $\mathbb{E}[A(t)] = t$ and denoting $\varphi = t/n$:
$$(1-\mu)\varphi \approx \frac{a}{n} + \frac{(np\varphi)^r}{r!}$$

**Critical seed scaling law block** `[data-status="tier2"]`  
From the saddle-node tangency of the self-consistent map:
$$a_c(\mu) = (1-\mu)^{r/(r-1)} \, a_c(0)$$
*Audience labels:*
- Raw: *"TIER 2 CONJECTURE — derived from mean-field saddle-node; simulation-confirmed."*
- Advisor: *"Tier 2 — conjectured scaling law from mean-field tangency; validated numerically
  at $n \in \{1000, 2000, 4000\}$, ratios match $(1-\mu)^{r/(r-1)}$ trend."*

---

### §5 — Limiting Cases & Reductions

**Source:** `janson_reformulation_with_fear.md` §6  
**Companion mapping row:** 15

**Purpose prose block** `[data-status="unchanged"]`  
Brief: these two cases verify that every "Modified" row above is an honest generalization.
Switching fear off recovers Janson exactly.

**Case 1: Pure Bootstrap Percolation ($\mu = 0$) block** `[data-status="unchanged"]`  
$f_i \equiv 0$ → $I_i^{\text{fear}}(j) = 0$ everywhere → $\mathcal{F}(k) = \emptyset$ → active
set recurrence collapses to $\mathcal{A}(T_k) = \mathcal{A}(T_{k-1}) \cup \mathcal{S}(k+1)$ →
matches Janson (2.1)–(2.13) exactly. $Y_i' = Y_i$.

**Case 2: Pure Fear-Only Branching ($p = 0$) block** `[data-status="new"]`  
$M_i(t) = 0$ → $\mathcal{S}(k) = \emptyset$ → queue driven solely by $\mathcal{F}(k)$. 
Expected offspring per failure $= \mathbb{E}[f] = \mu < 1$. Population dominated by a subcritical
Galton-Watson branching process; terminates in $o(n)$ steps with $A^* = O(a)$ w.h.p.

---

### Appendix — Companion Mapping Table

**Source:** `companion_mapping.md`

Embed the full correspondence table (15 rows). Columns: `#`, `Janson §2 object`, `Statement`,
`Our analog`, `Status`, `Reason`. Pull the full content verbatim from `companion_mapping.md`.

Style: standard HTML `<table>` with `booktabs`-style CSS (solid top/bottom border,
lighter mid-rule). The `Status` column cell should inherit the color coding from the taxonomy
in §5 (gray/amber/blue/green/purple/red) regardless of the annotation toggle — the table is
always a reference tool.

---

## 8. Visual Style Reference

| Property | Value |
|---|---|
| Font (body) | `Georgia, 'Times New Roman', serif` |
| Font (code/math labels) | `'SFMono', 'Consolas', monospace` |
| Body font size | `1.05rem` |
| Line height | `1.75` |
| Max content width | `780px`, centered |
| Background | `#ffffff` |
| Control bar | Fixed top, `background: #1e293b`, `color: #f8fafc`, `z-index: 100` |
| Control bar height | `52px` |
| Section headings | `font-size: 1.3rem`, `font-weight: 600`, `margin-top: 2.5rem` |
| Math block (annotated) | `border-left: 4px solid <status-color>`, `padding: 1rem 1rem 1rem 1.25rem`, `margin: 1.25rem 0`, `border-radius: 0 4px 4px 0` |
| Status chip | `position: absolute`, `top: 0.5rem`, `right: 0.75rem`, `font-size: 0.65rem`, `font-weight: 700`, `letter-spacing: 0.08em`, `padding: 2px 6px`, `border-radius: 3px` |
| Math block (clean mode) | No border, no background, standard paragraph spacing |

Math blocks should be `position: relative` containers so the status chip can be positioned
inside them.

---

## 9. Deliverable Checklist

Before submitting the zip, verify:

- [ ] Opens correctly from `file://` (no server needed)
- [ ] MathJax renders all equations on first load
- [ ] Annotation toggle switches colors on/off without page reload or MathJax re-render
- [ ] Audience toggle switches gap labels without page reload
- [ ] Both toggles are independent (all four combinations work)
- [ ] Companion mapping table always shows status colors (not gated by annotation toggle)
- [ ] Page is readable on mobile (single-column, TOC collapsed into `<details>`)
- [ ] Zero API calls (check Network tab — only MathJax CDN should appear)
- [ ] All 15 companion mapping rows are present in the Appendix table
- [ ] $\mu=0$ case explicitly states it recovers Janson (2.1)–(2.13)

---

*End of spec.*
