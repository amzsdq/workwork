# Unit granularity near handoff

The predecessor should not artificially shorten all work units throughout the turn. That would increase checkpoint/control overhead.

Use two regimes:
- NORMAL: before the expected successor window, choose efficient substantive units normally.
- HANDOFF_WINDOW: near the scheduled successor wake, prefer naturally bounded substantive units with shorter expected completion tails.

Once READY is observed, admit no new ordinary unit. Complete only the already in-flight smallest safe unit, checkpoint, and transfer authority.

Measure unit-tail after READY directly. If tail dominates bootstrap time, improving unit admission/granularity may outperform waking the successor earlier.
