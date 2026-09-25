# Runtime research relay handoff — 2026-09-25

Status: PAUSED_BY_USER / RESUMABLE
Repository: amzsdq/workwork
Automation previously responsible: 6ab2823a68548191876ab2d55caf915f

## Resume rule

Before doing anything else, fresh-read default-main state/current.json, RUNTIME_RESEARCH_MASTER_PLAN.md, state/events.log, EVIDENCE_TABLE.md, state/README.md, runtime/TERMINAL_STATE_SYNC_PROTOCOL.md, runtime/STRICT_PROBE_EXECUTION_CHECKLIST.md, relevant r24 branches/open PRs, and issue #1 frontier. Immutable lifecycle evidence outranks mutable projections. Raw GitHub created_at is authoritative where available. Never overwrite newer state.

The relay is intentionally stopped after this checkpoint. Do not start a new strict probe merely because active_probe_id is null or R24 is reconciled. Admission must remain fail-closed until G1/G2/G3/G4 are verified on a final fresh read.

## Current repository state at pause

Fresh default-main state/current.json is schema_version 47, blob e2347ddcdad46bedcc661f171960f7e90a625919, status RECONCILIATION_REQUIRED. It still projects R24 as ORPHANED_PENDING_RECONCILIATION and denies new probes until R24 reconciliation completes. This projection is stale relative to immutable R24 recovery evidence, but is safer than promoting schema49 because it remains fail-closed.

Other last-verified default-main blobs:
- RUNTIME_RESEARCH_MASTER_PLAN.md: 7f853eee0fe412ac9ba3ba65cb744f0140560454 (stale execution pointer)
- state/events.log: 74e5d90af54cd2676c4ce69efb16bb8181655194
- EVIDENCE_TABLE.md: 4abb2a7dc11c3e32eb7f9feb7da81414e3c43d39
- state/README.md: 6e7b9733c7ae3dc037d3919b5f4abdbbce109bcf
- runtime/TERMINAL_STATE_SYNC_PROTOCOL.md: e71dd21e5253dededf27d7b535dcc1f443cf5d93
- runtime/STRICT_PROBE_EXECUTION_CHECKLIST.md: 1a5ad40ebf6101333b3e359ba2fc2127f59cebcd

Issue #1 last verified R24 frontier: START 5817062347 -> ledger 5817063999 -> PROGRESS 5817065020 -> CLOSE_CHECKPOINT 5817066845. No newer raw START was observed in the completed relay turns.

## Critical admission finding

Both known r24 current branches contain schema49 blob cab904e76fb807d9bf896c8a108a55d338d44d96. Schema49 is ACTIVE and says next_probe_requirement=ELIGIBLE_AFTER_R24_PROJECTION_VERIFIED_ON_MAIN. It has no G4 projection-hygiene admission gate. Do NOT promote schema49 as-is.

Designed schema50 is not repository state. It is a fail-closed design only: status RECONCILIATION_REQUIRED; deny new strict probes until G1&&G2&&G3&&G4 are verified after a final fresh read; projection_hygiene_gate must cover events/EVIDENCE/README/checklist reconciliation and absence of unsatisfied blocking obligations. Prior scratch full schema50 SHA256 was acd3489e865e91e6e5015f8c6394cd414bf7affdf0b49661af8b891c7598f3e5, but all scratch hashes must be regenerated from fresh bytes before use.

Gates:
- G1: reviewed fail-closed current projection actually on default main.
- G2: synchronized master-plan execution pointer.
- G3: lifecycle frontier clear: no newer START/comparable immutable conflict.
- G4: projection hygiene: all directly established blocking projection obligations reconciled or mechanically proven semantically subsumed; EVIDENCE consistent; state/README authority wording corrected; strict-probe checklist enforces fail-closed G1-G4 pre-START admission.
ADMIT = G1 && G2 && G3 && G4. A partial migration must never admit.

## R24 immutable recovery truth

R24 identity: PROBE-32M-REPRO-V2-20260924-R24.
Recovery disposition blob: 992f965a7d7752c88c9796ba8b947da074df4e31.
Recovery event: state/recovery-events/PROBE-32M-REPRO-V2-20260924-R24.json blob 01c44438434b7aec519ec57915e85111082815b4.
Raw START created_at durably recorded as 2026-09-24T15:26:20Z.
Classification: INTERRUPTED_ORPHANED_RECONCILED.
terminal_marker_observed=false; strict_substantive_pass=false; boundary_effect=NONE; runtime_lower_bound_effect=NONE.
Never synthesize END/PASS/duration for R24.

## Historical G4 reconciliation debt

