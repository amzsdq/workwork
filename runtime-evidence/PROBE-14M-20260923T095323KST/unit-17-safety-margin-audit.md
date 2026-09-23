# Unit 17 — Safety-margin provenance audit

Probe: PROBE-14M-20260923T095323KST

No numeric safety margin is currently justified because the upper runtime boundary remains unresolved and close-overhead evidence is sparse. A future safety margin must be derived from the observed boundary bracket, task-estimation error, and close-time variance; it must not duplicate close reserve.

Therefore this probe leaves SAFETY_MARGIN=UNRESOLVED rather than inventing a conservative constant.
