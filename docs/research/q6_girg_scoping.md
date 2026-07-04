# Q6 Scoping — Geometric Inhomogeneous Random Graph (GIRG)

**Status:** design document for Task P.
**Research question affected:** **Q6** (combining Q4 power-law degrees and Q5 geometric locality).

## 1. Graph model: GIRG
The GIRG assigns each node $i$:
1. A position $x_i \in \mathbb{T}^2$ (unit torus), drawn uniformly at random.
2. A weight $w_i$, drawn from a power-law distribution with exponent $\tau$ and minimum weight $w_{\min}$.

The probability of an edge between $i$ and $j$ is:
$$ \mathbb{P}(i \sim j) = \min\left\{1, \left( \frac{w_i w_j}{n \| x_i - x_j \|^2} \right)^{\alpha_g} \right\} $$
where $\alpha_g > 2$ controls the decay of long-range edges.

## 2. Fear Model Integration
We combine:
- **Degree-dependent fear (Q4):** A node's baseline fear susceptibility $f_i$ depends on its weight $w_i$ using a tilt parameter $\gamma$. Hubs (high $w_i$) can be made more fearful ($\gamma > 0$) or less fearful ($\gamma < 0$).
- **Local fear field (Q5):** The fear field is evaluated over a local radius $\ell$.

The fear update for node $i$ is:
$$ g_t^{(i)} = \frac{\#\{j \in B(x_i, \ell) : j \text{ failed in round } t-1\}}{\#\{j \in B(x_i, \ell)\}} $$
A node fails from fear with probability $f_i \, g_t^{(i)}$.

## 3. Simulation Objectives
- Run simulations to test whether a highly central hub (high weight) positioned in a local geometric neighborhood can cause a global cascade when the fear field is local but highly tilted ($\gamma > 0$).
- Compare duration scaling and remote nucleation against global fear baselines.
