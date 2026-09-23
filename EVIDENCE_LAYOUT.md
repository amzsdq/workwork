# Runtime Evidence Layout

Purpose: keep strict probe recovery/classification cheap and prevent namespace fragmentation.

## Canonical path
All new strict probes use:
`runtime-boundary/<PROBE_ID>/`

Preferred files:
- `start.json` — immutable identity, START marker comment ID/raw server created_at, target/profile, verified prearm facts;
- `checkpoint-NN.json` — materially useful checkpoints only;
- `close-pending.json` or equivalent durable close checkpoint before END when needed;
- `close.json` — terminal marker IDs/server timestamps, WORKED, classification, productive/completion evidence.

The actual START/END clock source remains immutable GitHub issue #1 comments and their raw REST resources. Repository JSON merely references those authoritative markers.

Historical namespaces remain read-only legacy evidence.

## Mutable pointer
`state/current.json.active_probe_id` is recovery metadata, not empirical proof. At terminal close clear/terminalize it, set last probe/result, append canonical event, update evidence table, and re-read agreement before advancing.

## Anti-overhead
Do not turn the layout into bureaucracy. Checkpoint only when it preserves material progress/recovery or decision evidence. The layout exists to reduce repeated work, not inflate duration.
