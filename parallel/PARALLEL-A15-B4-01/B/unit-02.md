# B unit 02

Policy replay: early parallel wake is useful when B bootstrap plus coordination cost is substantially less than remaining A horizon. Unlike EARLY_READY_HANDOFF, B does not consume A residual budget: both workers continue useful work. Therefore, if disjoint tasks are available, the optimization variable shifts from successor lead time to spawn timing versus bootstrap amortization. Earlier spawning increases potential throughput but also increases total concurrent resource use and coordination exposure.
