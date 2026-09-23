# R4 next-case profile rotation plan

This plan is conditional and does not advance state before R4 terminal classification.

## If R4 PASS + retrospective WAKE_OK

Generate SC-A24-CLOCK+ at 24m. To broaden coarse-ascent coverage rather than repeating W3, prefer W5 MICRO_UNIT_CHAIN for the next target because:

- W3 is being exercised at 22m,
- W5 stresses many genuine short admission decisions,
- it complements the earlier legacy W6 large-unit and W4 reasoning-heavy observations,
- it provides useful evidence for later SOFT_CUTOFF/NEXT_TASK_ADMISSION design without changing the Phase-A goal.

The exact next profile remains subject to fresh canonical state/master policy at that invocation.

## If R4 duration-fail candidate

Do not rotate profile. Hold W3 fixed and obtain a server-clock same-profile lower anchor/refinement bracket before claiming a profile-specific boundary.

## If R4 UNDER_TARGET or NON_DURATION_FAIL

Remain SC-A22-CLOCK-01 and repeat only after correcting the identified cause. Do not treat repetition itself as evidence.

## Decision value

Predefining these branches reduces post-run improvisation and preserves the master plan's causal-control rules.
