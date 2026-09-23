# Successor Shadow Handoff Research

## Objective
Turn intentional overlap into controlled zero/near-zero-idle handoff after runtime boundary/cap validation.

## Proven prerequisite
Historical overlap testing showed same-automation concurrent execution is possible. Treat that as supporting concurrency evidence; exact future lead/gap optimization must use authoritative server-side timing.

## Roles
Exactly one ACTIVE_OWNER. At most one intended SHADOW_SUCCESSOR.

SHADOW may read durable state/checkpoints, restore context, prepare the next non-duplicating unit, and publish immutable READY evidence. SHADOW may not execute owner-only side effects, publish authoritative shared transitions, overwrite predecessor evidence, or mutate scheduler before ownership.

## Authoritative owner record
The existing canonical owner record is **`handoff-state.json`** at repository root. Do not refer to nonexistent `handoff/control.json` unless a deliberate migration is performed later.

Minimum owner fields:
- generation
- active_invocation_id
- status
- predecessor_invocation_id
- successor_invocation_id

Model-authored `updated_at` fields are metadata only and are not empirical timing evidence.

Authority transfer:
- predecessor fresh-reads `handoff-state.json`;
- update using exact current blob SHA;
- generation increments by 1;
- active_invocation_id changes to successor;
- stale SHA/update failure means transfer did not succeed;
- predecessor performs no further authoritative writes after successful transfer.

Unique immutable evidence lives under `handoff/runs/<invocation_id>/` and `handoff/transfers/` when live testing resumes.

## State machine
1. ACTIVE_OWNER works in bounded units.
2. Prearmed wake starts SHADOW_SUCCESSOR.
3. SHADOW restores state and prepares a concrete next unit.
4. SHADOW publishes READY with identity/generation/source evidence; timing fields count quantitatively only when authoritative.
5. ACTIVE_OWNER validates READY at a safe unit boundary.
6. After READY, start no new ordinary unit; finish/checkpoint current safe unit.
7. ACTIVE_OWNER CAS-transfers generation/owner in `handoff-state.json`.
8. SUCCESSOR fresh-reads transferred generation, records ACCEPTED, becomes ACTIVE_OWNER, starts prepared unit.
9. Only the new ACTIVE_OWNER prearms the next successor.

## Scheduler rule
Only ACTIVE_OWNER may schedule. Baseline remains S1 ACTIVE_OWNER_IMMEDIATE_PREARM. SHADOW scheduler writes remain prohibited until a stronger scheduler-generation reservation mechanism is experimentally proven.

## Timing authority
Future empirical metrics such as successor wake lateness, bootstrap-ready time, transfer tail, overlap, and handoff gap require authoritative server-side timing endpoints. Model-authored timestamps in JSON/Markdown are non-authoritative and must be marked unresolved for quantitative timing if no server clock exists.

The initial 3m lead remains a candidate baseline, not an empirically promoted optimum under the final clock discipline.

## Optimization variables
- SUCCESSOR_LEAD: start with 3m candidate; later compare shorter/longer leads using authoritative timing.
- READY_HANDOFF_POLICY: EARLY_READY_HANDOFF vs TARGET_HOLD.
- NEXT_UNIT_ADMISSION: before READY continue bounded work; after READY finish only current safe unit and transfer.
- SCHEDULER_STRATEGY: S1 baseline, S2 comparison, S3 isolated only after stronger fencing.

## Safety metrics
- duplicate authoritative work count
- stale write rejection
- scheduler writer conflict
- checkpoint loss
- clean handoff
- next wake success

## Quantitative timing metrics
Only when authoritative endpoints exist:
- successor wake lateness
- bootstrap-ready duration
- predecessor unit tail after READY
- authority transfer latency
- handoff gap
- overlap
- residual budget abandoned

## Promotion
Require repeated clean handoffs, initially >=5, with zero duplicate authoritative side effects and zero scheduler-writer collision. Quantitative lead/gap claims additionally require authoritative timing evidence.

## Final reusable policy target
- nominal active runtime / operating cap
- successor lead
- READY criteria
- safe-unit boundary rule
- CAS transfer rule on `handoff-state.json`
- scheduler-writer rule
- stale-owner fence
- timeout/fallback
- authoritative handoff-gap distribution when measurable
- overlap/preload utilization
- rollback rule
