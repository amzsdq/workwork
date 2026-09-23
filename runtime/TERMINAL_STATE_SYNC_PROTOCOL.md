# Terminal State Synchronization Protocol

Status: CANONICAL
Purpose: eliminate lost terminal evidence and reduce shared-projection write conflicts.

## Canonical truth ordering
1. raw GitHub marker REST resources
2. immutable per-probe terminal evidence
3. immutable per-probe event record
4. mutable projections: `state/current.json`, `state/events.log`, `EVIDENCE_TABLE.md`

A mutable projection may lag. It never overrides immutable probe/event truth.

## Immutable terminal write — CREATE ONLY
At terminal classification **create** exactly once:
- `runtime-boundary/<PROBE_ID>/terminal.json`
- then `state/events/<PROBE_ID>.json`

Do not use update/replace semantics for either immutable path. If either path already exists:
1. fetch it;
2. if content is semantically identical, treat the write as idempotently complete;
3. if content differs, classify `IMMUTABLE_TERMINAL_CONFLICT`, preserve the existing file, write a reconciliation record under `state/reconciliation/<PROBE_ID>-immutable-conflict.json`, and never silently merge/overwrite.

The immutable event contains probe/case identity, classification, raw server marker IDs/timestamps, worked/productive/close metrics, boundary effect, next case, and terminal evidence path.

## Mutable projection reconciliation
### state/current.json
1. fetch latest SHA;
2. recompute desired projection from immutable terminal event(s);
3. update with that SHA;
4. on 409, re-fetch/reconcile/retry up to 3 times;
5. never blind overwrite or regress a newer probe/generation.

### state/events.log and EVIDENCE_TABLE.md
Derived projections only. On 409, re-fetch and append/render only when probe_id is absent; retry up to 3 times. If still blocked, create `state/reconciliation/<PROBE_ID>.json` with `PENDING_PROJECTION_RECONCILE`.

Projection conflict is bookkeeping NON_DURATION_FAIL only; it does not invalidate raw terminal evidence or change duration-boundary classification.

## Completion semantics
Empirical terminal truth is durable once both immutable files exist and agree. Projection synchronization may complete immediately or later. Before a new strict probe, reconcile pending projection records first, but never re-run an already completed probe merely because a projection lagged.

## Single-writer / idempotency rule
Only the active invocation for a probe may originate its immutable terminal/event records. Retries are compare-and-accept-identical, never overwrite. Shared mutable projections use CAS and may be reconciled by a later invocation.
