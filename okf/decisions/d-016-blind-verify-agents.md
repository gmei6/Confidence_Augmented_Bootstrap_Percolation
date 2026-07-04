---
type: Decision
mutability: append-only
timestamp: 2026-06-06
---

# D-016: reviewer/critic/auditor blind verification gate

Verbatim entry migrated from `docs/PROJECT_TRACKER.md` §11 (Decision Log) on 2026-07-04:

> D-016 | 2026-06-06 | Split the single adversarial-review agent into three blind, single-purpose agents — reviewer (design & interface-contract correctness), critic (adversarial tests, boundary/memory, and the §5.4 cross-validation run), auditor (independent §5.6/§5.4 integrity gate, binary PASS/FAIL) — and added a /verify workflow running reviewer→critic→auditor. Also added /self-succession (context-handoff protocol) and /watchdog (subagent-liveness cron, notify-don't-kill). Deleted the old adversarial-review skill and rewired call-sites in /research-cycle (Step 3 → /verify), /plan (red-team → critic), /harden (reviewer+critic per round, auditor gate at convergence), and GEMINI.md. | Ports the high-value primitives from Google Antigravity's teamwork-preview into the human-in-the-loop harness while preserving the propose-don't-write and approval-gate guardrails. Separating review/critique/audit raises code quality and makes "done" gated by an independent check tied to the §5.6 Definition of Done and §5.4 cross-validation (not generic anti-cheating); the auditor must not flag expected C++/Python RNG-stream divergence (§5.4). Self-succession lifts the single-context-window cap on long runs; the watchdog catches stalls (e.g. the Week-2 explorer's pytest-permission timeout) without fighting approval gates. | Agent harness (AGENTS.md/GEMINI.md, .agents/skills, .agents/workflows); verification process for §5.4/§5.6 — no frozen tracker text changed.
