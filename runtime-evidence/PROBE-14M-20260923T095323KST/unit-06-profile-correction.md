# Unit 06 — Workload-profile correction

Probe: PROBE-14M-20260923T095323KST

Fresh execution plan specifies the 14m coarse-ascent profile as **W3 MIXED_IO**. The start record used the generic label TEST_GENERATED_MIXED_LOAD; this unit records the canonical profile mapping without rewriting immutable start evidence.

Canonical empirical workload_profile for classification: `W3_MIXED_IO`.

The work performed in this invocation is consistent with W3: repeated GitHub reads, bounded reasoning/audits, and durable writes/checkpoints.
