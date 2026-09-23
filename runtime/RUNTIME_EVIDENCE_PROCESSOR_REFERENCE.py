from __future__ import annotations
from dataclasses import dataclass,field
from datetime import datetime
from typing import Iterable,Optional
SERVER_CLOCK="GITHUB_SERVER_MARKER_V1";HARNESS_V2="STRICT_RUNTIME_HARNESS_V2"
def parse_github_ts(v):
    if not v or not v.endswith("Z"):raise ValueError("GitHub marker timestamp must be UTC Z form")
    return datetime.fromisoformat(v.replace("Z","+00:00"))
def worked_sec(a,b):
    s=int((parse_github_ts(b)-parse_github_ts(a)).total_seconds())
    if s<0:raise ValueError("END marker precedes START marker")
    return s
@dataclass
class Probe:
    probe_id:str;target_runtime_sec:int;case_id:Optional[str]=None;workload_profile:Optional[str]=None;clock_protocol:Optional[str]=None
    start_marker_comment_id:Optional[int]=None;start_marker_created_at:Optional[str]=None;work_start_marker_comment_id:Optional[int]=None;work_start_marker_created_at:Optional[str]=None;pre_close_marker_comment_id:Optional[int]=None;pre_close_marker_created_at:Optional[str]=None;end_marker_comment_id:Optional[int]=None;end_marker_created_at:Optional[str]=None
    harness_version:Optional[str]=None;harness_valid:Optional[bool]=None;close_trigger:Optional[str]=None;generated_unique_units:int=0;semantic_unique_units:int=0;duplicate_units_rejected:int=0;semantic_repeats_rejected:int=0;batches_completed:int=0
    scheduler_write_ok:bool=False;scheduler_state_ok:bool=False;checkpoint_saved:bool=False;clean_close:bool=False;forced_stop_or_timeout:bool=False;non_duration_failure:bool=False;substantive_unit_count:int=0;active_work_sec:Optional[int]=None;productive_ratio:Optional[float]=None;recorded_worked_sec:Optional[int]=None;prior_next_wake_observed:bool=False;legacy:bool=False;anomalies:list[str]=field(default_factory=list)
def interval_metrics(p):
    out={"prearm_overhead_sec":None,"productive_window_sec":None,"close_overhead_sec":None,"productive_marker_pair_valid":False,"interval_anomalies":[]}
    def safe(label,a,b):
        if not a or not b:return None
        try:return worked_sec(a,b)
        except ValueError as e:out["interval_anomalies"].append(f"{label}_INVALID:{e}");return None
    out["prearm_overhead_sec"]=safe("PREARM",p.start_marker_created_at,p.work_start_marker_created_at);out["productive_window_sec"]=safe("PRODUCTIVE_WINDOW",p.work_start_marker_created_at,p.pre_close_marker_created_at);out["close_overhead_sec"]=safe("CLOSE_OVERHEAD",p.pre_close_marker_created_at,p.end_marker_created_at)
    out["productive_marker_pair_valid"]=p.work_start_marker_comment_id is not None and p.pre_close_marker_comment_id is not None and out["productive_window_sec"] is not None
    return out
