# Transfer atomicity

The GitHub content update of the owner record is the authority linearization point for this experiment.

Before that update succeeds, predecessor remains owner and successor remains SHADOW. After it succeeds with generation increment and successor ID, predecessor is stale and successor may accept ownership.

Immutable transfer/accepted evidence documents what happened but does not itself create authority. This avoids a split-brain interval caused by treating separate evidence files as simultaneous state changes.

Because the owner-record update and evidence creation are not one transaction, recovery must always fresh-read the owner record first. Missing transfer evidence after a successful owner-record update is an observability defect to repair, not permission for the predecessor to resume authority.
