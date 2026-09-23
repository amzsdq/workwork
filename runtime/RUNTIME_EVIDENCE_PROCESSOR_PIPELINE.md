# Runtime Evidence Processor — End-to-End Pipeline

## Trust boundary

Strict duration authority is restricted to raw GitHub issue-comment resources for the marker IDs. Repository copies of `created_at`, model/local timestamps, scheduler metadata, and historical `actual_elapsed_sec` are comparison fields only.

## Pipeline

1. Discover probe identities from raw probe files and event ledger.
2. Normalize records without field-wise merging across conflicting duplicates.
3. For current-protocol records with marker IDs, fetch both raw comment resources.
4. Verify fetched comment IDs equal requested IDs and bodies identify the expected probe/case/marker role.
5. Recompute WORKED from raw `created_at`; never repair from recorded elapsed values.
6. Apply causal precedence: explicit independent provider/network/scheduler failure => NON_DURATION_FAIL.
7. Apply clock validity gate.
8. Apply target/result classification.
9. Apply retrospective wake transition separately.
10. Aggregate bounds from eligible terminal records only.
11. Compare derived state against current.json and EVIDENCE_TABLE.md; report diffs, do not silently overwrite evidence.

## Partial-probe reconciliation

- START only: active/incomplete if current invocation is known live; otherwise CLOCK_EVIDENCE_INVALID/abandoned after explicit reconciliation. Never duration fail solely because END is absent.
- END only: CLOCK_EVIDENCE_INVALID.
- Duplicate identical event: idempotent.
- Duplicate conflicting event: anomaly requiring manual/deterministic conflict resolution; never field-wise merge.
- Multiple START or END markers for one probe: require an explicit selected marker pair backed by probe identity; do not choose by convenient duration.

## Marker integrity

A marker pair is valid only if:
- both comment IDs exist;
- both raw resources are fetchable;
- raw IDs match requested IDs;
- bodies contain expected START/END role and same probe_id;
- both raw server `created_at` values parse;
- END >= START.

The current reference classifier accepts normalized authoritative timestamps; a raw-fetch adapter must establish the above integrity before calling it.

## Productive evidence

`active_work_sec` is nullable. `productive_ratio` must be null unless direct active work is defensibly measured. Goal-directed wall-clock windows must remain separately labeled and cannot be silently mapped to active work.

## Boundary aggregation

- CLEAN_PASS_WAKE_OK may advance the coarse server-clock lower bound.
- CLEAN_PASS_PENDING_WAKE does not yet advance it.
- UNDER_TARGET, NON_DURATION_FAIL, CLOCK_EVIDENCE_INVALID and AMBIGUOUS have no boundary effect.
- DURATION_FAIL_CANDIDATE is not a confirmed boundary. Reproduce profile-controlled and bracket against a lower clean class before promotion.

## Completion envelope extraction

For marker-valid clean closes preserve:
- checkpoint_saved;
- clean_close;
- pre-END close sample only when endpoints use compatible trustworthy clocks;
- post-END synchronization separately;
- scheduler prearm verification separately.

Do not infer a close reserve from legacy or incompatible timing domains.

## Concurrency-safe terminal synchronization

The four terminal surfaces are logically one transaction but GitHub file writes are physically separate. Use optimistic concurrency:

1. fetch fresh SHAs for raw terminal evidence, events.log, current.json and EVIDENCE_TABLE.md;
2. write raw terminal evidence first;
3. re-fetch shared files immediately before each replacement write;
4. on SHA conflict, re-read and reconcile; never overwrite a concurrent writer;
5. only declare terminal sync complete after re-reading all four surfaces and checking the same probe/result/bounds/case;
6. if synchronization cannot converge because of provider/tool failure, classify the operational attempt NON_DURATION_FAIL and leave runtime bounds unchanged.

## Migration acceptance gates

Before the processor can become a canonical control component it must:
- reproduce all current server-clock probes exactly;
- detect recorded/recomputed WORKED mismatch;
- reject malformed/reversed/missing marker evidence;
- preserve causal NON_DURATION_FAIL precedence;
- prevent forced-stop + clean-close from becoming PASS;
- reject conflicting duplicate normalized records;
- leave synthetic and legacy records unable to move strict bounds;
- emit deterministic state diffs rather than mutating empirical truth implicitly.
