# B unit 03

Static partitioning is appropriate for the first controlled sample because ownership is obvious: A and B write separate immutable namespaces. A later dynamic-claim design should add an atomic claim record per work unit before execution; otherwise two concurrent invocations can select the same next task. Scheduler ownership should likewise remain singular even when useful work is parallelized.
