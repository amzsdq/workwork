# Runtime Cap Rollback Rule

Purpose: prevent a promoted operating cap from remaining active after new evidence shows increased continuation/completion risk. Operational only after Phase B promotion.

## Eligible evidence window
Maintain the most recent 10 eligible runs at/near promoted cap. For post-clock-protocol runtime rollback, eligible timing evidence requires a valid GitHub server START/END marker pair and no independent non-duration failure.

Track clean close, duration failure, ambiguous close loss, continuation observation, authoritative wake/idle timing when available, current-protocol pre-END close behavior, strict WORKED overshoot, and productive evidence separately.

Legacy pre-server-clock runs may inform historical context but do not satisfy the current-protocol rollback window's strict timing requirement.

## Failure-layer separation
- Runtime/completion failure: duration-attributable forced stop/lost durable close/repeated pre-END close-budget exhaustion near cap.
- Wake-layer failure: clean close + valid prearm but continuation missing/late; diagnose scheduler/gap first.
- Productivity failure: survives/closes but sparse useful work; fix workload/admission, not runtime boundary.
- Independent provider/tool failure: no cap movement unless causally linked to runtime pressure.

## Immediate rollback
Reduce to highest lower current-protocol validated class if either:
1. one confirmed duration-related failure at/below promoted cap loses durable close despite valid prearm; or
2. two ambiguous close-loss events near cap before independent cause is established.

If no lower current-protocol validated class exists, reopen validation conservatively rather than treating a legacy class as automatically re-promoted.

## Degradation
Reopen cap if eligible rolling evidence shows materially worse continuation/completion behavior, repeated strict-WORKED overshoot, or rising current-protocol close requirements consuming margin. With sparse data remain conservative rather than inventing precise thresholds.

## Recovery
Return to highest lower current-protocol clean class when available, re-estimate reserve/margin from fresh evidence, and require normal Phase B repeated validation before re-promotion.

## Policy/gap interaction
If admission overshoot causes failures, first make policy more conservative. If only wake/gap behavior worsens, rollback gap policy rather than runtime cap. If only productivity worsens, improve work selection. Keep mechanisms separate.
