"""Fail-closed V3 runtime evidence evaluator."""
from dataclasses import dataclass, asdict, replace
from enum import Enum
from hashlib import sha256
import json
from datetime import datetime

class PredicateStatus(str, Enum):
    PASS="PASS"; FAIL="FAIL"; NOT_EXECUTED="NOT_EXECUTED"

@dataclass(frozen=True)
class PredicateResult:
    name:str; status:PredicateStatus; evidence_refs:tuple[str,...]=(); reason_code:str=""

@dataclass(frozen=True)
class RawMarkerEvidence:
    comment_id:int|None; raw_endpoint_fetched:bool; raw_created_at:str|None

@dataclass(frozen=True)
class SchedulerEvidence:
    attempted:bool=False; verified:bool=False; state_match:bool|None=None; evidence_ref:str|None=None

@dataclass(frozen=True)
class WakeEvidence:
    expected_continuation_id:str|None=None; observation_window_closed:bool=False
    observed:bool=False; absence_verified:bool=False; evidence_ref:str|None=None

@dataclass(frozen=True)
class ExecutedCheckEvidence:
    artifact_ref:str|None=None; artifact_hash_verified:bool=False
    executed_count:int=0; failed_count:int=0; structural_proof_only:bool=False

@dataclass(frozen=True)
class ManifestV3:
    schema_version:str; generator_version:str; proof_id:str|None; seed:int
    ordinal_start:int; ordinal_end_exclusive:int; chunk_size:int; chunk_count:int
    proven_unique_units:int; executed_assertion_count:int; failed_assertion_count:int
    duplicate_ids_rejected:int; semantic_repeats_rejected:int; anomaly_count:int
    ordered_chunk_hashes:tuple[str,...]; previous_manifest_hash:str|None=None
    manifest_hash:str|None=None

def _r(name,status,reason="",refs=()):
    return PredicateResult(name,status,tuple(x for x in refs if x),reason)

def _dt(s): return datetime.fromisoformat(s.replace("Z","+00:00"))

def eval_clock(start,end,target_sec):
    if start.comment_id is None or end.comment_id is None:
        return _r("clock",PredicateStatus.NOT_EXECUTED,"MISSING_RAW_MARKER")
    if not start.raw_endpoint_fetched or not end.raw_endpoint_fetched:
        return _r("clock",PredicateStatus.NOT_EXECUTED,"RAW_ENDPOINT_UNVERIFIED")
    try: elapsed=(_dt(end.raw_created_at)-_dt(start.raw_created_at)).total_seconds()
    except Exception: return _r("clock",PredicateStatus.FAIL,"CLOCK_ORDER_INVALID")
    if elapsed < 0: return _r("clock",PredicateStatus.FAIL,"CLOCK_ORDER_INVALID")
    if elapsed < target_sec: return _r("clock",PredicateStatus.FAIL,"CLOCK_TARGET_NOT_REACHED")
    return _r("clock",PredicateStatus.PASS,refs=(str(start.comment_id),str(end.comment_id)))

def eval_scheduler(e):
    if not e.attempted: return _r("scheduler",PredicateStatus.NOT_EXECUTED,"MISSING_SCHEDULER_ATTEMPT_EVIDENCE")
    if not e.verified: return _r("scheduler",PredicateStatus.NOT_EXECUTED,"MISSING_SCHEDULER_READBACK")
    if e.state_match is not True: return _r("scheduler",PredicateStatus.FAIL,"SCHEDULER_STATE_MISMATCH",(e.evidence_ref,))
    return _r("scheduler",PredicateStatus.PASS,refs=(e.evidence_ref,))

def eval_wake(e):
    if not e.expected_continuation_id: return _r("wake",PredicateStatus.NOT_EXECUTED,"MISSING_WAKE_IDENTITY")
    if e.observed: return _r("wake",PredicateStatus.PASS,refs=(e.evidence_ref,))
    if e.observation_window_closed and e.absence_verified:
        return _r("wake",PredicateStatus.FAIL,"WAKE_MISSED_VERIFIED",(e.evidence_ref,))
    return _r("wake",PredicateStatus.NOT_EXECUTED,"WAKE_OBSERVATION_INCOMPLETE")

def eval_substantive(e):
    if e.structural_proof_only: return _r("substantive",PredicateStatus.NOT_EXECUTED,"GENERATOR_PROOF_ONLY")
    if not e.artifact_ref: return _r("substantive",PredicateStatus.NOT_EXECUTED,"MISSING_EXECUTED_CHECK_ARTIFACT")
    if not e.artifact_hash_verified: return _r("substantive",PredicateStatus.FAIL,"EXECUTED_CHECK_ARTIFACT_INVALID",(e.artifact_ref,))
    if e.executed_count <= 0: return _r("substantive",PredicateStatus.NOT_EXECUTED,"MISSING_EXECUTED_CHECK_ARTIFACT")
    if e.failed_count < 0 or e.failed_count > e.executed_count or e.failed_count:
        return _r("substantive",PredicateStatus.FAIL,"SUBSTANTIVE_CHECK_FAILED",(e.artifact_ref,))
    return _r("substantive",PredicateStatus.PASS,refs=(e.artifact_ref,))

def aggregate_results(results):
    rs=tuple(results)
    return {"executed_assertion_count":sum(r.status!=PredicateStatus.NOT_EXECUTED for r in rs),
            "failed_assertion_count":sum(r.status==PredicateStatus.FAIL for r in rs)}

def promotion_eligible(results,hashes_verified,terminal_closed,mandatory=None):
    wanted=set(mandatory or [r.name for r in results])
    picked=[r for r in results if r.name in wanted]
    return hashes_verified and terminal_closed and len(picked)==len(wanted) and all(r.status==PredicateStatus.PASS for r in picked)

def canonical_manifest_bytes(m):
    d=asdict(m); d.pop("manifest_hash",None)
    return json.dumps(d,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()

def compute_manifest_hash(m): return sha256(canonical_manifest_bytes(m)).hexdigest()
def with_manifest_hash(m): return replace(m,manifest_hash=compute_manifest_hash(m))

def verify_manifest_chain(items):
    prev=None
    for m in items:
        if m.previous_manifest_hash != prev or m.manifest_hash != compute_manifest_hash(m): return False
        prev=m.manifest_hash
    return True
