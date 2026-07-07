---
type: Decision
mutability: append-only
timestamp: 2026-07-07
tags: [okf-convention, mutability-taxonomy]
---

# D-032: decisions/index.md and changes/index.md reclassified as append-only

**Decision.** `okf/decisions/index.md` and `okf/changes/index.md` are reclassified from `mutability: live` to `mutability: append-only`. All other `index.md` files in the bundle (`okf/index.md`, `architecture/index.md`, `model/index.md`, `references/index.md`) remain `live`.

**Rationale.** The `decisions/` and `changes/` folders are strictly append-only: entries are sequential, never renamed, never removed, never edited once written. Their two indexes therefore only ever grow by one bullet line per new entry — the same append-only growth pattern as the folders they mirror, not the free-form "overwrite to reflect current truth" semantics `live` implies for e.g. `status.md` or `architecture/index.md` (which do get restructured, entries renamed or removed, over time). Tagging these two indexes `live` was an oversight in the original mutability legend: it permitted edits (reordering, rewording) that the underlying folder's own invariant forbids. Reclassifying them closes that gap — going forward, adding a new `d-NNN`/`s-NNN` entry also appends its index line via `append_okf.py` in the same step, so the index and the folder can never drift out of sync via an out-of-band edit.

Note (raised by Gary, 2026-07-07): a companion question — whether individual decision/change entries should instead be tagged `frozen` rather than `append-only` — was considered and rejected. In this bundle's vocabulary `frozen` is the *weaker* guarantee (editable via a decision-file-first protocol); `append-only` is stricter (no edits, ever — only superseding entries). Since a decision or change record must never be revised after the fact, `append-only` remains correct for individual entries; this decision only touches the two index files.

**Affects.** `okf/decisions/index.md`, `okf/changes/index.md` (frontmatter + permission lock), `.agents/skills/edit-okf/SKILL.md` (mutability legend, steps 2 and 3). Supersedes nothing. Approved by Gary on 2026-07-07.
