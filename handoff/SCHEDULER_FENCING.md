# Scheduler fencing design

Current safe rule: only the invocation named as active owner in the current generation may mutate the recurring automation.

Before an owner scheduler write:
1. Fresh-read handoff-state.json.
2. Confirm active_invocation_id and generation match local ownership.
3. Perform the single intended scheduler mutation.
4. Persist returned schedule metadata in the owner's immutable evidence.

This does not make the external scheduler update itself CAS-atomic with GitHub ownership. Therefore scheduler writes should occur immediately after ownership acquisition, before long work, and no SHADOW may write the scheduler.

S3 SHADOW_IMMEDIATE_PREARM would require a stronger reservation model, for example a scheduler_generation assigned to the intended successor that cannot collide with the predecessor's generation. Until experimentally implemented and verified, S3 remains non-production.
