# R4 wake-jitter separation audit

## Observed supporting samples

Historical continuation/wake lateness includes small and large values, including approximately +4s, +21s, and +168s in prior experiments.

## Why jitter is separate

WORKED is bounded by START/END server markers within the current invocation. Wake lateness occurs at continuation and therefore affects relay idle/overlap behavior, not the elapsed duration already measured for the predecessor.

## Strict gate behavior

A clean predecessor run remains pending until a later invocation is actually observed. Large lateness can delay promotion, but unless the scheduler/provider failure is causally tied to runtime duration it must not lower the runtime boundary.

## Later optimization

Phase D will vary planned gap only after runtime policy stabilizes. Phase C overlap testing may absorb jitter by waking successors before predecessor close, but that must be evaluated with single-owner fencing and server-authoritative handoff markers.

## R4

Keep +3m fixed and do not reinterpret wake jitter as evidence about 22m survival.
