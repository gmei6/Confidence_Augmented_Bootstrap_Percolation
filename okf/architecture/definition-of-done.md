---
type: Concept
title: "§5 — Coding Standards & Architecture (5.6: Definition of Done)"
description: "Frozen §5.6 Definition of Done: committed config + logged seed, saved raws, regenerable figure, validation."
mutability: frozen
---

# §5 — Coding Standards & Architecture (5.6: Definition of Done)

### 5.6 Definition of Done (apply to every result)
A deliverable is "done" only when: (1) it is produced by a script from a committed config + logged
seed; (2) raw outputs are saved to `results/raw/`; (3) the figure regenerates from those raw outputs
via `plotting.py`; (4) for anything validatable, the validation passes (e.g. $\mu=0$ reproduces
$a_c$); (5) any result from the C++ core has passed the cross-language check in §5.4 against the
Python reference; and (6) the result is recorded in §8 and, if it resolves a fork, in §11.
