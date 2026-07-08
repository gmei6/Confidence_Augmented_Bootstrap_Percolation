---
type: Decision
title: "D-033: title/description frontmatter added bundle-wide; one-time metadata normalization"
description: "Every okf/ file gains the SPEC's title and description keys; a one-time frontmatter-only edit to append-only files is authorized; five malformed change files repaired; type casing normalized."
mutability: append-only
timestamp: 2026-07-07
tags: [okf-convention, frontmatter, spec-compliance]
---

# D-033: title/description frontmatter added bundle-wide; one-time metadata normalization

**Decision.** Every file in the `okf/` bundle gains the OKF SPEC's optional `title` and `description` frontmatter keys (`title` = the file's H1 text minus emoji and italic annotations; `description` = a one-line summary). To apply this uniformly, a **one-time, frontmatter-only** edit to the `append-only` files (`decisions/`, `changes/`, `log.md`, and their two indexes) is authorized: bodies remain byte-identical; only the frontmatter block changes. Riding along in the same pass: (a) the five malformed `changes/` files from the 2026-07-04 Antigravity sessions are repaired — `s-041`, `s-042`, `s-044`, `s-045` gain the REQUIRED frontmatter block (`type: Session Change`, `mutability: append-only`, `timestamp: 2026-07-04` per git first-commit dates) and `s-043`'s nonstandard `type: change-record` becomes `type: Session Change` with its missing timestamp added; (b) `type` casing is normalized (`concept`→`Concept`, `index`→`Index`, `log`→`Log`) to match the existing `Decision` / `Session Change` / `Reference`. Going forward, every new bundle file includes `title` and `description` at creation, and the append-only rule again binds absolutely, frontmatter included.

**Rationale.** The SPEC (GoogleCloudPlatform/knowledge-catalog `okf/SPEC.md`) treats `title` and `description` as the producer-supplied machine-readable summary layer; adding them makes `session-start` context loading and index maintenance cheaper and less error-prone than parsing H1 headings. The append-only invariant exists to keep the *record* — the narrative content of decisions and session changes — tamper-evident; frontmatter metadata *about* the record is not the record itself, and the five malformed files show the metadata layer needed a repair pass anyway (they violate the SPEC's REQUIRED `type` key). Bounding the exemption to a single audited, body-preserving pass (verified by diffing every body before/after) keeps the tamper-evidence guarantee intact, mirroring the D-032 precedent of correcting a metadata-taxonomy oversight via an explicit decision.

**Affects:** every file in `okf/` (frontmatter only); edit-okf conventions (new-entry template now includes `title` and `description`).
