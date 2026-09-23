# Runtime Stress Workload Matrix

Purpose: test runtime safety across heterogeneous genuine workload shapes without overfitting one easy pattern. Phase-A planned gap baseline remains +3m.

## Profiles
W1 READ_HEAVY — repository/evidence reads and consistency analysis, low writes.

W2 WRITE_CHECKPOINT_HEAVY — many useful bounded units with necessary durable writes; no fabricated checkpoint churn.

W3 MIXED_IO — alternating necessary reads/writes, state reconstruction, evidence reconciliation, compact repairs; primary general-purpose profile.

W4 REASONING_HEAVY — deeper boundary/failure/policy analysis with fewer tool calls; durable writes only for real results.

W5 MICRO_UNIT_CHAIN — many genuine short units chained without premature close while more useful work exists.

W6 LARGE_UNIT — one/few larger analyses with fewer internal stopping points.

W7 CLOSE_HEAVY — substantive work followed by realistic **pre-END durable close checkpoint work**, then END_MARKER. Post-END terminal ledger/state/table synchronization is measured separately as control overhead and is outside strict WORKED. No normal-close scheduler mutation.

## Discipline
- Select profile before substantive work and record it.
- Work must genuinely advance/validate the research.
- No artificial API calls, sleeps, token generation, duplicate prose, or meaningless loops for load.
- Synthetic logic cases validate logic only, never empirical runtime bounds.
- Strict duration always uses GitHub START/END server markers regardless of profile.
- Different profiles may have different safe behavior; universal cap requires representative replication.

## Generalization
Near candidate cap include at least W3, W5, and W4 or W6; W7 is required for completion-envelope validation. If one realistic profile is materially worse, use worst credible risk or profile-aware policy only when justified.

Historical coarse rotation is supporting context; post-final-clock validation must be marker-valid.
