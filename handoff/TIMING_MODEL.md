# Handoff timing model

The successor wake lead must cover two different intervals: successor preparation and the predecessor's remaining safe-unit tail after READY is noticed.

Measure both separately. A successor that becomes READY quickly can still experience a late authority transfer when the predecessor is inside a long indivisible unit.

Operational implication: optimize unit granularity together with successor lead. Near the expected handoff window, ACTIVE_OWNER should prefer bounded units whose expected tail is small enough to preserve the intended transfer latency, without replacing substantive work with no-op padding.

EARLY_READY_HANDOFF rule remains: after READY is observed, do not admit another ordinary unit. Finish the in-flight safe unit, checkpoint, transfer.

A lead reduction is justified only when repeated observations show preparation plus unit-tail comfortably fits the smaller lead and handoff remains clean.
