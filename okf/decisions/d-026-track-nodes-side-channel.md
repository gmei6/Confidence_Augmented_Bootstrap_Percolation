---
type: Decision
mutability: append-only
timestamp: 2026-06-25
---

# D-026: track_nodes diagnostic side-channel in reference.py

Verbatim entry migrated from `docs/PROJECT_TRACKER.md` §11 (Decision Log) on 2026-07-04:

> D-026 | 2026-06-25 | Adds a Python-only diagnostic side-channel (track_nodes/tracked_failure_rounds) in reference.py as a backward-compatible, observational extension; exempts it from §5.4 C++ parity. | The change is strictly additive, observational, backward-compatible, and does not alter cascade dynamics. Exemption is bounded as it does not change the core verification criteria of §5.4 (engine-logic identity at μ=0, statistical agreement of P(systemic) / |A*|/n). Any future reference.py change requires a new standalone instruction. | §5.3, §5.4
