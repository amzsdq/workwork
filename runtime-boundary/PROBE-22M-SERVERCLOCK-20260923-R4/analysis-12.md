# R4 close-reserve sampling plan

## Current deficiency

The completion-envelope objective needs a defensible CLOSE_OVERHEAD distribution, but current canonical evidence contains only one direct 32s sample plus contaminated/indirect observations. A fixed 60s reserve is therefore provisional.

## Minimal future sampling plan

During Phase B/W7 and suitable clean Phase-A closes, record server-authoritative or independently defensible markers for:

- last normal task admission,
- durable close checkpoint start,
- durable close checkpoint completion,
- END_MARKER creation.

Prefer server timestamps from GitHub comments/commits when they correspond exactly to the event. Do not use model-written timestamps as authoritative durations.

For promotion, retain at minimum:
- sample count,
- median,
- maximum or upper-tail statistic,
- profile context,
- whether close included contention/retry anomalies.

## Reserve selection principle

Start with a simple fixed reserve derived from upper-tail clean observations plus safety margin. Only adopt adaptive reserve if fixed reserve materially wastes useful capacity or fails reliability tests.

## R4 action

Do not retrofit additional close instrumentation mid-probe because that changes the workload. At R4 close, preserve the required durable checkpoint -> END marker ordering and record only what is directly defensible.
