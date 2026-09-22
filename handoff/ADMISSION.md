# Handoff-window task admission

Before successor READY, the owner should continue useful work. Near the expected successor wake, admission should account for expected unit duration so an oversized new unit does not dominate transfer latency.

Baseline rule for the experiment:
- outside handoff window: admit normal substantive units;
- inside handoff window but before READY: prefer bounded substantive units whose expected duration is below the remaining lead/safety budget;
- after READY: admit no new ordinary unit; finish only the in-flight safe unit and transfer.

Record estimated unit duration and actual tail where practical. Later compare this simple bounded-window rule against a more adaptive estimator only if evidence shows meaningful benefit.
