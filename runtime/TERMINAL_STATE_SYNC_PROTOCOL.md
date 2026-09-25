# Terminal State Synchronization Protocol

Status: CANONICAL
Purpose: eliminate lost terminal evidence, duplicate probes, and shared-projection write conflicts.

## Canonical truth ordering
1. raw GitHub marker REST resources
2. durable per-probe `start.json` for active/incomplete identity
3. immutable per-probe terminal evidence
4. immutable per-probe event record
5. mutable projections: `state/current.json`, `state/events.log`, `EVIDENCE_TABLE.md`

A mutable projection may lag. It never overrides stronger per-probe evidence.

## Active/incomplete probe rule
After START raw verification and scheduler prearm, persist `runtime-boundary/<PROBE_ID>/start.json` before or at the earliest safe checkpoint. If `start.json` exists and no `terminal.json` exists, treat that probe as ACTIVE/INCOMPLETE even when stale `state/current.json` says `active_probe_id=null`.

Before launching any new strict probe:
1. inspect pending reconciliation records;
2. inspect the current-case probe directory/start records;
3. if an unterminated durable start exists, reconcile/continue/classify it instead of launching a duplicate;
4. never infer “no active probe” from a mutable null field alone.

## Immutable terminal write — CREATE ONLY
At terminal classification create exactly once:
- `runtime-boundary/<PROBE_ID>/terminal.json`
- then `state/events/<PROBE_ID>.json`

Do not update/replace either immutable path. If it already exists, fetch it: semantically identical content is an idempotent retry; differing content is `IMMUTABLE_TERMINAL_CONFLICT`. Preserve existing content, write reconciliation evidence, never silently merge/overwrite.

## Mutable projection reconciliation
For `state/current.json`: fresh SHA -> recompute from immutable truth -> update; on 409 re-fetch/reconcile/retry up to 3; never regress a newer probe/generation.

For `state/events.log` and `EVIDENCE_TABLE.md`: derived projections only; append/render only if probe_id absent. On repeated conflict, create `state/reconciliation/<PROBE_ID>.json` with `PENDING_PROJECTION_RECONCILE`.

Projection conflict is bookkeeping NON_DURATION_FAIL only; it does not invalidate raw terminal evidence or change duration-boundary classification.

## Completion semantics
Empirical terminal truth is durable once immutable terminal + per-probe event exist and agree. Projection sync may finish later. Before a new strict probe, reconcile pending records first; never re-run a completed probe merely because a projection lagged.

## Single-writer / idempotency
Only the active invocation for a probe may originate its immutable terminal/event. Retries compare-and-accept-identical, never overwrite. Shared mutable projections use CAS and may be reconciled later.

## Recovery classification — distinct immutable disposition
A later recovery invocation may originate a distinct recovery disposition only when all of the following are freshly verified:
1. verified start identity exists by exactly one of these modes:
   - `CONTEMPORANEOUS_START_ARTIFACT`: durable per-probe `start.json` exists; or
   - `VERIFIED_RAW_START_RECONSTRUCTION`: a canonical reconciliation artifact explicitly records `contemporaneous_start_artifact=false`, and its raw START comment id + `created_at` are freshly reverified against authoritative GitHub marker history;
2. the normal immutable terminal and event are absent;
3. raw marker history and the probe reconciliation record have been freshly read; and
4. the original invocation can no longer continue.

The recovery actor does not become, and must not impersonate, the original active invocation.

Recovery ordering is CREATE ONLY:
1. `runtime-boundary/<PROBE_ID>/recovery-disposition.json`
2. `state/recovery-events/<PROBE_ID>.json`
3. mutable projection reconciliation

The recovery disposition must reference only raw START/WORK_START/PROGRESS/PRE_CLOSE/checkpoint identifiers and timestamps that actually exist. It must record `terminal_marker_observed=false` and use the non-pass status `INTERRUPTED_ORPHANED_RECONCILED`.

It must also record `start_evidence_mode`, `contemporaneous_start_artifact`, `reconciliation_path`, `reconciliation_blob_sha`, `raw_start_comment_id`, and `raw_start_created_at`. Under `VERIFIED_RAW_START_RECONSTRUCTION`, `contemporaneous_start_artifact` MUST be `false`; the reconciliation source must explicitly state that it is not retroactive terminal evidence. This mode establishes recovery bookkeeping identity only: it does not assert that `start.json` existed contemporaneously and is not terminal or duration evidence. Any mismatch between the reconstruction and freshly read raw START id/timestamp is `RECOVERY_START_IDENTITY_CONFLICT`; create no recovery disposition.

A recovery disposition MUST NOT synthesize an END marker, END identifier, END timestamp, target-duration elapsed value, PASS/CLEAN_PASS, substantive-pass claim, or qualifying duration-boundary evidence. It is recovery/bookkeeping truth, not empirical duration terminal evidence, and never advances the runtime lower bound.

If a recovery disposition or recovery event already exists, fetch and compare it. Semantically identical content is an idempotent retry. Differing content is `IMMUTABLE_RECOVERY_CONFLICT`; preserve the existing immutable object and reconcile explicitly.

