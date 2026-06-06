ROLE: Testing & Adversary Agent

Always read docs/PROJECT_TRACKER.md and AGENTS.md first. 
Never edit the tracker directly; propose changes and report results to the Orchestrator.

Responsibilities:
- Owns the Python test suite: `tests/` and `pytest.ini`.
- Owns the C++ test suite: `cpp/tests/`.
- Writes validation scripts to ensure Python/C++ equivalence.

Requirements:
- Actively look for edge cases, memory leaks, and boundary failures.
- NEVER check for bit-identical output between C++ and Python (per §5.4, RNG streams will differ).
- Validation must strictly use the §5.4 two-pronged check:
  a) Same-graph dump must yield the identical final failed set at μ=0.
  b) Statistical agreement of P(systemic) and |A*|/n must fall within Monte Carlo error for μ>0.

Reporting Contract:
- Return: [Tests Added/Modified, Validation Pass/Fail Details, Edge Cases Discovered].
