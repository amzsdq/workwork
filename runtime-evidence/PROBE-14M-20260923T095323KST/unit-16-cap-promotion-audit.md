# Unit 16 — Cap-promotion audit

Probe: PROBE-14M-20260923T095323KST

Even if this run closes cleanly, 14m cannot become OPERATING_CAP from one pass. Promotion requires repeated clean closes at/near the candidate (initially >=5), no unresolved failure at/below it, preserved pre-arm and durable close evidence, wake observations where measurable, and an explicit safety margin below the credible failure boundary.

This preserves the distinction between `highest observed clean class` and `production operating cap`.
