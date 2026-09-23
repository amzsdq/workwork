# Policy Utility Model

Purpose: keep Phase B/C optimization aligned with long-run useful-work utilization rather than longest runtime. Analytical aid only; never empirical boundary evidence.

## Timing discipline
Strict invocation duration is server-marker WORKED. Actual idle gap, wake lateness, and quantitative overlap may enter utility calculations only when their endpoints are authoritative/trustworthy. Planned gap is never substituted for actual idle gap.

Legacy pre-server-clock timing may appear only in explicitly labeled sensitivity analysis.

## Productive-work framing
Let:
- W = useful/goal-directed work delivered, direct where possible or explicitly labeled proxy/window;
- p_close = clean durable close probability from eligible evidence;
- p_wake = continuation observation probability;
- G_actual = authoritative observed idle gap when available;
- failure_penalty = observed recovery cost when enough evidence exists.

A conceptual utility is:
`U = p_close * p_wake * W / (cycle_wall_time + failure_penalty)`

Do not calculate a precise value when wall-time components are not authoritatively measured.

## Historical sensitivity only
Earlier raw-duration models/tables remain historical sensitivity aids and cannot select final cap/gap because they assumed runtime was productive and used pre-final-clock timing.

## Phase C comparison
Compare useful-work delivery, clean close, continuation, strict WORKED overshoot, lost finalization, early-handoff waste, control overhead, estimate error, and profile robustness. Quantitative wall-clock utilization requires authoritative timing inputs.

## Admission framing
P3/P4 require predicted remaining budget for:
`estimated_next_task + pre_end_close_reserve + safety_margin`.

An in-flight control elapsed estimate may guide admission but is not strict WORKED. Final empirical outcome is reconciled after END_MARKER. Hard cap/reserve/margin come from direct evidence, not this model.

## Gap selection
After cap stabilization, compare gaps using authoritative actual-idle/wake/overlap evidence plus useful work and clean-close/continuation rates. Choose the smallest gap preserving reliability; do not optimize theoretical ratios alone.
