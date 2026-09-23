# Unit 27 — Classification checklist

Probe: PROBE-14M-20260923T095323KST

At close, CLEAN_PASS requires all true:
- observed elapsed >=840s;
- W3 mixed I/O substantive workload sustained;
- durable close record written;
- scheduler write/state already verified;
- no forced stop/timeout;
- no explicit independent failure.

Retrospective wake observation is recorded next turn and is not fabricated here. Production-cap promotion remains prohibited from this single sample.
