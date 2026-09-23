# Runtime Evidence Processor — Phase B Bridge

Once Phase A identifies a server-clock candidate region, this processor should become the audit layer for cap validation rather than relying on hand-maintained summaries.

## Per-run validation tuple
- raw_pair_integrity
- recomputed_worked_sec
- target_runtime_sec
- profile
- result
- clean_close/checkpoint
- scheduler prearm verification
- retrospective wake existence
- completion-envelope sample availability
- productive evidence quality

## Cap candidate gate
For candidate C, aggregate only current-protocol marker-valid empirical runs. Initial gate remains >=5 clean runs at/near C with representative W3/W5/(W4 or W6)/W7 coverage, no unresolved duration failure at/below C, explicit safety margin, and zero unresolved raw-pair integrity mismatches.

## Why the processor matters
Manual tables are audit aids and can drift. A deterministic processor can make every cap promotion reproducible from raw evidence and expose exactly which run/profile satisfies or violates each gate.

## Phase C bridge
The same normalized records can feed P1-P4 replay, but replay outputs remain simulation-only. Empirical runtime bounds and cap validation stay separated from policy simulation.
