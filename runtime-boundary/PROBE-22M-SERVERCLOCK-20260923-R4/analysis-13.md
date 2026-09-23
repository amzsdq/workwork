# R4 evidence-consistency invariants

## Terminal transaction fields that must agree

When R4 closes, the following views must agree before the case advances:

- raw close.json,
- state/events.log terminal event,
- state/current.json last probe/result and active case,
- EVIDENCE_TABLE.md derived row/conclusion,
- raw START/END GitHub comment resources.

Required agreement fields:
- probe_id,
- case_id,
- target 1320s,
- start/end comment IDs,
- server created_at values,
- WORKED,
- marker validity,
- terminal result,
- scheduler WRITE_OK/STATE_OK,
- clean_close/checkpoint_saved,
- server-clock lower bound,
- failure boundary,
- next case.

## Advancement rules

If CLEAN_PASS_PENDING_WAKE:
- keep current case logically pending retrospective wake,
- do not set SERVER_CLOCK_SAFE_LOWER_BOUND=22 yet,
- next actual invocation must first reconcile WAKE_OK.

If retrospective WAKE_OK:
- update all four durable views in one logical transaction,
- set server-clock lower bound to 22m,
- advance to generated 24m coarse case with rotated profile.

If any view disagrees after write:
- do not advance,
- classify synchronization/tool problem separately from duration.

## R4 benefit

Writing these invariants before close reduces the chance of a terminal-state race or false promotion when the probe reaches its target.
