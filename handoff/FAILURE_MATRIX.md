# Controlled-overlap failure matrix

- Successor wakes but predecessor is gone: remain non-authoritative until canonical `handoff-state.json` explicitly permits recovery; absence is not ownership.
- Successor READY arrives after predecessor target: predecessor closes safely; later classify missed/late handoff before continuation.
- Multiple READY records: owner accepts only intended successor for generation; others stale.
- Owner CAS transfer fails: do not claim transfer; fresh-read and classify conflict.
- Successor sees TRANSFERRED but generation/ID mismatch: remain SHADOW/stale.
- Scheduler prearm fails before substantive work: continuation at risk; no false secured-relay claim.
- SHADOW scheduler mutation: scheduler-writer conflict; sample non-clean.
- Owner authoritative write after successful transfer: stale-owner violation; sample non-clean.
- Derived shared state conflicts with immutable evidence/CAS owner record: immutable evidence + canonical owner record win; rebuild derived state.
- Exact timing endpoint exists only as model-authored file/prose timestamp: mark quantitative timing metric unresolved; do not classify exact lead/gap/overlap from it.
- Isolated provider/tool failure: classify separately; do not convert into handoff-policy failure without causal evidence.
