# State contract

`events.log` is canonical append-only truth. Existing event lines are never edited or replaced.

`current.json` is derived state only. If it disagrees with valid canonical events, rebuild it from `events.log`.

Clean-success event fields should stay minimal:
- ts
- result
- work
- next

Only include write/state/wake/duplicate/anomaly/recovery/rollback/boundary details when non-clean, pending, mismatched, or otherwise diagnostically relevant.