def base_result(p):return {"probe_id":p.probe_id,"target_runtime_sec":p.target_runtime_sec,"case_id":p.case_id,"workload_profile":p.workload_profile}
def classify(p):
    base=base_result(p)
    if p.legacy or p.clock_protocol!=SERVER_CLOCK:return {**base,"result":"LEGACY_SUPPORTING","boundary_effect":"NONE","worked_sec":None,"marker_pair_valid":False,"anomalies":list(p.anomalies)}
    an=list(p.anomalies);ids=p.start_marker_comment_id is not None and p.end_marker_comment_id is not None;times=bool(p.start_marker_created_at and p.end_marker_created_at)
    if p.non_duration_failure:
        w=None
        if times:
            try:w=worked_sec(p.start_marker_created_at,p.end_marker_created_at)
            except ValueError as e:an.append(f"CLOCK_INVALID:{e}")
        return {**base,"result":"NON_DURATION_FAIL","boundary_effect":"NONE","worked_sec":w,"marker_pair_valid":ids and times and w is not None,"anomalies":an}
    if not ids:an.append("MARKER_ID_PAIR_INCOMPLETE")
    if not times:an.append("MARKER_TIMESTAMP_PAIR_INCOMPLETE")
    if not ids or not times:return {**base,"result":"CLOCK_EVIDENCE_INVALID","boundary_effect":"NONE","worked_sec":None,"marker_pair_valid":False,"anomalies":an}
    try:w=worked_sec(p.start_marker_created_at,p.end_marker_created_at)
    except ValueError as e:return {**base,"result":"CLOCK_EVIDENCE_INVALID","boundary_effect":"NONE","worked_sec":None,"marker_pair_valid":False,"anomalies":an+[f"CLOCK_INVALID:{e}"]}
    if p.recorded_worked_sec is not None and p.recorded_worked_sec!=w:an.append(f"RECORDED_WORKED_MISMATCH:{p.recorded_worked_sec}!={w}")
    if p.productive_ratio is not None and p.active_work_sec is None:an.append("PRODUCTIVE_RATIO_WITHOUT_DIRECT_ACTIVE_WORK")
    if p.active_work_sec is not None and p.active_work_sec>w:an.append("ACTIVE_WORK_EXCEEDS_WORKED")
    harness_quality_ok=True
    if p.harness_version==HARNESS_V2:
        harness_quality_ok=p.harness_valid is True and p.semantic_unique_units>0
        if p.harness_valid is not True:an.append("HARNESS_V2_VALIDITY_NOT_PROVEN")
        if p.semantic_unique_units<=0:an.append("HARNESS_V2_SEMANTIC_WORK_NOT_PROVEN")
    if w<p.target_runtime_sec:
        result="HARNESS_UNDER_TARGET" if p.close_trigger=="WORKLOAD_EXHAUSTED" else "UNDER_TARGET"
        if result=="HARNESS_UNDER_TARGET":an.append("FINITE_WORKLOAD_EXHAUSTION_IS_HARNESS_DEFECT")
    elif p.forced_stop_or_timeout:
        result="DURATION_FAIL_CANDIDATE"
        if p.clean_close:an.append("INCONSISTENT_FORCED_STOP_AND_CLEAN_CLOSE")
    elif p.scheduler_write_ok and p.scheduler_state_ok and p.checkpoint_saved and p.clean_close and p.substantive_unit_count>0 and harness_quality_ok:result="CLEAN_PASS_PENDING_WAKE"
    else:result="AMBIGUOUS"
    m=interval_metrics(p);an.extend(m["interval_anomalies"])
    return {**base,"result":result,"boundary_effect":"NONE","worked_sec":w,"marker_pair_valid":True,"prearm_overhead_sec":m["prearm_overhead_sec"],"productive_window_sec":m["productive_window_sec"],"close_overhead_sec":m["close_overhead_sec"],"productive_marker_pair_valid":m["productive_marker_pair_valid"],"harness_version":p.harness_version,"harness_valid":p.harness_valid,"close_trigger":p.close_trigger,"generated_unique_units":p.generated_unique_units,"semantic_unique_units":p.semantic_unique_units,"duplicate_units_rejected":p.duplicate_units_rejected,"semantic_repeats_rejected":p.semantic_repeats_rejected,"batches_completed":p.batches_completed,"anomalies":an}
def retrospective_wake(r,wake):
    out=dict(r)
    if r.get("result")=="CLEAN_PASS_PENDING_WAKE" and wake:out["result"]="CLEAN_PASS_WAKE_OK";out["boundary_effect"]="SAFE_LOWER_BOUND_MAY_ADVANCE"
    return out
def reconcile_duplicate_records(records:Iterable[Probe]):
    out={}
    for x in records:
        if x.probe_id not in out:out[x.probe_id]=x
        elif out[x.probe_id]!=x:raise ValueError(f"CONFLICTING_DUPLICATE_PROBE:{x.probe_id}")
    return out
def derive_bounds(rows):
    clean=[r for r in rows if r.get("result")=="CLEAN_PASS_WAKE_OK"];fails=[r for r in rows if r.get("result")=="DURATION_FAIL_CANDIDATE"];targets=[r.get("target_runtime_sec") for r in clean if isinstance(r.get("target_runtime_sec"),int)]
    return {"server_clock_safe_lower_bound_sec":max(targets) if targets else None,"server_clock_failure_boundary_sec":None,"duration_failure_candidate_count":len(fails),"clean_wake_ok_count":len(clean)}
if __name__=="__main__":
    p=Probe("V2-CLEAN",1320,clock_protocol=SERVER_CLOCK,start_marker_comment_id=1,start_marker_created_at="2026-09-23T17:47:04Z",end_marker_comment_id=2,end_marker_created_at="2026-09-23T18:09:06Z",harness_version=HARNESS_V2,harness_valid=True,semantic_unique_units=1,scheduler_write_ok=True,scheduler_state_ok=True,checkpoint_saved=True,clean_close=True,substantive_unit_count=1)
    r=retrospective_wake(classify(p),True);assert derive_bounds([r])["server_clock_safe_lower_bound_sec"]==1320
    tainted=Probe("V2-TAINT",1320,clock_protocol=SERVER_CLOCK,start_marker_comment_id=1,start_marker_created_at="2026-09-23T17:47:04Z",end_marker_comment_id=2,end_marker_created_at="2026-09-23T18:09:06Z",harness_version=HARNESS_V2,harness_valid=False,semantic_unique_units=0,scheduler_write_ok=True,scheduler_state_ok=True,checkpoint_saved=True,clean_close=True,substantive_unit_count=2048)
    assert classify(tainted)["result"]=="AMBIGUOUS"
