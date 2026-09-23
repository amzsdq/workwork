# Unit 02 — W3 mixed-I/O audit

Probe: STRICT-14M-20260923T092741KST

Checked boundary and measurement contracts against current state.

Findings:
1. Boundary rule requires start pre-arm + target reached + durable normal close for clean_pass.
2. One clean pass can advance coarse target by +2m but cannot promote a production cap.
3. Current derived EVIDENCE_TABLE is stale relative to state/current.json and PROBE_12M_RESULT.md; provenance must be reconciled before final cap claims.
4. Runtime measurement protocol correctly distinguishes scheduler pre-arm overhead from close reserve and prohibits invented useful-work precision.
5. This 14m probe will therefore report useful work as an evidence-producing active window/units rather than fabricated stopwatch precision.

This unit exercises alternating repository reads, cross-file reconciliation, reasoning, and durable write, matching W3 MIXED_IO.
