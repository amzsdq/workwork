from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterable, Optional

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
    case_id: Optional[str] = None
    workload_profile: Optional[str] = None
    clock_protocol: Optional[str] = None
    start_marker_comment_id: Optional[int] = None
    start_marker_created_at: Optional[str] = None
    work_start_marker_comment_id: Optional[int] = None
    work_start_marker_created_at: Optional[str] = None
    pre_close_marker_comment_id: Optional[int] = None
    pre_close_marker_created_at: Optional[str] = None
    end_marker_comment_id: Optional[int] = None
    end_marker_created_at: Optional[str] = None
    harness_version: Optional[str] = None
    close_trigger: Optional[str] = None
    generated_unique_units: int = 0
    duplicate_units_rejected: int = 0
    batches_completed: int = 0
    scheduler_write_ok: bool = False
    scheduler_state_ok: bool = False
    checkpoint_saved: bool = False
    clean_close: bool = False
    forced_stop_or_timeout: bool = False
    non_duration_failure: bool = False
    substantive_unit_count: int = 0
    active_work_sec: Optional[int] = None
    productive_ratio: Optional[float] = None
    recorded_worked_sec: Optional[int] = None
    prior_next_wake_observed: bool = False
    legacy: bool = False
    anomalies: list[str] = field(default_factory=list)


def interval_metrics(p: Probe) -> dict:
    out = {
        "worked_sec": None,
        "prearm_overhead_sec": None,
        "productive_window_sec": None,
        "close_overhead_sec": None,
        "productive_marker_pair_valid": False,
    }
    if p.start_marker_created_at and p.end_marker_created_at:
        out["worked_sec"] = worked_sec(p.start_marker_created_at, p.end_marker_created_at)
    if p.start_marker_created_at and p.work_start_marker_created_at:
        out["prearm_overhead_sec"] = worked_sec(p.start_marker_created_at, p.work_start_marker_created_at)
    if p.work_start_marker_created_at and p.pre_close_marker_created_at:
        out["productive_window_sec"] = worked_sec(p.work_start_marker_created_at, p.pre_close_marker_created_at)
        out["productive_marker_pair_valid"] = (
            p.work_start_marker_comment_id is not None and p.pre_close_marker_comment_id is not None
        )
    if p.pre_close_marker_created_at and p.end_marker_created_at:
        out["close_overhead_sec"] = worked_sec(p.pre_close_marker_created_at, p.end_marker_created_at)
    return out


def classify(p: Probe) -> dict:
    """Pure classifier. Never mutates empirical bounds or trusts model elapsed time."""
    if p.legacy or p.clock_protocol != SERVER_CLOCK:
        return {"probe_id": p.probe_id, "result": "LEGACY_SUPPORTING", "boundary_effect": "NONE", "worked_sec": None, "marker_pair_valid": False, "anomalies": list(p.anomalies)}

    anomalies = list(p.anomalies)
    marker_ids_complete = p.start_marker_comment_id is not None and p.end_marker_comment_id is not None
    marker_times_complete = bool(p.start_marker_created_at and p.end_marker_created_at)

    if p.non_duration_failure:
        worked = None
        if marker_times_complete:
            try:
                worked = worked_sec(p.start_marker_created_at, p.end_marker_created_at)
            except ValueError as exc:
                anomalies.append(f"CLOCK_INVALID:{exc}")
        return {"probe_id": p.probe_id, "result": "NON_DURATION_FAIL", "boundary_effect": "NONE", "worked_sec": worked, "marker_pair_valid": marker_ids_complete and marker_times_complete and worked is not None, "anomalies": anomalies}

    if not marker_ids_complete:
        anomalies.append("MARKER_ID_PAIR_INCOMPLETE")
    if not marker_times_complete:
        anomalies.append("MARKER_TIMESTAMP_PAIR_INCOMPLETE")
    if not marker_ids_complete or not marker_times_complete:
        return {"probe_id": p.probe_id, "result": "CLOCK_EVIDENCE_INVALID", "boundary_effect": "NONE", "worked_sec": None, "marker_pair_valid": False, "anomalies": anomalies}

    try:
        worked = worked_sec(p.start_marker_created_at, p.end_marker_created_at)
    except ValueError as exc:
        anomalies.append(f"CLOCK_INVALID:{exc}")
        return {"probe_id": p.probe_id, "result": "CLOCK_EVIDENCE_INVALID", "boundary_effect": "NONE", "worked_sec": None, "marker_pair_valid": False, "anomalies": anomalies}

    if p.recorded_worked_sec is not None and p.recorded_worked_sec != worked:
        anomalies.append(f"RECORDED_WORKED_MISMATCH:{p.recorded_worked_sec}!={worked}")
    if p.productive_ratio is not None and p.active_work_sec is None:
        anomalies.append("PRODUCTIVE_RATIO_WITHOUT_DIRECT_ACTIVE_WORK")
    if p.active_work_sec is not None and p.active_work_sec > worked:
        anomalies.append("ACTIVE_WORK_EXCEEDS_WORKED")

    if worked < p.target_runtime_sec:
        if p.close_trigger == "WORKLOAD_EXHAUSTED":
            result = "HARNESS_UNDER_TARGET"
            anomalies.append("FINITE_WORKLOAD_EXHAUSTION_IS_HARNESS_DEFECT")
        else:
            result = "UNDER_TARGET"
    elif p.forced_stop_or_timeout:
        result = "DURATION_FAIL_CANDIDATE"
        if p.clean_close:
            anomalies.append("INCONSISTENT_FORCED_STOP_AND_CLEAN_CLOSE")
    elif (p.scheduler_write_ok and p.scheduler_state_ok and p.checkpoint_saved and p.clean_close
          and p.substantive_unit_count > 0):
        result = "CLEAN_PASS_PENDING_WAKE"
    else:
        result = "AMBIGUOUS"

    metrics = interval_metrics(p)
    return {
        "probe_id": p.probe_id,
        "result": result,
        "boundary_effect": "NONE",
        "worked_sec": worked,
        "marker_pair_valid": True,
        "prearm_overhead_sec": metrics["prearm_overhead_sec"],
        "productive_window_sec": metrics["productive_window_sec"],
        "close_overhead_sec": metrics["close_overhead_sec"],
        "productive_marker_pair_valid": metrics["productive_marker_pair_valid"],
        "harness_version": p.harness_version,
        "close_trigger": p.close_trigger,
        "generated_unique_units": p.generated_unique_units,
        "duplicate_units_rejected": p.duplicate_units_rejected,
        "batches_completed": p.batches_completed,
        "anomalies": anomalies,
    }


