from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterable, Optional
SERVER_CLOCK="GITHUB_SERVER_MARKER_V1"

def parse_github_ts(value:str)->datetime:
    if not value or not value.endswith("Z"): raise ValueError("GitHub marker timestamp must be UTC Z form")
    return datetime.fromisoformat(value.replace("Z","+00:00"))

def worked_sec(start_created_at:str,end_created_at:str)->int:
    seconds=int((parse_github_ts(end_created_at)-parse_github_ts(start_created_at)).total_seconds())
    if seconds<0: raise ValueError("END marker precedes START marker")
    return seconds

@dataclass
class Probe:
    probe_id:str; target_runtime_sec:int; case_id:Optional[str]=None; workload_profile:Optional[str]=None; clock_protocol:Optional[str]=None
    start_marker_comment_id:Optional[int]=None; start_marker_created_at:Optional[str]=None
    work_start_marker_comment_id:Optional[int]=None; work_start_marker_created_at:Optional[str]=None
    pre_close_marker_comment_id:Optional[int]=None; pre_close_marker_created_at:Optional[str]=None
    end_marker_comment_id:Optional[int]=None; end_marker_created_at:Optional[str]=None
    harness_version:Optional[str]=None; close_trigger:Optional[str]=None; generated_unique_units:int=0; duplicate_units_rejected:int=0; batches_completed:int=0
    scheduler_write_ok:bool=False; scheduler_state_ok:bool=False; checkpoint_saved:bool=False; clean_close:bool=False; forced_stop_or_timeout:bool=False; non_duration_failure:bool=False
    substantive_unit_count:int=0; active_work_sec:Optional[int]=None; productive_ratio:Optional[float]=None; recorded_worked_sec:Optional[int]=None; prior_next_wake_observed:bool=False; legacy:bool=False; anomalies:list[str]=field(default_factory=list)

def interval_metrics(p:Probe)->dict:
    out={"worked_sec":None,"prearm_overhead_sec":None,"productive_window_sec":None,"close_overhead_sec":None,"productive_marker_pair_valid":False,"interval_anomalies":[]}
    def safe(label,a,b):
        if not a or not b: return None
        try: return worked_sec(a,b)
        except ValueError as exc:
            out["interval_anomalies"].append(f"{label}_INVALID:{exc}"); return None
    out["worked_sec"]=safe("WORKED",p.start_marker_created_at,p.end_marker_created_at)
    out["prearm_overhead_sec"]=safe("PREARM",p.start_marker_created_at,p.work_start_marker_created_at)
    out["productive_window_sec"]=safe("PRODUCTIVE_WINDOW",p.work_start_marker_created_at,p.pre_close_marker_created_at)
    out["close_overhead_sec"]=safe("CLOSE_OVERHEAD",p.pre_close_marker_created_at,p.end_marker_created_at)
    out["productive_marker_pair_valid"]=(p.work_start_marker_comment_id is not None and p.pre_close_marker_comment_id is not None and out["productive_window_sec"] is not None)
    return out

def base_result(p:Probe)->dict:
    return {"probe_id":p.probe_id,"target_runtime_sec":p.target_runtime_sec,"case_id":p.case_id,"workload_profile":p.workload_profile}

