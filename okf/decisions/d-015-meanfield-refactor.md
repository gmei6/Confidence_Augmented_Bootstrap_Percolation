---
type: Decision
mutability: append-only
timestamp: 2026-06-06
---

# D-015: Scaling formula moved to meanfield.py

Verbatim entry migrated from `docs/PROJECT_TRACKER.md` §11 (Decision Log) on 2026-07-04:

> D-015 | 2026-06-06 | Move combined seed scaling formula from model.py to meanfield.py and decouple plotting.py. | Resolves structural drift and code duplication between model.py and meanfield.py; plotting.py now imports scaling_ratio directly from meanfield.py. | §5.3
