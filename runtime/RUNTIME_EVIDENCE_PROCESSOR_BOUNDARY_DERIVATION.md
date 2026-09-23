# Runtime Evidence Processor — Boundary Derivation

## Pure aggregation contract
Input: already-classified empirical records plus explicit evidence-quality gates. Simulation/legacy records never move current strict bounds.

## Safe lower bound eligibility
A target requires:
1. valid raw START/END marker integrity and WORKED>=target;
2. clean scheduler/prearm + durable close;
3. no duration-attributable forced stop;
4. sustained substantive-work quality under the current harness (semantic/decision uniqueness, not ID-only uniqueness);
5. retrospective WAKE_OK.

A `CLEAN_PASS_WAKE_OK` label discovered later to violate a quality gate must be audited: preserve independently valid clock survival, but revalidate/supersede the strict substantive lower-bound promotion. Production operating cap still requires Phase-B replication even after a valid coarse lower bound.

## Failure boundary
DURATION_FAIL_CANDIDATE is profile-specific until controlled reproduction/refinement excludes independent causes and brackets against a lower eligible clean target.

## Non-promoting states
UNDER_TARGET, HARNESS_UNDER_TARGET, NON_DURATION_FAIL, CLOCK_EVIDENCE_INVALID, AMBIGUOUS, PENDING_WAKE, simulation and legacy evidence do not move strict bounds.

## Current state after R9 posthoc audit
- raw server-clock clean survival observation: R9 WORKED=1322s, clean close, WAKE_OK;
- R9 workload-quality audit: generator-v1 repeated 720 semantic scenarios while changing IDs, so its >=2048 ID-unique count is not equivalent to decision-unique sustained work;
- strict substantive-work safe lower bound: revalidation/supersession pending;
- failure boundary: unresolved; credible duration failure count 0;
- active coarse case: SC-A24-CLOCK+ using semantic generator V2.

A clean semantically-valid 24m+ probe with retrospective wake supersedes the R9 workload-quality concern for lower-bound purposes.

## Future aggregation output
Per profile and globally: highest eligible clean target, lowest credible/confirmed duration failure, bracket width, replication count, workload-profile coverage, semantic-workload quality, completion-envelope failures, raw marker anomalies, and posthoc evidence-quality corrections.
