# Unit 17 — Failure-mechanism separation

Probe: STRICT-14M-20260923T092741KST

A transient GitHub RemoteProtocolError occurred while creating Unit 16; an immediate retry succeeded. Classification: tool/network transient, recovered, no loss of probe checkpoint and no evidence of duration-related termination.

This event must not be counted as a runtime-boundary failure. It is useful evidence for the failure-discipline rule: independent connector transport errors remain separate from invocation-duration failure unless they prevent durable close and no independent cause can be established.

No scheduler mutation was performed during recovery.
