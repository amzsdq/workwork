# B unit 05

Spawn timing should eventually be optimized against measured bootstrap cost and available independent work. A useful adaptive rule is to spawn only when the remaining primary horizon is comfortably larger than expected B bootstrap plus a minimum useful-work window. This prevents paying concurrency overhead for a worker that becomes productive only as A is finishing.
