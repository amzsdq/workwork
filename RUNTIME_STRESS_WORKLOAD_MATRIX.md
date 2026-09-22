# Runtime Stress Workload Matrix

Purpose: test runtime safety across heterogeneous *real* workload shapes instead of overfitting the safe limit to one easy task pattern.

Relay lead remains fixed at +3 minutes. Only workload shape and target runtime vary.

## Core profiles

### W1 — READ_HEAVY
Characteristics:
- repeated GitHub reads/fetches,
- compare durable files,
- parse event/state consistency,
- low write frequency.

Goal:
Measure whether long read-heavy turns exhibit different runtime/close behavior.

### W2 — WRITE_CHECKPOINT_HEAVY
Characteristics:
- many bounded useful units,
- frequent durable checkpoint/event writes,
- small files or append-style state evidence,
- higher mutation/control overhead.

Goal:
Stress continuation with frequent durable side effects without fabricating writes.

### W3 — MIXED_IO
Characteristics:
- alternating GitHub reads and necessary writes,
- state reconstruction followed by repair/normalization,
- closest to ordinary relay maintenance work.

Goal:
Provide the primary general-purpose boundary evidence.

### W4 — REASONING_HEAVY
Characteristics:
- fewer tool calls,
- deeper analysis of boundary estimation, policy replay, failure classification, or statistical/decision logic,
- durable write only when the analysis produces a real artifact/result.

Goal:
Check whether a compute/reasoning-heavy turn behaves differently from I/O-heavy turns.

### W5 — MICRO_UNIT_CHAIN
Characteristics:
- many genuine 20s–2m bounded units,
- immediately continue to the next useful unit before target,
- checkpoint only when materially justified; do not end after each unit.

Goal:
Directly emulate the common relay pattern that previously fragmented into very short invocations.

### W6 — LARGE_UNIT
Characteristics:
- one or a few larger bounded tasks such as full evidence-ledger reconciliation, full replay analysis, or consolidated reproducibility audit,
- fewer internal boundaries.

Goal:
Test overshoot/close behavior when the current unit cannot be stopped every few seconds.

### W7 — CLOSE_HEAVY
Characteristics:
- substantive work plus a deliberately realistic but necessary close path:
  checkpoint, derived-state update, evidence validation, final RRULE write.
- No redundant reads/writes solely to increase load.

Goal:
Measure close_overhead_sec and whether the safe cap must reserve more time for finalization.

## Experimental discipline
- A profile is selected before the substantive portion of a timing probe.
- Keep the profile stable within a probe whenever practical.
- Record workload_profile in every empirical timing event.
- Work must be genuinely useful to the single research goal.
- Never add artificial API calls, writes, sleeps, token generation, or meaningless loops merely to create load.
- Synthetic logic cases may test policy code/logic but do not count as runtime-boundary evidence.
- Different profiles may have different safe behavior. Do not promote a universal operating cap solely from one profile.
- Primary generalization requires evidence across multiple profiles, with at least MIXED_IO, MICRO_UNIT_CHAIN, and one of REASONING_HEAVY/LARGE_UNIT represented near the candidate cap.
- If one profile is systematically worse, final policy should use the worst credible operational profile or profile-aware admission logic rather than averaging away the risk.

## Rotation during coarse ascent
To avoid confounding target runtime with one workload type, rotate profiles rather than using a new profile only at higher runtimes.

Suggested initial sequence:
- 12m: W5 MICRO_UNIT_CHAIN
- 14m: W3 MIXED_IO
- 16m: W4 REASONING_HEAVY
- 18m: W2 WRITE_CHECKPOINT_HEAVY
- 20m: W6 LARGE_UNIT
Then continue rotating W1/W3/W5/W7 and revisit lower classes as needed.

This rotation is exploratory. Before declaring a universal cap, replicate the candidate cap across several profiles.

## Final generalization requirement
The final operating rule must specify whether it is:
- UNIVERSAL_CAP: one cap validated across representative workload profiles, or
- PROFILE_AWARE_CAP: cap/admission reserve varies by workload profile.

Prefer UNIVERSAL_CAP if it retains similar utilization without sacrificing reliability. Use PROFILE_AWARE_CAP only if evidence shows material profile-dependent risk.
