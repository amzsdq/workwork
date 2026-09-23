# Runtime Evidence Processor — Anomaly Policy

Anomalies must never be silently normalized into stronger empirical evidence.

## Severity
- FATAL_CLOCK: raw marker missing, reversed, wrong probe identity, or raw/persisted timestamp mismatch. No strict promotion.
- CAUSAL_CONFLICT: forced stop + clean close, independent provider failure + duration-failure flag, or mutually exclusive terminal results. Preserve weaker/non-promoting interpretation until reconciled.
- CACHE_MISMATCH: recorded WORKED differs from recomputation. Raw recomputation wins; emit anomaly.
- SUMMARY_DRIFT: current state/evidence table disagrees with raw/ledger classification. Repair derived summary only after raw evidence is verified.
- LEGACY_CONTAMINATION: pre-protocol elapsed value appears in current strict field. Remove from strict aggregation; preserve historical record.

## Boundary behavior
Any unresolved FATAL_CLOCK or CAUSAL_CONFLICT blocks promotion for the affected run. It does not automatically create a failure boundary. Explicit independent non-duration cause prevents duration attribution.

## Repair discipline
Never rewrite immutable marker comments or historical raw events to make summaries agree. Repair derived state/table or append a reconciliation event.
