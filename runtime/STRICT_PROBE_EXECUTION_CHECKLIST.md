# Strict Probe Execution Checklist

Use this operationally; canonical research rules remain in the clock/workload/sync protocols.

## Before substantive work
- [ ] read fresh `state/current.json` and master plan
- [ ] reconcile pending records that could change case/probe identity
- [ ] check for any durable `runtime-boundary/*/start.json` without terminal before assuming no active probe
- [ ] resolve unique probe_id/case_id/target/profile
- [ ] create START marker and raw-fetch exact ID/created_at
- [ ] prearm SAME automation at START + target + planned gap; verify RRULE/enabled/DTSTART
- [ ] persist durable `start.json` (probe identity, START, scheduler verification)
- [ ] create/raw-fetch WORK_START immediately before substantive work
- [ ] select semantic generator version; ID-only uniqueness is forbidden

## During work
- [ ] process semantically decision-unique units / justified independent repeats
- [ ] persist batch checkpoints with semantic_unique count and generator version
- [ ] use raw PROGRESS markers for authoritative admission/close elapsed
- [ ] do not close because a finite corpus ended
- [ ] do not use model/local elapsed to declare target/threshold crossing
- [ ] if a harness defect is discovered, correct counts fail-closed and continue with a valid workload source when safe

## Close
- [ ] authoritative progress reaches configured PRE_CLOSE/admission threshold
- [ ] create/raw-fetch PRE_CLOSE
- [ ] stop admitting new substantive work
- [ ] durable close checkpoint/finalization
- [ ] create/raw-fetch END exactly once
- [ ] recompute WORKED, PREARM, PRODUCTIVE_WINDOW, CLOSE_OVERHEAD from raw created_at only
- [ ] validate marker lifecycle ordering

## Terminal truth
- [ ] create-only `terminal.json`; existing identical = idempotent, different = conflict/no overwrite
- [ ] create-only per-probe event; same rule
- [ ] then reconcile mutable projections with fresh-SHA CAS
- [ ] queue pending reconciliation on repeated conflict
- [ ] report raw UTC plus full-date KST display
- [ ] CLEAN_PASS remains PENDING_WAKE until next actual invocation observes continuation

## Promotion quality gate
Clock survival alone is not strict substantive safe-runtime proof. Require valid clock + scheduler/close + sustained semantic work + wake. Longest one-off success never becomes production operating cap by itself.