Nine historical reconciliation/audit records were repeatedly direct-read. Six distinct historical state/events.log obligations remain directly established and absent from the aggregate:
- OP-CAP-14M-VALIDATION-01
- OP-CAP-14M-VALIDATION-02
- OP-CAP-14M-VALIDATION-03-R3
- OP-CAP-14M-VALIDATION-03-R5
- PROBE-22M-SERVERCLOCK-20260924-R9
- PROBE-24M-SERVERCLOCK-20260924-R10

Important semantics:
- OP-CAP-02 later immutable wake advances it to CLEAN_PASS_WAKE_OK / OPERATIONAL_CAP_14M_VALIDATION_CLEAN_RUN_2_CONFIRMED; current EVIDENCE row is stale and requires append-only correction.
- R3 is HARNESS_UNDER_TARGET 190/167/13, boundary NONE, INVALID_NON_DURATION_LOCAL_EXECUTOR_RESET. Do not call it a duration failure.
- R5 is 910/885/5 CLEAN_PASS_PENDING_WAKE with later immutable CLEAN_PASS_WAKE_OK/NONE. Stale historical current pointer is semantically subsumed; wake history still needs projection/EVIDENCE.
- R9 terminal records 1322/1257/57 CLEAN_PASS_WAKE_OK, but semantic audit blob 169d7895b9f05ffad5431a5b88c6fec1d25dacfd preserves clean 22m02s clock survival while posthoc-tainting strict-substantive promotion. Do not re-promote a strict lower bound solely from R9.
- R10 is 1402/1376/14 UNDER_TARGET, boundary NONE, shortfall due admission/close-control mismatch, not duration failure. Its EVIDENCE/master-plan effects were already reconciled; aggregate events debt remains.
- Stale R3/R5/R9/R10 current/active pointers and R5-WAKE historical current advancement are SEMANTICALLY_SUBSUMED by stronger later state and must not be replayed literally.

The last machine-readable G4 fixture contained 20 unique record/effect keys: 10 UNSATISFIED, 6 SEMANTICALLY_SUBSUMED, 4 SATISFIED. Regenerate it from fresh records before migration.

## Mandatory aggregate projection scope

Candidate scope is 13 distinct probe IDs: historical six above + R14, R15, R16, R17, R18, R19, R24. Existing legacy events.log lines are immutable; append only when probe_id is absent. Projection schema v2 must keep terminal result/boundary, wake result/boundary/source, and semantic audit qualification as separate layers.

Correct wake taxonomy:
- OP-CAP-01/02/R5: IMMUTABLE_WAKE_EVENT
- R9: EMBEDDED_TERMINAL plus semantic-audit qualification
- R3/R10: NONE
- R14/R18/R19: RAW_COMMENT
- R15/R16/R17: IMMUTABLE_WAKE_FILE
- R24: NONE

Critical corrected identities/paths:
- R19 is PROBE-32M-REPRO-V2-20260924-R19, NOT STRICT.
- R19 terminal: runtime/probes/PROBE-32M-REPRO-V2-20260924-R19/terminal.json blob 9d5bbe7d3b59bbe1c810da87e59faceba673a6af.
- R19 event: runtime/events/PROBE-32M-REPRO-V2-20260924-R19-terminal.json blob c699864f539ebea3a0f05639f271282ba1419919.
- Raw wake comment 5814866450 binds the same R19 REPRO identity.
- R24 recovery event is under state/recovery-events, not state/events.
- Historical six immutable event files are under state/events: OP-CAP-01 f9a67155581a6cc2517c984ddc768f3cc1c11df6; OP-CAP-02 9cd2f95c250774ac7e92b0bb6838d9cf25d95ed9; R3 083d0f42ec1aaddce4f619723e752e095c38c9c8; R5 cd9b43a13d9cdcc2a425c9ea8dc6b41bca86fd6f; R9 af3aec187ac44f68c001400e433c00f64ad50bd2; R10 e1684aef9589a9ce614beaeaf99e165fda51b27b.
- R17 corrected immutable wake is runtime/probes/PROBE-30M-STRICT-V2-20260924-R17/wake.json blob 88b5ff68f840d53d33fa34a11c718e49b36818b3.

Raw-comment body/identity bindings for R14 comment 5811854481, R18 5814164530, R19 5814866450 were fresh-verified, but the connector returned created_at=null. Do not overclaim fresh connector-level wake created_at verification. Aggregate row timestamps for these probes come from immutable terminal END.

## Candidate reproducibility warning — resolve before writing

An earlier 13-row scratch candidate was twice reported with SHA256 6df3abfd791d049e6729ca285d2f0b14184e0481743be453690055a9fd379da3. A later fresh reconstruction after correcting R19 REPRO identity and R24 recovery-event path produced SHA256 df5047e28042b5d81bd0a469f53aecca202bd3fcf9b8ffa7b07c14932d9b6ec5 instead.

