# Runtime Workload Profiles

Purpose: test runtime safety across different real workload shapes so the final safe limit does not overfit one easy task pattern.

Relay lead remains fixed at +3 minutes.

## Profiles

W1 READ_HEAVY
- repeated repository reads and evidence comparison
- low write frequency

W2 WRITE_CHECKPOINT_HEAVY
- many bounded useful units
- frequent necessary durable checkpoint/event writes

W3 MIXED_IO
- alternating reads and writes
- state reconstruction, evidence reconciliation, compact repairs
- closest to ordinary relay maintenance

W4 REASONING_HEAVY
- fewer tool calls
- deeper boundary estimation, failure classification, policy replay, or decision analysis

W5 MICRO_UNIT_CHAIN
- many genuine short units
- completing one unit before target never ends the turn when another useful unit exists

W6 LARGE_UNIT
- one or a few larger bounded analyses
- fewer internal stopping points

W7 CLOSE_HEAVY
- normal substantive work followed by realistic necessary close work
- checkpoint, state/evidence update, derived-view validation, and verification that the start-of-turn prearmed scheduler state remains valid
- no normal-close scheduler mutation; the same automation was already prearmed at invocation start

## Rules
- Choose a profile before each empirical probe and record workload_profile.
- Test-generated load is valid experimental work when it is deliberately selected to exercise runtime behavior and its profile is recorded.
- Allowed test load includes bounded reasoning, repeated repository reads, controlled read/write/checkpoint sequences, chains of short tasks, larger analysis units, and mixed-load sequences.
- Do not use idle waiting or sleeping merely to consume wall time. Do not perform unrecorded no-op activity.
- A safe runtime from one profile is not automatically universal.
- Candidate operating limits must later be replicated across representative profiles.
- At minimum, generalization should include MIXED_IO, MICRO_UNIT_CHAIN, and either REASONING_HEAVY or LARGE_UNIT near the candidate cap.
- If one realistic profile has a lower credible boundary, use that risk in the final cap or adopt profile-aware admission only if evidence justifies the extra complexity.

## Initial rotation
12m: W3/W5 TEST_GENERATED_MIXED_LOAD (reasoning + bounded reads/writes/checkpoints + micro-unit chaining)
14m: W3 MIXED_IO
16m: W4 REASONING_HEAVY
18m: W2 WRITE_CHECKPOINT_HEAVY
20m: W6 LARGE_UNIT

After coarse ascent, revisit candidate limits across multiple profiles before declaring a universal cap.
