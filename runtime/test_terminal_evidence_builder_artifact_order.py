from __future__ import annotations
import unittest
from unittest.mock import patch

import TERMINAL_EVIDENCE_BUILDER as builder
from ARTIFACT_ORDER_GUARD import ArtifactOrderError, ArtifactOrderState

COMMON=dict(
    probe_id="T",case_id="C",target_sec=10,workload_profile="test",
    start_id=1,start_at="2026-01-01T00:00:00Z",
    work_start_id=2,work_start_at="2026-01-01T00:00:01Z",
    pre_close_id=3,pre_close_at="2026-01-01T00:00:09Z",
    end_id=4,end_at="2026-01-01T00:00:11Z",
    scheduler_write_ok=True,scheduler_state_ok=True,checkpoint_saved=True,clean_close=True,
    semantic_unique_units=10,batches_completed=1,
)

class BuilderArtifactOrderTests(unittest.TestCase):
    def test_rejects_before_probe_or_classify(self):
        order=ArtifactOrderState(
            raw_start_verified=True,
            start_artifact_persisted=True,
            terminal_or_interrupted_persisted=False,
            immutable_event_persisted=True,
        )
        with patch.object(builder,"Probe") as probe, patch.object(builder,"classify") as classify:
            with self.assertRaisesRegex(ArtifactOrderError,"TERMINAL_OR_INTERRUPTED_ARTIFACT_NOT_PERSISTED"):
                builder.build_terminal(artifact_order=order,**COMMON)
            probe.assert_not_called()
            classify.assert_not_called()

    def test_success_path_regression(self):
        order=ArtifactOrderState(
            raw_start_verified=True,
            start_artifact_persisted=True,
            terminal_or_interrupted_persisted=True,
            immutable_event_persisted=True,
        )
        result=builder.build_terminal(artifact_order=order,**COMMON)
        self.assertEqual(result["classification"],"CLEAN_PASS_PENDING_WAKE")
        self.assertEqual(result["worked_sec"],11)
        self.assertEqual(result["productive_window_sec"],8)
        self.assertEqual(result["close_overhead_sec"],2)

if __name__=="__main__":
    unittest.main()
