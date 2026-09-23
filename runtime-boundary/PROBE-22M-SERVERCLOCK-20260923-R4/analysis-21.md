# R4 profile-sensitivity hypothesis set

These hypotheses guide later profile rotation without altering R4.

## W3 MIXED_IO
Expected risk: connector/write latency and state-reconciliation overhead. R4 exercises this now.

## W5 MICRO_UNIT_CHAIN
Expected risk: many admission boundaries may increase control overhead and tempt premature close. Useful for testing soft-cutoff/task-admission logic.

## W4 REASONING_HEAVY
Expected risk: fewer durable intermediate anchors; potential long indivisible reasoning units near close cutoff.

## W6 LARGE_UNIT
Expected risk: a large unit admitted too late can consume close reserve. Useful for estimated-next-task admission validation.

## W7 CLOSE_HEAVY
Expected risk: completion-envelope pressure even when survival is safe. Essential for reserve distribution.

## Implication

If failure boundaries differ materially by profile, a universal hard cap should use the lower realistic risk envelope unless profile-aware admission yields enough utilization benefit to justify complexity. This is why coarse rotation is exploratory and Phase B cross-profile replication is mandatory.
