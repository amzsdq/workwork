# A unit 001 — parallel workload decomposition

PRIMARY_A start: 2026-09-23T08:44:14+09:00
B scheduled: 2026-09-23T08:48:14+09:00
Primary nominal close: 2026-09-23T08:59:14+09:00
Target overlap if wake is exact: 660 seconds.

Durable handoff research already separates successor preparation from predecessor safe-unit tail. For cooperative parallelism, those two costs are no longer the main objective: B must consume a genuinely disjoint queue while A continues its own queue.

Measurement implication: count immutable completed A/B units and active worker-seconds, not merely concurrent invocation lifetime. Concurrency without useful disjoint units is not a throughput win.

Control implication: keeping A/* and B/* append-only avoids the CAS/shared-file contention that would otherwise contaminate the throughput sample.
