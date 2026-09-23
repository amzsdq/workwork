# Unit 18 — Final pre-close audit

Probe: PROBE-14M-20260923T095323KST

Before close classification:
- start evidence exists;
- recurring successor wake was pre-armed and validated;
- canonical profile is W3_MIXED_IO;
- multiple substantive mixed read/write/reasoning units are durable;
- no scheduler rewrite occurred after pre-arm;
- no independent GitHub/network/provider failure has been observed;
- strict lower bound remains 12m until close evidence proves target crossing.

Close classification must use an actually observed current timestamp; if target has not yet been crossed, the run must remain active or close UNDER_TARGET rather than fabricate elapsed time.
