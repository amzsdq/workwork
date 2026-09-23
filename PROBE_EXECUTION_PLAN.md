# Probe Execution Plan

Purpose: sustain auditable substantive runtime probes without padding or repeated setup-only turns.

## Execution rule
At invocation start:
1. resolve fresh active case/incomplete probe;
2. create canonical GitHub START_MARKER;
3. fetch raw server created_at;
4. prearm same recurring automation for `START_MARKER.created_at + target_runtime + planned_gap` and verify returned state;
5. persist start evidence;
6. work through multiple genuinely useful units without closing merely because one unit finished.

Model/local START/elapsed values are never authoritative duration evidence.

## Genuine workload corpus
Eligible units include, when still unresolved/useful:
1. fresh state/evidence reproducibility audit;
2. event-ledger vs current-state vs evidence-table reconciliation;
3. strict clock-schema contamination audit across all active protocols;
4. failure-classification regression vectors including CLOCK_EVIDENCE_INVALID;
5. boundary estimator/profile-confounding review;
6. completion-envelope two-endpoint audit and current-vs-legacy sample separation;
7. policy replay timing-source/authority validation;
8. handoff control-path existence and generation-fencing audit;
9. future handoff/parallel timing-authority audit;
10. rollback-layer separation audit;
11. legacy artifact qualification where it could be mistaken for current strict evidence;
12. final reproducibility re-audit after repairs.

Do not repeat already-settled validation solely to consume time. A document edit counts only when it repairs a material inconsistency or creates necessary reusable control/evidence logic.

## Close/classification
A strict target is **not** declared crossed in-flight by model/local time. Continue useful bounded work until the experiment is ready to close based on genuine work availability/control safety.

At close:
- finish current bounded unit;
- persist durable close checkpoint with clock pending;
- create END_MARKER;
- fetch raw END created_at;
- compute WORKED from server START/END;
- classify WORKED >= target as candidate clean pass only if all other criteria hold; otherwise UNDER_TARGET or the applicable explicit failure class;
- terminal-sync raw evidence + event ledger + current state + evidence table after END;
- do not mutate scheduler at normal close.

## Anti-fragmentation
Completing one useful unit is not a reason to stop when another useful unit exists. Chain units until terminal classification is decision-relevant, genuine work is exhausted, or a real block/risk occurs. A new same-target probe is justified only when it resolves a specific prior defect/ambiguity.

## Evidence integrity
Synthetic logic cases never alter empirical bounds. New strict evidence uses `runtime-boundary/<PROBE_ID>/`. Current-state active pointer is recovery metadata, not proof.

## Workload rotation
Use recorded profiles. Coarse ascent historically rotated W5/W3/W4/W2/W6; future targets continue rotation, but failures must be refined profile-controlled and final cap requires representative cross-profile validation.
