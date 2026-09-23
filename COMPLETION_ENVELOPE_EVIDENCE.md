# Completion Envelope Evidence

Purpose: keep direct close/completion timing evidence separate from target-survival evidence. This is a derived audit view; raw events and per-probe evidence remain authoritative.

| Probe/class | Target | Actual elapsed | Overshoot | Direct close overhead | Inferred pre-close offset from target | Clean close | Confidence |
|---|---:|---:|---:|---:|---:|---|---|
| 12m mixed-load canonical pass | 720s | 761s | 41s | 32s | +9s | yes | direct close-overhead sample |
| 14m W3 clean pass | 840s | 928s | 88s | unknown | unknown | yes | close overhead not isolated |
| 16m W4 clean pass | 960s | >=996s | >=36s | unknown | unknown | yes | close overhead not isolated |

For the 12m row only, `pre_close_offset = overshoot - close_overhead = 41 - 32 = +9s`, assuming the canonical event's elapsed/overshoot/close-overhead clocks share the same close endpoint as recorded. This is useful as one completion-envelope observation, not a universal cutoff.

## Current conclusion

- Direct `close_overhead_sec` sample count N = 1.
- Observed direct sample = 32s.
- Under `CLOSE_RESERVE_ESTIMATOR.md`, N=1 is LOW_CONFIDENCE; max/median are both 32s and no promoted reserve is justified yet.
- The configured `close_reserve_sec=60` in current state is therefore conservative/provisional configuration, not an empirically promoted reserve.
- 14m and 16m overshoot cannot be substituted for close overhead because their pre-close timestamps were not isolated.
- The active 18m W2 probe should capture `pre_close_ts` and `close_end_ts` directly to add the second valid close-overhead sample if it reaches clean close.
