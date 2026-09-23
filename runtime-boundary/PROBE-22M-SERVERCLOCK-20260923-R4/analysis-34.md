# R4 planned-gap metric audit

## Definitions

- planned_gap = scheduled next wake - (authoritative START + target runtime)
- actual_idle_gap = successor actual start - predecessor effective work/close boundary
- overlap = predecessor remains active after successor actual start

These are distinct quantities.

## Phase A use

planned_gap is fixed at +3m to stabilize continuation while runtime target changes. It is not optimized here.

## Phase D use

After runtime/cap policy stabilizes, compare +3m, +2m, +1m while measuring:
- scheduler pre-arm verification,
- predecessor WORKED,
- clean close,
- successor wake jitter,
- actual idle gap,
- overlap/concurrency,
- continuation loss.

## Interaction with overlap handoff

The overlap candidate intentionally targets negative/near-zero effective idle by waking a SHADOW successor before owner close. That is a different policy family from merely shrinking planned_gap and should be compared only after single-owner fencing is implemented.

## R4

No planned-gap change is justified during this probe.
