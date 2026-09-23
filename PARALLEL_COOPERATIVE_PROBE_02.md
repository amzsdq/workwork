# Cooperative Parallel Probe 02

probe_id: PARALLEL-A14-B4-02
status: DEFERRED_UNTIL_RUNTIME_BOUNDARY_AND_CAP_VALIDATION

Goal: test simultaneous disjoint useful work with stronger instrumentation. It is never a strict Phase-A duration PASS because its scheduler pattern intentionally differs from the strict runtime protocol.

## Safety/control requirements
- disjoint immutable A/* and B/* namespaces;
- no shared state/authority mutation by B;
- no duplicate work;
- no shared-write or scheduler collision;
- exact scheduler-writer ownership defined before live execution.

## Final-clock requirement
Future exact timing claims (A/B start/end, overlap seconds, wake jitter, active-worker seconds, parallelism factor) require authoritative server-side timestamps for every timing endpoint used. Model-authored timestamp strings in evidence files do not qualify.

Durable ordering may still support qualitative concurrency/control findings, but without authoritative endpoints exact timing metrics remain unresolved.

## Classification
PARALLEL_USEFUL / PARALLEL_CONCURRENT_BUT_LOW_GAIN / CONFLICTED / NOT_CONCURRENT / INCONCLUSIVE.

## Relationship to strict runtime research
Supporting-only. It cannot advance SERVER_CLOCK_SAFE_LOWER_BOUND or establish FAILURE_BOUNDARY. Resume only after Phase A/B gate unless explicitly reprioritized by the user.
