---
type: Decision
mutability: append-only
timestamp: 2026-07-02
---

# D-029: §4 display-math block reformatted

Verbatim entry migrated from `docs/PROJECT_TRACKER.md` §11 (Decision Log) on 2026-07-04:

> D-029 | 2026-07-02 | Reformatted the §4 critical-quantities display-math block (t_c, a_c, p_c) as a standalone $$ ... $$ block (blank line before/after, delimiters alone on their own lines); no mathematical content changed. | The block previously opened $$ mid-paragraph on the same line as preceding prose, continued for two more lines with no $ delimiters at all on the middle line, and closed with $$ on the third — unlike every other $$ block in the file (§3.2 line 103, §3.3 line 111), which is self-contained on one line. Because no blank line separated the block from the preceding sentence, it was parsed as one soft-wrapped paragraph rather than a distinct math block, so several renderers (including GitHub's) failed to recognize it and rendered the raw LaTeX as literal text. Logged per §14 rule 4 as a minimal edit to a 🔒 section, even though it is formatting-only (cf. D-018's precedent for minimal frozen-section edits). | §4
