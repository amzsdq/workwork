from __future__ import annotations
from RUNTIME_EVIDENCE_PROCESSOR_REFERENCE import Probe,SERVER_CLOCK,HARNESS_V2,classify

def build_terminal(*,probe_id:str,case_id:str,target_sec:int,workload_profile:str,
                   start_id:int,start_at:str,work_start_id:int,work_start_at:str,
                   pre_close_id:int,pre_close_at:str,end_id:int,end_at:str,
                   scheduler_write_ok:bool,scheduler_state_ok:bool,checkpoint_saved:bool,clean_close:bool,
                   semantic_unique_units:int,batches_completed:int,duplicate_ids_rejected:int=0,semantic_repeats_rejected:int=0,
                   harness_valid:bool=True,close_trigger:str="TIMING_ADMISSION",forced_stop:bool=False,non_duration_failure:bool=False)->dict:
    p=Probe(probe_id=probe_id,case_id=case_id,target_runtime_sec=target_sec,workload_profile=workload_profile,clock_protocol=SERVER_CLOCK,
        start_marker_comment_id=start_id,start_marker_created_at=start_at,work_start_marker_comment_id=work_start_id,work_start_marker_created_at=work_start_at,
        pre_close_marker_comment_id=pre_close_id,pre_close_marker_created_at=pre_close_at,end_marker_comment_id=end_id,end_marker_created_at=end_at,
        harness_version=HARNESS_V2,harness_valid=harness_valid,generated_unique_units=semantic_unique_units,semantic_unique_units=semantic_unique_units,
        duplicate_units_rejected=duplicate_ids_rejected,semantic_repeats_rejected=semantic_repeats_rejected,batches_completed=batches_completed,
        scheduler_write_ok=scheduler_write_ok,scheduler_state_ok=scheduler_state_ok,checkpoint_saved=checkpoint_saved,clean_close=clean_close,
        forced_stop_or_timeout=forced_stop,non_duration_failure=non_duration_failure,substantive_unit_count=semantic_unique_units,close_trigger=close_trigger)
    r=classify(p)
    return {
      "probe_id":probe_id,"case_id":case_id,"classification":r["result"],"boundary_effect":"NONE_PENDING_RETROSPECTIVE_WAKE" if r["result"]=="CLEAN_PASS_PENDING_WAKE" else "NONE",
      "target_sec":target_sec,"clock_protocol":SERVER_CLOCK,"clock_issue_number":1,"harness_version":HARNESS_V2,"harness_valid":harness_valid,
      "start_marker_comment_id":start_id,"start_marker_created_at":start_at,"work_start_marker_comment_id":work_start_id,"work_start_marker_created_at":work_start_at,
      "pre_close_marker_comment_id":pre_close_id,"pre_close_marker_created_at":pre_close_at,"end_marker_comment_id":end_id,"end_marker_created_at":end_at,
      "worked_sec":r.get("worked_sec"),"prearm_overhead_sec":r.get("prearm_overhead_sec"),"productive_window_sec":r.get("productive_window_sec"),"close_overhead_sec":r.get("close_overhead_sec"),
      "marker_pair_valid":r.get("marker_pair_valid"),"productive_marker_pair_valid":r.get("productive_marker_pair_valid"),
      "scheduler_write_ok":scheduler_write_ok,"scheduler_state_ok":scheduler_state_ok,"checkpoint_saved":checkpoint_saved,"clean_close":clean_close,
      "semantic_unique_units":semantic_unique_units,"duplicate_ids_rejected":duplicate_ids_rejected,"semantic_repeats_rejected":semantic_repeats_rejected,"batches_completed":batches_completed,
      "workload_profile":workload_profile,"close_trigger":close_trigger,"anomalies":r.get("anomalies",[])
    }

if __name__=="__main__":
    t=build_terminal(probe_id="T",case_id="C",target_sec=10,workload_profile="test",start_id=1,start_at="2026-01-01T00:00:00Z",work_start_id=2,work_start_at="2026-01-01T00:00:01Z",pre_close_id=3,pre_close_at="2026-01-01T00:00:09Z",end_id=4,end_at="2026-01-01T00:00:11Z",scheduler_write_ok=True,scheduler_state_ok=True,checkpoint_saved=True,clean_close=True,semantic_unique_units=10,batches_completed=1)
    assert t["classification"]=="CLEAN_PASS_PENDING_WAKE" and t["worked_sec"]==11 and t["productive_window_sec"]==8 and t["close_overhead_sec"]==2
