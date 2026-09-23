# Runtime Evidence Table

Strict timing authority: raw GitHub START/END created_at. Strict substantive promotion also requires valid Harness V2 semantic-work quality.

| Probe | WORKED | Productive | Close | Result | Boundary effect |
|---|---:|---:|---:|---|---|
| R3 | 652s | — | — | UNDER_TARGET | NONE |
| R4 | 736s | — | — | UNDER_TARGET | NONE |
| R5 | n/a | — | — | NON_DURATION_FAIL | NONE |
| R6 | 975s | — | — | UNDER_TARGET | NONE |
| R7 | 251s | — | — | UNDER_TARGET | NONE |
| R8 | 182s | — | — | UNDER_TARGET | NONE |
| R9 | 1322s | 1257s | 57s | clean clock/close + WAKE_OK; posthoc workload-quality taint | 22m02s survival retained; strict substantive promotion revalidation pending |
| R10 | **1402s** | **1376s** | **14s** | **UNDER_TARGET, Harness V2 valid** | **NONE — admission/close reserve mismatch, not duration failure** |
| OP-CAP-14M-VALIDATION-01 | **865s** | **829s** | **16s** | **CLEAN_PASS_WAKE_OK, Harness V2 valid** | **14m operational-cap validation clean run 1/5 confirmed** |

## OP-CAP-14M-VALIDATION-01 authoritative markers
- START `2026-09-23T19:45:09Z` (`2026-09-24 04:45:09 KST`)
- WORK_START `2026-09-23T19:45:29Z` (`2026-09-24 04:45:29 KST`)
- PRE_CLOSE `2026-09-23T19:59:18Z` (`2026-09-24 04:59:18 KST`)
- END `2026-09-23T19:59:34Z` (`2026-09-24 04:59:34 KST`)
- WORKED 865s (14m25s), target 840s
- productive window 829s (13m49s), close overhead 16s, prearm overhead 20s
- generated unique units minimum 750,000,000; stress chunks 19; duplicate units rejected 0
- scheduler WRITE_OK/STATE_OK; durable clean close; forced stop/timeout false
- retrospective successor wake observed: WAKE_OK
- operational-cap validation progress: **1/5 clean confirmed runs**

## R10 authoritative markers
- START `2026-09-23T19:13:18Z` (`2026-09-24 04:13:18 KST`)
- WORK_START `2026-09-23T19:13:30Z` (`2026-09-24 04:13:30 KST`)
- PRE_CLOSE `2026-09-23T19:36:26Z` (`2026-09-24 04:36:26 KST`)
- END `2026-09-23T19:36:40Z` (`2026-09-24 04:36:40 KST`)
- WORKED 1402s (23m22s), target 1440s, shortfall 38s
- productive window 1376s (22m56s), close overhead 14s, prearm 12s
- semantic unique minimum 100,000; logical batches minimum 391; duplicate/collision observed 0
- scheduler WRITE_OK/STATE_OK; durable clean close; forced stop/timeout false

R10 shows the corrected harness can sustain semantically useful work, but the provisional 60s close reserve caused normal close too early because actual close overhead was only 14s. This does **not** establish a runtime failure boundary.

Current-protocol close samples: R9=57s (workload-quality tainted for substantive promotion but close interval clock-valid), R10=14s (Harness V2 valid), OP-CAP-14M-VALIDATION-01=16s (Harness V2 valid). Reserve remains unpromoted.
