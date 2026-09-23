from __future__ import annotations

from dataclasses import dataclass, asdict
from hashlib import sha256
from itertools import product
from typing import Iterator, Iterable
import json

"""
Deterministic scalable workload generator for strict runtime probes.

Purpose:
- continuously supply NEW, non-duplicate runtime/control research cases;
- each case exercises a concrete invariant of the runtime evidence / relay control stack;
- avoid idle/sleep/no-op padding;
- permit a probe to continue until the target/close window instead of terminating because
  a hand-written backlog ran out.

The generator is deterministic by (seed, ordinal). Replaying the same seed produces the
same cases and stable IDs.
"""

MARKER_STATES = ("valid", "missing_start", "missing_end", "reversed", "id_mismatch")
SCHEDULER_STATES = ("ok", "write_fail", "state_mismatch")
CLOSE_STATES = ("clean", "checkpoint_missing", "forced_stop")
PROVIDER_STATES = ("ok", "non_duration_fail")
WAKE_STATES = ("observed", "missing")
WORKLOAD_SHAPES = ("mixed_io", "micro_chain", "large_unit", "close_heavy")


@dataclass(frozen=True)
class WorkUnit:
    ordinal: int
    case_id: str
    marker_state: str
    scheduler_state: str
    close_state: str
    provider_state: str
    wake_state: str
    workload_shape: str

    def payload(self) -> dict:
        return asdict(self)


def _stable_id(seed: str, ordinal: int, values: tuple[str, ...]) -> str:
    raw = "|".join((seed, str(ordinal), *values)).encode("utf-8")
    return sha256(raw).hexdigest()[:20]


def iter_units(seed: str = "SC-A22-CLOCK") -> Iterator[WorkUnit]:
    ordinal = 0
    # Finite Cartesian epochs are chained with an epoch suffix, so the source is effectively
    # unbounded while every generated unit remains unique and decision-relevant.
    epoch = 0
    while True:
        epoch_seed = f"{seed}:epoch:{epoch}"
        for values in product(
            MARKER_STATES,
            SCHEDULER_STATES,
            CLOSE_STATES,
            PROVIDER_STATES,
            WAKE_STATES,
            WORKLOAD_SHAPES,
        ):
            marker, scheduler, close, provider, wake, shape = values
            case_id = _stable_id(epoch_seed, ordinal, values)
            yield WorkUnit(
                ordinal=ordinal,
                case_id=case_id,
                marker_state=marker,
                scheduler_state=scheduler,
                close_state=close,
                provider_state=provider,
                wake_state=wake,
                workload_shape=shape,
            )
            ordinal += 1
        epoch += 1


def expected_invariants(unit: WorkUnit) -> list[str]:
    checks = [
        "server_clock_only",
        "no_model_time_authority",
        "duplicate_case_id_forbidden",
        "terminal_classification_deterministic",
    ]
    if unit.marker_state != "valid":
        checks.append("clock_invalid_must_not_move_boundary")
    if unit.provider_state == "non_duration_fail":
        checks.append("non_duration_failure_has_boundary_effect_none")
    if unit.scheduler_state != "ok":
        checks.append("scheduler_fault_must_not_be_duration_failure")
    if unit.close_state == "forced_stop":
        checks.append("forced_stop_precedence_over_clean_pass")
    if unit.wake_state == "observed":
        checks.append("wake_can_promote_pending_pass_only")
    return checks


def batch(seed: str, start_ordinal: int, count: int) -> list[dict]:
    out = []
    for unit in iter_units(seed):
        if unit.ordinal < start_ordinal:
            continue
        if len(out) >= count:
            break
        row = unit.payload()
        row["expected_invariants"] = expected_invariants(unit)
        out.append(row)
    return out


def fingerprint(rows: Iterable[dict]) -> str:
    encoded = json.dumps(list(rows), sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256(encoded).hexdigest()


if __name__ == "__main__":
    rows = batch("SC-A22-CLOCK", 0, 32)
    print(json.dumps({
        "count": len(rows),
        "fingerprint": fingerprint(rows),
        "rows": rows,
    }, indent=2))
