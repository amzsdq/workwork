# Unit 01 — Evidence reconciliation

Probe: STRICT-14M-20260923T092741KST
Profile: W3 MIXED_IO

Observed inconsistency:
- state/current.json currently claims last_clean_target_minutes=12 and NEXT_STRICT_TARGET=14.
- EVIDENCE_TABLE.md still says 12m clean timing passes=0 and next empirical target=12m.
- PROBE_12M_RESULT.md records a 12m target crossing at 01:12:06 KST from a 00:59:57 KST start, using TEST_GENERATED_MIXED_LOAD.

Interpretation for this invocation:
- Do not rewrite historical evidence during the active timing probe merely to make derived files agree.
- Treat the 14m run as requested by the current control state, but flag the 12m promotion inconsistency for retrospective validation.
- A 14m result must not silently repair or erase the discrepancy.

Useful outcome: identified a provenance/control-state inconsistency that can affect boundary claims and preserved it as explicit evidence.
