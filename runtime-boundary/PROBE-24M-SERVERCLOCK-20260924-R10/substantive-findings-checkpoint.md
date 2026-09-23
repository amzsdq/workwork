# R10 substantive findings checkpoint

Probe: PROBE-24M-SERVERCLOCK-20260924-R10 / SC-A24-CLOCK+

This is an in-flight work checkpoint, not terminal duration evidence.

## Defects found and repaired

1. **Bound derivation target-loss defect.** Classifier output discarded `target_runtime_sec`, so `derive_bounds` could see a clean result but still derive no lower bound. Target identity is now preserved.
2. **Productive marker ordering crash path.** Reversed WORK_START/PRE_CLOSE could raise through interval calculation. Derived productive interval now fails closed with anomaly while START/END classification remains available.
3. **Terminal “immutability” contradiction.** Protocol said immutable terminal file could be create/update. Replaced with create-only + compare-identical retry; conflicting existing content is never overwritten.
4. **Generator ID-only pseudo-uniqueness.** V1 repeated 720 semantic Cartesian scenarios across epochs while changing IDs. Prior R10 productive count corrected fail-closed; R9 audited posthoc. Generator V2 varies target delta, marker skew, close reserve and validates semantic uniqueness.
5. **Reserve perturbation coverage bug.** Step 13 modulo 91 covered only 7 reserve values. Replaced with coprime step 17, covering every integer 30..120 before repeat.
6. **Outcome imbalance.** Broad Cartesian stress heavily weighted NON_DURATION_FAIL/CLOCK_INVALID. Added stratified evaluator quota across six result families.
7. **Harness-quality promotion gap.** Harness V2 clean-pass classifier previously required only `substantive_unit_count>0`; now it also requires explicit harness validity and positive semantic-unique evidence.
8. **Active-probe projection weakness.** `current.json` can lag with active_probe_id=null after START. Durable `start.json` without terminal now outranks stale null projection for duplicate-probe prevention.
9. **Protocol/document drift.** Master plan, evidence table, acceptance, pipeline, anomaly and boundary-derivation docs were stale relative to immutable sync V2 / R9. Reconciled or queued explicit reconciliation.

## Supporting implementations added
- semantic stress generator V2 + tests
- classifier stress evaluator + balanced stratification
- raw marker lifecycle validator + tests
- Harness V2 quality-gate tests
- 109,928-case admission-rule sensitivity grid
- strict probe execution checklist

## Current empirical caution
R9 still proves a clean 1322s server-clock survival/close observation, but its >=2048 ID-unique workload count overstated semantic decision uniqueness. Strict substantive-work lower-bound promotion is therefore being revalidated/superseded by this R10 semantic-V2 probe rather than silently trusting the old count.

R10 close reserve remains 60s for causal consistency. Prior current-protocol close sample is 57s (N=1), so reserve promotion is not justified yet.
