# Runtime Research Master Plan

Status: CANONICAL EXECUTION ROADMAP
Repo: amzsdq/workwork

## Objective
Find maximum safe substantive-work duration and simplest reproducible near-limit handoff/admission policy.

Authority: raw GitHub markers -> immutable probe terminal/event/wake -> mutable projections. Model/local time never classifies duration.

## Current evidence
- R9: raw clean survival WORKED=1322s, productive=1257s, close=57s, WAKE_OK; posthoc generator-v1 semantic-repeat audit means strict substantive promotion requires revalidation/supersession.
- R10: **Harness V2 valid**, WORKED=1402s, productive=1376s, close=14s, semantic unique minimum=100,000, clean durable close/scheduler OK, but **UNDER_TARGET by 38s** because provisional 60s close reserve began normal close too early. Boundary effect NONE; not a duration failure.
- R13: valid raw GitHub clock pair with WORKED=1649s, target progress elapsed=1617s, productive-marker wall-clock window=1619s, close=25s, scheduler prearm verified. This establishes clock survival beyond 24m but strict substantive promotion is FAIL_CLOSED because full sustained semantic-work evidence was incomplete.
- R14: **clean strict 24m substantive pass** under target-reaching admission. WORKED=1523s, productive window=1506s, close=6s; 310,000,000 semantic-unique units, >=2,480,000,000 assertions, duplicate/repeat/anomaly=0; terminal/event immutable and separate WAKE_OK confirmed.
- R15: **clean strict 26m substantive pass**. START=2026-09-24T09:52:27Z; qualifying PROGRESS=10:21:00Z (1713s); END=10:21:20Z; WORKED=1733s; close=13s; 110,000,000 semantic-unique units, >=880,000,000 assertions, duplicate/repeat/anomaly=0; terminal/event immutable and separate WAKE_OK comment=5812331309, wake commit=dc1261dae01c08c53e6462b025e5185f6010fcc9.
- R16: **clean strict 28m substantive pass**. START=2026-09-24T10:25:30Z; qualifying PROGRESS=10:56:54Z (1884s); PRE_CLOSE=10:57:00Z; END=10:57:03Z; WORKED=1893s; close=9s; 180,000,000 semantic-unique units, >=1,440,000,000 assertions, duplicate/repeat/anomaly=0; terminal/event immutable and separate WAKE_OK comment=5812770743, wake commit=8e33f36894b3fb1690f5a87ef2198d80e1841561.
- FAILURE_BOUNDARY: unresolved; credible duration failures=0.

## Phase A decision
R14, R15, and R16 independently establish clean strict substantive passes at 24m, 26m, and 28m with separate wake evidence. Coarse boundary search therefore advances one step to **30m strict substantive**. This does not promote the operational cap: the conservative operating cap remains 14m until Phase B reproducibility/safety-margin evidence explicitly changes it.

The next probe must use a fresh identity, target-reaching admission, complete durable workload ledger, timely START/WORK_START markers, raw GitHub created_at authority, immutable terminal/event, and separate WAKE_OK. Survival alone is insufficient.

## Close/admission correction
Promoted for strict repeats: **target-reaching admission**.
- Normal substantive admission does not stop merely because `remaining_budget <= provisional_close_reserve`.
- Continue valid substantive work until a raw GitHub PROGRESS marker proves elapsed from START is at least target T.
- Only then enter normal PRE_CLOSE and durable finalization.
- A separately configured emergency close cap remains a safety guard. If it forces close before T, that run is early-close safety/harness evidence, not a duration failure and not a clean target pass.
- The reserve is never credited as target runtime.

## Phase B
After an eligible coarse lower bound, require >=5 clean current-protocol runs near candidate with representative profiles, valid semantic-work quality, completion-envelope samples, and explicit safety margin. Longest one-off success is never operating cap.

## Phase C
P3 task-aware admission remains analytically stronger than fixed reserve; synthetic grids are supporting only. Estimation margin requires empirical error data. Overlap/handoff live tests remain deferred.

## Phase D
Gap optimization +3m -> +2m -> +1m after cap stabilization.

## Current execution pointer
CURRENT_CASE_ID = SC-A30-STRICT+
ACTIVE_TARGET = 30m
LATEST_TERMINAL_PROBE = PROBE-28M-STRICT-V2-20260924-R16
LATEST_TERMINAL_RESULT = CLEAN_STRICT_SUBSTANTIVE_PASS_WAKE_OK
LATEST_WORKED = 1893s
LATEST_QUALIFYING_PROGRESS_ELAPSED = 1884s
LATEST_CLOSE_OVERHEAD = 9s
STRICT_SUBSTANTIVE_SAFE_LOWER_BOUND = 28m_ONE_CLEAN_CURRENT_PROTOCOL_SAMPLE
CLOCK_SURVIVAL_OBSERVED_AT_OR_ABOVE_28M = true
FAILURE_BOUNDARY = unresolved
OPERATIONAL_CAP = 14m_PROMOTED_CONSERVATIVE_5_OF_5
NEXT_ACTION = RUN_FRESH_30M_STRICT_SUBSTANTIVE_PROBE
