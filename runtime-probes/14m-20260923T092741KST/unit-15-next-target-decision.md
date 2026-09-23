# Unit 15 — Conditional next-target decision

Probe: STRICT-14M-20260923T092741KST

Decision prepared before close:
- If this run reaches >=840s and durably closes with no independent failure: classify CLEAN_PASS, SAFE_LOWER_BOUND=14m, next strict target=16m W4 REASONING_HEAVY.
- If execution is cut off near/after target before durable close with no independent cause: classify DURATION_FAIL and create failure-boundary candidate 14m, requiring refinement/reproduction per rule.
- If an explicit GitHub/tool/provider failure independently prevents completion: NON_DURATION_FAIL; boundary unchanged.
- If substantive work ends before 840s: UNDER_TARGET; boundary unchanged.

No result is assigned yet. This file records the decision rule before observing the outcome, reducing hindsight classification bias.
