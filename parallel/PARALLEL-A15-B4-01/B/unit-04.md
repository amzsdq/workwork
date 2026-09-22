# B unit 04

Parallel useful work and scheduler authority should be separated. Multiple workers can safely process disjoint immutable units, but only one designated scheduler writer should control the next wake. This preserves horizontal work parallelism without turning scheduler state into a last-writer-wins race. A scalable version therefore needs a work-plane with multiple workers and a single fenced control-plane writer.
