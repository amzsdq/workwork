# Policy Case-Study Notes

Purpose: external design analogies for the later handoff/admission policy. These are design inputs only, never empirical runtime evidence.

## Google SRE — load shedding / graceful degradation
Source: https://sre.google/sre-book/addressing-cascading-failures/

Relevant pattern:
- Near overload, reject/drop work that is unlikely to be worth completing rather than admitting everything and losing the whole service.
- Queue/admission control is preferable to allowing latency/resource use to grow without bound.

Mapping to this runtime:
- The invocation hard cap is analogous to a finite deadline/resource ceiling.
- Near the completion envelope, starting a unit that cannot plausibly finish plus close reserve is worse than rejecting that unit and preserving durable close.
- This supports P2/P3 semantics: graceful degradation of admitted task size near the boundary, not blind continuation until hard failure.

## Amazon Builders' Library — timeouts, retries, backoff, jitter
Source: https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/

Relevant patterns:
- Timeout values should be based on observed latency behavior rather than arbitrary constants.
- Retries can amplify load; side-effecting operations should be retry-safe/idempotent before automatic retry.
- Backoff/jitter address correlated retry load but add delay and therefore should not be introduced without a demonstrated need.

Mapping to this runtime:
- CLOSE_RESERVE and SAFETY_MARGIN should come from observed close/task distributions rather than fixed intuition.
- Durable write retries must preserve idempotency/identity; a timeout does not prove a side effect did not occur.
- Do not add retry/backoff complexity to the normal path unless observed failures justify it; this matches the program's preference for the simplest policy with equivalent reliability.

## Design implication

The external patterns support a simple ordering for Phase C:
1. P1 fixed cutoff as baseline.
2. P2 graceful degradation near cutoff.
3. P3 deadline/slack-aware admission when task-duration estimates add measurable utilization.
4. P4 adaptive logic only if observed variance makes fixed reserves materially inferior.

This is consistent with the current research principle: maximize useful work while preserving the completion envelope, and add complexity only when evidence shows practical benefit.
