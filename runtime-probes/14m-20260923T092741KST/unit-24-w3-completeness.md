# Unit 24 — W3 workload completeness

Probe: STRICT-14M-20260923T092741KST

The run has exercised the intended W3 characteristics rather than a single repeated operation:
- repository reads of state, canonical event ledger, runtime protocol, workload profiles, close estimator, rollback rule, utility model, README, and prior probe artifact;
- evidence reconciliation and contradiction resolution;
- derived-table repair;
- repeated state reconstruction to detect concurrent control mutation;
- multiple immutable checkpoint writes;
- transient connector failure classification and successful retry;
- pre-close decision preparation.

Thus workload_profile=W3_MIXED_IO is substantively supported, not merely labeled.
