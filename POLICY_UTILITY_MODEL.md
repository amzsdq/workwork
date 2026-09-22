# Policy Utility Model

Purpose: keep Phase B/C optimization aligned with long-run useful-work utilization rather than raw longest runtime. This is an analytical aid, not empirical runtime evidence.

## Baseline
Wake scheduling is pre-armed at turn start.
Initial planned gap: `G_plan = 3 minutes`.
Prior operating baseline: `T0 = 10 minutes`.
The actual idle gap is not fixed: `G_actual = next_start - prior_close`.
If close occurs after the target, `G_actual < G_plan`. Therefore optimization must use observed actual idle gap, not only the planned value.

## Minimal model
For candidate active duration `T`, observed/expected actual idle gap `G_actual`, clean-close probability `p(T)`, and an illustrative failed-close recovery penalty `R`, use:

`U(T) = p(T)*T / (T + G_actual + (1-p(T))*R)`

This deliberately penalizes longer turns when clean-close probability falls. It is not a claim that failure always loses all work; actual observed recovery semantics should replace the simplified term when enough evidence exists.

The previous fixed-3m table is only a historical comparison. Under pre-arm mode, recompute comparisons from observed `G_actual`; do not treat planned 3m as actual idle time.

| T | p(T) needed to beat 10m baseline |
|---|---:|
| 12m | 96.78% |
| 14m | 94.34% |
| 16m | 92.44% |
| 18m | 90.91% |
| 20m | 89.66% |

Interpretation: a longer target can tolerate some loss of reliability and still improve expected utilization, but the acceptable loss must be measured rather than assumed. These thresholds depend on the recovery-loss model and therefore must not be used as runtime-boundary evidence.

## Phase C implication
Policy selection should compare at least:
- observed useful-work / wall-clock time,
- clean-close probability,
- wake continuation probability,
- close/recovery overhead,
- overshoot probability,
- early-handoff waste.

A policy that reaches a longer average active duration but loses finalization often can be worse than a shorter policy.

## Admission framing
For P3/P4, an admission decision is safe only when the predicted remaining budget covers all of:

`estimated_next_task + close_overhead + safety_margin`

Therefore the practical rule is:

`continue iff elapsed + estimated_next_task + close_overhead + safety_margin < hard_cap`

The model does not set `hard_cap`, `close_overhead`, or `safety_margin`; those must come from direct timing evidence.

## Gap-selection implication
After the runtime cap is sufficiently characterized, compare planned gaps using:
- actual idle gap distribution,
- clean close probability,
- wake continuation probability,
- overlap/concurrency rate,
- long-run useful-work / wall-clock time.

Choose the smallest planned gap that preserves reliability; a smaller planned gap is not better if it creates overlap or close loss.

## Anti-bias rule
Do not choose a production cap or gap solely from theoretical ratios. Boundary evidence, observed actual idle gaps, and repeated clean closes/wakes dominate the model.