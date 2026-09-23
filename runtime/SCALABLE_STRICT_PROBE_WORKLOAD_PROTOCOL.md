# Scalable Strict-Probe Workload Protocol

Status: CANONICAL FOR STRICT RUNTIME BOUNDARY PROBES

## Problem fixed

The prior 22m experiments terminated when a hand-written work package ran out. That measured workload-package exhaustion rather than invocation runtime.

For strict runtime-boundary probes, `WORKLOAD_EXHAUSTED` is no longer a normal close condition before the target/close window.

## Generator rule

Use `runtime/RUNTIME_STRESS_WORKLOAD_GENERATOR.py` to generate deterministic, unique, non-duplicate work units.

Each unit exercises runtime/control evidence invariants across combinations of:
- marker validity,
- scheduler state,
- close state,
- provider/non-duration failure,
- wake observation,
- workload shape.

The source is scalable by deterministic epochs. A probe may request additional batches until the close window begins.

## What counts as substantive

A generated unit is substantive only when it produces at least one of:
- a classifier/invariant assertion,
- a state-machine transition check,
- a conflict/precedence check,
- a raw-marker integrity check,
- an admission/handoff safety check,
- a durable batch summary/fingerprint used for later regression.

A unit must have a unique stable case_id. Repeating an already completed case_id does not count.

## Runtime-loop rule

After START/WORK_START markers and scheduler pre-arm:

1. process a batch of unique units;
2. persist a compact batch checkpoint with ordinal range, pass/fail/anomaly counts, and fingerprint;
3. read authoritative server clock marker(s) only as needed for control decisions;
4. if still before PRE_CLOSE threshold, request the next unique batch;
5. never voluntarily close merely because the current batch/corpus finished;
6. stop admitting new batches only when the close policy says PRE_CLOSE should begin, or on a genuine blocking/non-duration/duration failure.

No sleeping, idle waiting, or duplicate-work padding is allowed.

## Completion condition

Normal strict probe close is driven by the timing/admission policy, not backlog exhaustion.

For target T and close reserve R:
- continue admitting useful generator batches while estimated_batch_sec + R <= remaining_budget;
- when admission fails, create PRE_CLOSE marker and enter durable close;
- after close checkpoint, create END marker.

If a batch naturally finishes early, load the next unique batch.

## Productivity accounting

Persist:
- generated_unique_units
- duplicate_units_rejected
- batches_completed
- batch_fingerprints
- anomaly_count
- assertion_count

These are workload-quality metrics. They supplement, but do not replace, server-clock productive-window measurement.
