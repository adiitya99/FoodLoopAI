# Decisions Log

Append decisions; do not silently rewrite prior rationale.

## D-001 — SQLite for the first local prototype
- Status: accepted.
- Why: no separate database server or credentials needed.
- Trade-off: not intended for production multi-user workloads.

## D-002 — Deterministic matching before LLM integration
- Status: accepted for initial baseline.
- Why: rules are inspectable and testable.
- Trade-off: no true distance or nuanced needs optimization.
- Revisit only after baseline tests pass and a clear LLM use case is defined.

## D-003 — Human review required
- Status: accepted.
- Why: rules cannot establish food safety, recipient consent, or delivery.
