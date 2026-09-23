from __future__ import annotations
from dataclasses import dataclass, asdict
from hashlib import sha256
from itertools import product, islice
from math import gcd
from typing import Iterator, Iterable
import json

"""Deterministic, scalable, semantically non-duplicate strict-runtime workload source."""
MARKER_STATES=("valid","missing_start","missing_end","reversed","id_mismatch")
SCHEDULER_STATES=("ok","write_fail","state_mismatch")
CLOSE_STATES=("clean","checkpoint_missing","forced_stop")
PROVIDER_STATES=("ok","non_duration_fail")
WAKE_STATES=("observed","missing")
WORKLOAD_SHAPES=("mixed_io","micro_chain","large_unit","close_heavy")
UNITS_PER_EPOCH=(len(MARKER_STATES)*len(SCHEDULER_STATES)*len(CLOSE_STATES)*len(PROVIDER_STATES)*len(WAKE_STATES)*len(WORKLOAD_SHAPES))

@dataclass(frozen=True)
class WorkUnit:
    ordinal:int; case_id:str; epoch:int
    marker_state:str; scheduler_state:str; close_state:str; provider_state:str; wake_state:str; workload_shape:str
    target_delta_sec:int; marker_skew_sec:int; close_reserve_sec:int
    def payload(self)->dict:return asdict(self)

def epoch_parameters(epoch:int)->tuple[int,int,int]:
    magnitude=1+(epoch//2); target_delta=(-magnitude if epoch%2==0 else magnitude)
    marker_skew=((epoch*17)%121)-60
    # 17 is coprime to 91, so all 91 reserve values (30..120s) are covered before repetition.
    close_reserve=30+((epoch*17)%91)
    return target_delta,marker_skew,close_reserve

def _stable_id(seed:str,ordinal:int,epoch:int,values:tuple[str,...],numeric:tuple[int,int,int])->str:
    return sha256("|".join((seed,str(ordinal),str(epoch),*values,*(str(x) for x in numeric))).encode()).hexdigest()[:20]

def iter_units(seed:str="SC-A22-CLOCK",start_ordinal:int=0)->Iterator[WorkUnit]:
    """Yield from start_ordinal in O(1) positioning time, not O(start_ordinal)."""
    if start_ordinal < 0: raise ValueError("start_ordinal must be >= 0")
    ordinal=start_ordinal
    epoch, offset=divmod(start_ordinal,UNITS_PER_EPOCH)
    while True:
        numeric=epoch_parameters(epoch)
        values_iter=product(MARKER_STATES,SCHEDULER_STATES,CLOSE_STATES,PROVIDER_STATES,WAKE_STATES,WORKLOAD_SHAPES)
        for values in islice(values_iter,offset,None):
            marker,scheduler,close,provider,wake,shape=values
            yield WorkUnit(ordinal,_stable_id(seed,ordinal,epoch,values,numeric),epoch,marker,scheduler,close,provider,wake,shape,*numeric)
            ordinal+=1
        epoch+=1;offset=0

def expected_invariants(unit:WorkUnit)->list[str]:
    checks=["server_clock_only","no_model_time_authority","duplicate_case_id_forbidden","terminal_classification_deterministic","epoch_semantics_not_id_only"]
    if unit.marker_state!="valid":checks.append("clock_invalid_must_not_move_boundary")
    if unit.provider_state=="non_duration_fail":checks.append("non_duration_failure_has_boundary_effect_none")
    if unit.scheduler_state!="ok":checks.append("scheduler_fault_must_not_be_duration_failure")
    if unit.close_state=="forced_stop":checks.append("forced_stop_precedence_over_clean_pass")
    if unit.wake_state=="observed":checks.append("wake_can_promote_pending_pass_only")
    if abs(unit.target_delta_sec)<=2:checks.append("near_boundary_off_by_one_or_two")
    if unit.close_reserve_sec<60:checks.append("tight_close_reserve_behavior")
    if unit.close_reserve_sec>90:checks.append("conservative_close_reserve_behavior")
    return checks

def batch(seed:str,start_ordinal:int,count:int)->list[dict]:
    if count < 0: raise ValueError("count must be >= 0")
    out=[]
    for unit in islice(iter_units(seed,start_ordinal),count):
        row=unit.payload();row["expected_invariants"]=expected_invariants(unit);out.append(row)
    return out

def fingerprint(rows:Iterable[dict])->str:return sha256(json.dumps(list(rows),sort_keys=True,separators=(",",":")).encode()).hexdigest()

def validate_semantic_uniqueness(rows:Iterable[dict])->bool:
    seen=set()
    for r in rows:
        key=(r["marker_state"],r["scheduler_state"],r["close_state"],r["provider_state"],r["wake_state"],r["workload_shape"],r["target_delta_sec"],r["marker_skew_sec"],r["close_reserve_sec"])
        if key in seen:return False
        seen.add(key)
    return True

if __name__=="__main__":
    assert gcd(17,91)==1 and gcd(17,121)==1 and UNITS_PER_EPOCH==720
    rows=batch("SC-A22-CLOCK",0,50000)
    assert len({r["case_id"] for r in rows})==len(rows) and validate_semantic_uniqueness(rows)
    # Regression: high-offset batch must preserve ordinal continuity without replaying the prefix.
    high=batch("scale-regression",10**9,3)
    assert [r["ordinal"] for r in high]==[10**9,10**9+1,10**9+2]
    assert len({r["case_id"] for r in high})==3
    reserves={r["close_reserve_sec"] for r in batch("coverage",0,91*720)}
    assert len(reserves)==91 and min(reserves)==30 and max(reserves)==120
    print(json.dumps({"count":len(rows),"fingerprint":fingerprint(rows),"semantic_unique":True,"reserve_coverage":len(reserves),"high_offset_random_access":True},indent=2))
