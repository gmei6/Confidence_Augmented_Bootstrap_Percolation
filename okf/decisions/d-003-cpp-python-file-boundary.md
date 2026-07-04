---
type: Decision
mutability: append-only
timestamp: 2026-06-03
---

# D-003: Fork E1: standalone C++ executable + file I/O

Verbatim entry migrated from `docs/PROJECT_TRACKER.md` §11 (Decision Log) on 2026-07-04:

> D-003 | 2026-06-03 | Resolved engineering fork E1: C++↔Python boundary = (a) standalone C++ executable + file I/O — Python writes config/args, C++ writes raw per-realization outcomes to results/raw/, Python reads them back. Reject pybind11 for now; keep it as a stretch/second-iteration polish layer (§6). Build the C++ core as a library (graph/rng/engine) with a thin main.cpp CLI wrapper so a pybind11 binding can be added over the same core later without a rewrite. | Boundary crossing is tiny and infrequent (scalars in, compact outcomes out, once per cell — no hot data path), so pybind11's in-memory advantage is moot here; (a) is far easier to debug with standard C++ tooling (gdb/ASan/valgrind), maps trivially to PACE array jobs for the 10^6–10^7-run critical-window study, and makes the §5.4 same-graph cross-language check a natural file dump. pybind11's gains are mainly résumé-oriented and can be layered on later; owner is new to C++, so debuggability/maintainability win. | §5.1, §9, §10
