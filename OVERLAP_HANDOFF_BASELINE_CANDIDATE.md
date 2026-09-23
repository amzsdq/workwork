# Overlap Handoff Baseline Candidate

Status: CANDIDATE_ACCEPTED_REPLAY_PASS_LIVE_DEFERRED
Repo: amzsdq/workwork
Purpose: reduce idle gap by waking the successor before predecessor work completes, while preserving single scheduler ownership.

## Baseline model
- OWNER_WORK_TARGET = 15m
- SUCCESSOR_WAKE_OFFSET = +12m from OWNER_ACTIVATED_AT
- NOMINAL_OVERLAP = 3m
- successor wakes as SHADOW, not owner
- successor prepares from durable state/checkpoint
- predecessor continues useful work toward cutoff
- ownership transfers atomically
- only the confirmed new owner schedules the next successor
- next cycle anchors to successor OWNER_ACTIVATED, not earlier SHADOW wake

## Core invariants
1. SINGLE_SCHEDULER_OWNER — at most one invocation may mutate scheduler/control state.
2. SHADOW_NO_SCHEDULER_WRITE — early successor does not schedule until ownership transfer.
3. GENERATION_FENCING — stale generations fail closed.
4. DURABLE_HANDOFF — successor restores from durable state, not predecessor chat output.
5. OWNER_ACTIVATION_ANCHOR — next cycle is based on ownership activation, not shadow wake.
6. TRANSFER_BEFORE_FULL_EXIT is allowed only after predecessor loses owner-write authority.
7. AUTHORITATIVE_TIMING_ONLY — future empirical lead/gap/overlap optimization must use server-side timestamps or other explicitly authoritative clocks. Model-authored timestamp strings are identity/context metadata only and cannot establish empirical timing.

## Existing support
Historical overlap probe established concurrent same-automation execution and reported approximately 198s overlap with a +4s wake observation. Other historical wake observations include +21s and +168s. These are pre-final-clock supporting observations; preserve them as design evidence, but future promotion of exact lead/gap values requires authoritative timing under the final clock discipline.

Implication remains qualitative: a 3m nominal lead may be sufficient in low-jitter cases and marginal in high-jitter cases, so 15/12 is a baseline, not a final answer.

## Decision
KEEP / TEST / NOT PROMOTED.

Reasons:
- controlled overlap directly targets idle-gap reduction;
- single-owner fencing avoids unconstrained dual-writer renewal;
- concurrent execution is historically demonstrated;
- exact optimal lead remains unvalidated under authoritative timing.

## Future live matrix
After strict runtime boundary and operating-cap validation, compare:
- H11: 15m owner / wake +11m / nominal lead 4m
- H12: 15m owner / wake +12m / nominal lead 3m
- H13: 15m owner / wake +13m / nominal lead 2m

Require repeated cycles.

Per-cycle safety evidence:
- owner/generation identity
- successor READY validity
- duplicate owner detected
- stale owner write rejected
- scheduler conflict
- state conflict
- next successor schedule success
- predecessor clean close

Timing evidence, only when authoritative:
- predecessor owner activation
- successor scheduled time
- successor actual wake
- successor ready
- transfer
- predecessor authoritative-work end
- successor authoritative-work start
- handoff idle gap
- overlap

If an endpoint lacks authoritative timing, mark that metric unresolved rather than filling it from model-authored time text.

## Promotion rule
Prefer the shortest lead that repeatedly has zero duplicate-owner/scheduler-conflict/stale-write-success events, preserves continuation, and achieves near-zero authoritative handoff gap without material residual-capacity waste.

Generalized candidate:
`SUCCESSOR_WAKE_TARGET = OWNER_ACTIVATED + OWNER_WORK_TARGET - REQUIRED_HANDOFF_LEAD`

where required lead is derived from observed wake jitter + successor preparation + transfer/unit-tail + safety margin, using authoritative timing evidence.

## Rollback
Fall back to non-overlap/prearm relay on duplicate owner, unfenceable scheduler ownership, successful stale-owner overwrite, repeated successor lateness beyond safe close, or materially increased continuation/forced-stop risk.

## Selective Workaholic absorption

Reviewed source: installed Workaholic continuous-relay skill.

### ADOPT
The following semantics are promoted into this candidate because they directly improve continuity without fixing an unvalidated timing constant:

1. **SAME_CANONICAL_REUSE** — normal continuation reuses the same canonical RRULE automation; no replacement automation merely for continuation.
2. **NORMAL_STOP_GATES** — once this handoff policy is promoted to operational relay mode, the only normal voluntary stop gates are:
   - PROGRAM_COMPLETE
   - HANDOFF_COMPLETE
   A subtask/checkpoint/phase completion or merely expecting a successor is not a normal stop gate.
3. **PREPARE_BEFORE_TRANSFER** — successor must reconstruct durable state and become READY before ownership transfer.
4. **PREDECESSOR_RETAINS_AUTHORITY** — successor wake/existence alone never completes handoff. Until durable transfer commits, predecessor remains OWNER.
5. **AMBIGUOUS_HANDOFF_FAILS_CLOSED** — ambiguous transfer means predecessor remains authoritative; never infer success.
6. **POST_TRANSFER_SINGLE_OWNER** — after transfer, predecessor stops owner-only substantive side effects and successor becomes the sole active owner.
7. **WHOLE_PROGRAM_COMPLETION** — PROGRAM_COMPLETE means the entire requested program is complete, not just the current unit.

Preferred authority sequence:

`PREDECESSOR_ACTIVE -> SUCCESSOR_AWAKE -> SUCCESSOR_PREPARED -> SUCCESSOR_READY -> TRANSFER_COMMITTED -> SUCCESSOR_ACTIVE`

The new OWNER, not the SHADOW, performs the next scheduler mutation after transfer.

### REJECT / DO NOT PROMOTE
The following Workaholic rules are intentionally not absorbed:

- **Fixed +14m wake offset** — rejected as an invariant. Wake lead is an empirical tunable and must be derived from jitter + preparation + transfer latency + safety margin.
- **Successor re-arms before ownership transfer** — rejected because it violates SINGLE_SCHEDULER_OWNER / SHADOW_NO_SCHEDULER_WRITE and creates split-brain scheduler risk.
- **EGO=WORKAHOLIC** — not required for correctness and has no control-plane authority.
- **Any fixed 15/12 timing as permanent policy** — 15/12 remains only a test baseline.

### Scope guard
NORMAL_STOP_GATES applies to the future operational relay after runtime-boundary/cap validation. It does **not** override strict runtime-probe PRE_CLOSE/END semantics during Phase A/B experiments.

If a promoted operational predecessor approaches the empirically established hard runtime cap before HANDOFF_COMPLETE, this is an abnormal recovery/safety condition, not a successful normal stop. The system must preserve durable continuation evidence and avoid pretending handoff succeeded.