The corrected reconstruction passed row_count=13, unique IDs=13, all IDs absent from current events.log, JSON validity, and append-twice exact no-op. A full fresh events target (legacy prefix + corrected 13 rows) had scratch SHA256 42ae54c36842d2ccbdf27ce46d8ef5266db0c26fac61210174b07df8768ab507, length 28081, prefix_identity=true.

However, the 6df-vs-df50 mismatch has NOT been fully explained. Treat this as the immediate technical blocker to aggregate write authorization. Recover/derive the old serialization if possible, diff field-by-field, determine whether mismatch is formatting/null/schema-only or substantive provenance, then freeze one canonical schema and independently reproduce its hash twice. Do not write events.log while this is unresolved.

## EVIDENCE / README / checklist migration targets

EVIDENCE_TABLE currently has R9, R10, OP-CAP-01, OP-CAP-02. It has no R3/R5 identifiers. OP-CAP-02 remains stale as CLEAN_PASS_PENDING_WAKE despite immutable wake. Append-only addendum target must cover OP-CAP-02 wake advancement, R3/R5, R14-R19, R24. Preserve existing R9 semantic-audit and R10 non-duration interpretation. R15/R19 Productive/Qualifying values use qualifying elapsed. R24 timing is n/a and never PASS.

state/README currently incorrectly says events.log is canonical truth and current should be rebuilt from events.log. This conflicts with TERMINAL_STATE_SYNC_PROTOCOL. Target semantics: events.log is append-only derived history projection; authority is raw marker -> durable start -> immutable terminal -> immutable event/recovery -> mutable projections; current is rebuilt from strongest validated lifecycle evidence, not stale events.log alone.

runtime/STRICT_PROBE_EXECUTION_CHECKLIST lacks explicit G4 admission verification. Planned minimal patch adds: require fresh G1/G2/G3/G4 before START; any UNSATISFIED non-superseded blocking reconciliation effect denies admission even if active_probe_id=null; final admission only from fresh read after required projections reconcile, never write success alone.

Prior scratch full-target SHA256 identifiers (not Git blobs, regenerate before use):
- schema50: acd3489e865e91e6e5015f8c6394cd414bf7affdf0b49661af8b891c7598f3e5
- master-plan target: 220956cb0eb1ad036e00807cf898e9c9b5d4c822be847681b146400e46fa50a8
- EVIDENCE target: 447eb8d08c863e930530762d65e7ef3f00cb64f29c6bd9e6b754bd9552e990fa
- README target: 447885dd2a7cea161d43714636a6a0c0b2468076a5a54fdfa9ca43f1d7d40f96
- checklist target: e7791787bf6bda65a02dc787d1a54bf20e1b8b2334015d329a195d03c0b05764

## Safe future migration protocol

Six mutable targets are planned: state/current schema50 fail-closed; master-plan pointer; events.log v2 append; EVIDENCE append-only addendum; state/README authority correction; STRICT_PROBE_EXECUTION_CHECKLIST G1-G4 pre-START check.

Before EVERY write: immediately fresh-fetch default-main target, validate assumptions, use only that just-returned full blob SHA. After EVERY write: fresh-fetch same path and require fetched SHA == returned content_sha AND byte/semantic invariant. On SHA mismatch/409/new START/newer projection/readback mismatch, stop the migration step, refetch all gates, recompute, and keep admission false. Never use old observed SHA as future write permission. Never bypass with low-level Git object/ref writes.

Migration simulator previously showed fail-closed behavior: baseline -> current -> master-plan -> events -> EVIDENCE -> README -> checklist -> final fresh-read admits only at final fresh-read. Injected stale-SHA, 409, new START, newer projection, or readback mismatch at each mutable stage kept admission false through final. Regenerate before actual migration.

## Resume order

1. Fresh-read all control files, r24 branches/open PRs, and issue frontier.
2. Resolve the 6df-vs-df50 events candidate mismatch, preserving corrected R19 REPRO and R24 recovery-event path.
3. Reconstruct all six target artifacts from fresh bytes and independently reproduce hashes/invariants.
4. Rebuild the G4 effect fixture from the exact reconciliation records; every declared effect must have exactly one disposition and every UNSATISFIED blocker must map to a migration artifact.
5. Re-run six-stage failure simulator.
6. Only then consider high-level CAS writes. Never promote schema49 as-is.
7. After any eventual migration, only a final fresh read of all six targets + terminal-sync + issue frontier may authorize admission.

## Pause note

This checkpoint intentionally preserves unresolved debt rather than papering it over. No repository projection migration was performed during the final relay turn because candidate reproducibility was not yet deterministic. The project is safe to resume from this document plus fresh repository state.
