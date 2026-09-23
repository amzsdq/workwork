# R4 safety-margin derivation constraints

## Why SAFETY_MARGIN cannot be chosen yet

A safety margin should reflect uncertainty below a credible failure boundary and variability in close/continuation behavior. Current strict server-clock evidence has:

- no credible duration failure,
- no server-clock safe lower bound yet,
- insufficient close-overhead distribution,
- one under-target migration run,
- active 22m revalidation.

Any numeric safety margin now would therefore be arbitrary.

## Evidence needed

A defensible margin requires some combination of:
- profile-controlled lower/upper runtime bracket,
- repeated clean-close variance near candidate,
- upper-tail close overhead,
- continuation/wake reliability,
- workload-profile sensitivity.

## Selection principle

Prefer a simple fixed margin below the empirically credible upper region. Increase the margin when variance or profile sensitivity is high. Only use profile-aware/adaptive margin if a fixed margin is materially inefficient or unsafe.

## Current status

SAFETY_MARGIN = unresolved. R4 should not introduce a guessed value merely to complete the output schema.
