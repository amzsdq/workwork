# Controlled-overlap failure matrix

- Successor wakes but predecessor is gone: successor remains non-authoritative until durable ownership state explicitly permits recovery; do not infer ownership from absence alone.
- Successor READY arrives after predecessor target: predecessor closes safely; later invocation must classify the missed/late handoff before continuing.
- Multiple successor READY files: owner accepts only the intended successor for its generation; all others are stale observers.
- Owner CAS transfer fails: owner must not claim transfer succeeded. Fresh-read and classify conflict; avoid duplicate side effects.
- Successor sees TRANSFERRED but generation/ID mismatch: remain SHADOW/stale; do not work authoritatively.
- Scheduler prearm fails before substantive work: classify continuation at risk and persist evidence; do not pretend the relay is secured.
- Shadow scheduler mutation detected: mark scheduler-writer conflict and sample non-clean.
- Owner continues authoritative work after successful transfer: stale-owner violation; sample non-clean.
- Shared derived state conflicts with immutable evidence: immutable per-invocation evidence and CAS owner record win; rebuild derived state later.
