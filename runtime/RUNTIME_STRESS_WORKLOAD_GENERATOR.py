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


@dataclass(frozen=True)
class CheckOutcome:
    name:str; passed:bool

@dataclass(frozen=True)
class ChunkArtifact:
    seed:str; ordinal_start:int; ordinal_end_exclusive:int
    proven_unique_units:int; proof_id:str
    executed_assertion_count:int; failed_assertion_count:int
    duplicate_ids_rejected:int; anomaly_count:int; content_digest:str; previous_chunk_hash:str; chunk_hash:str

GENERATOR_VERSION="v3-streaming-actual-checks"
PROOF_ID="iter_units-ordinal-uniqueness-v1"

def evaluate_concrete_checks(unit:WorkUnit)->tuple[CheckOutcome,...]:
    """Actually invoke bounded structural predicates; labels alone never count."""
    return (
        CheckOutcome("ordinal_epoch_consistent",unit.epoch==unit.ordinal//UNITS_PER_EPOCH),
        CheckOutcome("marker_state_domain",unit.marker_state in MARKER_STATES),
        CheckOutcome("scheduler_state_domain",unit.scheduler_state in SCHEDULER_STATES),
        CheckOutcome("close_state_domain",unit.close_state in CLOSE_STATES),
        CheckOutcome("provider_state_domain",unit.provider_state in PROVIDER_STATES),
        CheckOutcome("wake_state_domain",unit.wake_state in WAKE_STATES),
        CheckOutcome("workload_shape_domain",unit.workload_shape in WORKLOAD_SHAPES),
        CheckOutcome("close_reserve_range",30<=unit.close_reserve_sec<=120),
    )

def _chain_hash(seed:str,ordinal_start:int,ordinal_end_exclusive:int,previous_chunk_hash:str,content_digest:str)->str:
    header={"seed":seed,"ordinal_start":ordinal_start,"ordinal_end_exclusive":ordinal_end_exclusive,"previous_chunk_hash":previous_chunk_hash,"content_digest":content_digest}
    return sha256(json.dumps(header,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def verify_chunk_chain(artifacts:Iterable[ChunkArtifact],checkpoint_prev_hash:str="")->bool:
    expected_prev=checkpoint_prev_hash
    expected_start=None
    seen=False
    for artifact in artifacts:
        seen=True
        if artifact.previous_chunk_hash!=expected_prev:return False
        if artifact.ordinal_end_exclusive<=artifact.ordinal_start:return False
        if expected_start is not None and artifact.ordinal_start!=expected_start:return False
        if artifact.chunk_hash!=_chain_hash(artifact.seed,artifact.ordinal_start,artifact.ordinal_end_exclusive,artifact.previous_chunk_hash,artifact.content_digest):return False
        expected_prev=artifact.chunk_hash
        expected_start=artifact.ordinal_end_exclusive
    return seen

def iter_evaluated_chunks(seed:str="SC-A22-CLOCK",start_ordinal:int=0,chunk_size:int=1024)->Iterator[ChunkArtifact]:
    """Bounded-memory actual predicate execution with independently verifiable chained artifacts."""
    if chunk_size<=0: raise ValueError("chunk_size must be > 0")
    units=iter_units(seed,start_ordinal); ordinal=start_ordinal; previous_chunk_hash=""
    while True:
        content=sha256()
        executed=failed=duplicates=anomalies=0; ids=set(); count=0
        chunk_start=ordinal
        for _ in range(chunk_size):
            unit=next(units); count+=1
            outcomes=evaluate_concrete_checks(unit)
            if unit.case_id in ids: duplicates+=1
            ids.add(unit.case_id)
            for outcome in outcomes:
                executed+=1
                if not outcome.passed: failed+=1
                content.update(json.dumps({"ordinal":unit.ordinal,"case_id":unit.case_id,"check":outcome.name,"passed":outcome.passed},sort_keys=True,separators=(",",":")).encode()); content.update(b"\n")
            if unit.ordinal!=ordinal: anomalies+=1
            ordinal+=1
        content_digest=content.hexdigest()
        chunk_hash=_chain_hash(seed,chunk_start,ordinal,previous_chunk_hash,content_digest)
        yield ChunkArtifact(seed,chunk_start,ordinal,count,PROOF_ID,executed,failed,duplicates,anomalies,content_digest,previous_chunk_hash,chunk_hash)
        previous_chunk_hash=chunk_hash

