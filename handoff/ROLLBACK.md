# Handoff rollback rule

Rollback controlled overlap to a non-overlapping relay when duplicate authoritative side effects, ambiguous owner, scheduler-writer collision, checkpoint loss, authority without explicit generation transfer, or repeated wake/READY failure erases utilization advantage.

A single isolated infrastructure/tool failure is classified separately.

When rollback triggers:
- preserve immutable evidence;
- stop overlap admissions;
- reinitialize/restore exactly one ACTIVE_OWNER in canonical root `handoff-state.json` using explicit generation state;
- restore a positive non-overlap wake margin;
- diagnose before resuming overlap.

Exact timing-based rollback claims (late READY, excessive handoff gap, overlap duration) require authoritative server-side timing endpoints. Safety/control violations such as duplicate owner or scheduler collision do not require timing precision to trigger rollback.
