# Cooperative Parallel Probe 02

probe_id: PARALLEL-A15-B4-02

Goal: repeat the cooperative parallel test with stronger instrumentation so true simultaneous useful work can be proven.

Parameters:
- PRIMARY_A nominal runtime: 15m
- PARALLEL_B wake offset: A_START +4m
- B target active work: ~8m
- disjoint immutable namespaces: A/* and B/*
- same recurring automation

PRIMARY_A instrumentation:
1. Persist primary-start.json.
2. Immediately pre-arm same automation for A_START+4m, recurring RRULE, enabled=true.
3. Perform disjoint A work continuously.
4. Persist an immutable A heartbeat/work-unit at least once every ~60-90s while useful work is continuing.
5. Critically, after B has started, A must persist at least TWO new A evidence files timestamped after B_START before A can count as concurrent-useful.
6. Persist primary-end.json near/after 15m.
7. A never mutates scheduler again after spawning B.

PARALLEL_B:
1. Persist parallel-b-start.json.
2. Perform only disjoint B work and persist immutable B work units.
3. Do not mutate shared state/authority or A files.
4. Persist parallel-b-end.json.
5. After B finishes, schedule observer no earlier than max(now+3m, A_START+16m).

Observer PASS requires:
- B_START < A_END,
- >=2 A evidence timestamps after B_START,
- >=1 B useful work timestamp before A_END,
- no duplicate work,
- no shared-write collision,
- no scheduler collision.

Measure:
A_active_work_sec, B_active_work_sec, overlap_useful_sec, combined_active_worker_sec,
parallelism_factor=combined_active_worker_sec / wall_clock_probe_sec,
A/B units, conflicts, throughput-gain estimate.

Classification:
PARALLEL_USEFUL / PARALLEL_CONCURRENT_BUT_LOW_GAIN / CONFLICTED / NOT_CONCURRENT / INCONCLUSIVE.