def classify(p:Probe)->dict:
    base=base_result(p)
    if p.legacy or p.clock_protocol!=SERVER_CLOCK: return {**base,"result":"LEGACY_SUPPORTING","boundary_effect":"NONE","worked_sec":None,"marker_pair_valid":False,"anomalies":list(p.anomalies)}
    anomalies=list(p.anomalies); ids=p.start_marker_comment_id is not None and p.end_marker_comment_id is not None; times=bool(p.start_marker_created_at and p.end_marker_created_at)
    if p.non_duration_failure:
        worked=None
        if times:
            try: worked=worked_sec(p.start_marker_created_at,p.end_marker_created_at)
            except ValueError as exc: anomalies.append(f"CLOCK_INVALID:{exc}")
        return {**base,"result":"NON_DURATION_FAIL","boundary_effect":"NONE","worked_sec":worked,"marker_pair_valid":ids and times and worked is not None,"anomalies":anomalies}
    if not ids: anomalies.append("MARKER_ID_PAIR_INCOMPLETE")
    if not times: anomalies.append("MARKER_TIMESTAMP_PAIR_INCOMPLETE")
    if not ids or not times: return {**base,"result":"CLOCK_EVIDENCE_INVALID","boundary_effect":"NONE","worked_sec":None,"marker_pair_valid":False,"anomalies":anomalies}
    try: worked=worked_sec(p.start_marker_created_at,p.end_marker_created_at)
    except ValueError as exc: return {**base,"result":"CLOCK_EVIDENCE_INVALID","boundary_effect":"NONE","worked_sec":None,"marker_pair_valid":False,"anomalies":anomalies+[f"CLOCK_INVALID:{exc}"]}
    if p.recorded_worked_sec is not None and p.recorded_worked_sec!=worked: anomalies.append(f"RECORDED_WORKED_MISMATCH:{p.recorded_worked_sec}!={worked}")
    if p.productive_ratio is not None and p.active_work_sec is None: anomalies.append("PRODUCTIVE_RATIO_WITHOUT_DIRECT_ACTIVE_WORK")
    if p.active_work_sec is not None and p.active_work_sec>worked: anomalies.append("ACTIVE_WORK_EXCEEDS_WORKED")
    if worked<p.target_runtime_sec:
        result="HARNESS_UNDER_TARGET" if p.close_trigger=="WORKLOAD_EXHAUSTED" else "UNDER_TARGET"
        if result=="HARNESS_UNDER_TARGET": anomalies.append("FINITE_WORKLOAD_EXHAUSTION_IS_HARNESS_DEFECT")
    elif p.forced_stop_or_timeout:
        result="DURATION_FAIL_CANDIDATE"
        if p.clean_close: anomalies.append("INCONSISTENT_FORCED_STOP_AND_CLEAN_CLOSE")
    elif p.scheduler_write_ok and p.scheduler_state_ok and p.checkpoint_saved and p.clean_close and p.substantive_unit_count>0: result="CLEAN_PASS_PENDING_WAKE"
    else: result="AMBIGUOUS"
    metrics=interval_metrics(p); anomalies.extend(metrics["interval_anomalies"])
    return {**base,"result":result,"boundary_effect":"NONE","worked_sec":worked,"marker_pair_valid":True,"prearm_overhead_sec":metrics["prearm_overhead_sec"],"productive_window_sec":metrics["productive_window_sec"],"close_overhead_sec":metrics["close_overhead_sec"],"productive_marker_pair_valid":metrics["productive_marker_pair_valid"],"harness_version":p.harness_version,"close_trigger":p.close_trigger,"generated_unique_units":p.generated_unique_units,"duplicate_units_rejected":p.duplicate_units_rejected,"batches_completed":p.batches_completed,"anomalies":anomalies}

def retrospective_wake(result:dict,wake_observed:bool)->dict:
    out=dict(result)
    if result.get("result")=="CLEAN_PASS_PENDING_WAKE" and wake_observed: out["result"]="CLEAN_PASS_WAKE_OK"; out["boundary_effect"]="SAFE_LOWER_BOUND_MAY_ADVANCE"
    return out

def reconcile_duplicate_records(records:Iterable[Probe])->dict[str,Probe]:
    out={}
    for record in records:
        prior=out.get(record.probe_id)
        if prior is None: out[record.probe_id]=record
        elif prior!=record: raise ValueError(f"CONFLICTING_DUPLICATE_PROBE:{record.probe_id}")
    return out

def derive_bounds(classified:Iterable[dict])->dict:
    clean=[r for r in classified if r.get("result")=="CLEAN_PASS_WAKE_OK"]; fails=[r for r in classified if r.get("result")=="DURATION_FAIL_CANDIDATE"]
    targets=[r.get("target_runtime_sec") for r in clean if isinstance(r.get("target_runtime_sec"),int)]
    return {"server_clock_safe_lower_bound_sec":max(targets) if targets else None,"server_clock_failure_boundary_sec":None,"duration_failure_candidate_count":len(fails),"clean_wake_ok_count":len(clean)}

if __name__=="__main__":
    p=Probe("REGRESSION-CLEAN",1320,clock_protocol=SERVER_CLOCK,start_marker_comment_id=1,start_marker_created_at="2026-09-23T17:47:04Z",work_start_marker_comment_id=3,work_start_marker_created_at="2026-09-23T17:47:12Z",pre_close_marker_comment_id=4,pre_close_marker_created_at="2026-09-23T18:08:09Z",end_marker_comment_id=2,end_marker_created_at="2026-09-23T18:09:06Z",scheduler_write_ok=True,scheduler_state_ok=True,checkpoint_saved=True,clean_close=True,substantive_unit_count=1)
    r=retrospective_wake(classify(p),True); assert derive_bounds([r])["server_clock_safe_lower_bound_sec"]==1320
    bad=Probe("BAD-PRODUCTIVE-ORDER",1,clock_protocol=SERVER_CLOCK,start_marker_comment_id=1,start_marker_created_at="2026-09-23T00:00:00Z",work_start_marker_comment_id=3,work_start_marker_created_at="2026-09-23T00:00:10Z",pre_close_marker_comment_id=4,pre_close_marker_created_at="2026-09-23T00:00:05Z",end_marker_comment_id=2,end_marker_created_at="2026-09-23T00:00:20Z")
    br=classify(bad); assert br["productive_window_sec"] is None and not br["productive_marker_pair_valid"] and any("PRODUCTIVE_WINDOW_INVALID" in x for x in br["anomalies"])
