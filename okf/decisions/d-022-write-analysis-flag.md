---
type: Decision
title: "D-022: Plotting analysis-write gated behind flag"
description: "Analysis-JSON writes in plot_wk3_4.py gated behind --write-analysis; plotting is read-only on analysis artifacts."
mutability: append-only
timestamp: 2026-06-16
---

# D-022: Plotting analysis-write gated behind flag

Verbatim entry migrated from `docs/PROJECT_TRACKER.md` §11 (Decision Log) on 2026-07-04:

> D-022 | 2026-06-16 | Gated the adherence-JSON write + metadata-stamping in scripts/plot_wk3_4.py behind an explicit --write-analysis flag (default off); normal plotting now runs in-memory and only READS results/analysis/*_adherence.json. Restored the three adherence files' analysis_runtime_commit to 283776f to match the note. | A plain plot run had re-stamped analysis_runtime_commit (283776f → current HEAD), desyncing the artifacts from the provenance cited in janson_scaling_validation.md; gating keeps plotting read-only on analysis artifacts while preserving a committed producer path (run with --write-analysis) for §5.6 reproducibility. | §5.3, §5.4, §5.6
