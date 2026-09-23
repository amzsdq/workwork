# Runtime Evidence Processor — End-to-End Pipeline

## Trust boundary
Strict duration authority is raw GitHub marker comment resources. Repository timestamps are audit copies. Workload-quality evidence is separate and cannot repair clock evidence.

## Pipeline
1. Discover probe identity from durable start/terminal/event records.
2. Raw-fetch START/END and verify IDs, roles, probe identity, UTC created_at, ordering.
3. Raw-fetch WORK_START/PRE_CLOSE when productive/completion intervals are claimed; invalid productive ordering fails that interval closed without crashing START/END classification.
4. Normalize without field-wise merge and **preserve target_runtime_sec**.
5. Apply causal NON_DURATION_FAIL precedence, clock validity gate, target/result classification, then retrospective wake transition.
6. Validate workload quality: ID uniqueness is insufficient; semantic/decision uniqueness or justified independent repeat evidence is required for strict sustained-substantive-work promotion.
7. Aggregate only eligible terminal records.
8. Compare mutable projections against immutable truth and reconcile explicitly.

## Partial probe reconciliation
- durable start without terminal: active/incomplete unless explicitly abandoned; missing END alone is never duration failure;
- END only: CLOCK_EVIDENCE_INVALID;
- identical immutable retry: idempotently accepted;
- conflicting immutable same-probe content: IMMUTABLE_TERMINAL_CONFLICT, never overwrite/merge;
- multiple markers: explicit identity-backed selection only, never choose a convenient duration.

## Boundary aggregation
- CLEAN_PASS_WAKE_OK may advance strict lower bound only when clock, close, scheduler, and sustained substantive-work quality gates all pass;
- PENDING_WAKE, UNDER_TARGET, HARNESS_UNDER_TARGET, NON_DURATION_FAIL, CLOCK_EVIDENCE_INVALID, AMBIGUOUS: no promotion;
- DURATION_FAIL_CANDIDATE requires profile-controlled reproduction/refinement;
- a posthoc workload-quality defect can retain clock survival evidence while requiring substantive lower-bound revalidation.

## Terminal synchronization V2
Empirical truth is not a four-file pseudo-transaction.
1. raw marker REST resources;
2. create-only immutable `runtime-boundary/<PROBE>/terminal.json`;
3. create-only immutable `state/events/<PROBE>.json`;
4. mutable `state/current.json`, `state/events.log`, `EVIDENCE_TABLE.md` are projections.

Immutable path retry is compare-and-accept-identical; differing existing content is a conflict and is never overwritten. Mutable projections use fresh-SHA CAS with up to three reconcile retries, then a pending reconciliation record. Projection failure is bookkeeping NON_DURATION_FAIL and does not erase valid terminal truth.

## Active-probe safety
A durable `runtime-boundary/<PROBE>/start.json` without terminal.json is stronger evidence of an active/incomplete probe than a stale mutable `current.json` field saying active_probe_id=null. Reconcile the projection; do not launch a duplicate probe solely from stale null state.

## Migration acceptance gates
Processor must preserve target through classification, reproduce raw WORKED, fail malformed clocks closed, preserve non-duration/forced-stop precedence, reject conflicting duplicates, validate productive-marker ordering without crashing, distinguish semantic from ID uniqueness, and keep synthetic/legacy evidence from mutating empirical bounds.
