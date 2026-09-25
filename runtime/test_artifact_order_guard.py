from __future__ import annotations
import unittest

from ARTIFACT_ORDER_GUARD import (
    ArtifactOrderError,
    ArtifactOrderState,
    require_terminal_construction_admission,
    require_terminal_projection_admission,
    require_workload_admission,
)

class ArtifactOrderGuardTests(unittest.TestCase):
    def state(self, **overrides):
        values = dict(
            raw_start_verified=True,
            start_artifact_persisted=True,
            terminal_or_interrupted_persisted=True,
            immutable_event_persisted=True,
        )
        values.update(overrides)
        return ArtifactOrderState(**values)

    def test_workload_rejects_unverified_raw_start(self):
        with self.assertRaisesRegex(ArtifactOrderError, "RAW_START_NOT_VERIFIED"):
            require_workload_admission(self.state(raw_start_verified=False))

    def test_workload_rejects_missing_start_artifact(self):
        with self.assertRaisesRegex(ArtifactOrderError, "START_ARTIFACT_NOT_PERSISTED"):
            require_workload_admission(self.state(start_artifact_persisted=False))

    def test_workload_accepts_verified_persisted_start(self):
        require_workload_admission(self.state())

    def test_terminal_construction_accepts_before_terminal_and_event_persistence(self):
        require_terminal_construction_admission(self.state(
            terminal_or_interrupted_persisted=False,
            immutable_event_persisted=False,
        ))

    def test_terminal_construction_rejects_unverified_raw_start(self):
        with self.assertRaisesRegex(ArtifactOrderError, "RAW_START_NOT_VERIFIED"):
            require_terminal_construction_admission(self.state(raw_start_verified=False))

    def test_terminal_construction_rejects_missing_start_artifact(self):
        with self.assertRaisesRegex(ArtifactOrderError, "START_ARTIFACT_NOT_PERSISTED"):
            require_terminal_construction_admission(self.state(start_artifact_persisted=False))

    def test_terminal_rejects_missing_terminal_or_interrupted_artifact(self):
        with self.assertRaisesRegex(ArtifactOrderError, "TERMINAL_OR_INTERRUPTED_ARTIFACT_NOT_PERSISTED"):
            require_terminal_projection_admission(self.state(terminal_or_interrupted_persisted=False))

    def test_terminal_rejects_missing_immutable_event(self):
        with self.assertRaisesRegex(ArtifactOrderError, "IMMUTABLE_TERMINAL_EVENT_NOT_PERSISTED"):
            require_terminal_projection_admission(self.state(immutable_event_persisted=False))

    def test_terminal_accepts_complete_artifact_order(self):
        require_terminal_projection_admission(self.state())

if __name__ == "__main__":
    unittest.main()
