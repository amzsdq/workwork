# Unit 08 — Timestamp integrity audit

Probe: STRICT-14M-20260923T092741KST

Existing integrity note correctly excludes one non-monotonic historical timestamp from timing inference while preserving append order and artifact-existence meaning.

For the current 14m probe:
- start timestamp is supplied by the automation runtime context and persisted before workload;
- target crossing/close timestamps must be directly observed later, not inferred from commit timestamps;
- Git commit time/order may corroborate write ordering but must not substitute for missing runtime clock points;
- no historical suspect timestamp is used to compute the 14m elapsed duration.

This keeps the new probe independent of the previously identified timestamp-integrity defect.
