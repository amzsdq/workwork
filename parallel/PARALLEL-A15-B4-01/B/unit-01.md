# B unit 01

This probe distinguishes invocation overlap from useful parallelism. A valid gain requires A to continue independent bounded work after B starts, while B completes separate bounded work. Static A/B partitioning avoids claim contention, so this is a best-case baseline for parallel throughput. Promotion requires post-B-start A evidence, completed B units, no duplicate units, and no shared-write or scheduler conflict.
