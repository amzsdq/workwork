# R4 stopping-rule audit

## Valid reasons to stop this probe

- valid server-clock target reached and durable close sequence begins,
- credible forced termination/timeout prevents continuation,
- independent provider/GitHub/scheduler failure makes the probe non-interpretable,
- an actual safety/blocking condition prevents meaningful work.

## Invalid reasons

- a finite analysis list was completed,
- a convenient summary point was reached,
- model-estimated elapsed time feels sufficient,
- legacy evidence suggests 22m probably works,
- desire to reduce token/tool use while useful decision-relevant work remains.

## R3 lesson

R3 stopped for an invalid reason: its prepared workload was exhausted before the server target. R4 explicitly removes that stopping condition.

## R4 operational rule

Continue bounded decision-relevant work until the server-authoritative target condition can be established, then perform durable close -> END marker. Do not create END merely because the current analysis batch is complete.
