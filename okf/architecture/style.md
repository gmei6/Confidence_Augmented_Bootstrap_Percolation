---
mutability: frozen
type: concept
---

# §5 — Coding Standards & Architecture (5.5: style)

### 5.5 Style
- Small **pure functions**; no hidden global state. The engine takes a graph + params + RNG and
  returns outcomes — it does no I/O and no plotting (true in both languages).
- **Python:** type hints; concise docstrings (what it computes, units, the relevant equation §);
  parameters in a single validated dataclass ($0\le\theta\le1$, $r\ge2$, $p$ in regime).
- **C++:** RAII and value semantics; pass big objects by `const&`, never copy the graph; **CSR**
  adjacency for cache locality (a `vector<vector<int>>` is an acceptable first cut, CSR is the
  optimization); `reserve()` buffers to avoid per-round reallocation; const-correctness; **no shared
  mutable state in the parallel realization loop** (each thread owns its RNG and buffers). Build
  `-O3 -march=native` for runs (dispatched per-arch: `-mcpu=native` on arm64), `-O0 -g
  -fsanitize=address,undefined` for debugging — **except on macOS, where Debug uses UBSan only
  (`-fsanitize=undefined`); ASan deadlocks pre-main on macOS 26.5 / Apple Clang 17 (D-018), so
  full ASan coverage is obtained on Linux (PACE / CI).**
- Optimize only where it aids speed *and* clarity, and **profile before optimizing** — the reason the
  core is C++ is that the cascade loop is the measured hot path, not faith.
