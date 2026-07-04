---
type: Session Change
mutability: append-only
timestamp: 2026-07-02
---

# S-039: §4 math-block rendering fixed (D-029)

Verbatim entry migrated from `docs/PROJECT_TRACKER.md` §12 (Session Changelog) on 2026-07-04:

> S-039 | 2026-07-02 | v1.13 | Fixed a §4 markdown rendering bug (D-029): the critical-quantities display-math block ($t_c$, $a_c$, $p_c$) opened `$$` mid-paragraph with no blank line separating it from the preceding sentence, and its middle line (`a_c := ...`) had no `$` delimiters at all — unlike every other $$ block in the file, which is self-contained on one line. Reformatted as a standalone block (blank line before/after, `$$` alone on its own opening/closing line); no mathematical content changed. Frozen edit to §4, minimal per §14 rule 4, logged as D-029. | §4, §11, §12
