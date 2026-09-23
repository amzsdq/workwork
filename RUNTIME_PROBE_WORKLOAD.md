# Runtime Probe Workload

Purpose: provide genuine bounded research work that can sustain timing probes without padding.

## Work units
A probe may chain still-useful units until target, genuine exhaustion, or a real block/risk.

1. Evidence integrity audit
- Reconcile server-clock protocol, master plan, decision rule, current state, event ledger, and evidence table.
- Repair only contradictions that can change classification/recovery.

2. Clock-schema hardening
- Ensure every strict timing schema uses START/END raw GitHub server markers for WORKED.
- Find and remove accidental reliance on model/local timestamps.
- Preserve secondary completion/control instrumentation without letting it override WORKED.

3. Failure-classification regression
- Validate clean pass, under-target, duration failure, non-duration failure, ambiguous close loss, scheduler mismatch, missing wake, and CLOCK_EVIDENCE_INVALID.
- Ensure each has exactly one boundary effect.

4. Boundary estimator review
- Check coarse/refinement rules for target/profile confounding and false promotion.
- Verify only marker-valid clean/duration-fail evidence moves strict bounds.

5. Completion-envelope audit
- Separate durable close checkpoint, END marker, and post-END ledger synchronization.
- Track close/control overhead only when directly observable and clock-compatible.
- Keep legacy close samples labeled legacy/supporting.

6. Policy replay logic
- Prepare P1-P4 replay using observed samples without contaminating Phase A.
- Compare early-handoff waste vs overshoot/close risk only with available evidence.

7. Handoff control-path audit
- Verify one canonical owner record, generation fencing, READY acceptance, scheduler-writer rule, and rollback.
- Future quantitative handoff timing must use authoritative server-side endpoints; model file timestamps do not qualify.

8. Rollback policy audit
- Ensure runtime-cap rollback, wake-layer rollback, productivity diagnosis, and gap rollback remain causally separated.

9. Reproducibility audit
- Verify another worker can reconstruct current case, target, clock invariant, and exact next action from durable state only.

10. Legacy contamination audit
- Locate pre-server-clock artifacts that could be mistaken for current strict evidence and label/qualify them without rewriting historical raw events.

## Discipline
- Never sleep/spin or create meaningless reads/writes to consume time.
- Document edits count only when they materially improve measurement, classification, continuation safety, control correctness, or reproducibility.
- If genuine units exhaust before target, close honestly as UNDER_TARGET.
- Strict target crossing is determined only after END_MARKER by server-clock WORKED; model/local clocks do not declare it.
