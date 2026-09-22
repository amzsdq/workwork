# Handoff rollback rule

Rollback controlled overlap to a non-overlapping relay when any of these recur or cannot be cleanly classified:
- duplicate authoritative side effects,
- ambiguous active owner,
- scheduler-writer collisions,
- checkpoint loss at transfer,
- successor taking authority without an explicit transfer,
- repeated successor wake/READY failures that erase the utilization advantage.

A single isolated infrastructure/tool failure is classified separately and does not by itself invalidate the policy.

When rollback is triggered, preserve immutable evidence, stop overlapping admissions, restore one ACTIVE_OWNER with a positive non-overlap wake margin, and diagnose before resuming overlap trials.
