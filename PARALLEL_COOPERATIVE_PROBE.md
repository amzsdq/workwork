# Cooperative Parallel Probe

## Probe
probe_id: PARALLEL-A15-B4-01

## Goal
Test whether one recurring ChatGPT automation can intentionally use overlapping invocations as two cooperating workers that perform disjoint useful work concurrently.

This is not a handoff test. The predecessor keeps working while the successor works in parallel.

## Parameters
- PRIMARY_A nominal runtime: 15 minutes
- PARALLEL_B wake offset: PRIMARY_A_START + 4 minutes
- target parallel window: up to ~11 minutes
- PRIMARY_A and PARALLEL_B must operate on disjoint work units
- same recurring automation
- no shared-file concurrent rewrites

## Role selection
Evidence root:
parallel/PARALLEL-A15-B4-01/

1. If primary-start.json does not exist: role=PRIMARY_A.
2. If primary-start.json exists, primary-end.json does not exist, and parallel-b-start.json does not exist: role=PARALLEL_B.
3. If both workers have end evidence: role=OBSERVER.
4. Never start a second PARALLEL_B for this probe.

## PRIMARY_A
1. Capture actual start and create primary-start.json.
2. Immediately schedule the SAME automation for PRIMARY_A_START + 4 minutes using complete recurring RRULE and enabled=true.
3. Never mutate scheduler again during this probe.
4. Perform disjoint workload A for up to 15 minutes:
   - audit and analyze runtime/handoff evidence;
   - compute timing/jitter/bootstrap summaries;
   - produce bounded immutable work-unit files under parallel/.../A/.
5. Create A heartbeat/work-unit evidence during useful work.
6. Continue through the target unless forced stop/non-duration failure occurs.
7. Create primary-end.json.

## PARALLEL_B
1. Capture actual start and create parallel-b-start.json.
2. Read primary-start and existing A evidence only for coordination.
3. Claim workload B, disjoint from A:
   - analyze policy/throughput implications;
   - replay alternative lead/handoff policies against durable evidence;
   - produce bounded immutable work-unit files under parallel/.../B/.
4. Do not modify A files, handoff authority, state/current.json, or handoff control.
5. Work concurrently while PRIMARY_A is alive, targeting ~8 minutes of active useful work or until the primary target horizon is nearly reached.
6. Create parallel-b-end.json.
7. After B work is durable, schedule a follow-up observer for a time no earlier than max(actual_now + 3m, PRIMARY_A_START + 16m). This isolated probe permits B to be the scheduler writer only after its parallel work; PRIMARY_A never writes scheduler again after spawning B.

## Disjoint-write rule
- A writes only parallel/PARALLEL-A15-B4-01/A/*
- B writes only parallel/PARALLEL-A15-B4-01/B/*
- role lifecycle evidence uses unique filenames
- no concurrent rewrite of one shared file

## Success criteria
A useful PARALLEL PASS requires:
- B actually starts while A is still alive;
- A produces evidence after B_start;
- B produces useful work before A_end;
- no duplicate work units;
- no shared-file write collision;
- no scheduler collision;
- no checkpoint loss;
- combined useful work during the overlap exceeds what one worker completed in the same wall-clock interval, using completed bounded work units and active_work_sec as evidence.

## Metrics
- primary_start / end / elapsed
- parallel_b_start / end / elapsed
- wake_jitter
- observed_overlap_sec
- A_active_work_sec
- B_active_work_sec
- A_units_completed
- B_units_completed
- duplicate_unit_count
- write_conflict_count
- scheduler_conflict_count
- combined_active_worker_sec
- wall_clock_probe_sec
- parallelism_factor = combined_active_worker_sec / wall_clock_probe_sec
- useful_throughput_gain estimate
- result classification

## Classification
- PARALLEL_USEFUL: concurrent, disjoint useful work with no material conflicts.
- PARALLEL_CONCURRENT_BUT_LOW_GAIN: concurrency works but overhead erases most gain.
- CONFLICTED: write/task/scheduler conflict invalidates the sample.
- NOT_CONCURRENT: B does not overlap A.
- INCONCLUSIVE: insufficient evidence.

## Follow-up variables if viable
Later probes may vary:
- B wake offset: +2m, +4m, +6m, +8m
- number/size of work units
- static partition vs dynamic claim
- B duration
- whether B becomes next ACTIVE_OWNER or exits after parallel work

The first probe uses +4m wake offset to create a substantial overlap window and make concurrency benefits/failures easy to observe.
