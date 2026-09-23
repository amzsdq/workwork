# R4 rollback-rule design audit

## Final program requirement

A reusable operating contract needs a rollback rule when failure rate rises. It is too early to set numeric thresholds, but the structure can be constrained now.

## Candidate rollback hierarchy

1. If duplicate/concurrent ownership or scheduler conflict appears during later overlap policy testing, immediately revert to single-owner non-overlap/prearm control.
2. If duration-attributable close/run-out failures appear at or below promoted operating cap, lower the cap to the highest repeatedly clean class while re-opening boundary validation.
3. If failures are provider/GitHub/network-specific, do not lower the duration cap automatically; classify and retry under clean conditions.
4. If productive utilization collapses while survival remains safe, adjust admission/checkpoint policy before lowering hard survival cap.
5. If wake jitter rises materially, adjust planned gap/handoff lead independently after runtime causality is protected.

## Promotion discipline

Numeric rollback triggers should be chosen only after Phase B produces a validation denominator and failure-rate baseline. Until then, rollback semantics remain qualitative.

## R4 relevance

This separation prevents a future wake/provider anomaly from being incorrectly treated as evidence that the invocation runtime itself is unsafe.
