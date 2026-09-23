# R8 Large Genuine Workload Corpus

Probe: PROBE-22M-SERVERCLOCK-20260924-R8
Case: SC-A22-CLOCK-01
Profile: W3_MIXED_IO

Purpose: avoid repeating exhausted protocol audits. This probe extends the runtime evidence processor into a genuinely reusable end-to-end implementation design and migration corpus.

Planned decision-bearing units:
1. define canonical normalized ProbeRecord schema with identity, raw-clock, scheduler, productive, completion, causal and retrospective-wake fields;
2. define validation precedence and anomaly taxonomy;
3. define event-ledger parser rules for legacy/current clock classes;
4. define duplicate-event and partial-probe reconciliation;
5. define marker raw-fetch integrity interface and trust boundary;
6. define deterministic boundary aggregation with profile coverage;
7. define completion-envelope sample extraction;
8. define admission-policy evidence extraction;
9. define migration strategy from existing reference classifier without altering historical evidence;
10. define executable regression corpus expansion and acceptance gates;
11. define concurrency-safe terminal synchronization transaction semantics;
12. audit existing canonical files against the implementation and repair only real mismatches.

No unit may be repeated merely to consume runtime. If the corpus is genuinely exhausted before 1320 server seconds, close UNDER_TARGET.

Clock START comment id: 5799384221
Clock START server created_at: 2026-09-23T17:15:25Z
