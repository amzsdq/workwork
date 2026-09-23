# R8 Schema Consistency Audit

Probe: PROBE-22M-SERVERCLOCK-20260924-R8

Decision-relevant findings from the implementation corpus:

1. The pre-R8 reference classifier accepted timestamp pairs without immutable marker IDs. This was weaker than `GITHUB_SERVER_CLOCK_PROTOCOL.md` and `TIMING_EVENT_SCHEMA.md`. Fixed: normalized strict records now require both marker IDs and timestamps; raw-fetch adapter remains responsible for body/identity verification.

2. The regression dataset omitted marker IDs and R7. Fixed in schema v2; R3/R4/R6/R7 now include immutable IDs and R7=251s UNDER_TARGET is part of the corpus.

3. Duplicate normalized records had no explicit policy. Fixed: exact duplicates collapse idempotently; conflicting duplicates are rejected. Field-wise merge is prohibited because it could fabricate a stronger record.

4. Productive evidence misuse was not surfaced. Fixed: productive_ratio without direct active_work_sec and active_work_sec > WORKED emit anomalies.

5. Failure-candidate aggregation could be misread as a confirmed boundary. The pipeline/acceptance contract now states pure aggregation never confirms a failure boundary; profile-controlled reproduction/bracketing is required.

6. Terminal synchronization is logically transactional but physically multi-file. The pipeline now requires optimistic concurrency and fresh reconciliation after SHA conflict, matching the observed prior conflict mode.

7. Existing canonical state and EVIDENCE_TABLE agree before R8 terminal evidence: server-clock safe lower bound unresolved; failure boundary unresolved; R3/R4/R6/R7 UNDER_TARGET; R5 NON_DURATION_FAIL.

These are implementation/control findings. They do not themselves move runtime bounds.
