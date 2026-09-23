# Unit 15 — Gap-variable separation audit

Probe: PROBE-14M-20260923T095323KST

During runtime-boundary search, planned_gap remains fixed at +3m so wake-gap optimization does not confound duration classification. Actual idle gap is measured retrospectively and may differ because of target overshoot and close overhead.

Only after the runtime policy is sufficiently characterized should planned gap move 3m -> 2m -> 1m, with overlap and continuation reliability measured separately.
