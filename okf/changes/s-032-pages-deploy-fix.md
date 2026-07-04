---
type: Session Change
mutability: append-only
timestamp: 2026-06-29
---

# S-032: GitHub Pages path-filter deploy fix

Verbatim entry migrated from `docs/PROJECT_TRACKER.md` §12 (Session Changelog) on 2026-07-04:

> S-032 | 2026-06-29 | v1.12 | Logistics-only session. Diagnosed that commit bff403d ("updated viz") deleted viz-temp/ and temp_zip/ but did not touch viz/, so the GitHub Actions path filter (viz/**) did not trigger a Pages redeploy. Resolved by adding a trailing newline to viz/README.md and pushing — confirmed GitHub Pages now reflects the Part A/B walkthroughs from S-031. No code, simulation, or frozen-section changes. | §8, §12
