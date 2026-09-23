# Terminal State Synchronization Protocol

Status: CANONICAL
Purpose: eliminate lost terminal evidence and reduce 409 conflicts from shared-file writes.

## Canonical truth ordering

1. raw GitHub marker REST resources
2. immutable per-probe terminal evidence
3. immutable per-probe event record
4. mutable projections: state/current.json, state/events.log, EVIDENCE_TABLE.md

A mutable projection may lag. It must never override immutable probe/event truth.

## Immutable terminal write

At terminal classification create/update the unique probe terminal file:

`runtime-boundary/<PROBE_ID>/terminal.json`

Then create the unique append-only event file:

`state/events/<PROBE_ID>.json`

These paths are probe-specific and avoid cross-probe write contention.

The immutable event contains:
- probe_id / case_id
- classification
- server marker IDs/timestamps
- worked/productive/close metrics
- boundary_effect
- next_case
- terminal_evidence_path

Once written, conflicting content for the same probe_id is a reconciliation error; never silently merge.

## Mutable projection reconciliation

### state/current.json
Use optimistic concurrency:
1. fetch latest SHA;
2. recompute desired projection from immutable latest terminal event(s);
3. update with fetched SHA;
4. on 409, re-fetch, reconcile, retry up to 3 times;
5. never blind overwrite.

If the fresh current state already contains a newer terminal generation/probe, do not regress it. Mark the older event as incorporated.

### state/events.log and EVIDENCE_TABLE.md
These are derived projections, not canonical transaction members.

On 409:
- re-fetch;
- append/render only if the probe_id is absent;
- retry up to 3 times;
- if still blocked, write `state/reconciliation/<PROBE_ID>.json` with status=PENDING_PROJECTION_RECONCILE.

A projection conflict is NON_DURATION_FAIL for bookkeeping only. It does not invalidate valid raw terminal evidence and does not change runtime boundary classification.

## Completion semantics

Terminal empirical truth is durable once:
- terminal.json is written, and
- state/events/<PROBE_ID>.json is written.

Projection synchronization may complete immediately or in the next invocation.

Before starting a new strict probe, reconcile any PENDING_PROJECTION_RECONCILE records first, but do not re-run the already completed probe.

## Single-writer rule

Only the active invocation for a probe may write its probe-specific terminal/event files.
Shared mutable projections are CAS-updated and may be reconciled by a later invocation.
