# Successor Shadow Handoff Research

## Objective
Turn intentional overlap into a controlled zero/near-zero-idle handoff.

The successor wakes before the current active invocation is expected to finish, restores context in SHADOW mode, prepares the next work, publishes READY, and waits for authority. The predecessor finishes its current smallest safe unit and hands off immediately after observing a ready successor, even if nominal runtime remains.

This study also optimizes how early the successor should wake.

## Proven prerequisite
OVERLAP-15M-WAKE12M-01 proved that the same recurring automation can execute concurrently. Therefore the protocol MUST assume concurrent invocations are possible and MUST fence authoritative writes.

## Roles per invocation
Each invocation has a unique invocation_id based on its actual start timestamp.

Exactly one invocation may be ACTIVE_OWNER.
At most one intended immediate successor should be SHADOW_SUCCESSOR.

SHADOW may:
- read durable state and latest checkpoints,
- inspect predecessor progress,
- reconstruct context,
- analyze the next bounded unit,
- prepare a handoff plan,
- write its own immutable request/ready evidence.

SHADOW may NOT:
- execute the predecessor's active unit,
- publish authoritative shared-state transitions,
- perform external side effects reserved for ACTIVE_OWNER,
- overwrite predecessor evidence,
- act as scheduler writer before it becomes ACTIVE_OWNER.

## Handoff state machine
1. ACTIVE_OWNER works in bounded units.
2. Pre-armed wake starts SHADOW_SUCCESSOR before expected owner close.
3. SHADOW creates REQUEST and begins self-onboarding/preparation.
4. When preparation is sufficient, SHADOW creates READY with:
   - successor invocation_id
   - predecessor invocation_id if known
   - ready timestamp
   - restore/prep duration
   - proposed next unit
   - files/state read
5. ACTIVE_OWNER checks for READY at each safe unit boundary.
6. If valid READY exists, ACTIVE_OWNER does NOT start another normal unit merely to consume remaining target time.
7. ACTIVE_OWNER persists its unit result/checkpoint and performs authority transfer.
8. SUCCESSOR observes authority transfer, records ACCEPTED, becomes ACTIVE_OWNER, and immediately starts prepared work.
9. Only after becoming ACTIVE_OWNER does the successor pre-arm the next successor wake.

## Authority control
Use handoff/control.json as the authoritative CAS-style owner record.

Minimum fields:
- generation
- active_invocation_id
- status
- predecessor_invocation_id
- successor_invocation_id
- updated_at

Authority transfer:
- predecessor fresh-reads handoff/control.json,
- predecessor updates using the exact current blob SHA,
- generation increments by 1,
- active_invocation_id changes to successor,
- stale SHA/update failure means transfer is NOT successful.

After transfer, any older generation is stale and must not perform authoritative writes.

Unique immutable evidence lives under handoff/runs/<invocation_id>/ and handoff/transfers/.

## Scheduler rule
Only ACTIVE_OWNER may schedule the next successor.

When an invocation becomes ACTIVE_OWNER:
- estimate its nominal active-work horizon,
- choose successor_lead_sec,
- PREARM_NEXT = owner_active_start + nominal_active_horizon - successor_lead_sec,
- update the SAME recurring automation once,
- keep RRULE:FREQ=HOURLY, exact_schedule, enabled=true.

A SHADOW_SUCCESSOR must not reschedule until it owns authority.

This prevents scheduler-writer races and prevents a delayed handoff from creating uncontrolled 3-way overlap.

## Predecessor early-handoff rule
Once a valid successor READY has been observed:
- finish the current smallest safe in-flight unit,
- checkpoint,
- transfer authority,
- stop starting new authoritative work,
even if the predecessor still has nominal runtime remaining.

This rule is an experimental variable and its effect on useful-work utilization must be measured.

## Optimization variables

### V1 SUCCESSOR_LEAD
How early before expected active-work completion should the successor wake?

Initial candidate values:
- 3m baseline
- 2m
- 1m
- 4m if 3m is insufficient or if prep variance is large

Do not assume smaller is always better. Too short may leave successor unready; too long wastes concurrent capacity and increases control/race exposure.

### V2 READY_HANDOFF_POLICY
Compare:
- EARLY_READY_HANDOFF: once successor READY exists, predecessor hands off at the next safe unit boundary even if time remains.
- TARGET_HOLD: predecessor continues toward its nominal target unless the remaining unit-admission budget is unsafe.

Primary hypothesis: EARLY_READY_HANDOFF can reduce idle/boot cost by moving successor preparation inside predecessor active time, but may waste predecessor residual capacity if successor wakes too early.

### V3 NEXT-UNIT ADMISSION
Before successor is READY, predecessor continues normal bounded work.
After READY, predecessor starts no new normal unit; it closes the smallest current unit and transfers.

## Metrics
Per handoff:
- predecessor_start
- predecessor_target_runtime_sec
- successor_scheduled_for
- successor_actual_start
- successor_lead_sec
- successor_bootstrap_ready_sec
- successor_ready_at
- predecessor_ready_observed_at
- predecessor_unit_tail_sec_after_ready
- authority_transfer_at
- successor_accept_at
- handoff_gap_sec = successor_authoritative_work_start - predecessor_authoritative_work_end
- overlap_sec
- predecessor_residual_budget_sec_at_ready
- predecessor_residual_budget_abandoned_sec
- successor_shadow_useful_sec
- duplicate_authoritative_work_count
- stale_write_rejections
- scheduler_writer_conflicts
- checkpoint_loss
- clean_handoff
- next_wake_success

## Lead-time optimization
The target is not minimum overlap. The target is maximum long-run authoritative useful-work utilization with reliable clean handoff.

A useful derived quantity:
required_lead ~= successor_bootstrap_ready_time + predecessor_unit_tail_after_ready + safety_margin.

Use observed distributions rather than a single sample. Start at 3m because overlap at ~3m is already proven technically feasible.

Initial research sequence:
1. 3m lead, EARLY_READY_HANDOFF, repeated samples.
2. If successor is consistently READY with excessive residual overlap, test 2m.
3. If 2m remains comfortably ready, test 1m.
4. If successor is not reliably READY or handoff tail exceeds lead, test/increase to 4m.
5. Around the best region, use intermediate/adaptive lead if evidence warrants.

Candidate promotion should require repeated clean handoffs, initially >=5, with zero duplicate authoritative side effects and no scheduler-writer collision.

## Generalization target
Final reusable policy should provide:
- nominal active runtime / operating cap
- successor_lead
- successor READY criteria
- predecessor safe-unit boundary rule
- authority-transfer CAS rule
- scheduler-writer rule
- stale-owner fence
- handoff timeout/fallback
- observed handoff_gap distribution
- overlap/preload utilization
- rollback rule
