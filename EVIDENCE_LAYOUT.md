# Runtime Evidence Layout

Purpose: stop the namespace fragmentation seen in the historical 18m probes and make crash recovery/classification cheap.

## Canonical path for new runtime probes

For all new strict runtime probes, use one directory:

`runtime-boundary/<PROBE_ID>/`

Preferred files:
- `start.json` — immutable start/prearm facts.
- `checkpoint-NN.json` — useful durable checkpoints only; do not checkpoint every tiny unit.
- `close.json` — terminal timing/classification evidence.

Do not create new strict runtime evidence under the historical namespaces `runtime/`, `runtime/probes/`, `runtime-probes/`, or `runtime-evidence/`. Those remain read-only legacy evidence.

## Mutable pointer

`state/current.json` should carry an `active_probe_id` while a probe is running. This is a recovery pointer, not empirical proof. Raw per-probe evidence remains authoritative.

At terminal close:
- clear or terminalize the active pointer,
- set last probe/result fields,
- append canonical event,
- update derived evidence table,
- re-read and verify agreement before advancing the case.

## Why

Historical 18m evidence is spread across five namespaces and at least 18 prior probe IDs. That makes terminal-close discovery expensive and contributed to repeated start/checkpoint-only attempts. A single canonical path improves:
- crash recovery,
- terminal-decision yield,
- evidence audits,
- duplicate-probe prevention,
- state reconciliation.

## Anti-overhead rule

Do not turn the layout into extra bureaucracy. A normal clean probe should need only start, a small number of materially useful checkpoints, and close. The layout exists to reduce repeated work, not increase write count.
