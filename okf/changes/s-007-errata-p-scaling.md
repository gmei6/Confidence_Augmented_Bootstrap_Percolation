---
type: Session Change
title: "S-007: ERRATA: p-scaling / finite-size corrections"
description: "ERRATA: corrections of record for the S-005/S-006 p-scaling claims; BETA frozen at a fixed N_REF."
mutability: append-only
timestamp: 2026-06-03
---

# S-007: ERRATA: p-scaling / finite-size corrections

Verbatim entry migrated from `docs/PROJECT_TRACKER.md` §12 (Session Changelog) on 2026-07-04:

> S-007 | 2026-06-03 | v1.4 | ERRATA — correction of record for two inaccuracies that entered the logs during the F4 / p-scaling work, both now fixed. (A) S-005 and the original §8 framed the ~28% gap between the empirical threshold (≈25.3) and a_c (20) at n=4000 as an "expected finite-np correction" the Janson regime would shrink; this was wrong — a multi-n check showed it is a finite-size effect set by the magnitude of a_c (larger a_c → sharper transition → ratio→1), present in ANY p–n regime, with the bounded-degree and Janson p-forms numerically identical at n=4000. Corrected in live §8/§10 under S-006. (B) S-006 stated the "Janson p_n scaling is applied," but the test then set BETA = TARGET_MEAN_DEGREE / N**(1-ALPHA), pinning BETA to the live N — which cancels ALPHA (P reduces to 10/N) and holds np constant, i.e. the bounded-degree regime in disguise: the FORM of D-004 but not its scaling. Fixed by FREEZING BETA at a fixed reference N_REF (BETA = TARGET_MEAN_DEGREE / N_REF**(1-ALPHA)), so np = BETA·N^(1-ALPHA) grows as N is varied; suite still passes 4/4 (P=0.0025 unchanged at n=4000) and np now grows (≈8→15 over n=2000–16000). Note: append-only S-005/S-006 retain their original wording; this entry is the correction of record. Live-only; no frozen edits; v1.4 unchanged.
