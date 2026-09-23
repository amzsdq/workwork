# Unit 07 — Control-contract audit

Probe: STRICT-14M-20260923T092741KST

README and current strict contract agree on the key experimental controls:
- same recurring automation;
- complete RRULE:FREQ=HOURLY;
- pre-arm at turn start;
- planned gap baseline +3m;
- no normal scheduler mutation at close;
- direct elapsed/close evidence required;
- synthetic/generated bounded workload allowed only when purposeful and profiled;
- production cap requires repeated validation and safety margin.

Potential wording debt:
README still says the optimization target includes avoiding concurrent wakes, while separate completed overlap research has proven same-automation concurrency exists and later parallel research may intentionally exploit it. This is not a Phase-A contradiction because strict duration research currently treats overlap as undesirable/control-confounding. No README change is required during this probe.
