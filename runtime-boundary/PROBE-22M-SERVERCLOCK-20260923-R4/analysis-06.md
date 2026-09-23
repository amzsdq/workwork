# R4 boundary-search efficiency review

## Question

Given that the strict server-clock lower bound is currently unresolved, is revalidating 22m directly methodologically acceptable, or should the study restart at a lower target?

## Assessment

Direct 22m revalidation is acceptable and more efficient because:

- legacy evidence contains clean operational observations through 20m and a pre-protocol 22m clean-close observation,
- the new clock protocol invalidates exact-duration authority for promotion but does not erase the qualitative survival evidence,
- R3's 652s UNDER_TARGET was not a failure and therefore gives no reason to retreat,
- the active question is whether 22m can be reproduced under authoritative timing, not whether shorter durations have ever worked.

If R4 cleanly reaches 22m and later WAKE_OK, the new strict lower bound can be 22m without separately re-running 10/12/14/16/18/20 under the new clock. This is a lower-bound observation, not a universal safety proof; Phase B replication and profile coverage still apply before production-cap promotion.

## Failure interpretation

If R4 yields a credible duration failure at 22m, legacy 20m evidence may guide test selection but cannot serve as the new strict lower anchor. A same-profile/server-clock lower anchor must then be obtained during refinement before claiming a strict bracket.

## Decision

Continue R4 at 22m. Do not waste turns revalidating every lower historical class unless a 22m failure forces bracket construction.
