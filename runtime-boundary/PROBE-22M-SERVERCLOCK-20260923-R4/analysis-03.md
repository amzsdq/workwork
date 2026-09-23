# R4 server-authority instrumentation audit

## Observation

GitHub provides several server-side timestamps during this probe:

- issue-comment `created_at` for START/END markers,
- commit author/committer timestamps for durable repository writes.

Only issue-comment START/END `created_at` is designated by the final invariant as WORKED authority. Commit timestamps are therefore used only as corroboration that substantive repository work occurred after START and as optional productive-window anchors; they never classify target duration.

## Current R4 durable-work anchors

- START marker server time: 2026-09-23T13:58:33Z.
- Sparse checkpoint commit server-side commit metadata: 2026-09-23T13:59:30Z.
- Master-pointer repair commit metadata: 2026-09-23T13:59:52Z.
- Boundary analysis commit metadata: 2026-09-23T14:00:36Z.
- Completion-envelope analysis commit metadata: 2026-09-23T14:00:55Z.

These anchors demonstrate mixed read/write/reconciliation work after START, but they do not establish target completion. END_MARKER remains mandatory.

## Measurement discipline

Direct active_work_sec is still not defensibly separable from connector/tool latency, so it must remain null rather than fabricated. Substantive-unit evidence is preferable until a server-authoritative active-work instrumentation mechanism exists.

## Research implication

The final operating policy should not depend on model-estimated elapsed time. If future admission decisions require elapsed time during a live turn, they should use a server-authoritative observable clock primitive or conservative state derived from such a primitive. This is a Phase C design requirement, not a reason to modify Phase A now.
