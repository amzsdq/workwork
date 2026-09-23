from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

SERVER_CLOCK = "GITHUB_SERVER_MARKER_V1"


def parse_github_ts(value: str) -> datetime:
    if not value or not value.endswith("Z"):
        raise ValueError("GitHub marker timestamp must be UTC Z form")
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def worked_sec(start_created_at: str, end_created_at: str) -> int:
    delta = parse_github_ts(end_created_at) - parse_github_ts(start_created_at)
    seconds = int(delta.total_seconds())
    if seconds < 0:
        raise ValueError("END marker precedes START marker")
    return seconds


@dataclass
class Probe:
    probe_id: str
    target_runtime_sec: int
    clock_protocol: Optional[str] = None
    start_marker_created_at: Optional[str] = None
    end_marker_created_at: Optional[str] = None
    scheduler_write_ok: bool = False
    scheduler_state_ok: bool = False
    checkpoint_saved: bool = False
    clean_close: bool = False
    forced_stop_or_timeout: bool = False
    non_duration_failure: bool = False
    substantive_unit_count: int = 0
    recorded_worked_sec: Optional[int] = None
    legacy: bool = False
    anomalies: list[str] = field(default_factory=list)


def classify(p: Probe) -> dict:
    if p.legacy or p.clock_protocol != SERVER_CLOCK:
        return {"result": "LEGACY_SUPPORTING", "boundary_effect": "NONE", "worked_sec": None}

    if not p.start_marker_created_at or not p.end_marker_created_at:
        return {"result": "CLOCK_EVIDENCE_INVALID", "boundary_effect": "NONE", "worked_sec": None}

    try:
        worked = worked_sec(p.start_marker_created_at, p.end_marker_created_at)
    except ValueError as exc:
        return {"result": "CLOCK_EVIDENCE_INVALID", "boundary_effect": "NONE", "worked_sec": None, "error": str(exc)}

    anomalies = list(p.anomalies)
    if p.recorded_worked_sec is not None and p.recorded_worked_sec != worked:
        anomalies.append(f"RECORDED_WORKED_MISMATCH:{p.recorded_worked_sec}!={worked}")

    if p.non_duration_failure:
        result = "NON_DURATION_FAIL"
    elif worked < p.target_runtime_sec:
        result = "UNDER_TARGET"
    elif (p.scheduler_write_ok and p.scheduler_state_ok and p.checkpoint_saved and p.clean_close
          and not p.forced_stop_or_timeout and p.substantive_unit_count > 0):
        result = "CLEAN_PASS_PENDING_WAKE"
    elif p.forced_stop_or_timeout and not p.non_duration_failure:
        result = "DURATION_FAIL_CANDIDATE"
    else:
        result = "AMBIGUOUS"

    return {"result": result, "boundary_effect": "NONE", "worked_sec": worked, "anomalies": anomalies}


def retrospective_wake(result: dict, wake_observed: bool) -> dict:
    out = dict(result)
    if result.get("result") == "CLEAN_PASS_PENDING_WAKE" and wake_observed:
        out["result"] = "CLEAN_PASS_WAKE_OK"
        out["boundary_effect"] = "SAFE_LOWER_BOUND_MAY_ADVANCE"
    return out


if __name__ == "__main__":
    corpus = [
        Probe("R3", 1320, SERVER_CLOCK, "2026-09-23T13:32:22Z", "2026-09-23T13:43:14Z", True, True, True, True, False, False, 137, 652),
        Probe("R4", 1320, SERVER_CLOCK, "2026-09-23T13:58:33Z", "2026-09-23T14:10:49Z", True, True, True, True, False, False, 40, 736),
        Probe("R5", 1320, SERVER_CLOCK, None, None, False, False, False, False, False, True, 0, None),
        Probe("R6", 1320, SERVER_CLOCK, "2026-09-23T15:23:53Z", "2026-09-23T15:40:08Z", True, True, True, True, False, False, 59, 975),
    ]
    for probe in corpus:
        print(probe.probe_id, classify(probe))
