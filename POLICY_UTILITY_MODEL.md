# Policy Utility Model

Purpose: keep Phase B/C optimization aligned with long-run useful-work utilization rather than raw longest runtime. This is an analytical aid, not empirical runtime evidence.

## Baseline
Wake scheduling is pre-armed at turn start.
Initial planned gap: `G_plan = 3 minutes`.
Prior operating baseline: `T0 = 10 minutes`.
The actual idle gap is not fixed: `G_actual = next_start - prior_close`.
If close occurs after the target, `G_actual < G_plan`. Therefore optimization must use observed actual idle gap, not only the planned value.

## Productive-work correction
Raw runtime `T` is not the optimization numerator. Let:
- `W(T)` = useful/goal-directed work delivered during an invocation at target class T, measured directly where possible or represented by an explicitly labeled proxy/window when direct active seconds are inseparable from necessary tool I/O;
- `p_close(T)` = probability of clean durable close;
- `p_wake(T)` = probability that the prearmed continuation is retrospectively observed;
- `G_actual` = observed idle gap after close;
- `R` = observed/estimated recovery penalty after failed continuation when enough evidence exists.

A minimal expected-useful-work framing is:

`U(T) = p_close(T) * p_wake(T) * W(T) / (T + G_actual + failure_penalty)`

where `failure_penalty` must eventually be derived from observed recovery behavior rather than an invented constant.

This prevents a low-density 18m survival run from appearing superior to a dense 16m run merely because it remained alive longer.

## Historical simplified model
The earlier exploratory model used raw active duration:

`U_legacy(T) = p(T)*T / (T + G_actual + (1-p(T))*R)`

It remains useful only as a historical sensitivity calculation. It must not select the final cap because it assumes runtime is productive work.

The previous fixed-3m table is likewise only a historical comparison. Under pre-arm mode, recompute comparisons from observed `G_actual`; do not treat planned 3m as actual idle time.

| T | legacy p(T) needed to beat 10m baseline |
|---|---:|
| 12m | 96.78% |
| 14m | 94.34% |
| 16m | 92.44% |
| 18m | 90.91% |
| 20m | 89.66% |

These thresholds are sensitivity aids only and are not runtime-boundary or policy-promotion evidence.

## Phase C implication
Policy selection should compare at least:
- observed useful-work / wall-clock time,
- goal-directed-window / wall-clock time when direct active work is not separable,
- substantive unit density as a secondary cross-check,
- clean-close probability,
- wake continuation probability,
- close/recovery overhead,
- overshoot probability,
- early-handoff waste.

A policy that reaches a longer average active duration but performs sparse useful work or loses finalization often can be worse than a shorter policy.

## Admission framing
For P3/P4, an admission decision is safe only when the predicted remaining budget covers all of:

`estimated_next_task + close_overhead + safety_margin`

Therefore the practical rule is:

`continue iff elapsed + estimated_next_task + close_overhead + safety_margin < hard_cap`

The model does not set `hard_cap`, `close_overhead`, or `safety_margin`; those must come from direct timing evidence.

## Gap-selection implication
After the runtime cap is sufficiently characterized, compare planned gaps using:
- actual idle gap distribution,
- useful work delivered per cycle,
- clean close probability,
- wake continuation probability,
- overlap/concurrency rate,
- long-run useful-work / wall-clock time.

Choose the smallest planned gap that preserves reliability; a smaller planned gap is not better if it creates overlap or close loss.

## Anti-bias rule
Do not choose a production cap or gap solely from theoretical ratios. Boundary evidence, productive-work evidence, observed actual idle gaps, and repeated clean closes/wakes dominate the model.
