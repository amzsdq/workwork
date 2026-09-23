# R4 pre-close checklist design

When server-authoritative evidence indicates the target class has been reached, execute this checklist without changing the scheduler:

1. Stop admitting new substantive units.
2. Persist a durable close checkpoint identifying R4, target, profile, scheduler verification, substantive-unit summary, and `clock_status=END_PENDING`.
3. Create exactly one END_MARKER in issue #1.
4. Raw-fetch END comment and read server created_at.
5. Compute WORKED = END.created_at - START.created_at.
6. Classify according to marker-valid WORKED and causal outcome.
7. Write close.json with marker IDs/timestamps, WORKED, clean_close/checkpoint_saved, profile, productive metrics only if defensible.
8. Synchronize events.log, state/current.json, EVIDENCE_TABLE.md.
9. Re-read and verify agreement.
10. Leave scheduler pre-arm unchanged.

If target is not actually established from server-authoritative evidence, do not enter this close sequence merely because a local/model clock suggests it.
