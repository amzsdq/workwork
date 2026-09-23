# Runtime Research Master Plan

Status: CANONICAL EXECUTION ROADMAP
Repo: amzsdq/workwork

## 1. Research objective
Answer empirically:
1. maximum safe substantive-work duration per invocation;
2. simplest reproducible handoff/admission policy near that limit with high long-run useful-work utilization and no material increase in forced-stop/run-out risk.

Evidence authority:
1. raw GitHub START/END marker REST resources for strict WORKED;
2. raw per-probe evidence;
3. state/events.log;
4. state/current.json;
5. derived summaries.

## Final clock invariant
`WORKED = END_MARKER.created_at - START_MARKER.created_at`

Only raw GitHub server marker `created_at` values are strict duration evidence. Model/local time strings are non-authoritative. Invalid marker pair => CLOCK_EVIDENCE_INVALID, no boundary effect. Pre-protocol timing is legacy supporting only.

## Anti-drift / terminal sync
Resolve fresh active case and incomplete evidence before work. Every repeat must add decision value. Terminal classification synchronizes raw terminal evidence + event ledger + current state + evidence table and then re-reads agreement. Provider/sync failure is NON_DURATION_FAIL.

No padding. A probe needs a predeclared genuinely useful workload corpus large enough for the class.

## Three axes
A. SURVIVAL_BOUNDARY — strict WORKED + causal termination/close outcome.
B. PRODUCTIVE_WINDOW — direct active seconds only when defensible; otherwise labeled goal-directed/substantive evidence.
C. COMPLETION_ENVELOPE — derive cap/cutoff/reserve/admission from direct evidence.

## Phase A — boundary search
- LEGACY_EXPLORATORY_LOWER_BOUND = 20m
- SERVER_CLOCK_SAFE_LOWER_BOUND = unresolved
- FAILURE_BOUNDARY = unresolved
- active target = 22m
- planned_gap = +3m
- profile = W3 MIXED_IO

Server-clock attempts:
- R3 = 652s UNDER_TARGET: useful migration/audit queue exhausted.
- R4 = 736s UNDER_TARGET: stopping defect corrected, but protocol-analysis workload saturated.
- R5 = CLOCK_EVIDENCE_INVALID / NON_DURATION_FAIL: mandatory START_MARKER creation was provider-blocked; no boundary effect.
- R6 = ACTIVE: START marker succeeded at raw server `created_at=2026-09-23T15:23:53Z`, scheduler prearm verified for START+22m+3m, and a materially larger W3 corpus is executing. The corpus includes cross-document clock semantics, classification regression, completion-envelope reconciliation, handoff control-path integrity, legacy contamination, reproducibility, and terminal reconciliation.

R6 has already produced decision-relevant repairs including server-clock schema alignment and discovery/repair of a nonexistent `handoff/control.json` assumption; canonical future handoff authority is root `handoff-state.json`. These are genuine research/control tasks, not padding.

After strict 22m clean PASS + retrospective WAKE_OK, continue +2m coarse ascent with rotated profiles. First credible duration failure creates profile-specific F; refine to about 1m.

## Phase B — operating-cap validation
Require at least 5 clean marker-valid runs at/near candidate, no unresolved duration failure at/below candidate, scheduler verification, durable close, continuation observation where measurable, and representative W3/W5/(W4 or W6)/W7 coverage.

## Phase C — handoff/admission
Compare P1-P4, simplest practically equivalent wins. Overlap candidate remains KEEP/TEST/NOT_PROMOTED. Future exact handoff lead/gap metrics require authoritative server-side timing; legacy model/file timestamps are supporting-only.

## Phase D — planned-gap optimization
After runtime/cap stabilizes: +3m -> +2m -> +1m if reliable.

## Phase E — deferred parallel
PARALLEL-A14-B4-02 remains deferred/supporting-only until Phase A/B gate.

## Study cases
### SC-A22-CLOCK-01
PASS: valid marker pair, WORKED >=1320s, sustained substantive W3 work, durable close checkpoint, scheduler WRITE_OK/STATE_OK, no duration-attributable forced stop. Then CLEAN_PASS_PENDING_WAKE; retrospective WAKE_OK advances SERVER_CLOCK_SAFE_LOWER_BOUND=22m and next case.

UNDER_TARGET: valid marker pair, WORKED <1320s, boundary unchanged; repeat only after correcting cause.
CLOCK_EVIDENCE_INVALID/NON_DURATION_FAIL: no boundary effect.
DURATION_FAIL_CANDIDATE: profile-controlled bracket/refinement.

### SC-A24-CLOCK+
Prior 22m server-clock clean pass + wake; target +2m, rotated profile.

### SC-AR-*
~1m profile-controlled refinement after first credible duration failure.

### SC-B-CAP-*
Repeated representative validation.

### SC-C-POLICY-*
Replay then live.

### SC-D-GAP-*
3m -> 2m -> 1m.

### SC-E-PARALLEL-01
Deferred until Phase A/B gate.

## Current execution pointer
CURRENT_CASE_ID = SC-A22-CLOCK-01
ACTIVE_PROBE_ID = PROBE-22M-SERVERCLOCK-20260924-R6
LATEST_TERMINAL_PROBE = PROBE-22M-SERVERCLOCK-20260923-R5
LATEST_TERMINAL_RESULT = CLOCK_EVIDENCE_INVALID / NON_DURATION_FAIL

Immediate objective: continue R6's predeclared genuine W3 corpus. Do not start a duplicate probe. At close, persist durable close checkpoint, create END_MARKER, fetch raw server created_at, compute strict WORKED, then terminal-sync all views.

## Final completion gate
Program completes only when server-clock safe lower bound, failure boundary or unresolved status, operating/productive caps, cutoff/hard cap, close overhead, safety margin, next-task admission, validation confidence/count, workload coverage, rollback, and selected planned gap are traceable to durable evidence.
