# Evidence Integrity Note

Observed during the 12-minute boundary probe preparation:

- `state/events.log` contains `BOUNDARY_DECISION_RULE_ADDED` with timestamp `2026-09-22T23:33:14+09:00`.
- A later-appended `PROBE_WORKLOAD_AND_SCHEMA_ADDED` record carries timestamp `2026-09-22T23:00:00+09:00`.
- Because the latter timestamp is non-monotonic relative to append order and was not established as a trustworthy direct clock observation, it must not be used for elapsed-time, idle-gap, WAKE_OK latency, or runtime-boundary inference.

Append order remains preserved. Do not rewrite historical evidence to make timestamps look consistent.

Boundary effect: NONE. The affected record remains valid only as evidence that the workload/schema artifact was added; its timestamp is excluded from timing calculations.

Rule going forward: when event timestamp and durable append order conflict, preserve both, mark timing trust explicitly, and exclude the suspect timestamp from duration calculations unless independently corroborated.