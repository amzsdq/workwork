# Unit 11 — Profile coverage plan

Probe: STRICT-14M-20260923T092741KST

Current coarse rotation is internally consistent:
- 14m W3 MIXED_IO (current)
- 16m W4 REASONING_HEAVY
- 18m W2 WRITE_CHECKPOINT_HEAVY
- 20m W6 LARGE_UNIT

Important interpretation:
Passing 14m W3 would establish only an observed lower bound at that class. It would not prove 14m safe across profiles. After the failure bracket is found, candidate-cap replication must include W3, W5, and W4 or W6 near the candidate.

This avoids conflating coarse-ascent workload rotation with cross-profile validation.
