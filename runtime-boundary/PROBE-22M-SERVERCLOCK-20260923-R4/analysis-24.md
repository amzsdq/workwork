# R4 server-clock protocol edge cases

## Marker identity collision

Each probe uses a unique probe_id in both marker bodies. Classification must match marker IDs to the same probe/case; merely finding two nearby comments is insufficient.

## Comment update risk

Markers are intended immutable. The authoritative field is created_at, not updated_at. Marker comments must not be edited to represent a different event.

## Duplicate END marker

Normal close creates exactly one END marker. If a retry accidentally creates another, terminal evidence must explicitly select the first valid intended END associated with the durable close checkpoint and record the anomaly; do not choose a later marker to inflate WORKED.

## Missing raw fetch

If the connector creates a marker but raw REST fetch cannot recover server created_at, exact duration is CLOCK_EVIDENCE_INVALID until recovered. Model/local time cannot fill the gap.

## Cross-run confusion

A successor invocation must reconcile an incomplete predecessor by durable probe_id/marker IDs before starting a replacement. This prevents a later invocation's timestamp from being paired with an earlier START.

## R4 status

R4 START marker identity is unique and raw-fetch validated. END remains pending.
