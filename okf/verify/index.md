---
type: Index
title: "Verify"
description: "Criteria consumed by the generic ~/ai verify skill's reviewer/critic/auditor gate."
mutability: live
---

# Verify

Project-specific criteria fed to the generic `verify` skill (`~/ai/skills/verify`) at Step 0.
This replaces `.agents/workflows/verify.md`'s per-role criteria as the source the skill reads;
`.agents/workflows/verify.md` itself is kept for now (flagged in d-007 to possibly thin to a
pointer later) since it also documents the step-loop mechanics that live in the skill now.

- [Reviewer](reviewer.md) - design & interface-contract correctness
- [Critic](critic.md) - adversarial tests, boundary/memory, §5.4 cross-validation
- [Auditor](auditor.md) - §5.6 Definition of Done, binary integrity gate
