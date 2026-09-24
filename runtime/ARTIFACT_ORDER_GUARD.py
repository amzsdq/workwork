from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ArtifactOrderState:
    raw_start_verified: bool
    start_artifact_persisted: bool
    terminal_or_interrupted_persisted: bool
    immutable_event_persisted: bool

class ArtifactOrderError(RuntimeError):
    pass

def require_workload_admission(state: ArtifactOrderState) -> None:
    if not state.raw_start_verified:
        raise ArtifactOrderError("RAW_START_NOT_VERIFIED")
    if not state.start_artifact_persisted:
        raise ArtifactOrderError("START_ARTIFACT_NOT_PERSISTED")

def require_terminal_projection_admission(state: ArtifactOrderState) -> None:
    require_workload_admission(state)
    if not state.terminal_or_interrupted_persisted:
        raise ArtifactOrderError("TERMINAL_OR_INTERRUPTED_ARTIFACT_NOT_PERSISTED")
    if not state.immutable_event_persisted:
        raise ArtifactOrderError("IMMUTABLE_TERMINAL_EVENT_NOT_PERSISTED")
