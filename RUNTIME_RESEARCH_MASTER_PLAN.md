# Runtime Research Master Plan

Status: CANONICAL EXECUTION ROADMAP
Repo: amzsdq/workwork

## Objective
Find maximum safe substantive-work duration and simplest reproducible near-limit handoff/admission policy.

Authority: raw GitHub markers -> immutable probe terminal/event -> mutable projections. Model/local time never classifies duration.

## Current evidence
- R9: raw clean survival WORKED=1322s, productive=1257s, close=57s, WAKE_OK; posthoc generator-v1 semantic-repeat audit means strict substantive promotion requires revalidation/supersession.
- R10: **Harness V2 valid**, WORKED=1402s, productive=1376s, close=14s, semantic unique minimum=100,000, clean durable close/scheduler OK, but **UNDER_TARGET by 38s** because provisional 60s close reserve began normal close too early. Boundary effect NONE; not a duration failure.
- FAILURE_BOUNDARY: unresolved; credible duration failures=0.

## Phase A decision
Current case remains `SC-A24-CLOCK+`. Do not ascend to 26m. Before repeat, correct the admission/close timing defect exposed by R10.

The important distinction is now empirical:
- runtime/harness did not fail at 24m;
- workload did not exhaust;
- close control intentionally stopped substantive work at server elapsed 1388s PRE_CLOSE (progress trigger at 1382s), while actual close took only 14s;
- therefore END landed at 1402s, 38s below target.

Do not classify this as a 24m failure boundary.

## Close/admission correction research
Current-protocol close samples: 57s (R9 clock-valid but workload-quality tainted) and 14s (R10 fully Harness-V2 valid). N is too small/variable to promote a fixed reserve. Next repeat should use a target-reaching admission rule that does not assume close overhead itself will fill the remaining target budget. Candidate direction: continue substantive work closer to target while separately preserving a hard emergency close cap; validate from server PROGRESS markers. Exact rule must be durable before the next strict probe.

## Phase B
After an eligible coarse lower bound, require >=5 clean current-protocol runs near candidate with representative profiles, valid semantic-work quality, completion-envelope samples, and explicit safety margin. Longest one-off success is never operating cap.

## Phase C
P3 task-aware admission remains analytically stronger than fixed reserve; synthetic grids are supporting only. Estimation margin requires empirical error data. Overlap/handoff live tests remain deferred.

## Phase D
Gap optimization +3m -> +2m -> +1m after cap stabilization.

## Current execution pointer
CURRENT_CASE_ID = SC-A24-CLOCK+
ACTIVE_TARGET = 24m
LATEST_TERMINAL_PROBE = PROBE-24M-SERVERCLOCK-20260924-R10
LATEST_TERMINAL_RESULT = UNDER_TARGET
LATEST_WORKED = 1402s
LATEST_PRODUCTIVE_WINDOW = 1376s
LATEST_CLOSE_OVERHEAD = 14s
STRICT_SUBSTANTIVE_SAFE_LOWER_BOUND = REVALIDATION_PENDING
FAILURE_BOUNDARY = unresolved
NEXT_ACTION = FIX_CLOSE_ADMISSION_THEN_REPEAT_24M
