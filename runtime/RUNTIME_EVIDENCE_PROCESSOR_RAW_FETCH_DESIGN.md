# Runtime Evidence Processor — Raw Marker Fetch Design

## Goal
Make classification independently reproducible from marker comment IDs rather than trusting persisted timestamp copies.

## Resolution algorithm
For every strict probe with marker IDs:
1. GET `https://api.github.com/repos/amzsdq/workwork/issues/comments/<start_id>`.
2. Verify returned `id == start_id` and body identifies expected `probe_id` / `RUNTIME_START_MARKER`.
3. Read server `created_at`; ignore model/local timestamp fields.
4. Repeat for END comment.
5. Verify END body identifies same probe/case and `RUNTIME_END_MARKER`.
6. Compute `WORKED = END.created_at - START.created_at`.
7. Compare raw timestamps and recomputed WORKED against persisted close evidence. Any mismatch is an integrity anomaly; raw REST values win.

## Integrity states
- RAW_PAIR_VERIFIED: both resources fetched, IDs/body identity match, timestamps valid.
- RAW_PAIR_MISMATCH: fetched resources exist but identity/persisted copy differs; quarantine for manual reconciliation, no bound promotion.
- RAW_PAIR_UNAVAILABLE: resource/provider unavailable; do not infer from model time.
- LEGACY_NO_RAW_PAIR: pre-protocol evidence, supporting only.

## Why this matters
Persisted `start_marker_created_at`/`end_marker_created_at` are convenient cached evidence, but the declared hierarchy says raw GitHub marker resources are the highest authority. The processor must therefore treat cached values as assertions to verify, not as an alternate clock.

## Batch behavior
- Fetch each unique comment ID once per processing run.
- Cache by comment ID only for that run.
- Never overwrite historical raw close evidence automatically on mismatch.
- Emit a reconciliation report and leave strict bounds unchanged until the mismatch is resolved.

## Phase-B extension
Near an operating-cap candidate, batch verification should also compute marker-valid run count, profile coverage, and any integrity mismatch rate. Cap promotion requires zero unresolved raw-pair mismatches in the validation set.
