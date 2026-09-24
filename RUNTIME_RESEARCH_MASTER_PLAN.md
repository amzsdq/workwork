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
Current case remains `SC-A24-CLOCK+`. Do not ascend to 26m. R10's admission/close timing defect is corrected durably in `runtime/SCALABLE_STRICT_PROBE_WORKLOAD_PROTOCOL.md` at commit `86d21949a09dce91c3a8701b866ff2fbff065cbe`.

The important distinction is empirical:
- runtime/harness did not fail at 24m;
- workload did not exhaust;
- close control intentionally stopped substantive work at server elapsed 1388s PRE_CLOSE (progress trigger at 1382s), while actual close took only 14s;
- therefore END landed at 1402s, 38s below target;
- this is not a 24m failure boundary.

## Close/admission correction
Promoted for the next strict repeat: **target-reaching admission**.
- Normal substantive admission does not stop merely because `remaining_budget <= provisional_close_reserve`.
- Continue valid substantive work until a raw GitHub PROGRESS marker proves elapsed from START is at least target T.
- Only then enter normal PRE_CLOSE and durable finalization.
- A separately configured emergency close cap remains a safety guard. If it forces close before T, that run is early-close safety/harness evidence, not a duration failure and not a clean target pass.
- The reserve is never credited as target runtime.

This rule removes the R10 under-target artifact without pretending close overhead is productive target time. The next strict 24m repeat must test this rule before any 26m ascent.

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
NEXT_ACTION = REPEAT_24M_WITH_TARGET_REACHING_ADMISSION
