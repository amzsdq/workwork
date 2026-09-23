# Clean handoff sample acceptance

A handoff sample is CLEAN only if all safety/control conditions are evidenced:
- scheduled successor wake is observed;
- successor starts as SHADOW and performs no authoritative work before transfer;
- successor reaches READY with a concrete non-duplicating next unit;
- predecessor remains sole owner until transfer;
- transfer owner-record update succeeds with generation increment;
- predecessor performs no authoritative work after transfer;
- successor fresh-reads and accepts transferred generation;
- successor begins the prepared unit;
- no scheduler-writer collision occurs;
- no checkpoint is lost.

For a sample to count in **quantitative lead/gap/overlap optimization**, every timing endpoint used in the metric must additionally have authoritative server-side timing evidence. Model-authored timestamp strings do not qualify. A safety-clean sample with unresolved authoritative timing may support protocol correctness but not exact lead/gap optimization.

A technically successful concurrent wake without authority transfer is overlap evidence only, not a clean handoff sample.
