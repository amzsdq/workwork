# Unit 14 — Close-sample preparation

Probe: STRICT-14M-20260923T092741KST

Known valid close-overhead evidence before this run:
- canonical 12m event: close_overhead_sec=32.

Sparse-sample implication:
- N=1, so 32s is only a LOW_CONFIDENCE provisional observed reference, not a promoted reserve.
- The current 14m close should add another direct observation if pre-close and close-end can both be captured.
- Safety margin must remain separate from close overhead.

At target crossing, close sequence should be minimal and durable: target-cross/pre-close evidence -> final event/state checkpoint -> close-end evidence where feasible, with no scheduler rewrite.
