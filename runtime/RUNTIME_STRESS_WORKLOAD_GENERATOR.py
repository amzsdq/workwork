from __future__ import annotations
from dataclasses import dataclass, asdict
from hashlib import sha256
from itertools import product
from typing import Iterator, Iterable
import json

"""Deterministic, scalable, semantically non-duplicate strict-runtime workload source.

Epochs MUST add decision value. Merely changing an ID while replaying the same Cartesian
case is padding, so each epoch changes numeric boundary conditions as well as identity.
"""
MARKER_STATES=("valid","missing_start","missing_end","reversed","id_mismatch")
SCHEDULER_STATES=("ok","write_fail","state_mismatch")
CLOSE_STATES=("clean","checkpoint_missing","forced_stop")
PROVIDER_STATES=("ok","non_duration_fail")
WAKE_STATES=("observed","missing")
WORKLOAD_SHAPES=("mixed_io","micro_chain","large_unit","close_heavy")

@dataclass(frozen=True)
class WorkUnit:
    ordinal:int; case_id:str; epoch:int
    marker_state:str; scheduler_state:str; close_state:str; provider_state:str; wake_state:str; workload_shape:str
    target_delta_sec:int; marker_skew_sec:int; close_reserve_sec:int
    def payload(self)->dict: return asdict(self)

def epoch_parameters(epoch:int)->tuple[int,int,int]:
    # Deterministic expanding boundary perturbations. Each epoch is semantically distinct.
    magnitude=1+(epoch//2)
    target_delta=(-magnitude if epoch%2==0 else magnitude)
    marker_skew=((epoch*17)%121)-60
    close_reserve=30+((epoch*13)%91)  # 30..120s
    return target_delta,marker_skew,close_reserve

def _stable_id(seed:str,ordinal:int,epoch:int,values:tuple[str,...],numeric:tuple[int,int,int])->str:
    raw="|".join((seed,str(ordinal),str(epoch),*values,*(str(x) for x in numeric))).encode()
    return sha256(raw).hexdigest()[:20]

def iter_units(seed:str="SC-A22-CLOCK")->Iterator[WorkUnit]:
    ordinal=0; epoch=0
    while True:
        numeric=epoch_parameters(epoch)
        for values in product(MARKER_STATES,SCHEDULER_STATES,CLOSE_STATES,PROVIDER_STATES,WAKE_STATES,WORKLOAD_SHAPES):
            marker,scheduler,close,provider,wake,shape=values
            yield WorkUnit(ordinal,_stable_id(seed,ordinal,epoch,values,numeric),epoch,marker,scheduler,close,provider,wake,shape,*numeric)
            ordinal+=1
        epoch+=1

def expected_invariants(unit:WorkUnit)->list[str]:
    checks=["server_clock_only","no_model_time_authority","duplicate_case_id_forbidden","terminal_classification_deterministic","epoch_semantics_not_id_only"]
    if unit.marker_state!="valid": checks.append("clock_invalid_must_not_move_boundary")
    if unit.provider_state=="non_duration_fail": checks.append("non_duration_failure_has_boundary_effect_none")
    if unit.scheduler_state!="ok": checks.append("scheduler_fault_must_not_be_duration_failure")
    if unit.close_state=="forced_stop": checks.append("forced_stop_precedence_over_clean_pass")
    if unit.wake_state=="observed": checks.append("wake_can_promote_pending_pass_only")
    if abs(unit.target_delta_sec)<=2: checks.append("near_boundary_off_by_one_or_two")
    if unit.close_reserve_sec<60: checks.append("tight_close_reserve_behavior")
    if unit.close_reserve_sec>90: checks.append("conservative_close_reserve_behavior")
    return checks

def batch(seed:str,start_ordinal:int,count:int)->list[dict]:
    out=[]
    for unit in iter_units(seed):
        if unit.ordinal<start_ordinal: continue
        if len(out)>=count: break
        row=unit.payload(); row["expected_invariants"]=expected_invariants(unit); out.append(row)
    return out

def fingerprint(rows:Iterable[dict])->str:
    return sha256(json.dumps(list(rows),sort_keys=True,separators=(",",":")).encode()).hexdigest()

def validate_semantic_uniqueness(rows:Iterable[dict])->bool:
    seen=set()
    for r in rows:
        key=(r["marker_state"],r["scheduler_state"],r["close_state"],r["provider_state"],r["wake_state"],r["workload_shape"],r["target_delta_sec"],r["marker_skew_sec"],r["close_reserve_sec"])
        if key in seen: return False
        seen.add(key)
    return True

if __name__=="__main__":
    rows=batch("SC-A22-CLOCK",0,5000)
    assert len({r["case_id"] for r in rows})==len(rows)
    assert validate_semantic_uniqueness(rows)
    print(json.dumps({"count":len(rows),"fingerprint":fingerprint(rows),"semantic_unique":True},indent=2))
