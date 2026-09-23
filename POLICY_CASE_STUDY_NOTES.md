# Policy Case-Study Notes

Purpose: external design analogies for later handoff/admission policy. Design inputs only, never empirical runtime evidence.

## Google SRE — load shedding / graceful degradation
Pattern: reject work unlikely to complete usefully under finite resource/deadline pressure rather than admit everything and lose the service.

Mapping: near completion envelope, reject a unit that cannot plausibly fit with pre-END close reserve. Supports P2/P3 semantics.

## Google Aequitas — measured adaptive admission
Pattern: adapt admission from measured completion behavior rather than static intuition; tail behavior matters.

Mapping: P4 is justified only from enough **current-protocol trustworthy completion evidence**. Legacy/model timing must not drive adaptive reserve as if current empirical data.

## Borg / Autopilot analogy — utilization with explicit slack
Pattern: high utilization retains explicit reliability slack and adjusts from observations.

Mapping: CLOSE_RESERVE + SAFETY_MARGIN is intentional slack. Shrink/expand only from current trustworthy evidence; do not treat the provisional 60s configuration or legacy 32s sample as promoted reserve.

## Amazon Builders' Library — timeout/retry/backoff/jitter
Pattern: derive timeouts from observed latency; retries can amplify load; side effects need idempotency.

Mapping: reserve/margin derive from observed current-protocol behavior. Durable write retries must preserve identity/idempotency. Do not add backoff/retry complexity without observed need.

## Design implication
Phase C ordering remains P1 -> P2 -> P3 -> P4. Add complexity only when authoritative empirical evidence shows practical benefit. External analogies never set runtime cap, timing threshold, lead, or reserve.
