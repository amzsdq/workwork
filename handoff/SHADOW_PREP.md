# Useful SHADOW preparation

The successor's overlap interval should contain work that directly reduces post-transfer startup latency.

Count as useful preparation:
- reading the authority record and latest predecessor checkpoint,
- reconstructing current objective and constraints,
- reading files required for the next non-duplicating unit,
- identifying the exact next unit and its expected side effects,
- validating that the proposed unit does not duplicate the predecessor's in-flight unit,
- preparing a bounded execution plan and READY evidence.

Do not count idle waiting, repeated unchanged reads without a decision need, or speculative authoritative writes.

READY means the successor can begin the proposed unit immediately after a valid authority transfer without another broad bootstrap pass.
