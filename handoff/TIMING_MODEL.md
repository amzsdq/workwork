# Handoff timing model

Successor lead must cover successor preparation plus predecessor safe-unit tail after READY. A quickly prepared successor can still wait on a long indivisible predecessor unit.

Operational implication: optimize unit granularity together with lead. Near handoff, prefer bounded substantive units whose expected tail is compatible with remaining lead, without replacing real work with padding.

EARLY_READY_HANDOFF remains: after valid READY, admit no new ordinary unit; finish current safe unit, checkpoint, transfer.

Quantitative preparation time, unit-tail duration, transfer latency, overlap, and handoff gap require authoritative server-side timing endpoints. Model-authored READY/start/transfer timestamps are not empirical timing. Without authoritative endpoints, only qualitative ordering/control correctness is established.

Reduce lead only after repeated clean authoritative observations show preparation + tail fits the smaller lead with margin.
