# Evidence Integrity Note

Historical event timestamps are preserved but may be non-monotonic relative to append order. They must not be rewritten merely to look consistent.

## Final strict rule
For post-activation runtime duration classification, only raw GitHub issue-comment START/END server `created_at` values establish WORKED.

Event `ts`, file `updated_at`, model-authored KST/UTC strings, commit prose, and append order are never substitutes for the strict marker pair.

When any secondary timestamp conflicts with durable ordering or lacks an authoritative source:
- preserve the record;
- mark timing trust/scope explicitly;
- exclude it from strict duration, exact idle-gap, wake-lateness, overlap, or handoff-gap calculations unless independently corroborated by an authoritative server source.

## Historical example
A later-appended record previously carried an earlier model timestamp than a prior event. Its artifact-existence meaning remains valid; its timing meaning is excluded.

Boundary effect of suspect secondary timestamps: NONE unless authoritative evidence independently establishes a runtime event.
