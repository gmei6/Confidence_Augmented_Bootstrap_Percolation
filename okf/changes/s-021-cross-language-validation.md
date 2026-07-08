---
type: Session Change
title: "S-021: §5.4 cross-language validation completed"
description: "Completed §5.4 cross-language validation (Prongs A and B); §5.5 sanitizer note per D-018."
mutability: append-only
timestamp: 2026-06-11
---

# S-021: §5.4 cross-language validation completed

Verbatim entry migrated from `docs/PROJECT_TRACKER.md` §12 (Session Changelog) on 2026-07-04:

> S-021 | 2026-06-11 | v1.10 | Completed §5.4 cross-language validation: built arm64 Debug+Release, 4/4 C++ unit suites pass both configs; wrote tests/test_cpp_validation.py — Prong A PASS (2 automated cases incl. subcritical r=4 stall + 3 manual instances; failed sets identical to oracle) and Prong B PASS (1000 trials/engine at interior cell P(systemic)=0.22: z-test + KS<0.05); full suite 25/25. Repairs: CMakeLists OpenMP hints moved before find_package (dead appended block removed), per-arch native-flag dispatch kept, .gitignore now build*/. Frozen edit: §5.5 debug-flags line amended per D-018 (macOS Debug = UBSan only; ASan deadlocks pre-main on macOS 26.5/AppleClang 17). Correction of record: S-020 labeled itself v1.10 though no frozen section changed that session (header then still v1.9); the version is properly bumped to v1.10 NOW with this session's §5.5 edit, so the on-disk label sequence stays consistent. | §5.5, §8, §9, §10, §11, §12
