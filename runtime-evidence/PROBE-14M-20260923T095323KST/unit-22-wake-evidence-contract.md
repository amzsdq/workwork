# Unit 22 — Retrospective wake contract

Probe: PROBE-14M-20260923T095323KST

The successor invocation scheduled for 10:10:23 KST must first reconcile this probe's close record with its own actual invocation start. It should record:
- prior_next_wake_observed=true when this pre-armed wake is the actual trigger;
- actual_idle_gap_sec = successor_start - prior_close_end;
- wake_lateness_sec = successor_start - 10:10:23 KST.

This wake evidence is continuation evidence and must not be guessed by the current invocation.
