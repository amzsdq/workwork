# Operational Relay Policy

Status: CANDIDATE_CANONICAL
Purpose: define the operational relay semantics separately from maximum-runtime boundary research.

## Core operational rule

There is no fixed predecessor work duration.

Normal voluntary stop conditions are only:

- PROGRAM_COMPLETE
- HANDOFF_COMPLETE

A predecessor continues useful work while waiting for a successor. Wake jitter changes overlap length instead of creating idle time.

## Handoff sequence

PREDECESSOR_ACTIVE
-> SUCCESSOR_AWAKE
-> SUCCESSOR_PREPARED
-> SUCCESSOR_READY
-> TRANSFER_COMMITTED
-> SUCCESSOR_ACTIVE

The predecessor remains OWNER until TRANSFER_COMMITTED is durable.
The successor is SHADOW before transfer and does not perform OWNER-only scheduler/control writes.
The new OWNER pre-arms the next successor after transfer.

## Safety cap

A conservative operational safety cap exists only to avoid approaching forced termination.

It is not a normal stop condition and is not hard-coded here.

When the safety cap is approaching before HANDOFF_COMPLETE:
- stop admitting risky long units according to admission policy;
- persist fresh continuation/ownership checkpoint;
- remain honest that handoff did not complete;
- enter recovery/safety mode.

## Current candidate

14 minutes is a CANDIDATE conservative operating-cap class, not yet a promoted safe cap under the current strict server-clock harness.

Promotion requires repeated clean, marker-valid, semantically substantive runs across representative workload profiles.

Initial validation gate:
- >=5 clean 14m strict runs;
- valid GitHub server markers;
- sustained semantically unique substantive work;
- clean completion envelope;
- scheduler WRITE_OK / STATE_OK;
- no duration-attributable forced stop/timeout.

After 14m is validated as conservative operational cap, test successor wake lead separately.
Do not assume 15/12, +14m, or any other timing constant is final.

## Two separate research questions

1. HARD RUNTIME BOUNDARY
   Continue stress testing to determine where invocations actually become unreliable or are forced to terminate.

2. OPERATIONAL RELAY CAP
   Use a deliberately conservative point below the hard boundary that provides enough time for successor wake/preparation/handoff while keeping forced-stop risk low.

The operational cap does not need to equal the maximum surviving duration.

## Wake-lead optimization

Once the conservative operating cap is validated, derive successor wake lead from authoritative evidence:

REQUIRED_HANDOFF_LEAD =
wake_jitter_budget
+ successor_prepare_budget
+ transfer_budget
+ safety_margin

The predecessor does not stop at the nominal cap if handoff completes earlier; it stops immediately after HANDOFF_COMPLETE.
If the successor is late, the predecessor continues useful work up to the safety/recovery boundary.

## Source of invariants

Stable relay semantics come from the Workaholic plugin.
Numeric runtime values and experiment state come from repository durable state.
Automation prompts should point to these sources rather than duplicate the invariants.
