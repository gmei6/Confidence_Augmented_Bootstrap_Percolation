---
mutability: frozen
type: concept
---

# §4 — Analytical Benchmark (Janson et al. 2012) 🔒 *(reference)*

Janson, Łuczak, Turova & Vallier, *Ann. Appl. Probab.* 22(5), 1989–2047 (arXiv:1012.3535). The
$\mu=0$ case of this project **is** their model; reproducing their threshold is the **code-validation
test (Week 1).**

**Critical quantities (their eqs. 3.1–3.2, 3.12), fixed $r\ge2$:**

$$
t_c := \left(\frac{(r-1)!}{n p^{r}}\right)^{1/(r-1)},\qquad
a_c := \left(1-\frac1r\right) t_c,\qquad
p_c := \left(\frac{(r-1)^{r-1}(r-1)!}{r^{r-1}}\right)^{1/r}\!\!\left(n\,a^{r-1}\right)^{-1/r}.
$$

For $r=2$: $\;t_c = 1/(np^2)$, $\;a_c = 1/(2np^2)$.

**The dichotomy:** for $n^{-1}\ll p\ll n^{-1/r}$, w.h.p. the final active set is either $o(n)$
(subcritical; in fact $A^* < \frac{r}{r-1}a \le 2a$) or $n - o(n)$ (almost percolation). Threshold at
$a = a_c$. Subcritical fraction solves $r\varphi - \varphi^{r} = (r-1)\alpha$ with $\alpha=a/a_c$;
for $r=2$, $\varphi(\alpha)=1-\sqrt{1-\alpha}$. Once $p \gg n^{-1/r}$, any seed $a\ge r$ percolates
completely (the channel is degenerate there). **The interesting solvency physics lives in this
density window** — stay in it.

**How to scale $p$ with $n$ (do NOT hold $p$ fixed while growing $n$):**
choose $p_n = \beta\, n^{-\alpha}$ with $\alpha \in (1/r, 1)$ — e.g. $r=2,\alpha=0.7$;
$r=3,\alpha=0.5$. This keeps $np\to\infty$ and $np^r\to0$. For each $n$, seed at fixed multiples of
the per-$n$ $a_c$ so every $n$ sits the same relative distance from threshold. Holding $p$ fixed makes
large systems trivially easier to ignite and **confounds the finite-size scaling.**

**How the analytical check must be set up (do this, not the naive thing):**
compare the empirical boundary to the **tangency of the combined mean-field map** — a **saddle-node
tangency at an interior unstable fixed point**, *not* "find where $R=1$ at the all-solvent state."
Because the solvency channel is super-linear near zero (slope 0 in the linearization for $r\ge2$) and
fear contributes slope $\mu<1$, the empty state is linearly stable; a critical seed is needed to cross
the barrier.
- *Solvency piece:* with mean degree $c=np$ and failed fraction $\varphi$, a solvent bank has
  $\approx\text{Poisson}(c\varphi)$ failed neighbors, so fails via solvency w.p.
  $\approx (c\varphi)^r/r!$. Set the mean-field map tangent to the diagonal (map $=$ identity **and**
  derivative $=1$); this reproduces $a_c$.
- *Fear piece:* expected new fear-failures $\approx (a_{t-1}/n)\sum_i f_i \approx \mu\, a_{t-1}$ when
  most banks are solvent, i.e. $R_{\text{fear}}\approx\mu$.
- Machinery: Watts (2002) and Gleeson & Cahalane (2007) tree / generating-function recursions —
  implementable numerically by a strong programmer.
