---
type: Decision
title: "D-045: C++ GIRG port merged after full blind gate (AUDIT PASS); BKL level 8 warned-unvalidated"
mutability: append-only
timestamp: 2026-08-04
tags: [cpp, girg, verify, audit-pass]
---

# D-045: girg-cpp-port merged (a2b2596)

**Decision.** The C++ GIRG port (G0-G5.4, 10 commits, +3936/-15) is merged into
antigravity after the complete blind gate: four fresh reviewer rounds with fix
rounds G5.1-G5.4, critic NO MATERIAL BREAKAGE, auditor AUDIT PASS. Gary approved
the diff explicitly. BKL recursion level 8 (n>65536) has no committed test; a
runtime warning fires there (girg.hpp carries the per-level coverage table) and
the critic's probe at n=65537 held. Follow-ups N1-N4 + deferred advisories are
queued as post-merge hygiene, none gate-blocking.

**Rationale.** Unlocks the GIRG densification arms (~50x the Python oracle at
production n, measured and auditor-reproduced) and future large-n frontier
sweeps, with §5.4 parity evidence at production recursion depth (L=7 committed,
L=8 probed). The gate record — including two honest negative results — is in
okf/changes/s-064 and the walkthrough.

**Affects.** cpp/*, src/twocascade/runner.py, tests/*, §5.4 practice for GIRG;
okf/status.md, okf/next-actions.md.
