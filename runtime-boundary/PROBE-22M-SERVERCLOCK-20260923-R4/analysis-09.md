# R4 scheduler/clock ordering audit

## Required order

1. Resolve fresh case.
2. Create START_MARKER.
3. Fetch raw START created_at.
4. Pre-arm same automation for START + target + planned gap.
5. Validate returned recurring RRULE/enabled state.
6. Perform substantive work.
7. Persist durable close checkpoint.
8. Create END_MARKER.
9. Fetch raw END created_at and compute WORKED.
10. Synchronize terminal ledgers outside WORKED.

## R4 compliance so far

- Fresh canonical state was read first.
- START marker comment 5796189180 was created and raw server `created_at=2026-09-23T13:58:33Z` fetched.
- Same automation was pre-armed to 2026-09-23T14:23:33Z with recurring hourly RRULE and remained enabled.
- No scheduler mutation has occurred after pre-arm.
- Substantive W3 work is being recorded in bounded durable analyses.

## Potential ambiguity resolved

The phrase `START + target_runtime + planned_gap` must use the authoritative START marker server time for experimental intent. The scheduler accepts a concrete local DTSTART; the mapping for R4 is 13:58:33Z + 1500s = 14:23:33Z (23:23:33 KST). This does not make model time authoritative; it is a deterministic calculation from the GitHub server START timestamp.

## Decision

R4 scheduler/clock ordering is compliant. Preserve the pre-arm unchanged through normal close.
