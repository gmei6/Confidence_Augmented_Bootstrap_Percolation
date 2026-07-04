---
type: Decision
mutability: append-only
timestamp: 2026-06-11
---

# D-018: macOS Debug = UBSan only; ASan deferred

Verbatim entry migrated from `docs/PROJECT_TRACKER.md` §11 (Decision Log) on 2026-07-04:

> D-018 | 2026-06-11 | macOS Debug builds use UBSan only (-fsanitize=undefined); ASan dropped on macOS and deferred to Linux/PACE/CI. CMakeLists dispatches sanitizer flags on APPLE. Minimal edit made to the §5.5 debug-flags line. | Apple Clang 17's ASan runtime deadlocks before main() on macOS 26.5: re-entrant malloc inside InitializeShadowMemory during dyld shared-cache iteration spins forever on ASan's own init mutex (diagnosed via /usr/bin/sample stack capture; MallocNanoZone=0 ineffective) — every ASan-linked binary hangs at launch, making ASan unusable on this toolchain/OS. UBSan is unaffected and retained. | §5.5
