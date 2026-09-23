# R4 operating-cap promotion audit

## Current evidence versus Phase B gate

Phase B requires at least five clean runs at/near a candidate with valid server-clock markers, scheduler verification, durable close, continuation evidence where observable, and representative profile coverage.

Current post-clock evidence:
- R3: valid marker pair, UNDER_TARGET at 652s, clean close, W3. Does not count as near-cap clean pass.
- R4: active 22m W3 probe. Not terminal yet.

Therefore validation count for any production operating cap remains zero.

## Parameters that must remain unpromoted

- OPERATING_CAP: unresolved.
- PRODUCTIVE_CAP: unresolved.
- SOFT_CUTOFF: unresolved.
- HARD_CAP: unresolved.
- CLOSE_RESERVE: provisional only.
- SAFETY_MARGIN: unresolved until credible failure boundary/variance exists.
- NEXT_TASK_ADMISSION: candidate only.

## Profile coverage still required near candidate

- W3 MIXED_IO,
- W5 MICRO_UNIT_CHAIN,
- W4 REASONING_HEAVY or W6 LARGE_UNIT,
- W7 CLOSE_HEAVY.

## Consequence

Even if R4 succeeds at 22m and WAKE_OK, the correct conclusion is `SERVER_CLOCK_SAFE_LOWER_BOUND >=22m` for coarse exploration, not `OPERATING_CAP=22m`. Coarse ascent should continue to 24m with rotated profile until a credible upper failure is found or a practical external ceiling is reached.
