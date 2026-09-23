# R4 continuation-gate semantics audit

## Distinction

A strict clean runtime probe has two stages:

1. `CLEAN_PASS_PENDING_WAKE`: target WORKED reached, clean close/checkpoint, scheduler pre-arm verified, no duration failure.
2. `CLEAN_PASS_WAKE_OK`: a later actual invocation confirms the pre-armed continuation occurred.

Only stage 2 advances SERVER_CLOCK_SAFE_LOWER_BOUND under the current protocol.

## Why retain this gate

The research goal includes reproducible relay operation, not isolated survival. A run that survives 22m but loses its continuation is not sufficient evidence for an operating relay point even if the runtime itself was safe.

## Causal caution

Wake lateness or missed wake must still be classified separately. A provider/scheduler anomaly should not become a duration failure. The gate can withhold promotion without asserting that the runtime target is unsafe.

## R4 terminal behavior

If R4 closes cleanly >=1320s, state must remain at 22m pending wake. The next invocation must first reconcile R4 before starting the 24m case. This avoids the previous pattern of advancing target before continuation evidence is durable.
