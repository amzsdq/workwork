# R4 long-run utilization model audit

## Objective link

The primary program goal is not merely maximum survival; it is high long-run useful-work utilization with reliable continuation. Runtime length and planned gap jointly affect ideal duty cycle, while failure probability can dominate gains from longer turns.

## Deterministic baseline

With target runtime T and planned gap G, the naive no-jitter/no-failure duty-cycle proxy is:

`T / (T + G)`

At G=3m:
- 10m -> 76.9%
- 15m -> 83.3%
- 20m -> 87.0%
- 22m -> 88.0%
- 24m -> 88.9%

The marginal utilization gain shrinks as T grows. Therefore once a credible failure boundary appears, operating very near the absolute maximum may be inferior to a slightly lower cap if close/continuation risk rises sharply.

## Research consequence

Phase A should still locate the boundary rather than stop at 22m, because the safety margin cannot be evidence-based without an upper failure region. Phase B then determines whether the practical cap should sit materially below that boundary.

## Handoff implication

The overlap candidate can reduce effective idle time further than simply increasing T. This reinforces the sequencing: first establish a safe per-invocation envelope, then optimize handoff overlap. Otherwise runtime risk and handoff benefit become confounded.
