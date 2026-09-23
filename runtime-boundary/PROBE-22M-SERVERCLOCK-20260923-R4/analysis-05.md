# R4 productive-window evidence design

## Problem

The program requires PRODUCTIVE_WINDOW characterization, but direct active seconds are not currently separable from necessary connector/tool latency. Claiming active_work_sec from model perception would violate the evidence discipline.

## Defensible evidence available in R4

1. A predeclared bounded W3 work queue exists in start.json.
2. Multiple durable repository writes after START correspond to distinct decision-relevant analyses/repairs.
3. Each analysis is tied directly to boundary inference, completion-envelope design, clock authority, or failure classification.
4. No sleep, idle wait, or no-op padding is used.

## Reporting rule

For R4:
- `active_work_sec = null` unless a direct measurement becomes available.
- `productive_ratio = null` rather than inferred from wall time.
- `substantive_unit_count` counts completed bounded decision-relevant units documented in durable evidence.
- optional goal-directed server-side span may be reported only as a span between server-side durable-work anchors, clearly distinguished from active seconds.

## Future improvement candidate

A lightweight server-authoritative productive-event lane could record selected work-unit completion markers and derive a lower-bound productive span without trusting model time. However, adding that instrumentation during Phase A may distort workload and is therefore deferred unless productive-window ambiguity blocks cap selection.

## Decision

Do not expand instrumentation now. Preserve measurement honesty and finish the survival boundary first.
