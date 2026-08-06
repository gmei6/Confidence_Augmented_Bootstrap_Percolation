---
type: Concept
title: "Verify — Auditor"
description: "§5.6 Definition of Done, binary integrity gate for the verify skill's blind auditor subagent."
mutability: live
---

# Verify — Auditor

Runs an internal-consistency pass on the deliverable first (per the generic `verify` skill), then
verifies the §5.6 Definition of Done (`okf/architecture/definition-of-done.md`) actually holds
from artifacts on disk — not from what the diff or commit message claims. A deliverable is "done"
only when, checked against disk:

1. It is produced by a script from a committed config + logged seed.
2. Raw outputs are saved to `results/raw/`.
3. The figure regenerates from those raw outputs via `plotting.py`.
4. For anything validatable, the validation passes (e.g. $\mu=0$ reproduces $a_c$).
5. Any result from the C++ core has passed the §5.4 cross-language check against the Python
   reference (see `verify/critic.md`).
6. The result is recorded in `okf/status.md` / the relevant change record and, if it resolves a
   fork, in `okf/model/forks.md`.

Also check for laziness or fabrication (claimed tests not run, claimed files that don't exist),
and confirm no `okf/lessons.md` trap was repeated.

**AUDIT FAIL -> the change is not done.** Surface the required-to-pass list and route fixes back
to the owning agents; never override a FAIL. **AUDIT PASS ->** the change is eligible to be
marked done.
