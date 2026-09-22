# A unit 003 — throughput accounting model

For this probe:

- wall_clock_probe_sec = max(A_end,B_end) - min(A_start,B_start)
- combined_active_worker_sec = A_active_work_sec + B_active_work_sec
- parallelism_factor = combined_active_worker_sec / wall_clock_probe_sec

A factor above 1.0 demonstrates overlapping worker-time, but does not by itself prove useful throughput gain. Promotion additionally requires disjoint completed units, zero duplicate units, zero shared-write conflicts, and work products that would otherwise have consumed serial runtime.

A conservative useful-gain estimate should discount bootstrap/control seconds from each worker before comparing with the one-worker wall-clock baseline.
