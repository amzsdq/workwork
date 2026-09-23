# Scheduler strategy comparison notes

S1 ACTIVE_OWNER_IMMEDIATE_PREARM secures continuation earliest and keeps one scheduler writer. Its cost is that the wake is based on an early runtime estimate.

S2 POST_BOOTSTRAP_PREARM can use a better-informed runtime estimate, but continuation remains unsecured during bootstrap and the scheduler write consumes later runtime budget.

For controlled overlap, S1 remains the default unless measured evidence shows materially worse handoff behavior than S2.

S3 SHADOW_IMMEDIATE_PREARM must not be promoted merely because concurrent execution exists. Without scheduler-specific ownership/fencing it permits two invocations to overwrite one automation schedule. Test only in isolation after a durable scheduler generation/owner rule exists.

Safety comparison metrics: writer collisions, missed continuation, duplicate generations, stale-owner behavior.

Timing comparison metrics such as wake-to-write latency, wake timing error, and handoff gap count quantitatively only when their endpoints have authoritative server-side timing evidence. Model-authored timestamps are not empirical timing evidence.
