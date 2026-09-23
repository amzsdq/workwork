# Overlap Handoff Baseline Candidate

Status: CANDIDATE_ACCEPTED_REPLAY_PASS_LIVE_DEFERRED
Repo: amzsdq/workwork
Purpose: reduce idle gap by waking the successor before predecessor work completes, while preserving single scheduler ownership.

## 1. Baseline model

Nominal baseline:

- OWNER_WORK_TARGET = 15m
- SUCCESSOR_WAKE_OFFSET = +12m from OWNER_ACTIVATED_AT
- NOMINAL_OVERLAP = 3m
- successor wakes as SHADOW, not owner
- successor prepares from durable state/checkpoint
- predecessor continues useful work toward 15m target
- ownership transfers atomically near predecessor cutoff
- only after ownership is confirmed does successor schedule the next successor
- next cycle is anchored to successor OWNER_ACTIVATED_AT, not to its earlier shadow wake time

Nominal flow:

A OWNER_ACTIVATED
-> immediately pre-arm B for +12m
-> A performs useful work
-> B wakes around +12m as SHADOW
-> B loads checkpoint/state and prepares
-> A stops admitting new work near transfer point
-> A writes final handoff checkpoint
-> atomic owner/generation transfer A -> B
-> B verifies owner/generation
-> B begins/continues substantive work immediately
-> B pre-arms C for +12m from B OWNER_ACTIVATED_AT
-> A may finish non-owner close cleanup after transfer if fencing guarantees no further owner writes

## 2. Core invariants

1. SINGLE_SCHEDULER_OWNER
   At most one invocation may mutate the scheduler/control pointer at a time.

2. SHADOW_NO_SCHEDULER_WRITE
   A successor that woke early must not schedule the next successor until ownership is transferred.

3. GENERATION_FENCING
   Ownership is represented by a monotonic generation/lease token. A stale predecessor must fail closed after transfer.

4. DURABLE_HANDOFF
   Successor preparation depends on shared durable checkpoint/state, not predecessor chat output.

5. OWNER_ACTIVATION_ANCHOR
   The next +12m wake is measured from OWNER_ACTIVATED_AT, not SHADOW_WAKE_AT.

6. TRANSFER_BEFORE_PREDECESSOR_OWNER_CLOSE
   Ownership may transfer before the predecessor invocation fully exits, but after transfer the predecessor cannot perform owner-only writes.

## 3. Existing empirical support

Existing overlap probe:
- primary start: 01:17:18 KST
- successor/observer scheduled: 01:29:18
- successor actual start: 01:29:22
- wake lateness: +4s
- primary remained alive until 01:32:40
- observed overlap: 198s
- classification: CONCURRENT

This proves that same-automation invocations can overlap and that a scheduled successor need not preempt or wait for the predecessor.

Other observed wake lateness:
- 18m continuation: +21s
- 20m continuation: +168s

Implication for a 180s nominal lead:
- +4s lateness leaves about 176s for successor preparation/transfer.
- +21s lateness leaves about 159s.
- +168s lateness leaves about 12s.

Therefore 15m/12m is a useful baseline but is not yet proven to provide enough preparation time under observed high jitter.

## 4. Replay decision

Decision: KEEP / TEST.

Why:
- overlap execution is empirically possible,
- it directly targets idle-gap reduction,
- single-owner fencing can avoid scheduler last-writer-wins races,
- it is simpler than unconstrained dual-owner renewal,
- but 3m lead may be marginal under high wake jitter.

Do not promote 15m/12m as the final production policy from current evidence.

## 5. Live test matrix

Run only after strict runtime boundary characterization and operating-cap validation are sufficiently complete, unless the user explicitly reprioritizes handoff testing.

Compare:
- H11: 15m owner work / successor wake at +11m / nominal lead 4m
- H12: 15m owner work / successor wake at +12m / nominal lead 3m
- H13: 15m owner work / successor wake at +13m / nominal lead 2m

For each configuration, require repeated cycles rather than one handoff.

Minimum measurements per cycle:
- predecessor_owner_activated_at
- successor_scheduled_for
- successor_actual_wake_at
- wake_lateness_sec
- successor_ready_at
- successor_prepare_sec
- transfer_started_at
- owner_transferred_at
- predecessor_owner_stop_at
- successor_first_substantive_work_at
- handoff_idle_gap_sec
- overlap_sec
- duplicate_owner_detected
- stale_owner_write_rejected
- scheduler_conflict
- state_conflict
- next_successor_schedule_ok
- predecessor_clean_close

Primary metric:
HANDOFF_IDLE_GAP_SEC.

Safety metrics:
- duplicate owner count = 0
- scheduler conflict count = 0
- stale-owner write success count = 0
- lost continuation count = 0

Efficiency metrics:
- READY_BEFORE_TRANSFER rate
- median / p95 handoff idle gap
- overlap cost
- long-run useful-work utilization

## 6. Promotion rule

Prefer the shortest lead that:
- maintains zero duplicate-owner/scheduler-conflict events in validation,
- keeps continuation success acceptably high,
- produces near-zero handoff idle at p95 or better,
- does not materially reduce predecessor useful-work utilization.

If 15/13 is as reliable as 15/12, prefer 15/13 because it wastes less overlap.
If 15/12 fails under wake jitter but 15/11 succeeds, prefer 15/11.
If even 15/11 is unreliable, derive lead dynamically from observed wake jitter + preparation time + transfer time + safety margin.

## 7. Generalized policy

The final rule should be parameterized, not hard-coded to 12m:

SUCCESSOR_WAKE_TARGET =
OWNER_ACTIVATED_AT
+ OWNER_WORK_TARGET
- REQUIRED_HANDOFF_LEAD

where:

REQUIRED_HANDOFF_LEAD =
wake_jitter_budget
+ successor_prepare_budget
+ transfer_budget
+ safety_margin

The 15m/12m configuration is the initial baseline instance of this rule.

## 8. Rollback

Immediately fall back to non-overlap/prearm relay if any of the following occurs:
- duplicate owner observed,
- scheduler ownership cannot be fenced,
- stale predecessor successfully overwrites successor control state,
- successor wake repeatedly arrives after predecessor safe close window,
- overlap materially increases lost-continuation or forced-termination risk.

