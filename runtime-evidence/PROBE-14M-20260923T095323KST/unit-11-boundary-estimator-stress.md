# Unit 11 — Boundary estimator logic stress

Probe: PROBE-14M-20260923T095323KST
Type: SIMULATION/LOGIC_TEST — not empirical boundary evidence.

Cases checked:
1. 12 PASS, 14 PASS => exploratory next=16; lower-bound observation=14; cap remains unpromoted.
2. 12 PASS, 14 credible FAIL => candidate bracket [12,14], refine ~13.
3. 12 PASS, 14 ambiguous FAIL => repeat 14 before narrowing.
4. 12 PASS, 14 explicit network FAIL => keep boundary unresolved and retry 14.
5. 12 PASS, 14 PASS, 16 FAIL => candidate bracket [14,16], refine ~15.
6. 14 PASS once with poor next-wake evidence => runtime lower-bound observation can advance if strict clean criteria hold, but continuation confidence remains separately weak; production cap cannot be promoted.

No coarse-ascent/refinement rule contradiction found.
