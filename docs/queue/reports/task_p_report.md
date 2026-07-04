# Task P (Q6) Simulation Report

Tested whether a highly central hub can cause a global cascade when the fear field is local but highly tilted.

- $n = 2000$
- Hub weight = 216.27
- Hub degree = 1555
- Hub fear = 1.0000
- Local Fear Fraction = 0.0005 (1 rounds)
- Global Fear Fraction = 0.0005 (1 rounds)

Result: With only a single hub as the seed, the cascade does not propagate globally (or even locally) because a single failure only provides $r=1$ failed neighbor to its neighbors, which is less than the solvency threshold $r=2$. The fear failure probability is also too low to trigger fear-based secondary failures. A larger seed set is required to initiate a global cascade.
