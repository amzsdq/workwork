# Runtime Evidence Processor — Acceptance and Promotion Gates

Status: deterministic audit layer; never empirical clock authority by itself.

## A. Clock integrity
Raw marker resolver verifies immutable IDs, roles, probe/case identity, protocol, raw GitHub `created_at`, and monotonic START/END. Productive marker ordering is validated separately and fails closed without crashing main duration classification.

## B. Classification determinism and schema preservation
Recomputed WORKED overrides cached/model/local elapsed. Fixed input is deterministic. `target_runtime_sec` MUST survive every normalization/classification path; dropping it makes bound derivation silently unable to recover a clean target.

## C. Causal precedence
Independent provider/network/GitHub/scheduler cause cannot create a duration boundary. Forced-stop at/after target outranks contradictory clean-close flags.

## D. Duplicate/immutability safety
Identical normalized duplicates are idempotent; conflicting duplicates fail closed. Immutable terminal/event files are create-only. Retry accepts identical existing content; differing existing content is never overwritten or field-wise merged.

## E. Boundary safety
CLEAN_PASS_WAKE_OK is eligible for strict lower-bound advancement only when clock, scheduler/close, and sustained substantive-work quality gates all pass. A duration-failure candidate is not a confirmed boundary until controlled reproduction/bracketing.

## F. Productive evidence
Direct productive_ratio requires defensible active_work_sec. Server-clock WORK_START→PRE_CLOSE is separately labeled productive_window_sec. **ID uniqueness alone is not sufficient substantive evidence.** Generator workloads must be semantically/decision unique or have a persisted rationale for independent repeat evidence.

## G. Completion envelope
Current-protocol PRE_CLOSE→END samples only. Post-END projection sync is outside WORKED. Legacy samples do not increase current-protocol reserve N.

## H. Terminal synchronization V2
Raw markers -> immutable terminal -> immutable per-probe event establish durable empirical truth. current.json/events.log/EVIDENCE_TABLE are mutable CAS projections. Projection conflict cannot erase or reclassify valid terminal evidence.

## I. Regression corpus
Must reproduce R3=652 UNDER_TARGET, R4=736 UNDER_TARGET, R5=NON_DURATION_FAIL, R6=975 UNDER_TARGET, R7=251 UNDER_TARGET, and R9 raw intervals (WORKED 1322, prearm 8, productive 1257, close 57) plus wake transition. R9's later generator-v1 semantic-repeat audit must remain visible: its clock survival is valid, but strict sustained-substantive promotion requires revalidation/supersession.

Synthetic tests include exact target, forced-stop precedence, reversed/missing markers, recorded mismatch, provider precedence, productive-marker reversal, duplicate conflict, pending wake, target-field preservation, and semantic generator uniqueness/coverage.

## J. Current implementation status
- target-preserving pure classifier implemented;
- productive-marker invalid ordering now fails closed rather than raising through classification;
- regression dataset schema v3 includes R9;
- semantic generator V2 varies target delta, marker skew, close reserve and validates semantic uniqueness;
- close-reserve perturbation covers all integer values 30..120 before repeat;
- semantic stress evaluator and admission sensitivity grid implemented;
- terminal sync protocol upgraded to create-only immutable truth + CAS projections.

## K. Promotion gate
Processor can be the preferred deterministic audit layer, but raw GitHub resources remain clock Source of Truth. No processor output alone promotes OPERATING_CAP; Phase-B repeated clean evidence and profile coverage remain mandatory.
