# Policy Utility Model

Purpose: keep Phase B/C optimization aligned with long-run useful-work utilization rather than raw longest runtime. This is an analytical aid, not empirical runtime evidence.

## Baseline
Fixed relay lead/gap control: `G = 3 minutes`.
Prior operating baseline: `T0 = 10 minutes`.
Idealized no-failure baseline utilization: `U0 = 10/(10+3) = 0.7692`.

## Minimal model
For candidate active duration `T`, clean-close probability `p(T)`, and an illustrative failed-close recovery penalty `R`, use:

`U(T) = p(T)*T / (T + G + (1-p(T))*R)`

This deliberately penalizes longer turns when clean-close probability falls. It is not a claim that failure always loses all work; actual observed recovery semantics should replace the simplified term when enough evidence exists.

With `G=3m` and illustrative `R=3m`, the approximate minimum clean-close probability needed merely to beat the idealized 10m baseline is:

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

## Anti-bias rule
Do not choose a production cap solely because theoretical `T/(T+3)` improves. Boundary evidence and repeated clean closes dominate the model. Use this model only after empirical timing evidence exists to compare candidate policies/caps.