# Completion Envelope Evidence

Purpose: keep close/completion evidence separate from strict target-survival evidence.

## Legacy supporting observations
| Probe/class | Historical target | Historical elapsed | Historical close observation | Scope |
|---|---:|---:|---:|---|
| 12m mixed-load canonical pass | 720s | 761s | 32s close-overhead field | LEGACY_PRE_SERVER_CLOCK_SUPPORTING |
| 14m W3 clean pass | 840s | 928s | close overhead not isolated | LEGACY_PRE_SERVER_CLOCK_SUPPORTING |
| 16m W4 clean pass | 960s | >=996s | close overhead not isolated | LEGACY_PRE_SERVER_CLOCK_SUPPORTING |

These rows are preserved for historical context only. Their elapsed/model-local timing does not establish current strict WORKED. The 32s observation may remain a low-confidence legacy secondary close-cost clue but is **not** a current-protocol sample for reserve promotion.

## Current-protocol evidence
Current protocol: GITHUB_SERVER_MARKER_V1 with authoritative WORKED ending at END_MARKER.

- Current-protocol direct pre-END close sample count: **0**.
- Current-protocol post-END sync overhead sample count: **0**.
- Therefore current-protocol CLOSE_RESERVE remains **UNKNOWN / NOT PROMOTED**.
- Configured 60s remains provisional control configuration only.
- R3/R4 clean UNDER_TARGET runs did not directly instrument a compatible pre-END close interval; do not infer one.
- R6 should preserve strict START/END marker evidence and only report close/control overhead if compatible direct endpoints are genuinely observed.

## Endpoint rule
`MEASURED_WORK_END = END_MARKER.created_at`.
Post-END terminal ledger/state/table synchronization is bookkeeping outside strict WORKED and may be measured separately as control overhead.
