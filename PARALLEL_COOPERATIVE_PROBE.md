# Cooperative Parallel Probe

Status: DEFERRED / SUPPORTING DESIGN ONLY UNTIL RUNTIME PHASE A/B GATE

## Goal
Test whether overlapping invocations can perform disjoint useful work concurrently. This is not strict runtime-boundary evidence.

## Core safety rules
- same recurring automation;
- disjoint work units and immutable per-worker evidence;
- no shared-file concurrent rewrites;
- no duplicate authoritative work;
- explicit scheduler-writer ownership;
- parallel results never advance strict runtime SAFE_LOWER_BOUND.

## Final-clock qualification
Any future quantitative parallel timing must use authoritative server-side timestamps for each endpoint being compared. Model-authored `actual start/end` strings in JSON/Markdown are not empirical timing evidence.

Therefore future metrics such as worker elapsed, wake jitter, overlap seconds, wall-clock probe duration, and parallelism factor are quantitative only when their timing inputs are authoritative. If timing endpoints are unavailable, the run may still establish qualitative concurrency/control safety from durable ordering, but exact timing metrics remain unresolved.

## Work partition
PRIMARY_A and PARALLEL_B must claim disjoint useful units and write only their own immutable namespaces. A later observer may reconcile results after both are terminal.

## Success classes
- PARALLEL_USEFUL: authoritative concurrency evidence plus disjoint useful work and no material conflicts; quantitative gain only if authoritative timing exists.
- PARALLEL_CONCURRENT_BUT_LOW_GAIN: concurrency/control works but measured overhead erases gain.
- CONFLICTED: task/write/scheduler conflict invalidates sample.
- NOT_CONCURRENT: authoritative evidence shows no overlap.
- INCONCLUSIVE: insufficient evidence.

## Gate
Do not run/advance this probe until strict runtime boundary characterization and operating-cap validation are sufficiently complete, unless the user explicitly reprioritizes it.
