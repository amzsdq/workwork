# Runtime Workload Profiles

Purpose: test runtime safety across different genuine workload shapes so the final safe limit does not overfit one pattern. Phase-A planned gap baseline remains +3m.

W1 READ_HEAVY — repeated repository/evidence reads, low writes.

W2 WRITE_CHECKPOINT_HEAVY — many bounded useful units with frequent necessary durable writes.

W3 MIXED_IO — alternating reads/writes, state reconstruction, evidence reconciliation, compact repairs; closest to ordinary relay maintenance.

W4 REASONING_HEAVY — fewer tool calls, deeper boundary/failure/policy analysis.

W5 MICRO_UNIT_CHAIN — many genuine short units; one completed unit never ends the turn while another useful unit exists.

W6 LARGE_UNIT — one/few larger analyses with fewer internal boundaries.

W7 CLOSE_HEAVY — normal substantive work followed by realistic necessary **pre-END durable close checkpoint** work, then END_MARKER. Post-END terminal ledger/state/table synchronization and verification are separate control overhead outside strict WORKED. Scheduler was already prearmed; no normal-close scheduler mutation.

## Rules
- Choose/record profile before substantive work.
- Purposeful generated load is valid only when it genuinely advances/validates the research.
- No idle/sleep/no-op padding.
- Strict duration for every profile uses GitHub server START/END markers.
- One-profile safe runtime is not universal.
- Final generalization requires W3, W5, W4 or W6, and W7 near candidate cap under current marker-valid protocol.
- Use worst credible realistic profile unless profile-aware complexity has demonstrated utilization value.

Historical profile rotation remains supporting context; post-final-clock cap promotion requires marker-valid current evidence.
