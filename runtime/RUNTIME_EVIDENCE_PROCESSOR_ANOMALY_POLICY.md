# Runtime Evidence Processor — Anomaly Policy

Anomalies never silently normalize into stronger evidence.

## Severity / scope
- **FATAL_CLOCK**: START/END raw marker missing, reversed, wrong probe identity, or unresolvable raw mismatch. Exact duration invalid; no strict promotion.
- **PRODUCTIVE_CLOCK_INVALID**: WORK_START/PRE_CLOSE missing/reversed/mismatched. Main START/END WORKED may remain valid, but productive-window/completion claims using the bad interval fail closed.
- **CAUSAL_CONFLICT**: forced stop + clean close, independent failure + duration-failure flag, mutually exclusive terminal states. Preserve weaker/non-promoting interpretation until reconciled.
- **HARNESS_SEMANTIC_DUPLICATION**: workload changes IDs while replaying deterministic semantic cases without independent repeat value. Clock survival remains valid, but sustained-substantive-work promotion is blocked/revalidated.
- **IMMUTABLE_TERMINAL_CONFLICT**: an existing terminal/event path differs from a retry. Never overwrite; preserve existing truth and create reconciliation evidence.
- **CACHE_MISMATCH**: recorded WORKED differs from raw recomputation. Raw recomputation wins; emit anomaly.
- **SUMMARY_DRIFT**: mutable current/table/log disagrees with immutable evidence. Reconcile projection; do not mutate raw truth.
- **LEGACY_CONTAMINATION**: pre-protocol elapsed appears in strict aggregation. Remove from strict aggregation, preserve history.

## Boundary behavior
FATAL_CLOCK, unresolved CAUSAL_CONFLICT, or HARNESS_SEMANTIC_DUPLICATION blocks strict promotion for the affected run but does not create a duration failure boundary. PRODUCTIVE_CLOCK_INVALID blocks only the affected derived interval unless the clean-pass contract specifically requires that interval. Explicit independent non-duration cause prevents duration attribution.

## Repair discipline
Never rewrite immutable GitHub marker comments or immutable terminal/event records to make summaries agree. Append audit/correction evidence and reconcile mutable projections. Posthoc audit may weaken a promotion while preserving independently valid clock-survival facts.
