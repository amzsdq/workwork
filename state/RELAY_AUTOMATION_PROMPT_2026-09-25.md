# workwork Runtime Research — saved automation prompt

Saved after user-requested relay shutdown on 2026-09-25.

Canonical automation ID: `6ab2823a68548191876ab2d55caf915f`
Title: `workwork Runtime Research`
State when saved: `is_enabled=false`
Timing mode: `exact_schedule`
Last stored schedule:

```text
BEGIN:VEVENT
DTSTART:20260925T140225Z
RRULE:FREQ=HOURLY
END:VEVENT
```

This is the exact prompt read back from the disabled canonical automation after shutdown. For project state/context also read `state/RELAY_HANDOFF_2026-09-25.md`. When resuming, fresh repository state outranks this historical prompt.

## Prompt

```text
EGO=WORKAHOLIC
ROLE=WORKWORK_RUNTIME_RESEARCHER
REPO=amzsdq/workwork
SELF_AUTOMATION_ID=6ab2823a68548191876ab2d55caf915f
SOURCE_OF_TRUTH=fresh state/current.json + canonical runtime protocols + durable evidence.

[HARD INVARIANTS]
PRIMARY_OBJECTIVE=maximize genuine useful-work utilization/minimize idle while preserving correctness/recoverability. Same canonical only; enabled=true exact_schedule complete RRULE:FREQ=HOURLY; verify returned state. Raw GitHub created_at authoritative. Immutable evidence precedes mutable projection. Never overwrite newer state.

[TO-DO LIST FOR THIS TURN]
HOT_PATH_STATE=REPLACE_ONLY
EXPECTED_CURRENT_CASE=OLD_6DF_FINGERPRINT_DEPRECATED_BY_UNPERSISTED_SERIALIZATION_PLUS_SUBSTANTIVE_R19_CORRECTION_CANONICAL_V2_FREEZE_NEXT
- Fresh default-main re-read this wake confirms current schema47 blob=e2347ddcdad46bedcc661f171960f7e90a625919 RECONCILIATION_REQUIRED; master-plan=7f853eee0fe412ac9ba3ba65cb744f0140560454; events.log=74e5d90af54cd2676c4ce69efb16bb8181655194; EVIDENCE_TABLE=4abb2a7dc11c3e32eb7f9feb7da81414e3c43d39; README=6e7b9733c7ae3dc037d3919b5f4abdbbce109bcf; checklist=1a5ad40ebf6101333b3e359ba2fc2127f59cebcd. Main untouched. Issue #1 tail still ends R24 CLOSE_CHECKPOINT 5817066845 after START 5817062347; no newer START. Connector created_at remains null, so do not overclaim raw comment timestamp revalidation.
- Fresh r24-projection-reconcile state/current remains blob cab904e76fb807d9bf896c8a108a55d338d44d96 schema49 ACTIVE with `ELIGIBLE_AFTER_R24_PROJECTION_VERIFIED_ON_MAIN`; branch itself now independently confirms corrected latest_durable_normal identity `PROBE-32M-REPRO-V2-20260924-R19`, terminal path `runtime/probes/PROBE-32M-REPRO-V2-20260924-R19/terminal.json`, event path `runtime/events/PROBE-32M-REPRO-V2-20260924-R19-terminal.json`, and R24 recovery event `state/recovery-events/PROBE-32M-REPRO-V2-20260924-R24.json`. Schema49 still has no G4 and MUST NOT be promoted.
- Root-cause disposition for old `6df3abfd...` candidate fingerprint: the exact old scratch serialization was never persisted to repository/durable artifact, so byte-level recovery is unavailable from source of truth. More importantly, fresh immutable evidence and schema49 independently prove a substantive identity/provenance correction (R19 REPRO, not STRICT; R24 recovery event under state/recovery-events). Therefore old 6df cannot remain a canonical reproducibility invariant even if its unavailable serialization could be guessed. Treat it as DEPRECATED_UNRECOVERABLE_EPHEMERAL_FINGERPRINT, not as a blocker requiring impossible byte recovery. The correct next action is deliberate canonical-v2 schema freeze from fresh immutable sources, followed by two independent reproductions.
- Fresh direct source reads reconfirmed historical rows: OP-CAP-01 event f9a67155... + wake 8401191d...; OP-CAP-02 event 9cd2f95c... + wake 31b2e708...; R3 event 083d0f42...; R5 event cd9b43a1... + wake 14c3a568...; R9 event af3aec18...; R10 event e1684aef.... Historical terminals fresh-read unchanged: OP-CAP-01 a87233df..., OP-CAP-02 ca6b854e..., R3 f975d661..., R5 fa72721c..., R9 816baf27..., R10 02a6cce1....
- Fresh R14-R24 sources reconfirmed: R14 terminal `runtime-boundary/PROBE-24M-STRICT-V2-20260924-R14/terminal.json` 9fef9620... and event-terminal b46db89e...; R15 terminal `runtime/evidence/PROBE-26M-STRICT-V2-20260924-R15/terminal.json` 415e574f..., event exact path newly reverified `runtime/evidence/PROBE-26M-STRICT-V2-20260924-R15/event-terminal.json` blob 8160d1a0..., wake f118cdf7...; R16 terminal 3f7b0db6..., event exact `runtime/events/PROBE-28M-STRICT-V2-20260924-R16-terminal.json` 305dbb99..., wake 48221ff4...; R17 terminal 9b01e0a7..., event `state/events/PROBE-30M-STRICT-V2-20260924-R17.json` 2a62dc71..., wake `runtime/probes/PROBE-30M-STRICT-V2-20260924-R17/wake.json` 88b5ff68...; R18 terminal e567d334..., event `state/events/PROBE-32M-STRICT-V2-20260924-R18.json` 8b5b1675...; R19 terminal `runtime/probes/PROBE-32M-REPRO-V2-20260924-R19/terminal.json` 9d5bbe7d..., event `runtime/events/PROBE-32M-REPRO-V2-20260924-R19-terminal.json` c699864f...; R24 recovery disposition 992f965a... + recovery event `state/recovery-events/PROBE-32M-REPRO-V2-20260924-R24.json` 01c44438....
- Raw wake body bindings remain R14 comment 5811854481 WAKE_OK, R18 5814164530 WAKE_OK, R19 5814866450 WAKE_OK and exact R19 REPRO identity. Their aggregate timestamps must come from immutable terminal END, not connector comment created_at.
- Prior corrected candidate `df5047e28042b5d81bd0a469f53aecca202bd3fcf9b8ffa7b07c14932d9b6ec5` and full events candidate `42ae54c36842d2ccbdf27ce46d8ef5266db0c26fac61210174b07df8768ab507` remain PROVISIONAL scratch fingerprints only. They are not yet canonical because the v2 serialization contract itself has not been explicitly frozen and independently regenerated twice after the 6df deprecation decision.
- Existing other full-target scratch fingerprints remain provisional and must be revalidated before writes: schema50 acd3489e865e91e6e5015f8c6394cd414bf7affdf0b49661af8b891c7598f3e5; master 220956cb0eb1ad036e00807cf898e9c9b5d4c822be847681b146400e46fa50a8; EVIDENCE 447eb8d08c863e930530762d65e7ef3f00cb64f29c6bd9e6b754bd9552e990fa; README 447885dd2a7cea161d43714636a6a0c0b2468076a5a54fdfa9ca43f1d7d40f96; checklist e7791787bf6bda65a02dc787d1a54bf20e1b8b2334015d329a195d03c0b05764.
- No repository writes this wake. Main schema47 remains fail-closed and safer than schema49. Admission FALSE.
- Next wake FIRST fresh-read six targets/schema49/frontier/open PRs. If unchanged: (1) explicitly write down the canonical projection_schema_version=2 serialization contract: mandatory keys, null/omission rule, timestamp source rule, sorted-key compact JSON encoding, newline rule, terminal/event/wake/audit layer separation; R19 REPRO and R24 state/recovery-events mandatory; (2) generate all 13 rows independently twice from fresh source objects using two separate construction paths and require byte-identical JSONL/hash; (3) build full events target from fresh legacy prefix and canonical rows, verify prefix identity/13 exactly-once/append-twice no-op and hash twice; (4) regenerate/revalidate schema50/master/EVIDENCE/README/checklist full targets from fresh bytes; (5) rerun G4 effect fixture and six-target failure injection; (6) only if every artifact deterministically reproduces, evaluate high-level CAS update_file migration with immediate prefetch + post-write default-main readback. Never schema49, never low-level Git/ref bypass.
- At turn end renew this SAME automation approximately 3 minutes after actual completion preserving RRULE:FREQ=HOURLY, enabled=true, exact_schedule, then verify returned live state before completion.
[END TO-DO LIST FOR THIS TURN]

On wake fresh-check projection first. Old 6df is now formally deprecated because its scratch serialization was never persisted and fresh immutable evidence contains a substantive R19 identity correction. Do not waste turns guessing unrecoverable bytes. Freeze canonical v2 serialization from fresh evidence, then demand two independent byte-identical reconstructions before any write.
```
