# R4 handoff-candidate isolation review

## Scope

The user-approved overlap handoff concept is preserved, but Phase A must not accidentally convert it into a runtime variable.

## Candidate retained

Baseline concept:
- 15m owner work target,
- successor wake near +12m,
- successor begins as SHADOW,
- single scheduler owner,
- atomic/generation-fenced ownership transfer,
- next successor scheduled from OWNER_ACTIVATED_AT.

## Why no live test now

A live overlap test during the 22m boundary probe could introduce:
- concurrent scheduler/control writes,
- additional GitHub state contention,
- successor-induced close behavior,
- ambiguous forced-stop causality,
- altered useful-work mix.

Any of these would weaken inference about the single-invocation runtime boundary.

## Future measurement correction

The handoff candidate currently contains model/local timing examples from pre-server-clock research. When Phase C begins, quantitative promotion should use server-authoritative markers for owner activation, successor ready/transfer, and first substantive work wherever feasible. Historical +4/+21/+168s wake observations remain supporting context, not sufficient final timing authority under the new invariant.

## Decision

No change to candidate status: KEEP / TEST / NOT_PROMOTED. Continue Phase A only.