def retrospective_wake(result: dict, wake_observed: bool) -> dict:
    out = dict(result)
    if result.get("result") == "CLEAN_PASS_PENDING_WAKE" and wake_observed:
        out["result"] = "CLEAN_PASS_WAKE_OK"
        out["boundary_effect"] = "SAFE_LOWER_BOUND_MAY_ADVANCE"
    return out


def reconcile_duplicate_records(records: Iterable[Probe]) -> dict[str, Probe]:
    """Collapse duplicate normalized records conservatively.

    Exact duplicates are harmless. Conflicting records for the same probe are rejected
    rather than merged because field-wise merging can fabricate a marker pair or clean close.
    """
    out: dict[str, Probe] = {}
    for record in records:
        prior = out.get(record.probe_id)
        if prior is None:
            out[record.probe_id] = record
        elif prior != record:
            raise ValueError(f"CONFLICTING_DUPLICATE_PROBE:{record.probe_id}")
    return out


def derive_bounds(classified: Iterable[dict]) -> dict:
    """Derive only facts justified by terminal classifications.

    A failure candidate is deliberately not promoted to a confirmed boundary here.
    Confirmation requires profile-controlled reproduction outside this pure aggregator.
    """
    clean = [r for r in classified if r.get("result") == "CLEAN_PASS_WAKE_OK"]
    failure_candidates = [r for r in classified if r.get("result") == "DURATION_FAIL_CANDIDATE"]
    clean_targets = [r.get("target_runtime_sec") for r in clean if isinstance(r.get("target_runtime_sec"), int)]
    return {
        "server_clock_safe_lower_bound_sec": max(clean_targets) if clean_targets else None,
        "server_clock_failure_boundary_sec": None,
        "duration_failure_candidate_count": len(failure_candidates),
        "clean_wake_ok_count": len(clean),
    }


if __name__ == "__main__":
    corpus = [
        Probe("R3", 1320, clock_protocol=SERVER_CLOCK, start_marker_comment_id=1, start_marker_created_at="2026-09-23T13:32:22Z", end_marker_comment_id=2, end_marker_created_at="2026-09-23T13:43:14Z", scheduler_write_ok=True, scheduler_state_ok=True, checkpoint_saved=True, clean_close=True, substantive_unit_count=137, recorded_worked_sec=652),
        Probe("R4", 1320, clock_protocol=SERVER_CLOCK, start_marker_comment_id=3, start_marker_created_at="2026-09-23T13:58:33Z", end_marker_comment_id=4, end_marker_created_at="2026-09-23T14:10:49Z", scheduler_write_ok=True, scheduler_state_ok=True, checkpoint_saved=True, clean_close=True, substantive_unit_count=40, recorded_worked_sec=736),
        Probe("R5", 1320, clock_protocol=SERVER_CLOCK, non_duration_failure=True),
        Probe("R6", 1320, clock_protocol=SERVER_CLOCK, start_marker_comment_id=5, start_marker_created_at="2026-09-23T15:23:53Z", end_marker_comment_id=6, end_marker_created_at="2026-09-23T15:40:08Z", scheduler_write_ok=True, scheduler_state_ok=True, checkpoint_saved=True, clean_close=True, substantive_unit_count=59, recorded_worked_sec=975),
    ]
    for probe in corpus:
        print(classify(probe))
