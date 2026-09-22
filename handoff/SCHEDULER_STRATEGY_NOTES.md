# Scheduler strategy comparison notes

S1 ACTIVE_OWNER_IMMEDIATE_PREARM secures continuation earliest and keeps one scheduler writer. Its cost is that the wake is based on an early runtime estimate.

S2 POST_BOOTSTRAP_PREARM can use a better-informed runtime estimate, but continuation remains unsecured during bootstrap and the scheduler write consumes later runtime budget.

For a controlled-overlap relay, S1 is the default unless measured early-estimate error causes materially worse handoff timing than S2.

S3 SHADOW_IMMEDIATE_PREARM should not be promoted merely because concurrent execution exists. Without a scheduler-specific ownership/fencing mechanism, it permits two invocations to overwrite the same automation schedule. Test S3 only in isolation after a durable scheduler generation/owner rule exists.

Primary comparison metrics are wake-to-scheduler-write latency, wake timing error relative to desired handoff window, writer collisions, missed continuation, and resulting handoff gap.
