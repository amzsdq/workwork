# Lead-time evaluation

Measure successor preparation time, predecessor safe-unit tail after READY, configured lead, actual handoff gap, residual predecessor budget, and useful shadow preparation.

A sample is clean only when ownership is unambiguous, there is no duplicate authoritative work, no scheduler-writer collision, and no checkpoint loss.

Start at 180 seconds. Collect repeated clean samples before reducing to 120 seconds, then 60 seconds. Increase to 240 seconds if 180 seconds does not reliably cover preparation plus the safe-unit tail.

Prefer the simplest fixed lead when it performs equivalently to an adaptive rule. A future adaptive rule should be based on the observed upper range of preparation plus safe-unit tail and an explicit safety margin, not a single average.
