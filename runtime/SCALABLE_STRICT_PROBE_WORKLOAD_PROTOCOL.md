# Scalable Strict-Probe Workload Protocol

Status: CANONICAL FOR STRICT RUNTIME BOUNDARY PROBES

## Purpose
Strict probes measure runtime under sustained useful work. Finite backlog exhaustion is not a normal close trigger before PRE_CLOSE, but manufacturing different IDs for semantically identical deterministic work is also prohibited.

## Generator rule
Use `runtime/RUNTIME_STRESS_WORKLOAD_GENERATOR.py`. Generator V2 requires both:
- identity uniqueness: stable case_id has not appeared before in the probe;
- semantic uniqueness / decision value: the scenario changes at least one causal/test dimension or supplies justified repeat evidence that can alter confidence.

Generator V2 varies runtime/control states plus numeric epoch conditions (`target_delta_sec`, `marker_skew_sec`, `close_reserve_sec`). `validate_semantic_uniqueness` is a required harness check for generated batches.

## What counts as substantive
A unit must produce a classifier/invariant assertion, state-machine transition check, conflict/precedence check, raw-marker integrity check, admission/handoff safety check, or regression evidence with actual decision value.

A new ID alone does not make repeated deterministic work substantive. Exact semantic repeats are excluded from `semantic_unique_units`; if repeat trials are intentionally used for statistical/reproducibility evidence, the repeat rationale and independent varying/observable factor must be persisted.

## Runtime loop
After START, scheduler prearm, and WORK_START:
1. process a semantically unique batch;
2. persist ordinal range, identity-unique count, semantic-unique count, assertions/anomalies, and fingerprint;
3. create/raw-fetch PROGRESS_MARKER when admission/close control needs authoritative elapsed;
4. compute control elapsed only from PROGRESS.created_at - START.created_at;
5. while server-clock admission permits work, load the next semantically unique batch;
6. never close because a finite corpus ended;
7. stop admitting only when timing/admission enters PRE_CLOSE or a genuine block/failure/user stop occurs.

No sleeping, idle waiting, ID-only mutation, or duplicate-work padding.

## Target-reaching admission rule
For a strict target T, a provisional close reserve MUST NOT cause normal substantive work to stop before T. The reserve is not credited toward target attainment.

Normal target close is eligible only after an authoritative raw GitHub PROGRESS marker proves `PROGRESS.created_at - START.created_at >= T` while substantive work has remained valid through that sample. Once that condition is observed, stop admitting new substantive batches, create/raw-fetch PRE_CLOSE, perform durable close, then create/raw-fetch END.

A separately configured emergency close cap may force early close when required to preserve durable state or avoid a known hard execution boundary. If it fires before T, classify the probe as safety/harness early-close evidence, not as a duration failure and not as a clean target pass. The emergency cap is a safety guard only; it is never normal pre-target admission budget.

If the final admitted batch begins below T and finishes above T, its semantic work remains valid. Do not start another batch merely to pad elapsed time after an authoritative progress sample has already established target attainment.

## Completion condition
Continue useful work until authoritative server-clock evidence establishes target attainment, unless a genuine failure/block/user stop or emergency close cap occurs first. After target attainment, create/raw-fetch PRE_CLOSE, perform durable close checkpoint/finalization, then create/raw-fetch END.

## Productivity accounting
Persist at minimum:
- generated_id_unique_units
- generated_semantic_unique_units
- duplicate_ids_rejected
- semantic_repeats_rejected
- batches_completed
- batch_fingerprints
- anomaly_count / assertion_count
- generator_version

These supplement, never replace, server-clock PRODUCTIVE_WINDOW.

## Control-clock rule
Target/close decisions use raw GitHub server progress samples. Model/local elapsed may only hint when to sample. Exact PRE_CLOSE threshold is experimental evidence and must be recorded.

## Retrospective correction rule
If a later audit discovers that a prior productive-unit metric counted ID-only duplicates, preserve the original record and append a correction. Clock survival evidence remains unchanged, but any strict promotion that depended on sustained substantive-work quality must be revalidated or superseded by a clean semantically-valid probe.
