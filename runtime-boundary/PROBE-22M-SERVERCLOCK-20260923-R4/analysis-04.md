# R4 failure-classification stress cases

Purpose: exercise the causal classification logic before R4 reaches its target so a later anomaly is not misclassified under time pressure.

## Scenario matrix

### S1 — END marker >=1320s, clean close, scheduler verified
Classification: CLEAN_PASS_PENDING_WAKE.
Boundary effect: none until retrospective WAKE_OK; then server-clock lower bound becomes 22m.

### S2 — END marker <1320s, normal voluntary close
Classification: UNDER_TARGET.
Boundary effect: none. Diagnose why work ended early.

### S3 — GitHub write fails transiently but invocation remains alive and later closes >=1320s
Classification: potentially CLEAN_PASS if the failure is recovered and required terminal evidence is synchronized; transient provider failure itself is not a duration failure.

### S4 — GitHub END marker cannot be created because GitHub is independently unavailable
Classification: CLOCK_EVIDENCE_INVALID or NON_DURATION_FAIL depending on independent evidence.
Boundary effect: none.

### S5 — invocation disappears near/after target with no END marker and no independent provider failure
Classification: not automatically DURATION_FAIL solely from missing END. Inspect durable last checkpoint, scheduler/wake behavior, and provider evidence. If duration causality becomes credible, mark DURATION_FAIL_CANDIDATE and repeat same profile as required.

### S6 — invocation remains alive past target but useful work stops far earlier
Survival evidence may exist, but operating-policy evidence is weak. Do not promote productive cap from survival alone.

### S7 — useful work continues near target but durable close fails
This is completion-envelope risk. If causally related to running too late, it may define a practical cap below pure survival. It must not be averaged away.

### S8 — successor wake is late after an otherwise clean pass
WORKED remains unchanged. Retrospective continuation gate remains unresolved until wake is observed; wake jitter is recorded separately.

## Result

The current decision rule is sufficient for Phase A; no new classification category is needed. The most important discipline is to avoid treating missing terminal evidence as proof of timeout without an independent causal chain.
