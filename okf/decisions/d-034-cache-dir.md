---
type: Decision
title: "D-034: okf/cache/ established for LLM-derived reference material"
description: "New top-level okf/cache/ directory for AI-generated study/reference notes on external sources, distinct from references/'s bibliography stubs."
mutability: append-only
timestamp: 2026-07-08
tags: [okf-convention, mutability-taxonomy]
---

# D-034: okf/cache/ established for LLM-derived reference material

**Decision.** A new top-level directory, `okf/cache/`, is established to hold LLM-derived
reference/study material about external sources (e.g., a textbook's sections page-mapped to
specific code locations) — content generated once by an agent and worth reusing without
re-deriving it in a future session. `okf/cache/index.md` and every file within `okf/cache/` are
`mutability: live`. The directory is general-purpose, not limited to any one source.

**Rationale.** `okf/references/` already exists for §13-style bibliography stubs (title, canonical
URL/citation, one paragraph) and shouldn't be stretched to also hold heavier derived artifacts —
that blurs a citation index with working notes. `cache/` is `live`, not `append-only`: unlike
`decisions/`/`changes/` (audit trails that must never be rewritten, only superseded — see D-032),
a cache of derived facts should be corrected in place when a page number or code line reference
is found wrong or drifts after a refactor. Append-only would force every correction to pile up as
a new file, defeating the point of a cache.

**Affects.** New directory `okf/cache/` (+ `index.md`); root `okf/index.md` (new bullet);
`.agents/skills/edit-okf/SKILL.md` (Directory-Level Conventions, mutability legend). Supersedes
nothing. Approved by Gary on 2026-07-08.
