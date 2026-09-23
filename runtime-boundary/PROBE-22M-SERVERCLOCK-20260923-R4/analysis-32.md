# R4 same-profile refinement design

If 22m W3 becomes the first credible duration-fail candidate, refinement must avoid using a different-profile legacy pass as a strict lower anchor.

## Efficient sequence

1. Repeat/confirm 22m W3 once if failure causality is ambiguous.
2. Obtain a server-clock W3 lower anchor below 22m, guided by legacy evidence (for example 20m or 21m depending on failure shape).
3. Refine with approximately 1m W3 classes until the [clean lower, credible failure upper] bracket is <=1m.
4. Only after a W3 profile-specific bracket exists should cross-profile tests determine whether the risk is universal or workload-dependent.

## Why not binary-search immediately from legacy 20m

Legacy 20m is useful for experiment selection but lacks current server-clock authority. Treating it as the strict lower endpoint would violate the new invariant.

## If 22m passes

No refinement is needed; continue +2m coarse ascent with rotated profile until a credible failure appears.
