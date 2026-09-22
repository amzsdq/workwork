# Clean handoff sample acceptance

A handoff sample is CLEAN only if all of the following are evidenced:
- scheduled successor wake is observed,
- successor starts as SHADOW and does not perform authoritative work before transfer,
- successor reaches READY with a concrete non-duplicating next unit,
- predecessor remains sole owner until transfer,
- transfer owner-record update succeeds with generation increment,
- predecessor performs no authoritative work after transfer,
- successor fresh-reads and accepts the transferred generation,
- successor begins the prepared unit,
- no scheduler-writer collision occurs,
- no checkpoint is lost,
- timing fields needed for handoff gap and overlap are recorded.

A technically successful concurrent wake without authority transfer is not a clean handoff sample; it is only overlap evidence.
