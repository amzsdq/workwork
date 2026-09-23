# Unit 02 — Close-reserve estimator audit

Probe: PROBE-14M-20260923T095323KST

The estimator preserves the required separation between pre-arm overhead, close overhead, and safety margin. Sparse samples are intentionally prevented from creating a false precise reserve. This matters for the final admission policy: runtime-boundary evidence determines the feasible region; close-reserve observations determine how much of that region can be safely consumed.

No protocol change is required before continuing the 14m boundary probe.
