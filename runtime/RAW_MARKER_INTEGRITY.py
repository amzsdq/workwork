from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Mapping, Any

ROLE_TOKENS={
 "START":("RUNTIME_START_MARKER","START_MARKER"),
 "WORK_START":("RUNTIME_WORK_START_MARKER","WORK_START_MARKER"),
 "PRE_CLOSE":("RUNTIME_PRE_CLOSE_MARKER","PRE_CLOSE_MARKER"),
 "PROGRESS":("RUNTIME_PROGRESS_MARKER","PROGRESS_MARKER"),
 "END":("RUNTIME_END_MARKER","END_MARKER"),
}

def parse_z(s:str)->datetime:
    if not isinstance(s,str) or not s.endswith("Z"):raise ValueError("created_at_not_utc_z")
    return datetime.fromisoformat(s.replace("Z","+00:00"))

def body_has_identity(body:str,probe_id:str,case_id:str|None)->bool:
    if probe_id not in body:return False
    return case_id is None or case_id in body

@dataclass(frozen=True)
class MarkerCheck:
    valid:bool; role:str; comment_id:int|None; created_at:str|None; errors:tuple[str,...]

def validate_marker(resource:Mapping[str,Any],expected_id:int,role:str,probe_id:str,case_id:str|None=None)->MarkerCheck:
    errors=[]; rid=resource.get("id"); created=resource.get("created_at"); body=resource.get("body") or ""
    if rid!=expected_id:errors.append("RAW_ID_MISMATCH")
    if role not in ROLE_TOKENS:errors.append("UNKNOWN_ROLE")
    elif not any(tok in body for tok in ROLE_TOKENS[role]):errors.append("ROLE_TOKEN_MISSING")
    if not body_has_identity(body,probe_id,case_id):errors.append("IDENTITY_MISMATCH")
    try:parse_z(created)
    except Exception:errors.append("CREATED_AT_INVALID")
    return MarkerCheck(not errors,role,rid,created,tuple(errors))

def validate_lifecycle(start:Mapping[str,Any],work_start:Mapping[str,Any],pre_close:Mapping[str,Any],end:Mapping[str,Any],ids:Mapping[str,int],probe_id:str,case_id:str|None=None)->dict:
    resources={"START":start,"WORK_START":work_start,"PRE_CLOSE":pre_close,"END":end}
    checks={r:validate_marker(resources[r],ids[r],r,probe_id,case_id) for r in resources}
    errors=[f"{r}:{e}" for r,c in checks.items() for e in c.errors]
    times=[]
    if all(c.valid for c in checks.values()):
        times=[parse_z(checks[r].created_at) for r in ("START","WORK_START","PRE_CLOSE","END")]
        if times!=sorted(times):errors.append("LIFECYCLE_ORDER_INVALID")
    return {"valid":not errors,"errors":errors,"checks":{r:c.__dict__ for r,c in checks.items()}}

if __name__=="__main__":
    def m(i,role,t):return {"id":i,"body":f"{role}_MARKER probe_id=P case_id=C","created_at":t}
    good=validate_lifecycle(m(1,"START","2026-01-01T00:00:00Z"),m(2,"WORK_START","2026-01-01T00:00:01Z"),m(3,"PRE_CLOSE","2026-01-01T00:00:10Z"),m(4,"END","2026-01-01T00:00:11Z"),{"START":1,"WORK_START":2,"PRE_CLOSE":3,"END":4},"P","C")
    assert good["valid"],good
