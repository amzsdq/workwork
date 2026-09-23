# Probe Execution Plan

Purpose: convert the 12m+ boundary search from repeated setup/document turns into sustained, auditable substantive work.

## Problem observed
Recent invocations have mostly ended UNDER_TARGET after short instrumentation edits. Those edits improved the protocol but do not test the runtime boundary. Continuing to create one small document per invocation would optimize documentation rather than answer the research question.

The historical 18m inventory contains 18 prior unique probe IDs spread across five namespaces with no strict terminal close usable for 18m boundary promotion. Probe count is therefore a bad progress metric.

Track instead:
`terminal_decision_yield = terminally_classified_probes / started_probes`

For historical 18m boundary-promotion evidence before the active 20:00 probe, terminal-decision yield is effectively 0/18.

## Execution rule
At invocation start, resolve the active case/probe identity and immediately create the canonical GitHub START_MARKER defined by `GITHUB_SERVER_CLOCK_PROTOCOL.md`. Fetch the raw comment resource and use only its server `created_at` as the timing anchor. Before substantive work, pre-arm the next wake using `START_MARKER.created_at + target_runtime + planned_gap` and verify the returned recurring scheduler state. Then work through multiple substantive units without voluntarily closing merely because one unit finished.

Model-authored START_TS, local clock strings, or inferred elapsed values are never authoritative duration evidence.

Eligible units, in order:
1. Reproducibility audit: reconstruct target, lower bound, evidence counters, and next action from durable state; repair contradictions that would change classification.
2. Event-ledger audit: parse timing-related events and maintain compact evidence views with class, result, server-clock WORKED, useful/goal-directed work, close evidence, wake evidence, and boundary effect.
3. Failure-case test vectors: create concrete logic-only records for clean pass, under-target, duration failure, non-duration failure, ambiguous close loss, scheduler-state mismatch, and missing next wake; verify each has exactly one boundary effect.
4. Boundary estimator stress cases: test coarse/refinement rules against synthetic logic cases only; never count them as empirical runtime evidence. Hold the failure-producing profile fixed during refinement to avoid duration/profile confounding.
5. Policy-decision replay framework: define how future observed task/close samples can be replayed through P1-P4 without contaminating Phase-A evidence.
6. Completion-envelope audit: collect direct close-overhead samples and distinguish a scalar PRODUCTIVE_CAP from the task-size-aware completion frontier.
7. Reproducibility re-audit after changes.

If these units finish before target, identify and execute another genuinely necessary unit within the single research goal. Do not manufacture edits, sleep, spin, or claim elapsed time not directly observed.

## Target crossing and close
Do not use a model/local clock to decide empirical target crossing. Continue useful bounded work while the server-clock target has not been authoritatively established.

At close:
- finish the current bounded substantive unit;
- persist the durable close checkpoint with clock status pending;
- create the immutable END_MARKER;
- fetch raw END_MARKER `created_at`;
- compute `WORKED = END_MARKER.created_at - START_MARKER.created_at`;
- if WORKED >= target, evaluate clean-pass criteria; if WORKED < target, classify UNDER_TARGET unless another explicit class applies;
- synchronize terminal evidence, event ledger, state, and evidence table after END; this bookkeeping is outside WORKED;
- do not mutate the scheduler again; the next wake was already pre-armed from the authoritative START marker.

## Anti-fragmentation rule
Completing one useful unit is not a reason to hand off before target if another useful unit is available. The experiment specifically requires sustained invocation runtime, so useful units should be chained in the same invocation until the server-clock target is satisfied, genuine exhaustion of useful work, or a real blocking/risk condition.

A new same-target probe is justified only if it can materially improve terminal-decision yield or resolve a specific ambiguity. Another start/checkpoint-only probe is not progress.

## Evidence integrity
Synthetic cases validate decision logic only. They must be labeled SIMULATION/LOGIC_TEST and can never raise SAFE_LOWER_BOUND or create a FAILURE_BOUNDARY.

For new strict probes use the canonical layout in `EVIDENCE_LAYOUT.md`: `runtime-boundary/<PROBE_ID>/`. Historical namespaces remain read-only legacy evidence. `state/current.json.active_probe_id` is a recovery pointer, not empirical proof.

## Workload-profile rotation
Use `RUNTIME_WORKLOAD_PROFILES.md` for empirical probes. Record the selected workload_profile in each timing event.

Initial coarse-ascent rotation:
- 12m: W5 MICRO_UNIT_CHAIN
- 14m: W3 MIXED_IO
- 16m: W4 REASONING_HEAVY
- 18m: W2 WRITE_CHECKPOINT_HEAVY
- 20m: W6 LARGE_UNIT

Do not treat this rotation as cross-profile validation by itself. A failure discovered under a new profile must be refined with that profile held fixed. Before promoting a universal cap, retest the candidate limit across representative profiles.
