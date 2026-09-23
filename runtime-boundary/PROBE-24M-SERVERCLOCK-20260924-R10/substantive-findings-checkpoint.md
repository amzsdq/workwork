# R10 substantive findings checkpoint

Probe: PROBE-24M-SERVERCLOCK-20260924-R10 / SC-A24-CLOCK+

In-flight work checkpoint, not terminal duration evidence.

## Defects found/repaired
1. classifier dropped `target_runtime_sec`, breaking clean bound derivation;
2. reversed productive markers could raise instead of failing derived interval closed;
3. “immutable” terminal protocol incorrectly allowed update; now create-only/idempotent-identical;
4. generator V1 changed IDs while repeating 720 semantic scenarios; R10 count corrected and R9 audited;
5. reserve perturbation step 13 mod 91 covered only 7 values; coprime step 17 now covers 30..120;
6. broad stress outcome imbalance; balanced six-family stratification added;
7. Harness V2 clean pass lacked semantic-quality gate; now explicit harness validity + semantic units required;
8. stale `current.json active_probe_id=null` could permit duplicate probe; durable unterminated start now outranks stale null;
9. raw marker role validator used substring matching, allowing WORK_START to masquerade as START; fixed exact first-token matching;
10. raw probe/case identity validator used substring matching, allowing P to match P10; fixed exact key/value metadata matching;
11. master/evidence/acceptance/pipeline/anomaly/boundary/Phase-B docs drifted from sync/harness V2; reconciled or queued.

## Workload/evidence produced
- semantic generator V2B: 100,000 identity-unique + semantic-unique cases, 0 observed collisions, full 30..120 reserve and -60..60 skew coverage;
- conservative credited logical batches: 391 at batch size 256;
- classifier stress evaluator + balanced outcome selection;
- raw marker lifecycle validator + regressions;
- Harness V2 quality-gate tests;
- terminal evidence builder;
- 109,928-case admission grid plus 1,867,502 estimation-error expanded cases;
- strict execution checklist, preclose readiness, projection plan, close-control plan.

## Empirical cautions
R9 retains valid clean 1322s server-clock survival/close evidence, but its >=2048 ID-unique count overstated semantic decision uniqueness. Strict substantive lower-bound promotion is being revalidated/superseded by R10 rather than silently trusting it.

R10 reserve remains 60s for causal consistency; prior current-protocol close sample is 57s (N=1), so reserve is not promoted. No duration-attributable failure has been observed in R10 so far.
