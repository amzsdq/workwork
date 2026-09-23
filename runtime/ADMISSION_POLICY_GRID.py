from __future__ import annotations
from dataclasses import dataclass, asdict

@dataclass(frozen=True)
class Decision:
    remaining_sec:int; estimated_task_sec:int; reserve_sec:int; admit:bool; slack_if_admit:int

def p3(remaining_sec:int,estimated_task_sec:int,reserve_sec:int)->Decision:
    admit=estimated_task_sec+reserve_sec<=remaining_sec
    return Decision(remaining_sec,estimated_task_sec,reserve_sec,admit,remaining_sec-estimated_task_sec-reserve_sec)

def grid()->list[Decision]:
    return [p3(rem,task,reserve) for rem in range(30,181) for task in (1,5,10,15,20,30,45,60) for reserve in range(30,121)]

def summarize()->dict:
    rows=grid(); boundary=[r for r in rows if abs(r.slack_if_admit)<=1]
    monotonic_violations=0
    # For fixed remaining/task, increasing reserve must never turn reject back into admit.
    for rem in range(30,181):
        for task in (1,5,10,15,20,30,45,60):
            seq=[p3(rem,task,r).admit for r in range(30,121)]
            seen_reject=False
            for x in seq:
                if not x: seen_reject=True
                elif seen_reject: monotonic_violations+=1
    return {"grid_cases":len(rows),"near_boundary_cases":len(boundary),"monotonic_violations":monotonic_violations,
            "rule":"estimated_task_sec + reserve_sec <= remaining_sec",
            "note":"Synthetic policy validation only; does not promote empirical runtime or reserve."}

if __name__=="__main__":
    s=summarize(); assert s["monotonic_violations"]==0; print(s)
