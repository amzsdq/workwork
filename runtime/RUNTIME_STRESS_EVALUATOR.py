from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime,timedelta,timezone
from collections import Counter
from RUNTIME_STRESS_WORKLOAD_GENERATOR import batch,iter_units
from RUNTIME_EVIDENCE_PROCESSOR_REFERENCE import Probe,SERVER_CLOCK,classify,retrospective_wake
BASE=datetime(2026,1,1,tzinfo=timezone.utc)
def z(dt):return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
@dataclass
class Evaluation: case_id:str;ordinal:int;passed:bool;result:str;expected_family:str;anomalies:list[str]

def build_probe(row,target_sec=1440):
    start=BASE;end=start+timedelta(seconds=max(0,target_sec+row["target_delta_sec"]));sid=100000+row["ordinal"]*4;eid=sid+3
    start_id=sid;end_id=eid;start_ts=z(start);end_ts=z(end);ms=row["marker_state"]
    if ms=="missing_start":start_id=None;start_ts=None
    elif ms=="missing_end":end_id=None;end_ts=None
    elif ms=="reversed":start_ts=z(end+timedelta(seconds=1));end_ts=z(start)
    elif ms=="id_mismatch":start_id=None
    scheduler_ok=row["scheduler_state"]=="ok";close_clean=row["close_state"]=="clean";forced=row["close_state"]=="forced_stop";provider_fail=row["provider_state"]=="non_duration_fail"
    work_start=start+timedelta(seconds=5);pre_close=end-timedelta(seconds=max(1,min(row["close_reserve_sec"],max(1,int((end-start).total_seconds())-6))))
    return Probe(probe_id=row["case_id"],target_runtime_sec=target_sec,case_id="SC-A24-CLOCK+",workload_profile=row["workload_shape"],clock_protocol=SERVER_CLOCK,start_marker_comment_id=start_id,start_marker_created_at=start_ts,work_start_marker_comment_id=sid+1,work_start_marker_created_at=z(work_start),pre_close_marker_comment_id=sid+2,pre_close_marker_created_at=z(pre_close),end_marker_comment_id=end_id,end_marker_created_at=end_ts,harness_version="STRICT_RUNTIME_HARNESS_V2",generated_unique_units=1,batches_completed=1,scheduler_write_ok=scheduler_ok,scheduler_state_ok=scheduler_ok,checkpoint_saved=close_clean,clean_close=close_clean,forced_stop_or_timeout=forced,non_duration_failure=provider_fail,substantive_unit_count=1,close_trigger="TIMING_ADMISSION")

def expected_family(row,target_sec=1440):
    if row["provider_state"]=="non_duration_fail":return "NON_DURATION_FAIL"
    if row["marker_state"]!="valid":return "CLOCK_EVIDENCE_INVALID"
    if row["target_delta_sec"]<0:return "UNDER_TARGET"
    if row["close_state"]=="forced_stop":return "DURATION_FAIL_CANDIDATE"
    if row["scheduler_state"]!="ok" or row["close_state"]!="clean":return "AMBIGUOUS"
    return "CLEAN_PASS_PENDING_WAKE"

def evaluate(row,target_sec=1440):
    r=classify(build_probe(row,target_sec));expected=expected_family(row,target_sec);ok=r["result"]==expected;rr=retrospective_wake(r,row["wake_state"]=="observed")
    if r["result"]=="CLEAN_PASS_PENDING_WAKE" and row["wake_state"]=="observed":ok=ok and rr["result"]=="CLEAN_PASS_WAKE_OK"
    elif rr["result"]!=r["result"]:ok=False
    return Evaluation(row["case_id"],row["ordinal"],ok,r["result"],expected,r.get("anomalies",[]))

def run(seed,start,count,target_sec=1440):
    rows=batch(seed,start,count);results=[evaluate(r,target_sec) for r in rows];failed=[asdict(r) for r in results if not r.passed]
    return {"seed":seed,"start":start,"count":count,"passed":count-len(failed),"failed":len(failed),"expected_distribution":dict(Counter(r.expected_family for r in results)),"failures":failed[:50]}

def stratified(seed,per_family=100,target_sec=1440,max_scan=200000):
    families=("NON_DURATION_FAIL","CLOCK_EVIDENCE_INVALID","UNDER_TARGET","DURATION_FAIL_CANDIDATE","AMBIGUOUS","CLEAN_PASS_PENDING_WAKE")
    selected={f:[] for f in families}
    for unit in iter_units(seed):
        row=unit.payload();fam=expected_family(row,target_sec)
        if len(selected[fam])<per_family:selected[fam].append(row)
        if all(len(v)>=per_family for v in selected.values()):break
        if unit.ordinal>=max_scan:raise RuntimeError("STRATIFICATION_SCAN_LIMIT")
    results=[evaluate(r,target_sec) for fam in families for r in selected[fam]];failed=[asdict(r) for r in results if not r.passed]
    return {"families":families,"per_family":per_family,"count":len(results),"passed":len(results)-len(failed),"failed":len(failed),"failures":failed[:50]}

if __name__=="__main__":
    broad=run("SC-A24-CLOCK:R10:EVAL",0,50000);balanced=stratified("SC-A24-CLOCK:R10:STRAT",100)
    assert broad["failed"]==0,broad["failures"][:3];assert balanced["failed"]==0 and balanced["count"]==600,balanced
    print({"broad":broad,"balanced":balanced})
