# Intentional Overlap Probe

Status: HISTORICAL PROTOCOL / CONCURRENCY SUPPORTING EVIDENCE

## Goal
The original probe tested whether the same recurring automation could execute concurrently when a successor wake was scheduled before predecessor close. Its historical classification was CONCURRENT.

## Historical parameters
- probe_id: OVERLAP-15M-WAKE12M-01
- primary nominal target: 15m
- wake offset: 12m
- nominal overlap: 3m
- workload: TEST_GENERATED_MIXED_LOAD
- recurrence: same automation

## Final-clock qualification
The original protocol recorded model/file timestamp strings in immutable artifacts. Under the later `GITHUB_SERVER_MARKER_V1` invariant, those strings are not authoritative exact timing evidence.

Therefore:
- preserve the historical CONCURRENT result as supporting evidence that overlap is technically possible;
- do not promote exact historical overlap seconds, wake lateness, or optimal lead solely from those model/file timestamp strings;
- future quantitative overlap/lead tests must use authoritative server-side timing endpoints for every duration being compared;
- if an endpoint lacks authoritative timing, mark the exact metric unresolved.

## Future evidence model
Continue using independent immutable per-invocation artifacts to avoid concurrent shared-file races. Add authoritative server-clock markers/events for predecessor start/end and, where feasible, server-side evidence for successor wake/READY/transfer/work-start.

## Safety/control rules for future tests
- exactly one ACTIVE_OWNER;
- SHADOW performs no authoritative work or scheduler mutation;
- owner transfer uses generation/CAS fencing on canonical `handoff-state.json`;
- no concurrent append/rewrite race on shared evidence;
- exact timing optimization is deferred until Phase A/B runtime research is sufficiently complete.
