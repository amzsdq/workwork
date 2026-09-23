from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, timezone
from typing import Iterable
from RUNTIME_STRESS_WORKLOAD_GENERATOR import WorkUnit, batch
from RUNTIME_EVIDENCE_PROCESSOR_REFERENCE import Probe, SERVER_CLOCK, classify, retrospective_wake

BASE=datetime(2026,1,1,tzinfo=timezone.utc)
def z(dt:datetime)->str:return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

@dataclass
class Evaluation:
    case_id:str; ordinal:int; passed:bool; result:str; expected_family:str; anomalies:list[str]

def build_probe(row:dict,target_sec:int=1440)->Probe:
    start=BASE
    # valid cases straddle target by deterministic delta; malformed marker cases exercise fail-closed paths.
    end=start+timedelta(seconds=max(0,target_sec+row["target_delta_sec"]))
    sid=100000+row["ordinal"]*4; eid=sid+3
    start_id=sid; end_id=eid; start_ts=z(start); end_ts=z(end)
    ms=row["marker_state"]
    if ms=="missing_start": start_id=None; start_ts=None
    elif ms=="missing_end": end_id=None; end_ts=None
    elif ms=="reversed": start_ts=z(end+timedelta(seconds=1)); end_ts=z(start)
    elif ms=="id_mismatch": start_id=None  # pure classifier treats failed raw-ID verification as absent identity

    scheduler_ok=row["scheduler_state"]=="ok"
    close_clean=row["close_state"]=="clean"
    forced=row["close_state"]=="forced_stop"
    provider_fail=row["provider_state"]=="non_duration_fail"
    work_start=start+timedelta(seconds=5)
    pre_close=end-timedelta(seconds=max(1,min(row["close_reserve_sec"],max(1,int((end-start).total_seconds())-6))))
    return Probe(
        probe_id=row["case_id"],target_runtime_sec=target_sec,case_id="SC-A24-CLOCK+",workload_profile=row["workload_shape"],clock_protocol=SERVER_CLOCK,
        start_marker_comment_id=start_id,start_marker_created_at=start_ts,
        work_start_marker_comment_id=sid+1,work_start_marker_created_at=z(work_start),
        pre_close_marker_comment_id=sid+2,pre_close_marker_created_at=z(pre_close),
        end_marker_comment_id=end_id,end_marker_created_at=end_ts,
        harness_version="STRICT_RUNTIME_HARNESS_V2",generated_unique_units=1,batches_completed=1,
        scheduler_write_ok=scheduler_ok,scheduler_state_ok=scheduler_ok,
        checkpoint_saved=close_clean,clean_close=close_clean,forced_stop_or_timeout=forced,
        non_duration_failure=provider_fail,substantive_unit_count=1,close_trigger="TIMING_ADMISSION")

def expected_family(row:dict,target_sec:int=1440)->str:
    if row["provider_state"]=="non_duration_fail": return "NON_DURATION_FAIL"
    if row["marker_state"]!="valid": return "CLOCK_EVIDENCE_INVALID"
    if target_sec+row["target_delta_sec"]<target_sec: return "UNDER_TARGET"
    if row["close_state"]=="forced_stop": return "DURATION_FAIL_CANDIDATE"
    if row["scheduler_state"]!="ok" or row["close_state"]!="clean": return "AMBIGUOUS"
    return "CLEAN_PASS_PENDING_WAKE"

def evaluate(row:dict,target_sec:int=1440)->Evaluation:
    r=classify(build_probe(row,target_sec)); expected=expected_family(row,target_sec)
    ok=r["result"]==expected
    # Wake observation can only promote a pending clean pass.
    rr=retrospective_wake(r,row["wake_state"]=="observed")
    if r["result"]=="CLEAN_PASS_PENDING_WAKE" and row["wake_state"]=="observed": ok=ok and rr["result"]=="CLEAN_PASS_WAKE_OK"
    elif rr["result"]!=r["result"]: ok=False
    return Evaluation(row["case_id"],row["ordinal"],ok,r["result"],expected,r.get("anomalies",[]))

def run(seed:str,start:int,count:int,target_sec:int=1440)->dict:
    rows=batch(seed,start,count); results=[evaluate(r,target_sec) for r in rows]
    failed=[asdict(r) for r in results if not r.passed]
    return {"seed":seed,"start":start,"count":count,"passed":count-len(failed),"failed":len(failed),"failures":failed[:50]}

if __name__=="__main__":
    report=run("SC-A24-CLOCK:R10:EVAL",0,5000)
    assert report["failed"]==0,report["failures"][:3]
    print(report)
