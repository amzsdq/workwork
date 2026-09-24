# Astra Review Brief — Workwork Relay Runtime

Status: REQUEST_FOR_INDEPENDENT_REVIEW
Date: 2026-09-24
Repo: amzsdq/workwork

## Mission
Independently audit the current continuous-relay design and propose the smallest robust correction set. Do not assume existing conclusions are correct. Prefer evidence from fresh repository state and immutable/raw runtime evidence over prose summaries.

## Primary questions
1. Why did same-canonical RRULE self-renew repeatedly fall through to the next hourly occurrence?
2. Is the current wake-start prearm success condition sufficient to prevent a past/too-close DTSTART after the scheduler update returns?
3. What minimum future-time guard should be used, and should it be derived from observed scheduler/update jitter rather than hard-coded?
4. Can overlapping predecessor/successor execution remain safe under single-owner scheduler semantics, or is overlap itself creating an ownership race?
5. Does a replace-only `[TO-DO LIST FOR THIS TURN]` hot-path block materially improve continuation quality without becoming a second source of truth?
6. How should the predecessor size the successor TODO so useful work cannot exhaust before the target active duration?
7. Are runtime-boundary research and conservative operational-cap validation cleanly separated in current durable state/projections?

## Known failure pattern to verify
A prior canonical update stored a DTSTART that was already behind the update completion time. With `RRULE:FREQ=HOURLY`, the missed occurrence caused the scheduler to select the next hourly occurrence, producing an approximately one-hour idle gap. Treat this as a hypothesis to verify from evidence, not as an axiom.

## Current control principles
- Numeric experiment state comes from fresh repository durable state.
- Raw GitHub server timestamps are duration authority.
- Same canonical automation is reused; do not solve continuity by spawning replacement automations.
- Stable relay semantics belong in Workaholic; repository state owns tunable values/phase.
- Hot-path TODO is replace-only ephemeral continuation state. It must yield to fresh repository truth on conflict.
- TODO completion is not a stop condition; successor workload must include a scalable refill path.

## Audit targets
Read fresh:
- `state/current.json`
- `OPERATIONAL_RELAY_POLICY.md`
- `RUNTIME_RESEARCH_MASTER_PLAN.md`
- `GITHUB_SERVER_CLOCK_PROTOCOL.md`
- `runtime/SCALABLE_STRICT_PROBE_WORKLOAD_PROTOCOL.md`
- `runtime/TERMINAL_STATE_SYNC_PROTOCOL.md`
- latest `runtime-boundary/*` immutable evidence
- current Workaholic continuous-relay plugin source/invariants if accessible

## Required output
Produce a decision memo with:
- VERIFIED / FALSIFIED / UNRESOLVED for each primary question;
- concrete failure timeline for scheduler misses;
- minimal invariant/policy changes, explicitly separating plugin-level invariants from repo-level tunables;
- race analysis for overlap and scheduler ownership;
- assessment of the replace-only TODO design, including failure modes (stale prompt, oversized prompt, duplicated authority, successor rewrite race, finite-work exhaustion);
- recommended TODO schema and replacement timing;
- test matrix with pass/fail criteria;
- changes to reject because they add complexity without improving measured continuity/utilization.

Do not promote a hypothesis merely because it sounds architecturally clean. Require runtime evidence where feasible.