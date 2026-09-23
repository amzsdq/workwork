# Raw Pair Audit — R7 workload

During R7, raw GitHub REST resources were re-fetched for the complete marker pairs of R3, R4, and R6.

| Probe | START raw | END raw | Persisted pair | WORKED | Integrity |
|---|---|---|---|---:|---|
| R3 | 2026-09-23T13:32:22Z | 2026-09-23T13:43:14Z | exact match | 652s | RAW_PAIR_VERIFIED |
| R4 | 2026-09-23T13:58:33Z | 2026-09-23T14:10:49Z | exact match | 736s | RAW_PAIR_VERIFIED |
| R6 | 2026-09-23T15:23:53Z | 2026-09-23T15:40:08Z | exact match | 975s | RAW_PAIR_VERIFIED |

Bodies also identify the expected probe IDs and `GITHUB_SERVER_MARKER_V1`. No raw/persisted mismatch was found.

R5 has no marker pair because START creation was independently provider-blocked; it remains NON_DURATION_FAIL with clock-invalid secondary annotation and cannot affect the boundary.

This audit validates the processor's first production requirement: cached timestamp assertions for all completed server-clock pairs currently in the corpus agree with the highest-authority raw GitHub REST resources.
