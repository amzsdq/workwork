# Unit 01 — Boundary classification audit

Probe: PROBE-14M-20260923T095323KST

Findings:
- Durable state consistently identifies strict next target 14m and last strict clean target 12m.
- The decision rule correctly prevents supporting parallel-survival evidence from moving the strict boundary.
- A single strict clean 14m run may raise observed SAFE_LOWER_BOUND to 14m and advance exploratory target to 16m, but cannot promote an operating cap.
- First credible duration failure must remain a candidate until ambiguity is removed; non-duration failures do not narrow the bracket.

Integrity result: no contradiction found that blocks this strict probe.
