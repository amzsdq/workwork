# Lead-time evaluation

Measure successor preparation time, predecessor safe-unit tail after READY, configured lead, actual handoff gap, residual predecessor budget, and useful shadow preparation **only when the required timing endpoints have authoritative server-side evidence**.

Model-authored timestamp strings are non-authoritative metadata. If successor start/READY/transfer/work-start timing cannot be established from server-side evidence, leave the corresponding duration unresolved rather than deriving it from prose or file fields.

A sample is clean only when ownership is unambiguous, there is no duplicate authoritative work, no scheduler-writer collision, and no checkpoint loss.

Initial candidate lead remains 180 seconds because it is the current design baseline, not because it is already empirically optimal under the final clock discipline. After runtime/cap validation, collect repeated clean authoritative samples before reducing toward 120s or 60s; increase toward 240s if 180s does not reliably cover preparation plus safe-unit tail.

Prefer the simplest fixed lead when equivalent to adaptive behavior. Any adaptive rule must use observed authoritative upper-range preparation/tail evidence plus explicit safety margin, not a single average or model-authored timing estimate.
