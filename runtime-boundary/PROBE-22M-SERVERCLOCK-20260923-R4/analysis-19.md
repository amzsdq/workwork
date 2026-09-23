# R4 causal validity review

## Internal validity

Variables intentionally held fixed relative to the intended 22m revalidation:
- target = 22m,
- planned gap = +3m,
- profile = W3 MIXED_IO,
- same automation pre-arm,
- same server-clock marker protocol,
- no live parallel/overlap experiment.

The principal change from R3 is execution strategy: sufficient bounded work queue + sparse checkpoints + no voluntary close on queue exhaustion. This is necessary because R3's early close was an identified execution defect, not a treatment variable of interest.

## External validity

A successful W3 22m result does not establish universal safety. Generalization still requires profile coverage near the eventual candidate. The coarse ascent deliberately rotates profiles to discover profile-specific weaknesses.

## Construct validity

- Survival is measured by authoritative WORKED + close/failure outcome.
- Productive window is not equated with survival.
- Completion envelope is not equated with scheduler wake success.
- Wake continuation is a retrospective gate, not part of WORKED.

## Conclusion

R4 is a valid corrective repeat of SC-A22-CLOCK-01 and can contribute strict boundary evidence if it reaches terminal classification with a valid marker pair.
