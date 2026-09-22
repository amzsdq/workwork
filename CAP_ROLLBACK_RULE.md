# Runtime Cap Rollback Rule

Purpose: prevent a previously promoted operating cap from remaining active after new evidence shows that its continuation risk has increased.

This rule becomes operational only after Phase B promotes a cap. It does not itself promote any cap.

## Evidence window
Maintain a rolling window of the most recent 10 eligible runs at/near the promoted operating cap. Eligible means the run had trustworthy timing evidence and no independent non-duration failure.

Track:
- clean close count,
- duration-related failure count,
- ambiguous close-loss count,
- observed next-wake count where measurable,
- close-overhead upper tail/max,
- overshoot beyond intended hard cap.

## Immediate rollback triggers
Reduce the active cap to the highest lower target class with prior clean evidence if either occurs:
1. one confirmed duration-related failure at or below the promoted cap that loses the durable close or final recurring scheduler write; or
2. two ambiguous close-loss events at/near the cap before an independent non-duration cause is established.

Do not rollback for an explicit independent GitHub/network/tool/provider failure.

## Degradation trigger
Even without a catastrophic close-loss, re-open the cap if the rolling eligible window shows materially worse continuation behavior than during validation, including repeated overshoot or rising close-overhead that consumes the safety margin.

With sparse evidence, prefer conservative rollback rather than inventing a precise statistical threshold. Once enough samples exist, replace this qualitative trigger with an observed-rate criterion derived from the validation distribution.

## Recovery after rollback
- Return to the highest lower class with clean evidence.
- Re-estimate close reserve and safety margin from fresh runs.
- Do not immediately re-promote after one success.
- Require the normal Phase B repeated-validation rule before promotion again.

## Policy interaction
If failures are caused by admission-policy overshoot rather than the underlying runtime ceiling, first rollback the policy aggressiveness (larger reserve / earlier soft cutoff). If failures persist with conservative admission, rollback the operating cap itself.

This distinction is important: `runtime boundary` and `policy-induced overshoot` are different failure mechanisms.