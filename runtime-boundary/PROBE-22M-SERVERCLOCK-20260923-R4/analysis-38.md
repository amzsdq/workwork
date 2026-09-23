# R4 external-interference pre-close audit plan

Immediately before durable close, re-read fresh state/current.json and the master pointer.

## Purpose

Detect whether another actor/invocation changed:
- active probe identity,
- case identity,
- scheduler/control expectations,
- clock protocol,
- boundary state.

## Rule

If fresh canonical state has advanced or assigned ownership elsewhere, do not blindly overwrite it with R4 terminal bookkeeping. Reconcile the conflict first and classify any synchronization/control anomaly separately from duration.

## Why this matters

The project has historical concurrent-control evidence. Even though live overlap is deferred, an external/manual write can still create a stale-writer problem. Terminal synchronization must be based on fresh SHAs and current state.

## R4

This check is mandatory before terminal state writes, but it does not authorize scheduler mutation at normal close.
